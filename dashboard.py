"""
ДАШБОРД ПО ТЗ - ФИНАЛЬНАЯ РАБОЧАЯ ВЕРСИЯ
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import io
import warnings
warnings.filterwarnings('ignore')

# ========== НАСТРОЙКА ==========
st.set_page_config(
    page_title="Аналитика IT школы - Полный отчет",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Чистый стиль без эмодзи
st.markdown("""
<style>
    .main-title {font-size: 2.5rem; color: #1E3A8A; font-weight: 700; margin-bottom: 1rem;}
    .section-title {font-size: 1.5rem; color: #374151; font-weight: 600; margin-top: 2rem; margin-bottom: 1rem; 
                    border-bottom: 2px solid #3B82F6; padding-bottom: 0.5rem;}
    .metric-grid {display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin: 1rem 0;}
    .metric-card {background: #F8FAFC; padding: 1rem; border-radius: 0.5rem; border: 1px solid #E5E7EB;}
    .metric-value {font-size: 1.5rem; font-weight: 700; color: #1F2937;}
    .metric-label {font-size: 0.8rem; color: #6B7280; margin-top: 0.3rem;}
</style>
""", unsafe_allow_html=True)

# ========== ЗАГРУЗКА ДАННЫХ ==========
@st.cache_data(ttl=3600, show_spinner=False)
def load_all_data():
    deals = pd.read_parquet('deals_clean.parquet')
    spend = pd.read_parquet('spend_clean.parquet')
    contacts = pd.read_parquet('contacts_clean.parquet')
    
    # Конвертация дат
    for col in ['Created Time', 'Closing Date']:
        if col in deals.columns:
            deals[col] = pd.to_datetime(deals[col], errors='coerce')
    
    return deals, spend, contacts

deals, spend, contacts = load_all_data()

# ========== РАСЧЕТ ВСЕХ МЕТРИК ==========
TOTAL_UA = contacts['Id'].nunique()
active_students = deals[deals['stage_normalized'] == 'Active Student']
TOTAL_B = active_students['Contact Name'].nunique() if 'Contact Name' in active_students.columns else active_students['Id'].nunique()
total_revenue = deals['revenue'].sum()
total_spend = spend['Spend'].sum()
avg_check = total_revenue / TOTAL_B if TOTAL_B > 0 else 0
conversion_vacuum = (TOTAL_B / TOTAL_UA * 100) if TOTAL_UA > 0 else 0
romi_total = ((total_revenue - total_spend) / total_spend * 100) if total_spend > 0 else 0
cm_total = total_revenue - total_spend
products_count = deals['Product'].nunique()
managers_count = deals['Deal Owner Name'].nunique()
cities_count = deals['City'].nunique() if 'City' in deals.columns else 0
sources_count = deals['Source'].nunique()

# Deal Age
closed_deals = deals[
    (deals['stage_normalized'] == 'Active Student') & 
    (deals['Closing Date'].notna())
].copy()
if 'Deal_Age_days' in closed_deals.columns:
    closed_deals['Deal_Age_days'] = pd.to_numeric(closed_deals['Deal_Age_days'], errors='coerce')
    median_deal_age = closed_deals['Deal_Age_days'].median() if len(closed_deals) > 0 else 0
    mean_deal_age = closed_deals['Deal_Age_days'].mean() if len(closed_deals) > 0 else 0
else:
    median_deal_age = 0
    mean_deal_age = 0

# Топ продукт
if len(active_students) > 0:
    top_product = active_students.groupby('Product')['revenue'].sum().idxmax()
else:
    top_product = "Нет данных"

# Топ менеджер
if len(deals) > 0:
    top_manager = deals.groupby('Deal Owner Name')['revenue'].sum().idxmax()
    top_manager_revenue = deals.groupby('Deal Owner Name')['revenue'].sum().max()
else:
    top_manager = "Нет данных"
    top_manager_revenue = 0

# ========== ФИЛЬТРЫ ==========
with st.sidebar:
    st.markdown("### ФИЛЬТРЫ")
    
    # Даты
    min_date = deals['Created Time'].min().date()
    max_date = deals['Created Time'].max().date()
    date_range = st.date_input("Диапазон дат", [min_date, max_date], label_visibility="visible")
    
    # Списки с проверкой
    all_sources = sorted(deals['Source'].dropna().unique().tolist()) if 'Source' in deals.columns else []
    all_products = sorted(deals['Product'].dropna().unique().tolist()) if 'Product' in deals.columns else []
    all_cities = sorted(deals['City'].dropna().unique().tolist()) if 'City' in deals.columns else []
    all_managers = sorted(deals['Deal Owner Name'].dropna().unique().tolist()) if 'Deal Owner Name' in deals.columns else []
    
    if all_sources:
        selected_sources = st.multiselect("Источники", all_sources, default=all_sources[:3], label_visibility="visible")
    else:
        selected_sources = []
    
    if all_products:
        selected_products = st.multiselect("Продукты", all_products, default=all_products[:3], label_visibility="visible")
    else:
        selected_products = []
    
    if all_cities:
        selected_cities = st.multiselect("Города", all_cities, default=all_cities[:3], label_visibility="visible")
    else:
        selected_cities = []
    
    if all_managers:
        selected_managers = st.multiselect("Менеджеры", all_managers, default=all_managers[:3], label_visibility="visible")
    else:
        selected_managers = []

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
    
    return filtered

filtered_deals = apply_filters()

# ========== ЗАГОЛОВОК И МЕТРИКИ ==========
st.markdown('<div class="main-title">АНАЛИТИКА ОНЛАЙН-ШКОЛЫ IT СПЕЦИАЛИСТОВ</div>', unsafe_allow_html=True)
st.markdown("---")

# Метрики в сетке
st.markdown('<div class="section-title">КЛЮЧЕВЫЕ ПОКАЗАТЕЛИ</div>', unsafe_allow_html=True)

metrics = [
    ("Выручка", f"{total_revenue:,.0f} €"),
    ("Средний чек", f"{avg_check:,.0f} €"),
    ("Клиенты (B)", f"{TOTAL_B:,}"),
    ("Уникальные контакты", f"{TOTAL_UA:,}"),
    ("Продукты", str(products_count)),
    ("Менеджеры", str(managers_count)),
    ("Города", str(cities_count)),
    ("Источники", str(sources_count)),
    ("Конверсия", f"{conversion_vacuum:.1f}%"),
    ("ROMI", f"{romi_total:.1f}%"),
    ("Маржинальный вклад", f"{cm_total:,.0f} €"),
    ("Время сделки (медиана)", f"{median_deal_age:.0f} дн"),
    ("Время сделки (среднее)", f"{mean_deal_age:.0f} дн"),
    ("Топ продукт", str(top_product)),
    ("Топ менеджер", f"{top_manager} ({top_manager_revenue:,.0f}€)")
]

# Отображаем в 5 колонок
cols = st.columns(5)
for idx, (label, value) in enumerate(metrics):
    with cols[idx % 5]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ========== ВКЛАДКИ ==========
tab_names = [
    "ОПИСАТЕЛЬНАЯ СТАТИСТИКА",
    "АНАЛИЗ ВРЕМЕННЫХ РЯДОВ", 
    "ЭФФЕКТИВНОСТЬ КАМПАНИЙ",
    "ЭФФЕКТИВНОСТЬ ПРОДАЖ",
    "ПЛАТЕЖИ И ПРОДУКТЫ",
    "ГЕОГРАФИЧЕСКИЙ АНАЛИЗ",
    "ПРОДУКТОВАЯ АНАЛИТИКА",
    "ДАННЫЕ"
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
            numeric_data = filtered_deals[numeric_cols]
            stats = numeric_data.describe().T[['mean', '50%', 'min', 'max']]
            stats.columns = ['Среднее', 'Медиана', 'Минимум', 'Максимум']
            st.dataframe(stats.round(2), use_container_width=True)
    
    with col2:
        st.subheader("Категориальные поля")
        cat_cols = [col for col in ['Quality', 'Stage', 'Source', 'Product'] if col in filtered_deals.columns]
        for col in cat_cols[:3]:  # Первые 3 колонки
            st.write(f"**{col}:**")
            counts = filtered_deals[col].value_counts().head(5)
            for val, count in counts.items():
                percentage = (count / len(filtered_deals) * 100) if len(filtered_deals) > 0 else 0
                st.write(f"- {val}: {count} ({percentage:.1f}%)")

# ---------- ВКЛАДКА 2: АНАЛИЗ ВРЕМЕННЫХ РЯДОВ ----------
with tabs[1]:
    st.markdown('<div class="section-title">2. АНАЛИЗ ВРЕМЕННЫХ РЯДОВ</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("Тенденция создания сделок")
        
        # Ежемесячная статистика
        monthly = filtered_deals.set_index('Created Time').resample('M').agg({
            'Id': 'count',
            'stage_normalized': lambda x: (x == 'Active Student').sum()
        }).reset_index()
        monthly.columns = ['Month', 'Leads', 'Success']
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=monthly['Month'], y=monthly['Leads'], 
                               name='Лиды', line=dict(color='blue', width=3)))
        fig.add_trace(go.Scatter(x=monthly['Month'], y=monthly['Success'], 
                               name='Успешные', line=dict(color='green', width=3)))
        fig.update_layout(title="Динамика лидов и продаж по месяцам", height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Распределение времени закрытия")
        
        if 'Deal_Age_days' in filtered_deals.columns:
            valid_ages = filtered_deals[
                (filtered_deals['Deal_Age_days'].notna()) & 
                (filtered_deals['Deal_Age_days'] >= 0)
            ]['Deal_Age_days']
            
            if len(valid_ages) > 0:
                fig = px.histogram(valid_ages, nbins=30, 
                                 title='Распределение Deal Age',
                                 labels={'value': 'Дни'})
                fig.add_vline(x=median_deal_age, line_dash="dash", line_color="red",
                             annotation_text=f"Медиана: {median_deal_age:.0f}")
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Нет данных по времени закрытия")

# ---------- ВКЛАДКА 3: ЭФФЕКТИВНОСТЬ КАМПАНИЙ ----------
with tabs[2]:
    st.markdown('<div class="section-title">3. ЭФФЕКТИВНОСТЬ КАМПАНИЙ</div>', unsafe_allow_html=True)
    
    st.subheader("Маркетинговая воронка по источникам")
    
    if 'Source' in spend.columns and 'Source' in filtered_deals.columns:
        # Агрегация расходов
        spend_agg = spend.groupby('Source').agg({
            'Impressions': 'sum',
            'Clicks': 'sum',
            'Spend': 'sum'
        }).reset_index()
        
        # Агрегация лидов
        leads_agg = filtered_deals.groupby('Source')['Id'].count().reset_index().rename(columns={'Id': 'Leads'})
        
        # Объединение
        funnel_df = spend_agg.merge(leads_agg, on='Source', how='left').fillna(0)
        funnel_df = funnel_df.sort_values('Spend', ascending=False).head(10)
        
        # Визуализация
        fig = go.Figure()
        fig.add_trace(go.Bar(x=funnel_df['Source'], y=funnel_df['Impressions'], name='Показы'))
        fig.add_trace(go.Bar(x=funnel_df['Source'], y=funnel_df['Clicks'], name='Клики'))
        fig.add_trace(go.Bar(x=funnel_df['Source'], y=funnel_df['Leads'], name='Лиды'))
        
        fig.update_layout(barmode='group', title="Воронка по источникам (топ-10 по расходам)",
                         height=500, yaxis_type="log")
        st.plotly_chart(fig, use_container_width=True)
        
        # ROI анализ
        st.subheader("ROI по источникам")
        roi_df = funnel_df.copy()
        roi_df['CPC'] = (roi_df['Spend'] / roi_df['Clicks']).replace([np.inf], 0).round(2)
        roi_df['CPL'] = (roi_df['Spend'] / roi_df['Leads']).replace([np.inf], 0).round(2)
        
        fig2 = px.scatter(roi_df, x='CPC', y='Leads', size='Spend',
                         color='Source', hover_name='Source',
                         title='CPC vs Количество лидов')
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Нет данных по источникам в таблицах Spend или Deals")

# ---------- ВКЛАДКА 4: ЭФФЕКТИВНОСТЬ ПРОДАЖ ----------
with tabs[3]:
    st.markdown('<div class="section-title">4. ЭФФЕКТИВНОСТЬ ОТДЕЛА ПРОДАЖ</div>', unsafe_allow_html=True)
    
    if 'Deal Owner Name' in filtered_deals.columns:
        st.subheader("Рейтинг менеджеров")
        
        # Группировка по менеджерам
        manager_stats = filtered_deals.groupby('Deal Owner Name').agg({
            'Id': 'count',
            'revenue': 'sum',
            'is_paid': 'mean'
        }).sort_values('revenue', ascending=False).head(15)
        
        manager_stats['Конверсия'] = (manager_stats['is_paid'] * 100).round(1)
        
        fig = px.bar(manager_stats.reset_index(), x='Deal Owner Name', y='revenue',
                    color='Конверсия', title='Топ-15 менеджеров по выручке',
                    labels={'revenue': 'Выручка (€)', 'Deal Owner Name': 'Менеджер'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Таблица детализации
        st.subheader("Детальная статистика")
        st.dataframe(
            manager_stats.reset_index().rename(columns={'Id': 'Сделок', 'revenue': 'Выручка'})[['Deal Owner Name', 'Сделок', 'Выручка', 'Конверсия']]
            .style.format({'Выручка': '{:,.0f} €', 'Конверсия': '{:.1f}%'})
            .background_gradient(subset=['Конверсия'], cmap='RdYlGn'),
            use_container_width=True
        )
    else:
        st.info("Нет данных по менеджерам")

# ---------- ВКЛАДКА 5: ПЛАТЕЖИ И ПРОДУКТЫ ----------
with tabs[4]:
    st.markdown('<div class="section-title">5. ПЛАТЕЖИ И ПРОДУКТЫ</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Популярность продуктов")
        
        if 'Product' in filtered_deals.columns:
            product_stats = filtered_deals.groupby('Product').agg({
                'Id': 'count',
                'revenue': 'sum',
                'is_paid': 'mean'
            }).sort_values('revenue', ascending=False).head(10)
            
            product_stats['Конверсия'] = (product_stats['is_paid'] * 100).round(1)
            
            fig = px.bar(product_stats.reset_index(), x='Product', y='revenue',
                        color='Конверсия', title='Топ-10 продуктов по выручке',
                        labels={'revenue': 'Выручка (€)'})
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Типы оплаты")
        
        pay_col = 'Payment_Type_Recovered' if 'Payment_Type_Recovered' in filtered_deals.columns else 'Payment Type'
        if pay_col in filtered_deals.columns:
            payment_stats = filtered_deals[pay_col].value_counts().head(10)
            fig = px.pie(values=payment_stats.values, names=payment_stats.index,
                        title='Распределение по типам оплаты', hole=0.4)
            st.plotly_chart(fig, use_container_width=True)

# ---------- ВКЛАДКА 6: ГЕОГРАФИЧЕСКИЙ АНАЛИЗ ----------
with tabs[5]:
    st.markdown('<div class="section-title">6. ГЕОГРАФИЧЕСКИЙ АНАЛИЗ</div>', unsafe_allow_html=True)
    
    if 'City' in filtered_deals.columns:
        st.subheader("Распределение по городам")
        
        # Топ городов
        city_stats = filtered_deals.groupby('City').agg({
            'Id': 'count',
            'revenue': 'sum',
            'is_paid': 'mean'
        }).sort_values('revenue', ascending=False).head(20)
        
        city_stats['Конверсия'] = (city_stats['is_paid'] * 100).round(1)
        
        fig = px.bar(city_stats.reset_index(), x='City', y='revenue',
                    color='Конверсия', title='Топ-20 городов по выручке',
                    labels={'revenue': 'Выручка (€)'})
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Уровни немецкого
        if 'Level of Deutsch' in filtered_deals.columns:
            st.subheader("Влияние уровня немецкого")
            
            lang_stats = filtered_deals.groupby('Level of Deutsch').agg({
                'Id': 'count',
                'is_paid': 'mean'
            }).reset_index()
            lang_stats['Конверсия'] = (lang_stats['is_paid'] * 100).round(1)
            
            fig2 = px.bar(lang_stats, x='Level of Deutsch', y='Конверсия',
                         title='Конверсия по уровням языка')
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Нет данных по городам")

# ---------- ВКЛАДКА 7: ПРОДУКТОВАЯ АНАЛИТИКА ----------
with tabs[6]:
    st.markdown('<div class="section-title">7. ПРОДУКТОВАЯ АНАЛИТИКА</div>', unsafe_allow_html=True)
    
    if 'Product' in filtered_deals.columns and 'stage_normalized' in filtered_deals.columns:
        st.subheader("Юнит-экономика продуктов")
        
        # Расчет для активных студентов
        active_products = filtered_deals[filtered_deals['stage_normalized'] == 'Active Student']
        
        if len(active_products) > 0:
            product_econ = active_products.groupby('Product').agg({
                'Id': 'count',
                'revenue': 'sum'
            }).rename(columns={'Id': 'Студенты', 'revenue': 'Выручка'})
            
            product_econ['Средний чек'] = (product_econ['Выручка'] / product_econ['Студенты']).round(0)
            product_econ['Доля выручки'] = (product_econ['Выручка'] / product_econ['Выручка'].sum() * 100).round(1)
            
            st.dataframe(
                product_econ.style.format({
                    'Выручка': '{:,.0f} €',
                    'Средний чек': '{:,.0f} €',
                    'Доля выручки': '{:.1f}%'
                }).background_gradient(subset=['Выручка'], cmap='RdYlGn'),
                use_container_width=True
            )
            
            # Матрица продуктов
            st.subheader("Матрица продуктов")
            fig = px.scatter(product_econ.reset_index(), x='Студенты', y='Средний чек',
                            size='Выручка', color='Product', hover_name='Product',
                            title='Матрица: Студенты vs Средний чек')
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Нет данных для продуктовой аналитики")

# ---------- ВКЛАДКА 8: ДАННЫЕ ----------
with tabs[7]:
    st.markdown('<div class="section-title">8. ПОЛНЫЕ ДАННЫЕ</div>', unsafe_allow_html=True)
    
    dataset_choice = st.radio("Выберите таблицу:", ["Deals", "Spend", "Contacts"], horizontal=True)
    
    if dataset_choice == "Deals":
        df = filtered_deals
    elif dataset_choice == "Spend":
        df = spend
    else:
        df = contacts
    
    st.dataframe(df, use_container_width=True, height=500)
    
    # Экспорт
    col1, col2 = st.columns(2)
    with col1:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Скачать CSV", data=csv,
                          file_name=f"{dataset_choice.lower()}.csv",
                          mime="text/csv",
                          use_container_width=True)
    with col2:
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Data')
        excel_buffer.seek(0)
        st.download_button("Скачать Excel", data=excel_buffer,
                          file_name=f"{dataset_choice.lower()}.xlsx",
                          mime="application/vnd.ms-excel",
                          use_container_width=True)

# ========== ФУТЕР ==========
st.markdown("---")
st.markdown(f"""
**Дашборд обновлен:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Отфильтровано сделок:** {len(filtered_deals):,} из {len(deals):,}  
**Период данных:** {deals['Created Time'].min().date()} – {deals['Created Time'].max().date()}
""")