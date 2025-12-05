"""
ПОЛНЫЙ АНАЛИТИЧЕСКИЙ ДАШБОРД С ВСЕМИ ТАБЛИЦАМИ ИЗ АНАЛИЗА
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io
import warnings
warnings.filterwarnings('ignore')

# ========== НАСТРОЙКА ==========
st.set_page_config(
    page_title="Полный анализ IT школы",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Простой стиль
st.markdown("""
<style>
    .main-title {font-size: 2rem; color: #1E3A8A; font-weight: 700; margin-bottom: 0.5rem;}
    .section-title {font-size: 1.3rem; color: #374151; font-weight: 600; margin-top: 1.5rem; padding-bottom: 0.3rem; border-bottom: 2px solid #3B82F6;}
    .metric-box {background: #f8fafc; padding: 1rem; border-radius: 0.5rem; margin: 0.3rem 0; border: 1px solid #e5e7eb;}
    .dataframe-table {font-size: 0.9rem;}
</style>
""", unsafe_allow_html=True)

# ========== ЗАГРУЗКА ДАННЫХ ==========
@st.cache_data(ttl=3600, show_spinner=False)
def load_data():
    deals = pd.read_parquet('deals_clean.parquet')
    spend = pd.read_parquet('spend_clean.parquet')
    contacts = pd.read_parquet('contacts_clean.parquet')
    
    # Конвертация дат
    for col in ['Created Time', 'Closing Date']:
        if col in deals.columns:
            deals[col] = pd.to_datetime(deals[col], errors='coerce')
    
    # Удаляем timedelta колонки
    td_cols = deals.select_dtypes(include=['timedelta64[ns]']).columns
    for col in td_cols:
        deals[col] = deals[col].astype(str)
    
    return deals, spend, contacts

deals, spend, contacts = load_data()

# ========== РАСЧЕТ ВСЕХ МЕТРИК (как в твоем анализе) ==========
TOTAL_UA = contacts['Id'].nunique()
active_students = deals[deals['stage_normalized'] == 'Active Student']
TOTAL_B = active_students['Contact Name'].nunique() if 'Contact Name' in active_students.columns else len(active_students)
total_revenue = deals['revenue'].sum()
total_spend = spend['Spend'].sum()
avg_check = total_revenue / TOTAL_B if TOTAL_B > 0 else 0
conversion = (TOTAL_B / TOTAL_UA * 100) if TOTAL_UA > 0 else 0
romi = ((total_revenue - total_spend) / total_spend * 100) if total_spend > 0 else 0
cm = total_revenue - total_spend
products_count = deals['Product'].nunique()
managers_count = deals['Deal Owner Name'].nunique()
cities_count = deals['City'].nunique() if 'City' in deals.columns else 0
sources_count = deals['Source'].nunique()
campaigns_count = deals['Campaign'].nunique() if 'Campaign' in deals.columns else 0

# Deal Age
if 'Deal_Age_days' in deals.columns:
    valid_age = deals[deals['Deal_Age_days'].notna()]['Deal_Age_days']
    median_age = valid_age.median() if len(valid_age) > 0 else 0
    mean_age = valid_age.mean() if len(valid_age) > 0 else 0
else:
    median_age = 0
    mean_age = 0

# Топ продукт
if len(active_students) > 0:
    top_product = active_students.groupby('Product')['revenue'].sum().idxmax()
else:
    top_product = "Нет данных"

# Топ менеджер
top_manager_df = deals.groupby('Deal Owner Name')['revenue'].sum()
if len(top_manager_df) > 0:
    top_manager = top_manager_df.idxmax()
    top_manager_rev = top_manager_df.max()
else:
    top_manager = "Нет данных"
    top_manager_rev = 0

# ========== РАСЧЕТ ЮНИТ-ЭКОНОМИКИ (как в ячейке 24) ==========
def calculate_unit_economics():
    """Расчет юнит-экономики как в анализе"""
    
    # Подготовка данных
    deals_eco = deals.copy()
    deals_eco['Transactions'] = np.where(
        deals_eco['Payment_Type_Recovered'] == 'one payment', 
        1, 
        deals_eco['Months of study'].fillna(1)
    )
    deals_eco.loc[deals_eco['stage_normalized'] != 'Active Student', 'Transactions'] = 0
    
    # Расчет для всего бизнеса
    total_t = deals_eco['Transactions'].sum()
    total_cogs = 0  # Как в твоем анализе
    
    # TOTAL BUSINESS
    total_business = pd.DataFrame({
        'Product': ['TOTAL BUSINESS'],
        'UA': [TOTAL_UA],
        'B': [TOTAL_B],
        'C1': [TOTAL_B / TOTAL_UA if TOTAL_UA > 0 else 0],
        'AOV': [total_revenue / total_t if total_t > 0 else 0],
        'T': [total_t],
        'APC': [total_t / TOTAL_B if TOTAL_B > 0 else 0],
        'COGS': [total_cogs],
        'Revenue': [total_revenue],
        'CLTV': [total_revenue / TOTAL_B if TOTAL_B > 0 else 0],
        'LTV': [((total_revenue / TOTAL_B) * (TOTAL_B / TOTAL_UA)) if TOTAL_B > 0 and TOTAL_UA > 0 else 0],
        'AC': [total_spend],
        'CPA': [total_spend / TOTAL_UA if TOTAL_UA > 0 else 0],
        'CAC': [total_spend / TOTAL_B if TOTAL_B > 0 else 0],
        'CM': [cm],
        'ROMI': [romi]
    })
    
    # По продуктам
    active_products = deals_eco[deals_eco['stage_normalized'] == 'Active Student']
    product_stats = active_products.groupby('Product').agg({
        'Contact Name': 'nunique',
        'revenue': 'sum',
        'Transactions': 'sum'
    }).rename(columns={'Contact Name': 'B', 'revenue': 'Revenue', 'Transactions': 'T'})
    
    if len(product_stats) > 0:
        product_stats['UA'] = TOTAL_UA
        product_stats['C1'] = product_stats['B'] / product_stats['UA']
        product_stats['AOV'] = product_stats['Revenue'] / product_stats['T']
        product_stats['APC'] = product_stats['T'] / product_stats['B']
        product_stats['COGS'] = 0
        product_stats['CLTV'] = product_stats['AOV'] * product_stats['APC']
        product_stats['LTV'] = product_stats['CLTV'] * product_stats['C1']
        product_stats['AC'] = total_spend
        product_stats['CPA'] = total_spend / TOTAL_UA
        product_stats['CAC'] = total_spend / product_stats['B']
        product_stats['CM'] = product_stats['Revenue'] - total_spend
        product_stats['ROMI'] = (product_stats['CM'] / total_spend * 100) if total_spend > 0 else 0
        
        product_stats = product_stats.reset_index()
        product_stats = product_stats[product_stats['B'] > 0]  # Убираем продукты без продаж
        
        # Объединяем с TOTAL
        unit_econ = pd.concat([total_business, product_stats], ignore_index=True)
    else:
        unit_econ = total_business
    
    return unit_econ

unit_economics_df = calculate_unit_economics()

# ========== АНАЛИЗ ТОЧЕК РОСТА (как в ячейке 25) ==========
def calculate_growth_analysis():
    """Анализ точек роста"""
    
    # Берем топ-3 продукта
    top_products = unit_economics_df[unit_economics_df['Product'] != 'TOTAL BUSINESS'].nlargest(3, 'Revenue')
    
    growth_data = []
    for _, row in top_products.iterrows():
        product = row['Product']
        c1 = row['C1']
        aov = row['AOV']
        apc = row['APC']
        b = row['B']
        
        # Сценарии роста
        for metric, base, label in [('C1', c1, 'Конверсия'), 
                                   ('AOV', aov, 'Средний чек'), 
                                   ('APC', apc, 'Частота платежей')]:
            for change in [0.10, 0.20, 0.30]:  # +10%, +20%, +30%
                new_value = base * (1 + change)
                growth_data.append({
                    'Продукт': product,
                    'Метрика': label,
                    'Изменение': f"+{int(change*100)}%",
                    'Текущее': f"{base:.3f}" if metric == 'C1' else f"{base:.1f}",
                    'Новое': f"{new_value:.3f}" if metric == 'C1' else f"{new_value:.1f}"
                })
    
    return pd.DataFrame(growth_data)

growth_df = calculate_growth_analysis()

# ========== ФИЛЬТРЫ ==========
with st.sidebar:
    st.markdown("**ФИЛЬТРЫ ДАННЫХ**")
    
    # Даты
    min_date = deals['Created Time'].min().date()
    max_date = deals['Created Time'].max().date()
    date_range = st.date_input("Диапазон дат", [min_date, max_date])
    
    # Получаем ВСЕ значения
    all_sources = deals['Source'].dropna().unique().tolist() if 'Source' in deals.columns else []
    all_products = deals['Product'].dropna().unique().tolist() if 'Product' in deals.columns else []
    all_cities = deals['City'].dropna().unique().tolist() if 'City' in deals.columns else []
    all_managers = deals['Deal Owner Name'].dropna().unique().tolist() if 'Deal Owner Name' in deals.columns else []
    
    # По умолчанию ВСЕ значения
    selected_sources = st.multiselect("Источники", all_sources, default=all_sources)
    selected_products = st.multiselect("Продукты", all_products, default=all_products)
    selected_cities = st.multiselect("Города", all_cities, default=all_cities)
    selected_managers = st.multiselect("Менеджеры", all_managers, default=all_managers)
    
    st.markdown("---")
    if st.button("Сбросить фильтры", use_container_width=True):
        st.rerun()

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

# ========== ЗАГОЛОВОК ==========
st.markdown('<div class="main-title">ПОЛНЫЙ АНАЛИТИЧЕСКИЙ ОТЧЕТ IT ШКОЛЫ</div>', unsafe_allow_html=True)
st.markdown(f"*Период анализа: {min_date} - {max_date} | Отфильтровано: {len(filtered_deals):,} из {len(deals):,} сделок*")
st.markdown("---")

# ========== КЛЮЧЕВЫЕ МЕТРИКИ ==========
st.markdown('<div class="section-title">СВОДНЫЕ ПОКАЗАТЕЛИ БИЗНЕСА</div>', unsafe_allow_html=True)

metrics_data = [
    ("Выручка", f"{total_revenue:,.0f} €", "Total Revenue"),
    ("Средний чек", f"{avg_check:,.0f} €", "Average Check"),
    ("Клиенты (B)", f"{TOTAL_B:,}", "Buyers Count"),
    ("Уникальные контакты", f"{TOTAL_UA:,}", "UA Count"),
    ("Конверсия (B/UA)", f"{conversion:.1f}%", "Vacuum Conversion"),
    ("ROMI", f"{romi:.1f}%", "(Revenue-Spend)/Spend"),
    ("Маржинальный вклад", f"{cm:,.0f} €", "Contribution Margin"),
    ("Продуктов", str(products_count), "Products Count"),
    ("Менеджеров", str(managers_count), "Managers Count"),
    ("Городов", str(cities_count), "Cities Count"),
    ("Источников", str(sources_count), "Sources Count"),
    ("Кампаний", str(campaigns_count), "Campaigns Count"),
    ("Время сделки (медиана)", f"{median_age:.0f} дн", "Deal Age Median"),
    ("Время сделки (среднее)", f"{mean_age:.0f} дн", "Deal Age Mean"),
    ("Топ продукт", str(top_product), "Top Product by Revenue"),
    ("Топ менеджер", f"{top_manager} ({top_manager_rev:,.0f}€)", "Top Manager")
]

# Отображаем в 4 колонки
cols = st.columns(4)
for idx, (label, value, tooltip) in enumerate(metrics_data):
    with cols[idx % 4]:
        st.markdown(f'<div class="metric-box"><b>{label}</b><br>{value}<br><small style="color:#6b7280">{tooltip}</small></div>', unsafe_allow_html=True)

st.markdown("---")

# ========== ВКЛАДКИ ==========
tabs = st.tabs([
    "ЮНИТ-ЭКОНОМИКА",
    "ТОЧКИ РОСТА",
    "МАРКЕТИНГ",
    "ПРОДАЖИ",
    "ПРОДУКТЫ",
    "ГЕОГРАФИЯ",
    "СТАТИСТИКА",
    "ДАННЫЕ"
])

# ---------- ВКЛАДКА 1: ЮНИТ-ЭКОНОМИКА ----------
with tabs[0]:
    st.markdown('<div class="section-title">ЮНИТ-ЭКОНОМИКА БИЗНЕСА</div>', unsafe_allow_html=True)
    
    # Форматирование числовых значений
    def format_unit_econ(df):
        return df.style.format({
            'UA': '{:,.0f}',
            'B': '{:,.0f}',
            'C1': '{:.2%}',
            'AOV': '{:,.1f}',
            'T': '{:,.0f}',
            'APC': '{:.2f}',
            'COGS': '{:.1f}',
            'Revenue': '{:,.0f}',
            'CLTV': '{:,.1f}',
            'LTV': '{:.1f}',
            'AC': '{:,.0f}',
            'CPA': '{:.2f}',
            'CAC': '{:,.1f}',
            'CM': '{:,.0f}',
            'ROMI': '{:.1f}%'
        })
    
    st.subheader("1. ЭКОНОМИКА ВСЕГО БИЗНЕСА")
    total_business = unit_economics_df[unit_economics_df['Product'] == 'TOTAL BUSINESS']
    st.dataframe(
        format_unit_econ(total_business).background_gradient(subset=['ROMI', 'LTV'], cmap='RdYlGn'),
        use_container_width=True
    )
    
    st.subheader("2. ЭКОНОМИКА ПО ПРОДУКТАМ (ВАКУУМНАЯ МОДЕЛЬ)")
    products_econ = unit_economics_df[unit_economics_df['Product'] != 'TOTAL BUSINESS'].sort_values('Revenue', ascending=False)
    st.dataframe(
        format_unit_econ(products_econ).background_gradient(subset=['ROMI', 'LTV'], cmap='RdYlGn'),
        use_container_width=True
    )
    
    # Визуализация
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(products_econ, x='Product', y='Revenue',
                    title='Выручка по продуктам', color='LTV',
                    color_continuous_scale='RdYlGn')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig2 = px.scatter(products_econ, x='C1', y='LTV', size='Revenue',
                         color='Product', hover_name='Product',
                         title='Матрица: Конверсия vs LTV')
        st.plotly_chart(fig2, use_container_width=True)

# ---------- ВКЛАДКА 2: ТОЧКИ РОСТА ----------
with tabs[1]:
    st.markdown('<div class="section-title">АНАЛИЗ ТОЧЕК РОСТА</div>', unsafe_allow_html=True)
    
    st.subheader("Сценарии роста для топ-продуктов")
    
    if len(growth_df) > 0:
        # Таблица
        st.dataframe(
            growth_df.style.background_gradient(subset=['Новое'], cmap='YlOrBr'),
            use_container_width=True
        )
        
        # Визуализация
        st.subheader("Визуализация потенциала роста")
        
        pivot_df = growth_df.pivot_table(
            index=['Продукт', 'Метрика'],
            columns='Изменение',
            values='Новое',
            aggfunc='first'
        ).reset_index()
        
        fig = px.bar(pivot_df, x='Продукт', y=['+10%', '+20%', '+30%'],
                    barmode='group', title='Потенциал роста метрик')
        st.plotly_chart(fig, use_container_width=True)
        
        # Рекомендации
        st.subheader("Рекомендации")
        st.markdown("""
        1. **Приоритет 1: Повышение конверсии (C1) для digital marketing**  
           - Текущая конверсия: 2.52%  
           - Цель: +10% → 2.77%  
           - Метод: A/B тесты на посадочных страницах (2 недели)
        
        2. **Приоритет 2: Увеличение среднего чека (AOV) для ux/ui design**  
           - Текущий AOV: 881€  
           - Цель: +10% → 969€  
           - Метод: апсейл дополнительных модулей
        
        3. **Приоритет 3: Частота платежей (APC) для web developer**  
           - Текущий APC: 3.20  
           - Цель: +10% → 3.52  
           - Метод: внедрение подписочной модели
        """)
    else:
        st.info("Недостаточно данных для анализа точек роста")

# ---------- ВКЛАДКА 3: МАРКЕТИНГ ----------
with tabs[2]:
    st.markdown('<div class="section-title">ЭФФЕКТИВНОСТЬ КАМПАНИЙ</div>', unsafe_allow_html=True)
    
    if 'Source' in spend.columns:
        st.subheader("Маркетинговая воронка")
        
        # Агрегация
        spend_agg = spend.groupby('Source').agg({
            'Impressions': 'sum',
            'Clicks': 'sum',
            'Spend': 'sum'
        }).reset_index()
        
        leads_agg = filtered_deals.groupby('Source')['Id'].count().reset_index().rename(columns={'Id': 'Leads'})
        
        funnel_df = spend_agg.merge(leads_agg, on='Source', how='left').fillna(0)
        funnel_df = funnel_df.sort_values('Spend', ascending=False).head(10)
        
        # График
        fig = go.Figure()
        fig.add_trace(go.Bar(x=funnel_df['Source'], y=funnel_df['Impressions'], name='Показы'))
        fig.add_trace(go.Bar(x=funnel_df['Source'], y=funnel_df['Clicks'], name='Клики'))
        fig.add_trace(go.Bar(x=funnel_df['Source'], y=funnel_df['Leads'], name='Лиды'))
        
        fig.update_layout(barmode='group', title="Воронка по источникам (топ-10)",
                         height=500, yaxis_type="log")
        st.plotly_chart(fig, use_container_width=True)
        
        # ROI анализ
        st.subheader("ROI по источникам")
        roi_df = funnel_df.copy()
        roi_df['CPC'] = (roi_df['Spend'] / roi_df['Clicks']).replace([np.inf], 0).round(2)
        roi_df['CPL'] = (roi_df['Spend'] / roi_df['Leads']).replace([np.inf], 0).round(2)
        
        fig2 = px.scatter(roi_df, x='CPC', y='CPL', size='Spend',
                         color='Source', hover_name='Source',
                         title='Стоимость клика vs Стоимость лида')
        st.plotly_chart(fig2, use_container_width=True)

# ---------- ВКЛАДКА 4: ПРОДАЖИ ----------
with tabs[3]:
    st.markdown('<div class="section-title">ЭФФЕКТИВНОСТЬ ПРОДАЖ</div>', unsafe_allow_html=True)
    
    if 'Deal Owner Name' in filtered_deals.columns:
        st.subheader("Рейтинг менеджеров")
        
        manager_stats = filtered_deals.groupby('Deal Owner Name').agg({
            'Id': 'count',
            'revenue': 'sum',
            'is_paid': 'mean'
        }).sort_values('revenue', ascending=False).head(20)
        
        manager_stats['Конверсия'] = (manager_stats['is_paid'] * 100).round(1)
        
        fig = px.bar(manager_stats.reset_index(), x='Deal Owner Name', y='revenue',
                    color='Конверсия', title='Топ-20 менеджеров по выручке',
                    labels={'revenue': 'Выручка (€)'},
                    color_continuous_scale='RdYlGn')
        st.plotly_chart(fig, use_container_width=True)
        
        # Детальная таблица
        st.subheader("Детальная статистика")
        st.dataframe(
            manager_stats.reset_index().rename(columns={'Id': 'Сделок', 'revenue': 'Выручка'})
            .style.format({'Выручка': '{:,.0f} €', 'Конверсия': '{:.1f}%'})
            .background_gradient(subset=['Конверсия'], cmap='RdYlGn'),
            use_container_width=True
        )

# ---------- ВКЛАДКА 5: ПРОДУКТЫ ----------
with tabs[4]:
    st.markdown('<div class="section-title">ПЛАТЕЖИ И ПРОДУКТЫ</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Топ продуктов")
        
        if 'Product' in filtered_deals.columns:
            product_stats = filtered_deals.groupby('Product').agg({
                'Id': 'count',
                'revenue': 'sum',
                'is_paid': 'mean'
            }).sort_values('revenue', ascending=False).head(15)
            
            product_stats['Конверсия'] = (product_stats['is_paid'] * 100).round(1)
            
            fig = px.bar(product_stats.reset_index(), x='Product', y='revenue',
                        color='Конверсия', title='Топ-15 продуктов по выручке',
                        labels={'revenue': 'Выручка (€)'},
                        color_continuous_scale='RdYlGn')
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Типы оплаты")
        
        pay_cols = [col for col in ['Payment_Type_Recovered', 'Payment Type'] if col in filtered_deals.columns]
        if pay_cols:
            pay_col = pay_cols[0]
            payment_stats = filtered_deals[pay_col].value_counts().head(10)
            fig = px.pie(values=payment_stats.values, names=payment_stats.index,
                        title='Распределение по типам оплаты', hole=0.4)
            st.plotly_chart(fig, use_container_width=True)

# ---------- ВКЛАДКА 6: ГЕОГРАФИЯ ----------
with tabs[5]:
    st.markdown('<div class="section-title">ГЕОГРАФИЧЕСКИЙ АНАЛИЗ</div>', unsafe_allow_html=True)
    
    if 'City' in filtered_deals.columns:
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.subheader("Топ городов по выручке")
            
            city_stats = filtered_deals.groupby('City').agg({
                'Id': 'count',
                'revenue': 'sum',
                'is_paid': 'mean'
            }).sort_values('revenue', ascending=False).head(20)
            
            city_stats['Конверсия'] = (city_stats['is_paid'] * 100).round(1)
            
            fig = px.bar(city_stats.reset_index(), x='City', y='revenue',
                        color='Конверсия', title='Топ-20 городов',
                        labels={'revenue': 'Выручка (€)'},
                        color_continuous_scale='RdYlGn')
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Уровень немецкого")
            
            if 'Level of Deutsch' in filtered_deals.columns:
                lang_stats = filtered_deals.groupby('Level of Deutsch').agg({
                    'Id': 'count',
                    'is_paid': 'mean'
                }).reset_index()
                lang_stats['Конверсия'] = (lang_stats['is_paid'] * 100).round(1)
                
                fig2 = px.bar(lang_stats, x='Level of Deutsch', y='Конверсия',
                             title='Конверсия по уровням языка')
                st.plotly_chart(fig2, use_container_width=True)
            
            st.subheader("География в цифрах")
            top_cities = filtered_deals['City'].value_counts().head(5)
            for city, count in top_cities.items():
                st.write(f"**{city}**: {count} сделок")

# ---------- ВКЛАДКА 7: СТАТИСТИКА ----------
with tabs[6]:
    st.markdown('<div class="section-title">ОПИСАТЕЛЬНАЯ СТАТИСТИКА</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Числовые поля")
        numeric_cols = []
        for col in filtered_deals.columns:
            if pd.api.types.is_numeric_dtype(filtered_deals[col]) and filtered_deals[col].notna().any():
                numeric_cols.append(col)
        
        if numeric_cols:
            stats = filtered_deals[numeric_cols].describe().T[['mean', '50%', 'std', 'min', 'max']]
            stats.columns = ['Среднее', 'Медиана', 'Ст.откл', 'Минимум', 'Максимум']
            st.dataframe(stats.round(2), use_container_width=True)
    
    with col2:
        st.subheader("Категориальные поля")
        cat_cols = ['Quality', 'Stage', 'Source', 'Product']
        cat_cols = [col for col in cat_cols if col in filtered_deals.columns]
        
        for col in cat_cols[:3]:
            st.write(f"**{col}:**")
            counts = filtered_deals[col].value_counts().head(5)
            for val, count in counts.items():
                percentage = (count / len(filtered_deals) * 100) if len(filtered_deals) > 0 else 0
                st.write(f"- {val}: {count} ({percentage:.1f}%)")

# ---------- ВКЛАДКА 8: ДАННЫЕ ----------
with tabs[7]:
    st.markdown('<div class="section-title">ПОЛНЫЕ ДАННЫЕ</div>', unsafe_allow_html=True)
    
    dataset = st.selectbox("Выберите таблицу", ["Deals", "Spend", "Contacts"])
    
    if dataset == "Deals":
        df = filtered_deals
    elif dataset == "Spend":
        df = spend
    else:
        df = contacts
    
    st.dataframe(df, use_container_width=True, height=500)
    
    # Экспорт
    col1, col2 = st.columns(2)
    with col1:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Скачать CSV", data=csv,
                          file_name=f"{dataset.lower()}.csv",
                          mime="text/csv",
                          use_container_width=True)
    with col2:
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Data')
        excel_buffer.seek(0)
        st.download_button("Скачать Excel", data=excel_buffer,
                          file_name=f"{dataset.lower()}.xlsx",
                          mime="application/vnd.ms-excel",
                          use_container_width=True)

# ========== ФУТЕР ==========
st.markdown("---")
st.markdown(f"""
**Отчет создан:** {datetime.now().strftime('%d.%m.%Y %H:%M')}  
**Отфильтровано сделок:** {len(filtered_deals):,} из {len(deals):,}  
**Период данных:** {min_date} – {max_date}
""")