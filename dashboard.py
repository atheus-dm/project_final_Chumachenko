"""
ПОЛНЫЙ ДАШБОРД ПО ТЗ
Включает ВСЕ результаты анализа
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import io
import sys

# ========== НАСТРОЙКА ==========
st.set_page_config(
    page_title="Полный анализ школы IT",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Стили
st.markdown("""
<style>
    .main-title {font-size: 2.8rem; color: #1E3A8A; font-weight: 800; margin-bottom: 0.5rem;}
    .section-title {font-size: 1.8rem; color: #374151; font-weight: 700; margin-top: 2rem; margin-bottom: 1rem; border-bottom: 3px solid #3B82F6; padding-bottom: 0.5rem;}
    .metric-grid {display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin: 1.5rem 0;}
    .metric-card {background: white; padding: 1.2rem; border-radius: 0.75rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-left: 5px solid #3B82F6;}
    .metric-value {font-size: 1.8rem; font-weight: 700; color: #1F2937;}
    .metric-label {font-size: 0.9rem; color: #6B7280; margin-top: 0.5rem;}
</style>
""", unsafe_allow_html=True)

# ========== ЗАГРУЗКА ДАННЫХ ==========
@st.cache_data(ttl=3600, show_spinner=False)
def load_all_data():
    deals = pd.read_parquet('deals_clean.parquet')
    spend = pd.read_parquet('spend_clean.parquet')
    contacts = pd.read_parquet('contacts_clean.parquet')
    calls = pd.read_parquet('calls_clean.parquet')
    
    # Конвертация дат
    for col in ['Created Time', 'Closing Date']:
        if col in deals.columns:
            deals[col] = pd.to_datetime(deals[col], errors='coerce')
    
    # Конвертация timedelta
    if 'SLA' in deals.columns:
        deals['SLA'] = pd.to_timedelta(deals['SLA'].astype(str), errors='coerce')
    
    return deals, spend, contacts, calls

deals, spend, contacts, calls = load_all_data()

# ========== РАСЧЕТ ВСЕХ МЕТРИК ==========
# Базовые метрики
TOTAL_UA = contacts['Id'].nunique()
active_students = deals[deals['stage_normalized'] == 'Active Student']
TOTAL_B = active_students['Contact Name'].nunique()
total_revenue = deals['revenue'].sum()
total_spend = spend['Spend'].sum()
avg_check = total_revenue / TOTAL_B if TOTAL_B > 0 else 0
conversion_vacuum = (TOTAL_B / TOTAL_UA * 100) if TOTAL_UA > 0 else 0
romi_total = ((total_revenue - total_spend) / total_spend * 100) if total_spend > 0 else 0
cm_total = total_revenue - total_spend
products_count = deals['Product'].nunique()
managers_count = deals['Deal Owner Name'].nunique()
cities_count = deals['City'].nunique()
sources_count = deals['Source'].nunique()

# Deal Age
closed_deals = deals[
    (deals['stage_normalized'] == 'Active Student') & 
    (deals['Closing Date'].notna()) & 
    (deals['Deal_Age_days'].notna()) & 
    (deals['Deal_Age_days'] >= 0)
]
median_deal_age = closed_deals['Deal_Age_days'].median() if len(closed_deals) > 0 else 0
mean_deal_age = closed_deals['Deal_Age_days'].mean() if len(closed_deals) > 0 else 0

# Топ продукт
top_product_row = active_students.groupby('Product')['revenue'].sum().reset_index().sort_values('revenue', ascending=False).head(1)
top_product_name = top_product_row['Product'].iloc[0] if len(top_product_row) > 0 else None

# Бизнес-LTV (упрощенный)
deals['Transactions'] = np.where(
    deals['Payment_Type_Recovered'] == 'one payment', 
    1, 
    deals['Months of study'].fillna(1)
)
deals.loc[deals['stage_normalized'] != 'Active Student', 'Transactions'] = 0

product_stats = active_students.groupby('Product').agg({
    'Contact Name': 'nunique',
    'revenue': 'sum',
    'Transactions': 'sum'
}).rename(columns={'Contact Name': 'B', 'revenue': 'Revenue', 'Transactions': 'T'})

if len(product_stats) > 0:
    product_stats['AOV'] = product_stats['Revenue'] / product_stats['T']
    product_stats['APC'] = product_stats['T'] / product_stats['B']
    product_stats['CLTV'] = product_stats['AOV'] * product_stats['APC']
    product_stats['C1_vacuum'] = product_stats['B'] / TOTAL_UA
    product_stats['LTV'] = product_stats['CLTV'] * product_stats['C1_vacuum']
    
    cltv_weighted = (product_stats['CLTV'] * product_stats['B']).sum() / product_stats['B'].sum() if product_stats['B'].sum() > 0 else 0
    ltv_vacuum_business = cltv_weighted * (TOTAL_B / TOTAL_UA) if TOTAL_UA > 0 else 0
else:
    ltv_vacuum_business = 0

# Топ менеджер
top_manager_row = deals.groupby('Deal Owner Name')['revenue'].sum().reset_index().sort_values('revenue', ascending=False).head(1)
top_manager_name = top_manager_row['Deal Owner Name'].iloc[0] if len(top_manager_row) > 0 else None
top_manager_revenue = top_manager_row['revenue'].iloc[0] if len(top_manager_row) > 0 else 0

# ========== САЙДБАР ФИЛЬТРЫ ==========
with st.sidebar:
    st.markdown("### 🎛️ ФИЛЬТРЫ")
    
    # Даты
    min_date = deals['Created Time'].min().date()
    max_date = deals['Created Time'].max().date()
    date_range = st.date_input("Диапазон дат", [min_date, max_date])
    
    # Динамические списки
    all_sources = sorted(deals['Source'].dropna().unique().tolist())
    all_products = sorted(deals['Product'].dropna().unique().tolist())
    all_cities = sorted(deals['City'].dropna().unique().tolist())
    all_managers = sorted(deals['Deal Owner Name'].dropna().unique().tolist())
    all_stages = sorted(deals['stage_normalized'].dropna().unique().tolist())
    
    selected_sources = st.multiselect("Источники", all_sources, default=all_sources[:5])
    selected_products = st.multiselect("Продукты", all_products, default=all_products[:3])
    selected_cities = st.multiselect("Города", all_cities, default=all_cities[:5])
    selected_managers = st.multiselect("Менеджеры", all_managers, default=all_managers[:5])
    selected_stages = st.multiselect("Стадии", all_stages, default=all_stages)
    
    st.markdown("---")
    st.markdown("### 📊 ТИП АНАЛИЗА")
    analysis_type = st.radio("", ["Полный анализ", "Только успешные сделки", "Все сделки"])

# Фильтрация
def apply_filters():
    filtered = deals.copy()
    
    if len(date_range) == 2:
        filtered = filtered[
            (filtered['Created Time'].dt.date >= date_range[0]) &
            (filtered['Created Time'].dt.date <= date_range[1])
        ]
    
    if selected_sources:
        filtered = filtered[filtered['Source'].isin(selected_sources)]
    if selected_products:
        filtered = filtered[filtered['Product'].isin(selected_products)]
    if selected_cities:
        filtered = filtered[filtered['City'].isin(selected_cities)]
    if selected_managers:
        filtered = filtered[filtered['Deal Owner Name'].isin(selected_managers)]
    if selected_stages:
        filtered = filtered[filtered['stage_normalized'].isin(selected_stages)]
    
    if analysis_type == "Только успешные сделки":
        filtered = filtered[filtered['stage_normalized'] == 'Active Student']
    elif analysis_type == "Все сделки":
        pass
    
    return filtered

filtered_deals = apply_filters()

# ========== ЗАГОЛОВОК И СВОДКА ==========
st.markdown('<div class="main-title">📊 ПОЛНЫЙ АНАЛИЗ ОНЛАЙН-ШКОЛЫ IT</div>', unsafe_allow_html=True)
st.markdown("---")

# Сетка метрик
st.markdown('<div class="section-title">📈 СВОДНЫЕ ПОКАЗАТЕЛИ БИЗНЕСА</div>', unsafe_allow_html=True)

# Создаем сетку 4x4
metrics_data = [
    ("💰 Выручка", f"{total_revenue:,.0f} €", "Total Revenue"),
    ("💶 Средний чек", f"{avg_check:,.0f} €", "Average Check"),
    ("👥 Клиенты (B)", f"{TOTAL_B:,}", "Buyers Count"),
    ("📞 Уникальные контакты", f"{TOTAL_UA:,}", "UA Count"),
    ("📦 Продукты", f"{products_count}", "Products Count"),
    ("👤 Менеджеры", f"{managers_count}", "Managers Count"),
    ("🏙️ Города", f"{cities_count}", "Cities Count"),
    ("📊 Источники", f"{sources_count}", "Sources Count"),
    ("🎯 Конверсия", f"{conversion_vacuum:.1f}%", "Vacuum, B/UA"),
    ("📈 ROMI", f"{romi_total:.1f}%", "(Revenue-Spend)/Spend"),
    ("💼 Маржинальный вклад", f"{cm_total:,.0f} €", "Contribution Margin"),
    ("⚡ Время сделки (медиана)", f"{median_deal_age:.0f} дн", "Deal Age Median"),
    ("⚡ Время сделки (среднее)", f"{mean_deal_age:.0f} дн", "Deal Age Mean"),
    ("🏆 Топ продукт", top_product_name or "N/A", "Top Product by Revenue"),
    ("📊 Бизнес-LTV", f"{ltv_vacuum_business:.0f} €", "weighted CLTV × B/UA"),
    ("👑 Топ менеджер", f"{top_manager_name or 'N/A'} ({top_manager_revenue:,.0f}€)", "Top Manager")
]

# Отображаем в 4 колонки
cols = st.columns(4)
for idx, (label, value, tooltip) in enumerate(metrics_data):
    with cols[idx % 4]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div style="font-size: 0.7rem; color: #9CA3AF; margin-top: 0.3rem;">{tooltip}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ========== ВКЛАДКИ ПО БЛОКАМ ТЗ ==========
tab_names = [
    "📊 ОПИСАТЕЛЬНАЯ СТАТИСТИКА",
    "📈 АНАЛИЗ ВРЕМЕННЫХ РЯДОВ", 
    "🎯 ЭФФЕКТИВНОСТЬ КАМПАНИЙ",
    "👥 ЭФФЕКТИВНОСТЬ ПРОДАЖ",
    "📦 ПЛАТЕЖИ И ПРОДУКТЫ",
    "🗺️ ГЕОГРАФИЧЕСКИЙ АНАЛИЗ",
    "🚀 ПРОДУКТОВАЯ АНАЛИТИКА",
    "📁 ПОЛНЫЕ ДАННЫЕ"
]

tabs = st.tabs(tab_names)

# ---------- ВКЛАДКА 1: ОПИСАТЕЛЬНАЯ СТАТИСТИКА ----------
with tabs[0]:
    st.markdown('<div class="section-title">1. ОПИСАТЕЛЬНАЯ СТАТИСТИКА</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Числовые поля")
        numeric_cols = filtered_deals.select_dtypes(include=[np.number]).columns.tolist()
        if numeric_cols:
            stats_df = filtered_deals[numeric_cols].describe().T
            stats_df = stats_df[['mean', '50%', 'std', 'min', 'max']]
            stats_df.columns = ['Среднее', 'Медиана', 'Ст.отклонение', 'Минимум', 'Максимум']
            st.dataframe(stats_df.round(2), use_container_width=True)
    
    with col2:
        st.subheader("Категориальные поля")
        cat_cols = ['Quality', 'Stage', 'Source', 'Product', 'stage_normalized']
        for col in cat_cols:
            if col in filtered_deals.columns:
                st.write(f"**{col}:**")
                value_counts = filtered_deals[col].value_counts().head(5)
                for val, count in value_counts.items():
                    st.write(f"  - {val}: {count} ({count/len(filtered_deals)*100:.1f}%)")
                st.write("")

# ---------- ВКЛАДКА 2: АНАЛИЗ ВРЕМЕННЫХ РЯДОВ ----------
with tabs[1]:
    st.markdown('<div class="section-title">2. АНАЛИЗ ВРЕМЕННЫХ РЯДОВ</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("Тенденция создания сделок vs Звонки")
        
        # Еженедельная агрегация
        weekly_deals = filtered_deals.set_index('Created Time').resample('W').agg({
            'Id': 'count',
            'stage_normalized': lambda x: (x == 'Active Student').sum()
        }).reset_index()
        weekly_deals.columns = ['Week', 'Leads_Count', 'Success_Count']
        
        if 'Call Start Time' in calls.columns:
            weekly_calls = calls.set_index('Call Start Time').resample('W')['Id'].count().reset_index()
            weekly_calls.columns = ['Week', 'Calls_Count']
            weekly_stats = weekly_deals.merge(weekly_calls, on='Week', how='left').fillna(0)
        else:
            weekly_stats = weekly_deals
            weekly_stats['Calls_Count'] = 0
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=weekly_stats['Week'], y=weekly_stats['Leads_Count'], 
                               name='Лиды', line=dict(color='blue', width=3)),
                     secondary_y=False)
        fig.add_trace(go.Scatter(x=weekly_stats['Week'], y=weekly_stats['Success_Count'], 
                               name='Успешные', line=dict(color='green', width=3)),
                     secondary_y=False)
        fig.add_trace(go.Scatter(x=weekly_stats['Week'], y=weekly_stats['Calls_Count'], 
                               name='Звонки', line=dict(dash='dot', color='red')),
                     secondary_y=True)
        
        fig.update_layout(title="Динамика лидов, продаж и звонков", height=500)
        fig.update_yaxes(title_text="Количество сделок", secondary_y=False)
        fig.update_yaxes(title_text="Количество звонков", secondary_y=True)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Распределение времени закрытия")
        
        if len(closed_deals) > 0:
            fig = px.histogram(closed_deals, x='Deal_Age_days', nbins=30,
                             title='Распределение Deal Age (дни)',
                             labels={'Deal_Age_days': 'Дни'})
            fig.add_vline(x=median_deal_age, line_dash="dash", line_color="red",
                         annotation_text=f"Медиана: {median_deal_age:.0f}")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            st.metric("Медиана Deal Age", f"{median_deal_age:.0f} дней")
            st.metric("Среднее Deal Age", f"{mean_deal_age:.0f} дней")

# ---------- ВКЛАДКА 3: ЭФФЕКТИВНОСТЬ КАМПАНИЙ ----------
with tabs[2]:
    st.markdown('<div class="section-title">3. ЭФФЕКТИВНОСТЬ КАМПАНИЙ</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("Воронка по источникам")
        
        # Маркетинговая воронка (из ячейки 13)
        spend_agg = spend.groupby('Source').agg({
            'Impressions': 'sum',
            'Clicks': 'sum',
            'Spend': 'sum'
        }).reset_index()
        
        leads_agg = filtered_deals.groupby('Source')['Id'].count().reset_index().rename(columns={'Id': 'Leads'})
        qual_filter = ['A - High', 'B - Medium']
        qual_leads_agg = filtered_deals[filtered_deals['Quality'].isin(qual_filter)].groupby('Source')['Id'].count().reset_index().rename(columns={'Id': 'Quality_Leads'})
        
        funnel_df = spend_agg.merge(leads_agg, on='Source', how='left').merge(qual_leads_agg, on='Source', how='left').fillna(0)
        funnel_df = funnel_df.sort_values('Spend', ascending=False).head(10)
        
        fig = go.Figure()
        stages = ['Impressions', 'Clicks', 'Leads', 'Quality_Leads']
        colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA']
        
        for i, stage in enumerate(stages):
            fig.add_trace(go.Bar(name=stage, x=funnel_df['Source'], 
                                y=funnel_df[stage], marker_color=colors[i]))
        
        fig.update_layout(barmode='group', title="Маркетинговая воронка (топ-10 источников)",
                         height=500, yaxis_type="log")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Качество источников")
        
        # Efficiency Ratio кампаний
        campaign_leads = filtered_deals[filtered_deals['stage_normalized'] == 'Lead'].groupby('Campaign')['Id'].nunique()
        campaign_active = filtered_deals[filtered_deals['stage_normalized'] == 'Active Student'].groupby('Campaign')['Id'].nunique()
        campaign_df = pd.DataFrame({'Leads': campaign_leads, 'Active': campaign_active}).fillna(0)
        campaign_df['Efficiency_Ratio'] = (campaign_df['Active'] / campaign_df['Leads'] * 100).replace([np.inf], 0).round(1)
        
        top_campaigns = campaign_df[campaign_df['Leads'] > 10].sort_values('Efficiency_Ratio', ascending=False).head(10)
        
        fig2 = px.bar(top_campaigns.reset_index(), x='Campaign', y='Efficiency_Ratio',
                     title='Топ кампаний по Efficiency Ratio (%)',
                     labels={'Efficiency_Ratio': 'Эффективность'})
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)

# ---------- ВКЛАДКА 4: ЭФФЕКТИВНОСТЬ ПРОДАЖ ----------
with tabs[3]:
    st.markdown('<div class="section-title">4. ЭФФЕКТИВНОСТЬ ОТДЕЛА ПРОДАЖ</div>', unsafe_allow_html=True)
    
    st.subheader("Рейтинг менеджеров")
    
    # Расчет KPI менеджеров (из ячейки 17)
    df_clean = filtered_deals[filtered_deals['max_stage_rank'] >= 1].copy()
    
    manager_stats = df_clean.groupby('Deal Owner Name').agg({
        'Id': 'count',
        'revenue': 'sum',
        'stage_normalized': lambda x: (x == 'Active Student').sum()
    }).reset_index()
    manager_stats.columns = ['Manager', 'Leads', 'Revenue', 'Sales']
    
    manager_stats['Win_Rate'] = (manager_stats['Sales'] / manager_stats['Leads'] * 100).round(1)
    manager_stats['Avg_Check'] = (manager_stats['Revenue'] / manager_stats['Sales']).replace([np.inf], 0).fillna(0).round(0)
    
    top_managers = manager_stats[manager_stats['Leads'] >= 10].sort_values('Revenue', ascending=False)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        fig = px.bar(top_managers.head(15), x='Manager', y='Revenue', 
                    color='Win_Rate', text='Revenue',
                    title='Топ-15 менеджеров по выручке',
                    labels={'Revenue': 'Выручка (€)', 'Win_Rate': 'Win Rate (%)'},
                    color_continuous_scale='RdYlGn')
        fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.dataframe(
            top_managers[['Manager', 'Leads', 'Sales', 'Revenue', 'Win_Rate', 'Avg_Check']]
            .head(10)
            .style.format({
                'Revenue': '{:,.0f} €',
                'Win_Rate': '{:.1f}%',
                'Avg_Check': '{:,.0f} €'
            })
            .background_gradient(subset=['Win_Rate'], cmap='RdYlGn'),
            use_container_width=True
        )
    
    # Анализ SLA
    st.subheader("Влияние скорости ответа (SLA)")
    
    if 'SLA_Segment' in filtered_deals.columns:
        sla_global = filtered_deals[
            (filtered_deals['SLA_Segment'].notna()) & 
            (filtered_deals['SLA_Segment'] != 'Unknown')
        ]
        
        sla_impact = sla_global.groupby('SLA_Segment').agg({
            'Id': 'count',
            'is_paid': 'mean'
        }).reset_index()
        sla_impact['Win_Rate_Pct'] = (sla_impact['is_paid'] * 100).round(1)
        
        fig2 = px.bar(sla_impact, x='SLA_Segment', y='Win_Rate_Pct',
                     title='Конверсия по сегментам скорости ответа',
                     labels={'Win_Rate_Pct': 'Конверсия (%)'},
                     color='Id', color_continuous_scale='RdYlGn')
        st.plotly_chart(fig2, use_container_width=True)

# ---------- ВКЛАДКА 5: ПЛАТЕЖИ И ПРОДУКТЫ ----------
with tabs[4]:
    st.markdown('<div class="section-title">5. ПЛАТЕЖИ И ПРОДУКТЫ</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Популярность продуктов")
        
        product_stats = filtered_deals.groupby('Product').agg({
            'Id': 'count',
            'revenue': 'sum',
            'is_paid': 'mean'
        }).sort_values('revenue', ascending=False)
        
        product_stats['Конверсия'] = (product_stats['is_paid'] * 100).round(1)
        
        fig = px.bar(product_stats.reset_index().head(10), 
                    x='Product', y='revenue',
                    color='Конверсия',
                    title='Топ-10 продуктов по выручке',
                    labels={'revenue': 'Выручка (€)'},
                    color_continuous_scale='RdYlGn')
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Типы оплаты")
        
        pay_col = 'Payment_Type_Recovered' if 'Payment_Type_Recovered' in filtered_deals.columns else 'Payment Type'
        if pay_col in filtered_deals.columns:
            payment_stats = filtered_deals.groupby(pay_col).agg({
                'Id': 'count',
                'revenue': 'sum',
                'Offer Total Amount': 'mean'
            }).reset_index()
            
            fig2 = px.pie(payment_stats, values='revenue', names=pay_col,
                         title='Распределение выручки по типам оплаты',
                         hole=0.4)
            st.plotly_chart(fig2, use_container_width=True)
        
        # Типы обучения
        if 'Education Type' in filtered_deals.columns:
            edu_stats = filtered_deals['Education Type'].value_counts().head(5)
            st.write("**Топ типов обучения:**")
            for edu_type, count in edu_stats.items():
                st.write(f"- {edu_type}: {count} сделок")

# ---------- ВКЛАДКА 6: ГЕОГРАФИЧЕСКИЙ АНАЛИЗ ----------
with tabs[5]:
    st.markdown('<div class="section-title">6. ГЕОГРАФИЧЕСКИЙ АНАЛИЗ</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("Карта продаж")
        
        # Агрегация по городам
        city_stats = filtered_deals.groupby('City').agg({
            'Id': 'count',
            'revenue': 'sum',
            'is_paid': 'mean'
        }).reset_index()
        city_stats = city_stats.sort_values('revenue', ascending=False).head(50)
        city_stats['Win_Rate'] = (city_stats['is_paid'] * 100).round(1)
        
        # База координат городов (упрощенная)
        city_coords = {
            'Berlin': (52.5200, 13.4050), 'München': (48.1351, 11.5820),
            'Hamburg': (53.5511, 9.9937), 'Köln': (50.9375, 6.9603),
            'Frankfurt': (50.1109, 8.6821), 'Leipzig': (51.3397, 12.3731)
        }
        
        # Добавляем координаты
        city_stats['lat'] = city_stats['City'].map(lambda x: city_coords.get(x, (51.1657, 10.4515))[0])
        city_stats['lon'] = city_stats['City'].map(lambda x: city_coords.get(x, (51.1657, 10.4515))[1])
        
        fig = px.scatter_mapbox(
            city_stats,
            lat="lat",
            lon="lon",
            size="revenue",
            color="Win_Rate",
            hover_name="City",
            hover_data={'revenue': ':.0f', 'Id': True, 'Win_Rate': ':.1f'},
            zoom=4,
            center={"lat": 51.0, "lon": 10.0},
            title="Карта продаж по городам",
            color_continuous_scale='RdYlGn'
        )
        fig.update_layout(
            mapbox_style="carto-positron",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Влияние уровня немецкого")
        
        if 'Level of Deutsch' in filtered_deals.columns:
            lang_stats = filtered_deals.groupby('Level of Deutsch').agg({
                'Id': 'count',
                'is_paid': 'mean',
                'revenue': 'sum'
            }).reset_index()
            
            lang_stats['Конверсия'] = (lang_stats['is_paid'] * 100).round(1)
            
            # Порядок уровней
            level_order = ['A0', 'A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'Unknown']
            lang_stats['Level of Deutsch'] = pd.Categorical(lang_stats['Level of Deutsch'], 
                                                           categories=level_order, 
                                                           ordered=True)
            lang_stats = lang_stats.sort_values('Level of Deutsch')
            
            fig2 = px.bar(lang_stats, x='Level of Deutsch', y='Конверсия',
                         title='Конверсия по уровням немецкого',
                         labels={'Конверсия': 'Конверсия (%)'})
            st.plotly_chart(fig2, use_container_width=True)
            
            # Топ городов по уровню языка
            st.write("**Топ городов по количеству сделок:**")
            top_cities = filtered_deals['City'].value_counts().head(5)
            for city, count in top_cities.items():
                st.write(f"- {city}: {count} сделок")

# ---------- ВКЛАДКА 7: ПРОДУКТОВАЯ АНАЛИТИКА ----------
with tabs[6]:
    st.markdown('<div class="section-title">7. ПРОДУКТОВАЯ АНАЛИТИКА И ТОЧКИ РОСТА</div>', unsafe_allow_html=True)
    
    st.subheader("Юнит-экономика по продуктам")
    
    # Расчет как в ячейке 24
    deals_success = filtered_deals[filtered_deals['stage_normalized'] == 'Active Student'].copy()
    
    if len(deals_success) > 0:
        product_econ = deals_success.groupby('Product').agg({
            'Contact Name': 'nunique',
            'revenue': 'sum',
            'Transactions': 'sum'
        }).rename(columns={'Contact Name': 'B', 'revenue': 'Revenue', 'Transactions': 'T'})
        
        product_econ['AOV'] = (product_econ['Revenue'] / product_econ['T']).round(0)
        product_econ['APC'] = (product_econ['T'] / product_econ['B']).round(2)
        product_econ['C1'] = (product_econ['B'] / TOTAL_UA).round(4)
        product_econ['CLTV'] = (product_econ['AOV'] * product_econ['APC']).round(0)
        product_econ['LTV'] = (product_econ['CLTV'] * product_econ['C1']).round(2)
        product_econ['CAC'] = (total_spend / product_econ['B']).round(0)
        product_econ['CM'] = (product_econ['Revenue'] - total_spend - (product_econ['Revenue'] * 0.0)).round(0)
        product_econ['ROMI'] = (product_econ['CM'] / total_spend * 100).round(1)
        
        display_cols = ['B', 'Revenue', 'AOV', 'APC', 'C1', 'CLTV', 'LTV', 'CAC', 'CM', 'ROMI']
        
        st.dataframe(
            product_econ[display_cols]
            .sort_values('LTV', ascending=False)
            .style.format({
                'B': '{:,.0f}',
                'Revenue': '{:,.0f} €',
                'AOV': '{:,.0f} €',
                'C1': '{:.2%}',
                'CLTV': '{:,.0f} €',
                'LTV': '{:.2f} €',
                'CAC': '{:,.0f} €',
                'CM': '{:,.0f} €',
                'ROMI': '{:.1f}%'
            })
            .background_gradient(subset=['LTV', 'ROMI'], cmap='RdYlGn'),
            use_container_width=True
        )
        
        # Анализ чувствительности
        st.subheader("Анализ точек роста")
        
        sensitivity_data = []
        metrics = ['C1', 'AOV', 'APC']
        
        for product in product_econ.index[:3]:  # Топ-3 продукта
            row = product_econ.loc[product]
            for metric in metrics:
                base = row[metric]
                for change in [0.10, 0.20, 0.30]:  # +10%, +20%, +30%
                    new_value = base * (1 + change)
                    sensitivity_data.append({
                        'Продукт': product,
                        'Метрика': metric,
                        'Рост': f"+{int(change*100)}%",
                        'Текущее': f"{base:.2f}" if metric == 'C1' else f"{base:,.0f}",
                        'Новое': f"{new_value:.2f}" if metric == 'C1' else f"{new_value:,.0f}"
                    })
        
        sensitivity_df = pd.DataFrame(sensitivity_data)
        st.dataframe(sensitivity_df, use_container_width=True)
        
        st.info("**Рекомендация:** Сфокусироваться на росте **C1 (конверсии)** для продукта с наибольшим LTV через A/B тесты в течение 2 недель.")

# ---------- ВКЛАДКА 8: ПОЛНЫЕ ДАННЫЕ ----------
with tabs[7]:
    st.markdown('<div class="section-title">8. ПОЛНЫЕ ДАННЫЕ</div>', unsafe_allow_html=True)
    
    dataset_choice = st.radio("Выберите таблицу:",
                             ["Deals", "Spend", "Contacts", "Calls"],
                             horizontal=True)
    
    if dataset_choice == "Deals":
        df = filtered_deals
    elif dataset_choice == "Spend":
        df = spend
    elif dataset_choice == "Contacts":
        df = contacts
    else:
        df = calls
    
    st.dataframe(df, use_container_width=True, height=600)
    
    # Экспорт
    col1, col2 = st.columns(2)
    
    with col1:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Скачать CSV", data=csv,
                          file_name=f"{dataset_choice.lower()}_filtered.csv",
                          mime="text/csv",
                          use_container_width=True)
    
    with col2:
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Data')
        excel_buffer.seek(0)
        st.download_button("📊 Скачать Excel", data=excel_buffer,
                          file_name=f"{dataset_choice.lower()}_filtered.xlsx",
                          mime="application/vnd.ms-excel",
                          use_container_width=True)

# ========== ФУТЕР ==========
st.markdown("---")
st.markdown(f"""
**🔄 Последнее обновление:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**📊 Отфильтровано сделок:** {len(filtered_deals):,} из {len(deals):,}  
**🎯 Покрытие дат:** {deals['Created Time'].min().date()} — {deals['Created Time'].max().date()}
""")