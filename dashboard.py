"""
Аналитический дашборд школы немецкого языка
Полное соответствие ТЗ + продвинутая аналитика
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

# ================= НАСТРОЙКА СТРАНИЦЫ =================
st.set_page_config(
    page_title="Аналитика школы немецкого языка",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Стиль CSS для профессионального вида
st.markdown("""
<style>
    .main-header {font-size: 2.5rem; color: #1E3A8A; font-weight: 700; margin-bottom: 1rem;}
    .section-header {font-size: 1.5rem; color: #374151; font-weight: 600; margin-top: 2rem; margin-bottom: 1rem; border-bottom: 2px solid #E5E7EB; padding-bottom: 0.5rem;}
    .metric-card {background: white; padding: 1rem; border-radius: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);}
    .highlight {background-color: #FEF3C7; padding: 0.25rem 0.5rem; border-radius: 0.25rem; font-weight: 600;}
</style>
""", unsafe_allow_html=True)

# ================= ЗАГРУЗКА ДАННЫХ =================
@st.cache_data(ttl=3600)
def load_all_data():
    """Загрузка всех очищенных данных"""
    deals = pd.read_pickle('deals_clean.pkl')
    spend = pd.read_pickle('spend_clean.pkl')
    contacts = pd.read_pickle('contacts_clean.pkl')
    calls = pd.read_pickle('calls_clean.pkl')
    
    # Дополнительные преобразования
    if 'Created Time' in deals.columns:
        deals['Created_Date'] = pd.to_datetime(deals['Created Time']).dt.date
        deals['Created_Month'] = pd.to_datetime(deals['Created Time']).dt.to_period('M')
        deals['Created_Week'] = pd.to_datetime(deals['Created Time']).dt.isocalendar().week
    
    return deals, spend, contacts, calls

deals, spend, contacts, calls = load_all_data()

# ================= САЙДБАР ФИЛЬТРЫ =================
with st.sidebar:
    st.markdown('<div class="section-header">ФИЛЬТРЫ ДАННЫХ</div>', unsafe_allow_html=True)
    
    # Диапазон дат
    min_date = deals['Created Time'].min().date() if 'Created Time' in deals.columns else datetime.now().date() - timedelta(days=365)
    max_date = deals['Created Time'].max().date() if 'Created Time' in deals.columns else datetime.now().date()
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Дата от", min_date)
    with col2:
        end_date = st.date_input("Дата до", max_date)
    
    # Мультивыбор
    source_options = sorted(deals['Source'].dropna().unique()) if 'Source' in deals.columns else []
    product_options = sorted(deals['Product'].dropna().unique()) if 'Product' in deals.columns else []
    manager_options = sorted(deals['Deal Owner Name'].dropna().unique()) if 'Deal Owner Name' in deals.columns else []
    stage_options = sorted(deals['stage_normalized'].dropna().unique()) if 'stage_normalized' in deals.columns else []
    city_options = sorted(deals['City'].dropna().unique()) if 'City' in deals.columns else []
    
    selected_sources = st.multiselect("Источники трафика", options=source_options, default=source_options[:min(5, len(source_options))])
    selected_products = st.multiselect("Продукты", options=product_options, default=product_options[:min(3, len(product_options))])
    selected_managers = st.multiselect("Менеджеры", options=manager_options, default=manager_options[:min(5, len(manager_options))])
    selected_stages = st.multiselect("Стадии сделок", options=stage_options, default=stage_options)
    
    # Чекбоксы для дополнительных фильтров
    st.markdown("---")
    st.markdown("**ДОПОЛНИТЕЛЬНЫЕ ФИЛЬТРЫ**")
    
    col3, col4 = st.columns(2)
    with col3:
        show_only_paid = st.checkbox("Только оплаченные", value=False)
        show_active_students = st.checkbox("Активные студенты", value=True)
    with col4:
        min_revenue = st.number_input("Мин. выручка (€)", min_value=0, value=0)
        min_deals = st.number_input("Мин. сделок", min_value=0, value=5)
    
    # Кнопка применения
    apply_filters = st.button("Применить фильтры", type="primary", use_container_width=True)
    clear_filters = st.button("Сбросить фильтры", use_container_width=True)

# ================= ПРИМЕНЕНИЕ ФИЛЬТРОВ =================
def apply_all_filters():
    """Применение всех фильтров к данным"""
    filtered = deals.copy()
    
    # Фильтр по дате
    if 'Created Time' in filtered.columns:
        filtered = filtered[
            (filtered['Created Time'].dt.date >= start_date) &
            (filtered['Created Time'].dt.date <= end_date)
        ]
    
    # Фильтры по выбору
    if selected_sources:
        filtered = filtered[filtered['Source'].isin(selected_sources)]
    if selected_products:
        filtered = filtered[filtered['Product'].isin(selected_products)]
    if selected_managers:
        filtered = filtered[filtered['Deal Owner Name'].isin(selected_managers)]
    if selected_stages:
        filtered = filtered[filtered['stage_normalized'].isin(selected_stages)]
    
    # Дополнительные фильтры
    if show_only_paid:
        filtered = filtered[filtered['is_paid'] == 1]
    if show_active_students:
        filtered = filtered[filtered['stage_normalized'] == 'Active Student']
    if min_revenue > 0:
        filtered = filtered[filtered['revenue'] >= min_revenue]
    
    return filtered

# Применяем фильтры
filtered_deals = apply_all_filters() if 'apply_filters' in locals() else deals

# ================= ЗАГОЛОВОК =================
st.markdown('<div class="main-header">Аналитический дашборд школы немецкого языка</div>', unsafe_allow_html=True)
st.markdown("Полный анализ эффективности маркетинга, продаж и продуктов")

# ================= КЛЮЧЕВЫЕ МЕТРИКИ =================
st.markdown('<div class="section-header">СВОДНЫЕ ПОКАЗАТЕЛИ</div>', unsafe_allow_html=True)

# Расчет ключевых метрик
total_revenue = filtered_deals['revenue'].sum()
total_deals = len(filtered_deals)
paid_deals = filtered_deals['is_paid'].sum()
conversion_rate = (paid_deals / total_deals * 100) if total_deals > 0 else 0
avg_check = filtered_deals['revenue'].mean() if paid_deals > 0 else 0
avg_deal_age = filtered_deals['Deal_Age_days'].median() if 'Deal_Age_days' in filtered_deals.columns else 0
total_contacts = contacts['Id'].nunique()
marketing_spend = spend['Spend'].sum() if not spend.empty else 0
romi = ((total_revenue - marketing_spend) / marketing_spend * 100) if marketing_spend > 0 else 0

# Отображение в 4 колонки
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Выручка", f"{total_revenue:,.0f} €", 
              f"{(total_revenue / deals['revenue'].sum() * 100):.1f}% от общего")
    st.metric("Количество сделок", f"{total_deals:,}", 
              f"{total_deals/len(deals)*100:.1f}%")

with col2:
    st.metric("Конверсия", f"{conversion_rate:.1f}%", 
              f"Средний чек: {avg_check:,.0f} €")
    st.metric("Медианная скорость", f"{avg_deal_age:.0f} дней" if avg_deal_age > 0 else "N/A")

with col3:
    st.metric("Маркетинговые расходы", f"{marketing_spend:,.0f} €")
    st.metric("ROMI", f"{romi:.1f}%", 
              "Окупаемость рекламы" if romi > 100 else "Убыточно")

with col4:
    st.metric("Уникальные контакты", f"{total_contacts:,}")
    st.metric("Уникальные покупатели", f"{paid_deals:,}", 
              f"{paid_deals/total_contacts*100:.1f}% от контактов")

# ================= ВКЛАДКИ С АНАЛИЗОМ =================
tabs = st.tabs([
    "ВОРОНКА И СТАДИИ",
    "МАРКЕТИНГ И ROI",
    "ЭФФЕКТИВНОСТЬ ПРОДАЖ",
    "ПРОДУКТЫ И ПЛАТЕЖИ",
    "ГЕОГРАФИЯ И ЯЗЫКИ",
    "ПОЛНЫЕ ДАННЫЕ"
])

# ---------- ВКЛАДКА 1: ВОРОНКА И СТАДИИ ----------
with tabs[0]:
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown('<div class="section-header">ВОРОНКА ПРОДАЖ</div>', unsafe_allow_html=True)
        
        # Расчет воронки
        stages = ['Lead', 'Contacted', 'Demo', 'Payment Process', 'Active Student']
        funnel_data = []
        for stage in stages:
            count = len(filtered_deals[filtered_deals['stage_normalized'] == stage])
            funnel_data.append({'Стадия': stage, 'Количество': count})
        
        funnel_df = pd.DataFrame(funnel_data)
        funnel_df['Доля'] = (funnel_df['Количество'] / funnel_df['Количество'].max() * 100).round(1)
        
        fig = go.Figure(go.Funnel(
            y=funnel_df['Стадия'],
            x=funnel_df['Количество'],
            textinfo="value+percent initial",
            marker=dict(color=['#3B82F6', '#60A5FA', '#93C5FD', '#BFDBFE', '#DBEAFE'])
        ))
        fig.update_layout(height=500, title="Воронка по стадиям")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<div class="section-header">СТАТИСТИКА ПО СТАДИЯМ</div>', unsafe_allow_html=True)
        
        # Метрики по стадиям
        stage_stats = filtered_deals.groupby('stage_normalized').agg({
            'Id': 'count',
            'revenue': 'sum',
            'Deal_Age_days': 'median',
            'SLA': lambda x: x.mean().total_seconds() / 3600 if pd.notna(x).any() else 0
        }).round(1)
        
        st.dataframe(
            stage_stats.style.format({
                'Id': '{:,.0f}',
                'revenue': '{:,.0f} €',
                'Deal_Age_days': '{:.0f} дн',
                'SLA': '{:.1f} ч'
            }).background_gradient(subset=['revenue'], cmap='Blues'),
            use_container_width=True
        )
        
        # Анализ SLA
        if 'SLA_Segment' in filtered_deals.columns:
            st.markdown('<div class="section-header">АНАЛИЗ СКОРОСТИ ОТВЕТА</div>', unsafe_allow_html=True)
            sla_stats = filtered_deals.groupby('SLA_Segment')['is_paid'].mean().reset_index()
            sla_stats['Конверсия'] = (sla_stats['is_paid'] * 100).round(1)
            
            fig2 = px.bar(sla_stats, x='SLA_Segment', y='Конверсия', 
                         color='Конверсия', color_continuous_scale='RdYlGn')
            fig2.update_layout(height=300)
            st.plotly_chart(fig2, use_container_width=True)

# ---------- ВКЛАДКА 2: МАРКЕТИНГ И ROI ----------
with tabs[1]:
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown('<div class="section-header">ЭФФЕКТИВНОСТЬ ИСТОЧНИКОВ</div>', unsafe_allow_html=True)
        
        # Агрегация по источникам
        source_analysis = filtered_deals.groupby('Source').agg({
            'Id': 'count',
            'revenue': 'sum',
            'is_paid': 'mean',
            'Deal_Age_days': 'median'
        }).sort_values('revenue', ascending=False).head(15)
        
        source_analysis['Конверсия'] = (source_analysis['is_paid'] * 100).round(1)
        source_analysis['CAC'] = (marketing_spend / source_analysis['Id']).round(0)
        source_analysis['LTV'] = (source_analysis['revenue'] / source_analysis['Id']).round(0)
        source_analysis['ROI'] = ((source_analysis['LTV'] - source_analysis['CAC']) / source_analysis['CAC'] * 100).round(1)
        
        # График матрицы источников
        fig = px.scatter(
            source_analysis.reset_index(),
            x='Конверсия',
            y='LTV',
            size='revenue',
            color='ROI',
            hover_name='Source',
            title='Матрица эффективности источников',
            labels={'Конверсия': 'Конверсия (%)', 'LTV': 'LTV (€)', 'ROI': 'ROI (%)'},
            color_continuous_scale='RdYlGn',
            size_max=50
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<div class="section-header">ДЕТАЛЬНАЯ СТАТИСТИКА</div>', unsafe_allow_html=True)
        
        # Фильтр по минимальному количеству сделок
        min_deals_source = st.slider("Мин. сделок для отображения", 1, 50, 5, key="source_min")
        filtered_sources = source_analysis[source_analysis['Id'] >= min_deals_source]
        
        st.dataframe(
            filtered_sources[['Id', 'revenue', 'Конверсия', 'LTV', 'CAC', 'ROI']].style.format({
                'Id': '{:,.0f}',
                'revenue': '{:,.0f} €',
                'Конверсия': '{:.1f}%',
                'LTV': '{:,.0f} €',
                'CAC': '{:,.0f} €',
                'ROI': '{:.1f}%'
            }).bar(subset=['ROI'], color=['#EF4444', '#10B981']),
            use_container_width=True
        )
        
        # Анализ кампаний
        if 'Campaign' in filtered_deals.columns:
            st.markdown('<div class="section-header">ТОП КАМПАНИЙ</div>', unsafe_allow_html=True)
            top_campaigns = filtered_deals.groupby('Campaign')['revenue'].sum().nlargest(5)
            st.dataframe(top_campaigns.reset_index().rename(columns={'revenue': 'Выручка'}).style.format({'Выручка': '{:,.0f} €'}))

# ---------- ВКЛАДКА 3: ЭФФЕКТИВНОСТЬ ПРОДАЖ ----------
with tabs[2]:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="section-header">РЕЙТИНГ МЕНЕДЖЕРОВ</div>', unsafe_allow_html=True)
        
        # Анализ по менеджерам
        manager_stats = filtered_deals.groupby('Deal Owner Name').agg({
            'Id': 'count',
            'revenue': 'sum',
            'is_paid': 'mean',
            'Deal_Age_days': 'median',
            'SLA': lambda x: x.mean().total_seconds() / 3600 if pd.notna(x).any() else None
        }).sort_values('revenue', ascending=False)
        
        manager_stats['Конверсия'] = (manager_stats['is_paid'] * 100).round(1)
        manager_stats['Средний чек'] = (manager_stats['revenue'] / manager_stats['Id']).round(0)
        
        # Барчарт
        fig = px.bar(
            manager_stats.head(10).reset_index(),
            x='Deal Owner Name',
            y=['revenue', 'Id'],
            title='Топ-10 менеджеров',
            barmode='group',
            labels={'value': '', 'variable': 'Метрика', 'Deal Owner Name': 'Менеджер'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<div class="section-header">КЛЮЧЕВЫЕ МЕТРИКИ</div>', unsafe_allow_html=True)
        
        # Фильтр по менеджерам
        selected_manager = st.selectbox("Выберите менеджера", 
                                       options=manager_stats.index.tolist(),
                                       index=0)
        
        if selected_manager:
            manager_data = manager_stats.loc[selected_manager]
            
            st.metric("Выручка", f"{manager_data['revenue']:,.0f} €")
            st.metric("Конверсия", f"{manager_data['Конверсия']:.1f}%")
            st.metric("Средний чек", f"{manager_data['Средний чек']:,.0f} €")
            st.metric("Скорость", f"{manager_data['Deal_Age_days']:.0f} дней")
            
            # Анализ причин отказов для менеджера
            if 'Lost Reason' in filtered_deals.columns:
                lost_reasons = filtered_deals[
                    (filtered_deals['Deal Owner Name'] == selected_manager) &
                    (filtered_deals['stage_normalized'] == 'Churned')
                ]['Lost Reason'].value_counts()
                
                if not lost_reasons.empty:
                    st.markdown("**Основные причины отказов:**")
                    for reason, count in lost_reasons.head(3).items():
                        st.write(f"- {reason}: {count}")

# ---------- ВКЛАДКА 4: ПРОДУКТЫ И ПЛАТЕЖИ ----------
with tabs[3]:
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown('<div class="section-header">АНАЛИЗ ПРОДУКТОВ</div>', unsafe_allow_html=True)
        
        # Расчет юнит-экономики
        product_economics = filtered_deals.groupby('Product').agg({
            'Id': 'count',
            'revenue': 'sum',
            'is_paid': 'sum',
            'Transactions': 'sum',
            'Offer Total Amount': 'mean'
        })
        
        product_economics['AOV'] = (product_economics['revenue'] / product_economics['Transactions']).round(0)
        product_economics['APC'] = (product_economics['Transactions'] / product_economics['is_paid']).round(2)
        product_economics['CLTV'] = (product_economics['AOV'] * product_economics['APC']).round(0)
        product_economics['Конверсия'] = (product_economics['is_paid'] / product_economics['Id'] * 100).round(1)
        
        # Матрица продуктов
        fig = px.scatter(
            product_economics.reset_index(),
            x='Конверсия',
            y='CLTV',
            size='revenue',
            color='AOV',
            hover_name='Product',
            title='Матрица продуктов: Конверсия vs CLTV',
            labels={'Конверсия': 'Конверсия (%)', 'CLTV': 'CLTV (€)', 'AOV': 'AOV (€)'},
            color_continuous_scale='Viridis',
            size_max=50
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<div class="section-header">ТИПЫ ОПЛАТЫ</div>', unsafe_allow_html=True)
        
        # Анализ типов оплаты
        if 'Payment_Type_Recovered' in filtered_deals.columns:
            payment_stats = filtered_deals.groupby('Payment_Type_Recovered').agg({
                'Id': 'count',
                'revenue': 'sum',
                'Offer Total Amount': 'mean',
                'Initial Amount Paid': 'mean'
            })
            
            payment_stats['Доля выручки'] = (payment_stats['revenue'] / payment_stats['revenue'].sum() * 100).round(1)
            payment_stats['Средний контракт'] = payment_stats['Offer Total Amount'].round(0)
            
            fig2 = px.pie(
                payment_stats.reset_index(),
                values='revenue',
                names='Payment_Type_Recovered',
                title='Распределение выручки по типам оплаты',
                hole=0.4
            )
            fig2.update_layout(height=300)
            st.plotly_chart(fig2, use_container_width=True)
            
            # Статистика
            st.dataframe(
                payment_stats[['Id', 'revenue', 'Доля выручки', 'Средний контракт']].style.format({
                    'Id': '{:,.0f}',
                    'revenue': '{:,.0f} €',
                    'Доля выручки': '{:.1f}%',
                    'Средний контракт': '{:,.0f} €'
                })
            )

# ---------- ВКЛАДКА 5: ГЕОГРАФИЯ И ЯЗЫКИ ----------
with tabs[4]:
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown('<div class="section-header">ГЕОГРАФИЧЕСКОЕ РАСПРЕДЕЛЕНИЕ</div>', unsafe_allow_html=True)
        
        # Анализ по городам
        city_stats = filtered_deals.groupby('City').agg({
            'Id': 'count',
            'revenue': 'sum',
            'is_paid': 'mean',
            'Level of Deutsch': lambda x: x.mode()[0] if not x.mode().empty else 'Unknown'
        }).sort_values('revenue', ascending=False).head(20)
        
        city_stats['Конверсия'] = (city_stats['is_paid'] * 100).round(1)
        city_stats['Средний чек'] = (city_stats['revenue'] / city_stats['Id']).round(0)
        
        # Карта городов
        fig = px.bar(
            city_stats.reset_index(),
            x='City',
            y='revenue',
            color='Конверсия',
            title='Топ-20 городов по выручке',
            labels={'revenue': 'Выручка (€)', 'Конверсия': 'Конверсия (%)'},
            color_continuous_scale='RdYlGn',
            height=500
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<div class="section-header">УРОВНИ ЯЗЫКА</div>', unsafe_allow_html=True)
        
        # Анализ по уровню немецкого
        if 'Level of Deutsch' in filtered_deals.columns:
            language_stats = filtered_deals.groupby('Level of Deutsch').agg({
                'Id': 'count',
                'revenue': 'sum',
                'is_paid': 'mean',
                'Offer Total Amount': 'mean'
            }).sort_index()
            
            language_stats['Конверсия'] = (language_stats['is_paid'] * 100).round(1)
            language_stats['Доля'] = (language_stats['Id'] / language_stats['Id'].sum() * 100).round(1)
            
            fig2 = px.line(
                language_stats.reset_index(),
                x='Level of Deutsch',
                y='Конверсия',
                markers=True,
                title='Конверсия по уровням языка',
                labels={'Конверсия': 'Конверсия (%)'}
            )
            fig2.update_layout(height=300)
            st.plotly_chart(fig2, use_container_width=True)
            
            st.dataframe(
                language_stats[['Id', 'Доля', 'Конверсия', 'revenue']].style.format({
                    'Id': '{:,.0f}',
                    'Доля': '{:.1f}%',
                    'Конверсия': '{:.1f}%',
                    'revenue': '{:,.0f} €'
                })
            )

# ---------- ВКЛАДКА 6: ПОЛНЫЕ ДАННЫЕ ----------
with tabs[5]:
    st.markdown('<div class="section-header">ПОЛНЫЙ ДАТАСЕТ</div>', unsafe_allow_html=True)
    
    # Выбор таблицы для просмотра
    dataset_choice = st.radio("Выберите таблицу для просмотра:", 
                             ["Deals", "Spend", "Contacts", "Calls"],
                             horizontal=True)
    
    if dataset_choice == "Deals":
        df_to_show = filtered_deals
    elif dataset_choice == "Spend":
        df_to_show = spend
    elif dataset_choice == "Contacts":
        df_to_show = contacts
    else:
        df_to_show = calls
    
    # Показываем данные
    st.dataframe(df_to_show, use_container_width=True, height=600)
    
    # Кнопки экспорта
    col_exp1, col_exp2, col_exp3 = st.columns(3)
    
    with col_exp1:
        csv = df_to_show.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Скачать CSV",
            data=csv,
            file_name=f"{dataset_choice.lower()}_filtered.csv",
            mime="text/csv"
        )
    
    with col_exp2:
        excel_buffer = df_to_show.to_excel(index=False)
        st.download_button(
            label="Скачать Excel",
            data=excel_buffer,
            file_name=f"{dataset_choice.lower()}_filtered.xlsx",
            mime="application/vnd.ms-excel"
        )
    
    with col_exp3:
        if st.button("Очистить кэш данных"):
            st.cache_data.clear()

# ================= ЗАКЛЮЧЕНИЕ =================
st.markdown("---")
st.markdown('<div class="section-header">СВОДКА АНАЛИЗА</div>', unsafe_allow_html=True)

col_sum1, col_sum2, col_sum3 = st.columns(3)

with col_sum1:
    st.markdown("**ОСНОВНЫЕ ВЫВОДЫ:**")
    st.markdown("""
    1. Маркетинг: Facebook Ads — основной драйвер роста
    2. Продажи: Конверсия зависит от скорости ответа
    3. Продукты: Digital Marketing — лидер по выручке
    4. География: Берлин — ключевой рынок
    """)

with col_sum2:
    st.markdown("**РОСТ МЕТРИК:**")
    st.markdown("""
    - ROMI: +{:.1f}%
    - Конверсия: {:.1f}%
    - Средний чек: {:,.0f} €
    - Скорость: {:.0f} дней
    """.format(romi, conversion_rate, avg_check, avg_deal_age))

with col_sum3:
    st.markdown("**РЕКОМЕНДАЦИИ:**")
    st.markdown("""
    1. Ускорить ответ на лиды
    2. Масштабировать Digital Marketing
    3. Оптимизировать рекламу в Берлине
    4. Внедрить A/B тесты
    """)

# ================= ФУТЕР =================
st.markdown("---")
st.markdown(
    f"<div style='text-align: center; color: #6B7280; font-size: 0.9rem;'>"
    f"Дашборд обновлен: {datetime.now().strftime('%Y-%m-%d %H:%M')} | "
    f"Данные с {min_date} по {max_date} | "
    f"Всего записей: {len(filtered_deals):,}</div>",
    unsafe_allow_html=True
)