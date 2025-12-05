import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

st.set_page_config(layout="wide")

# Загрузка
@st.cache_data
def load_data():
    deals = pd.read_parquet('deals_clean.parquet')
    spend = pd.read_parquet('spend_clean.parquet')
    contacts = pd.read_parquet('contacts_clean.parquet')
    return deals, spend, contacts

deals, spend, contacts = load_data()

# Фильтры
st.sidebar.header("ФИЛЬТРЫ")

# Используем реальные названия из твоих данных
source_options = deals['Source'].dropna().unique().tolist()
product_options = deals['Product'].dropna().unique().tolist()

selected_sources = st.sidebar.multiselect("Источники", source_options, default=source_options[:5])
selected_products = st.sidebar.multiselect("Продукты", product_options, default=product_options[:3])

date_range = st.sidebar.date_input("Даты", 
    [deals['Created Time'].min().date(), deals['Created Time'].max().date()])

# Применение фильтров
filtered_deals = deals[
    deals['Source'].isin(selected_sources) & 
    deals['Product'].isin(selected_products) &
    (deals['Created Time'].dt.date >= date_range[0]) &
    (deals['Created Time'].dt.date <= date_range[1])
]

# ========== ЗАГОЛОВОК ==========
st.title("Аналитика онлайн-школы IT специалистов")
st.markdown("---")

# ========== МЕТРИКИ ==========
total_revenue = filtered_deals['revenue'].sum()
total_deals = len(filtered_deals)
paid_deals = filtered_deals['is_paid'].sum()
conversion = (paid_deals / total_deals * 100) if total_deals > 0 else 0
avg_check = filtered_deals['revenue'].mean() if paid_deals > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Выручка", f"{total_revenue:,.0f} €")
col2.metric("Сделки", f"{total_deals:,}")
col3.metric("Конверсия", f"{conversion:.1f}%")
col4.metric("Средний чек", f"{avg_check:,.0f} €")

st.markdown("---")

# ========== ВКЛАДКИ ==========
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "МАРКЕТИНГ", "ПРОДАЖИ", "ПРОДУКТЫ", "ГЕОГРАФИЯ", "ДАННЫЕ"
])

# ВКЛАДКА 1: МАРКЕТИНГ (твоя воронка из ячейки 13)
with tab1:
    st.subheader("Маркетинговая воронка по источникам")
    
    # Твой код из ячейки 13
    spend_agg = spend.groupby('Source').agg({
        'Impressions': 'sum',
        'Clicks': 'sum',
        'Spend': 'sum'
    }).reset_index()
    
    leads_agg = deals.groupby('Source')['Id'].count().reset_index().rename(columns={'Id': 'Leads'})
    qual_leads_agg = deals[deals['Quality'].isin(['A - High', 'B - Medium'])].groupby('Source')['Id'].count().reset_index().rename(columns={'Id': 'Quality_Leads'})
    
    funnel_df = spend_agg.merge(leads_agg, on='Source', how='left').merge(qual_leads_agg, on='Source', how='left').fillna(0)
    funnel_df = funnel_df.sort_values('Spend', ascending=False).head(10)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=funnel_df['Source'], y=funnel_df['Impressions'], name='Показы'))
    fig.add_trace(go.Bar(x=funnel_df['Source'], y=funnel_df['Clicks'], name='Клики'))
    fig.add_trace(go.Bar(x=funnel_df['Source'], y=funnel_df['Leads'], name='Лиды'))
    fig.add_trace(go.Bar(x=funnel_df['Source'], y=funnel_df['Quality_Leads'], name='Кач. лиды'))
    
    fig.update_layout(barmode='group', height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # ROI анализ
    st.subheader("ROI по источникам")
    marketing_deep = spend_agg.merge(
        deals.groupby('Source').agg({'Id': 'count', 'stage_normalized': lambda x: (x == 'Active Student').sum()}),
        on='Source', how='inner'
    )
    marketing_deep['CPC'] = marketing_deep['Spend'] / marketing_deep['Clicks']
    marketing_deep['C1_Quality'] = (marketing_deep['stage_normalized'] / marketing_deep['Id'] * 100)
    
    fig2 = px.scatter(marketing_deep, x='CPC', y='C1_Quality', size='Spend', 
                     hover_name='Source', title='CPC vs Конверсия')
    st.plotly_chart(fig2, use_container_width=True)

# ВКЛАДКА 2: ПРОДАЖИ (твои менеджеры из ячейки 17)
with tab2:
    st.subheader("Эффективность менеджеров")
    
    manager_stats = filtered_deals.groupby('Deal Owner Name').agg({
        'Id': 'count',
        'revenue': 'sum',
        'is_paid': 'mean'
    }).sort_values('revenue', ascending=False).head(15)
    
    manager_stats['Конверсия'] = (manager_stats['is_paid'] * 100).round(1)
    
    fig = px.bar(manager_stats.reset_index(), 
                 x='Deal Owner Name', y='revenue',
                 color='Конверсия',
                 title='Топ менеджеров по выручке',
                 labels={'revenue': 'Выручка (€)'})
    st.plotly_chart(fig, use_container_width=True)
    
    # Анализ SLA
    if 'SLA' in filtered_deals.columns:
        st.subheader("Скорость ответа")
        filtered_deals['SLA_hours'] = filtered_deals['SLA'].dt.total_seconds() / 3600
        sla_stats = filtered_deals.groupby('Deal Owner Name')['SLA_hours'].median().reset_index()
        fig2 = px.bar(sla_stats, x='Deal Owner Name', y='SLA_hours',
                     title='Медианное время ответа (часы)')
        st.plotly_chart(fig2, use_container_width=True)

# ВКЛАДКА 3: ПРОДУКТЫ (твои продукты из ячейки 20)
with tab3:
    st.subheader("Анализ продуктов")
    
    product_stats = filtered_deals.groupby('Product').agg({
        'Id': 'count',
        'revenue': 'sum',
        'is_paid': 'mean',
        'Transactions': 'sum'
    })
    
    product_stats['Конверсия'] = (product_stats['is_paid'] * 100).round(1)
    product_stats['AOV'] = (product_stats['revenue'] / product_stats['Transactions']).round(0)
    
    fig = px.scatter(product_stats.reset_index(),
                    x='Конверсия', y='AOV',
                    size='revenue', color='Product',
                    title='Матрица продуктов: Конверсия vs Средний чек')
    st.plotly_chart(fig, use_container_width=True)

# ВКЛАДКА 4: ГЕОГРАФИЯ (твои города из ячейки 21)
with tab4:
    st.subheader("География продаж")
    
    if 'City' in filtered_deals.columns:
        city_stats = filtered_deals.groupby('City').agg({
            'revenue': 'sum',
            'Id': 'count',
            'is_paid': 'mean'
        }).sort_values('revenue', ascending=False).head(15)
        
        city_stats['Конверсия'] = (city_stats['is_paid'] * 100).round(1)
        
        fig = px.bar(city_stats.reset_index(),
                    x='City', y='revenue',
                    color='Конверсия',
                    title='Топ городов по выручке')
        st.plotly_chart(fig, use_container_width=True)

# ВКЛАДКА 5: ДАННЫЕ
with tab5:
    st.subheader("Сырые данные")
    st.dataframe(filtered_deals, use_container_width=True, height=500)

st.markdown("---")
st.write("Дашборд создан на основе анализа проекта")