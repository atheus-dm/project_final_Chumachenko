"""
ПОЛНЫЙ АНАЛИТИЧЕСКИЙ ДАШБОРД IT ШКОЛЫ
Версия 2.0 - Полная переработка с интеграцией всех графиков и анализа из ноутбука
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

# ========== НАСТРОЙКА СТРАНИЦЫ ==========
st.set_page_config(
    page_title="Полный анализ IT школы",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Убираем белую подсветку карточек
st.markdown("""
<style>
    .main-title {font-size: 2rem; color: #1E3A8A; font-weight: 700; margin-bottom: 0.5rem;}
    .section-title {font-size: 1.3rem; color: #374151; font-weight: 600; margin-top: 1.5rem; padding-bottom: 0.3rem; border-bottom: 2px solid #3B82F6;}
    .metric-box {background: #f8fafc; padding: 1rem; border-radius: 0.5rem; margin: 0.3rem 0; border: 1px solid #e5e7eb;}
    .dataframe-table {font-size: 0.9rem;}
    
    /* Убираем белую подсветку */
    div[data-testid="stMetricValue"] {background-color: transparent !important;}
    div[data-testid="stMetricLabel"] {background-color: transparent !important;}
    div[data-testid="stMetricDelta"] {background-color: transparent !important;}
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
    
    # УДАЛЯЕМ НЕНУЖНЫЕ ПРОДУКТЫ
    useless_products = ['find yourself in it', 'data analytics']
    deals = deals[~deals['Product'].isin(useless_products)].copy()
    
    return deals, spend, contacts

deals, spend, contacts = load_data()

# ========== КООРДИНАТНАЯ БАЗА ДЛЯ КАРТЫ ==========
COORD_DB = {
    'Berlin': (52.5200, 13.4050), 'München': (48.1351, 11.5820), 'Hamburg': (53.5511, 9.9937),
    'Köln': (50.9375, 6.9603), 'Frankfurt': (50.1109, 8.6821), 'Leipzig': (51.3397, 12.3731),
    'Düsseldorf': (51.2277, 6.7735), 'Dortmund': (51.5136, 7.4653), 'Essen': (51.4556, 7.0116),
    'Bremen': (53.0793, 8.8017), 'Dresden': (51.0504, 13.7373), 'Hannover': (52.3759, 9.7320),
    'Nürnberg': (49.4521, 11.0767), 'Duisburg': (51.4344, 6.7623), 'Bochum': (51.4818, 7.2162),
    'Wuppertal': (51.2562, 7.1508), 'Bielefeld': (52.0302, 8.5325), 'Bonn': (50.7374, 7.0982),
    'Münster': (51.9607, 7.6261), 'Karlsruhe': (49.0069, 8.4037), 'Mannheim': (49.4875, 8.4660),
    'Augsburg': (48.3705, 10.8978), 'Wiesbaden': (50.0826, 8.2493), 'Gelsenkirchen': (51.5177, 7.0857),
    'Mönchengladbach': (51.1805, 6.4428), 'Braunschweig': (52.2689, 10.5268), 'Chemnitz': (50.8321, 12.9208),
    'Kiel': (54.3233, 10.1228), 'Aachen': (50.7753, 6.0839), 'Halle': (51.4826, 11.9697),
    'Magdeburg': (52.1205, 11.6276), 'Freiburg': (47.9961, 7.8494), 'Krefeld': (51.3388, 6.5853),
    'Lübeck': (53.8696, 10.6872), 'Oberhausen': (51.4780, 6.8625), 'Erfurt': (50.9848, 11.0299),
    'Mainz': (50.0012, 8.2763), 'Rostock': (54.0924, 12.0991), 'Kassel': (51.3127, 9.4797),
    'Hagen': (51.3671, 7.4633), 'Saarbrücken': (49.2402, 6.9969), 'Hamm': (51.6803, 7.8209),
    'Ludwigshafen': (49.4774, 8.4452), 'Mülheim': (51.4271, 6.8806), 'Oldenburg': (53.1435, 8.2146),
    'Osnabrück': (52.2799, 8.0472), 'Leverkusen': (51.0459, 7.0192), 'Heidelberg': (49.3988, 8.6724),
    'Solingen': (51.1694, 7.0815), 'Herne': (51.5372, 7.2223), 'Neuss': (51.2042, 6.6879),
    'Darmstadt': (49.8728, 8.6512), 'Paderborn': (51.7189, 8.7575), 'Regensburg': (49.0134, 12.1016),
    'Ingolstadt': (48.7632, 11.4251), 'Würzburg': (49.7913, 9.9534), 'Fürth': (49.4771, 10.9887),
    'Wolfsburg': (52.4227, 10.7865), 'Offenbach': (50.0956, 8.7761), 'Ulm': (48.4011, 9.9876),
    'Heilbronn': (49.1427, 9.2109), 'Pforzheim': (48.8922, 8.6946), 'Göttingen': (51.5413, 9.9158),
    'Bottrop': (51.5259, 6.9248), 'Trier': (49.7499, 6.6373), 'Recklinghausen': (51.6149, 7.1977),
    'Reutlingen': (48.4914, 9.2112), 'Bremerhaven': (53.5396, 8.5809), 'Koblenz': (50.3569, 7.5890),
    'Bergisch Gladbach': (50.9916, 7.1368), 'Jena': (50.9271, 11.5892), 'Remscheid': (51.1790, 7.1925),
    'Erlangen': (49.5897, 11.0039), 'Moers': (51.4516, 6.6403), 'Siegen': (50.8745, 8.0243),
    'Hildesheim': (52.1548, 9.9578), 'Salzgitter': (52.1508, 10.3593),
    'Wien': (48.2082, 16.3738), 'Graz': (47.0707, 15.4395), 'Linz': (48.3069, 14.2858),
    'Salzburg': (47.8095, 13.0550), 'Innsbruck': (47.2692, 11.4041), 'Klagenfurt': (46.6362, 14.3126),
    'Zürich': (47.3769, 8.5417), 'Basel': (47.5596, 7.5886), 'Bern': (46.9480, 7.4474),
    'Lausanne': (46.5197, 6.6323), 'Genf': (46.2044, 6.1432), 'Luzern': (47.0502, 8.3093),
    'St. Gallen': (47.4245, 9.3767), 'Lugano': (46.0037, 8.9511),
}

# ========== ФУНКЦИИ ГЕОКОДИРОВАНИЯ ==========
def geocode_city(city_name):
    """Геокодирование города через локальную базу COORD_DB"""
    if pd.isna(city_name):
        return None
    
    city_clean = str(city_name).strip()
    
    # Ищем в локальной базе
    for db_city, coords in COORD_DB.items():
        if db_city.lower() in city_clean.lower() or city_clean.lower() in db_city.lower():
            return coords
    
    return None

def prepare_geodata(city_stats):
    """Подготовка геоданных для карты"""
    top_cities = city_stats.head(50).copy()
    
    coordinates = []
    for city in top_cities['City']:
        coords = geocode_city(city)
        coordinates.append(coords)
    
    top_cities[['lat', 'lon']] = pd.DataFrame(coordinates, index=top_cities.index, columns=['lat', 'lon'])
    geocoded = top_cities.dropna(subset=['lat', 'lon'])
    
    return geocoded

# ========== ФИЛЬТРЫ ==========
with st.sidebar:
    st.markdown("**ФИЛЬТРЫ ДАННЫХ**")
    
    # Даты
    min_date = deals['Created Time'].min().date()
    max_date = deals['Created Time'].max().date()
    date_range = st.date_input("Диапазон дат", [min_date, max_date])
    
    # Получаем ВСЕ значения (только продукты и источники)
    all_sources = deals['Source'].dropna().unique().tolist() if 'Source' in deals.columns else []
    all_products = deals['Product'].dropna().unique().tolist() if 'Product' in deals.columns else []
    # По умолчанию ВСЕ значения
    selected_sources = st.multiselect("Источники", all_sources, default=all_sources)
    selected_products = st.multiselect("Продукты", all_products, default=all_products)
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
    return filtered

filtered_deals = apply_filters()

# ========== ИСПРАВЛЕННАЯ ФУНКЦИЯ КЛЮЧЕВЫХ МЕТРИК ==========
def calculate_business_metrics():
    """Расчет ключевых метрик бизнеса с ПРАВИЛЬНЫМ AOV (Revenue/T)"""
    
    # Базовые константы
    TOTAL_UA = contacts['Id'].nunique()
    total_marketing_spend = spend['Spend'].sum()
    
    # Активные студенты
    active_students_df = filtered_deals[filtered_deals['stage_normalized'] == 'Active Student']
    TOTAL_B_CORRECT = active_students_df['Contact Name'].nunique() if len(active_students_df) > 0 else 0
    
    # Инициализация значений по умолчанию
    total_revenue = 0
    products_count = 0
    managers_count = 0
    cities_count = 0
    sources_count = 0
    avg_check = 0
    win_rate_vacuum = 0
    cm_total = -total_marketing_spend  # если нет выручки, CM = -расходы
    romi_total = -100
    median_deal_age = 0
    mean_deal_age = 0
    top_product_name = "Нет данных"
    ltv_vacuum_business = 0
    
    # Если есть успешные сделки
    if len(active_students_df) > 0:
        # Базовые метрики
        total_revenue = filtered_deals['revenue'].sum()
        products_count = filtered_deals['Product'].nunique()
        managers_count = filtered_deals['Deal Owner Name'].nunique()
        cities_count = filtered_deals['City'].nunique() if 'City' in filtered_deals.columns else 0
        sources_count = filtered_deals['Source'].nunique()
        
        # Средний чек: Revenue / B
        avg_check = total_revenue / TOTAL_B_CORRECT if TOTAL_B_CORRECT > 0 else 0
        
        # Vacuum Win Rate (C1): B / UA
        win_rate_vacuum = (TOTAL_B_CORRECT / TOTAL_UA * 100) if TOTAL_UA > 0 else 0
        
        # Contribution Margin и ROMI
        cm_total = total_revenue - total_marketing_spend
        romi_total = (cm_total / total_marketing_spend * 100) if total_marketing_spend > 0 else 0
        
        # Deal Age
        active_student_ids = active_students_df['Id'].unique()
        closed_deals_clean = filtered_deals[
            (filtered_deals['Id'].isin(active_student_ids)) &
            (filtered_deals['Closing Date'].notna()) &
            (filtered_deals['Deal_Age_days'].notna()) &
            (filtered_deals['Deal_Age_days'] >= 0)
        ].copy()
        
        if len(closed_deals_clean) > 0:
            median_deal_age = closed_deals_clean['Deal_Age_days'].median()
            mean_deal_age = closed_deals_clean['Deal_Age_days'].mean()
        
        # --- ПРАВИЛЬНЫЙ РАСЧЕТ ПРОДУКТОВОЙ СТАТИСТИКИ (как в юнит-экономике) ---
        # Подготовка транзакций
        deals_calc = filtered_deals.copy()
        deals_calc['Transactions'] = np.where(
            deals_calc.get('Payment_Type_Recovered', None) == 'one payment',
            1,
            deals_calc.get('Months of study', pd.Series(index=deals_calc.index, dtype='float')).fillna(1)
        )
        deals_calc.loc[deals_calc['stage_normalized'] != 'Active Student', 'Transactions'] = 0
        
        # Агрегация по продуктам
        active_students_calc = deals_calc[deals_calc['stage_normalized'] == 'Active Student']
        
        if len(active_students_calc) > 0:
            product_stats = active_students_calc.groupby('Product').agg({
                'Contact Name': 'nunique',
                'revenue': 'sum',
                'Transactions': 'sum',
            }).reset_index().rename(columns={
                'Contact Name': 'B',
                'revenue': 'Revenue',
                'Transactions': 'T'
            })
            
            # ПРАВИЛЬНЫЙ AOV = Revenue / T
            product_stats['AOV'] = product_stats['Revenue'] / product_stats['T']
            product_stats['APC'] = product_stats['T'] / product_stats['B']
            
            COGS_FIXED_PER_TRANS = 0
            COGS_PERCENT_FROM_CHECK = 0.0
            total_cogs_amt_by_product = (product_stats['Revenue'] * COGS_PERCENT_FROM_CHECK) + (product_stats['T'] * COGS_FIXED_PER_TRANS)
            product_stats['COGS'] = total_cogs_amt_by_product / product_stats['T'].replace(0, np.nan)
            
            # ПРАВИЛЬНЫЙ CLTV = (AOV - COGS) × APC
            product_stats['CLTV'] = (product_stats['AOV'] - product_stats['COGS']) * product_stats['APC']
            product_stats['C1_vacuum'] = product_stats['B'] / TOTAL_UA if TOTAL_UA > 0 else 0
            product_stats['LTV'] = product_stats['CLTV'] * product_stats['C1_vacuum']
            
            # Топ продукт
            top_product_row = product_stats.sort_values('Revenue', ascending=False).head(1)
            top_product_name = top_product_row['Product'].iloc[0] if len(top_product_row) else "Нет данных"
            
            # Бизнес-LTV (weighted CLTV × B/UA)
            if product_stats['B'].sum() > 0:
                cltv_weighted = (product_stats['CLTV'] * product_stats['B']).sum() / product_stats['B'].sum()
            else:
                cltv_weighted = 0
            ltv_vacuum_business = cltv_weighted * (TOTAL_B_CORRECT / TOTAL_UA) if TOTAL_UA > 0 else 0
    
    # --- Сводный df ---
    summary_rows = [
        ('Выручка (Total Revenue)', total_revenue, '€'),
        ('Средний чек (Average Check)', avg_check, '€'),
        ('Клиенты (Buyers Count)', TOTAL_B_CORRECT, ''),
        ('Уникальные контакты (UA Count)', TOTAL_UA, ''),
        ('Продукты (Products Count)', products_count, ''),
        ('Менеджеры (Managers Count)', managers_count, ''),
        ('Города (Cities Count)', cities_count, ''),
        ('Маркетинговые расходы (Marketing Spend)', total_marketing_spend, '€'),
        ('Источники (Sources Count)', sources_count, ''),
        ('Конверсия (Vacuum, B/UA)', win_rate_vacuum, '%'),
        ('ROMI ((Revenue - Spend)/Spend)', romi_total, '%'),
        ('Маржинальный вклад (Contribution Margin)', cm_total, '€'),
        ('Время закрытия сделки (медиана)', median_deal_age, 'дн'),
        ('Время закрытия сделки (среднее)', mean_deal_age, 'дн'),
        ('Топовый продукт по выручке', top_product_name, 'str'),
        ('Бизнес-LTV (weighted CLTV × B/UA)', ltv_vacuum_business, '€'),
    ]

    summary_df = pd.DataFrame(summary_rows, columns=['Metric', 'Value', 'Unit'])
    date_min = contacts['Created Time'].min() if 'Created Time' in contacts.columns else None
    date_max = contacts['Created Time'].max() if 'Created Time' in contacts.columns else None
    
    return summary_df, date_min, date_max, TOTAL_UA, TOTAL_B_CORRECT, total_revenue, total_marketing_spend

# Вызов функции
summary_df, date_min, date_max, TOTAL_UA, TOTAL_B, total_revenue, marketing_spend = calculate_business_metrics()

# ========== ЗАГОЛОВОК ==========
st.markdown('<div class="main-title">ПОЛНЫЙ АНАЛИТИЧЕСКИЙ ОТЧЕТ IT ШКОЛЫ</div>', unsafe_allow_html=True)
st.markdown(f"*Период данных: {min_date} - {max_date}*")  # УБРАЛ СЧЕТ СДЕЛОК
st.markdown("---")

# ========== КЛЮЧЕВЫЕ МЕТРИКИ ==========
st.markdown('<div class="section-title">СВОДНЫЕ ПОКАЗАТЕЛИ БИЗНЕСА</div>', unsafe_allow_html=True)

# Форматирование для отображения
def format_value(val, unit):
    if pd.isna(val):
        return '—'
    if isinstance(val, (pd.Timestamp,)):
        return str(val.date())
    if isinstance(val, str):
        return val
    if unit == '%':
        return f"{val:,.1f}%"
    if unit == '€':
        return f"{val:,.0f} €"
    if unit == 'дн':
        return f"{val:,.0f} дн"
    return f"{val:,.0f}"

summary_df['Formatted'] = summary_df.apply(lambda r: format_value(r['Value'], r['Unit']), axis=1)

# Отображаем в 4 колонки
metrics_display = summary_df[['Metric', 'Formatted']].values.tolist()
cols = st.columns(4)
for idx, (label, value) in enumerate(metrics_display):
    with cols[idx % 4]:
        st.markdown(f'<div class="metric-box"><b>{label}</b><br>{value}</div>', unsafe_allow_html=True)

st.markdown("---")

# ========== ФУНКЦИЯ ЮНИТ-ЭКОНОМИКИ (как в ячейке 24) ==========
def calculate_unit_economics():
    """Расчет юнит-экономики как в Vacuum Model (ячейка 24)"""
    
    # Настройки
    COGS_FIXED_PER_TRANS = 0       
    COGS_PERCENT_FROM_CHECK = 0.0 
    
    # 1. Подготовка данных
    deals_calc = filtered_deals.copy()
    deals_calc['Transactions'] = np.where(
        deals_calc['Payment_Type_Recovered'] == 'one payment', 
        1, 
        deals_calc['Months of study'].fillna(1)
    )
    deals_calc.loc[deals_calc['stage_normalized'] != 'Active Student', 'Transactions'] = 0
    
    # 2. Расчет UA и AC
    TOTAL_UA = contacts['Id'].nunique()
    total_marketing_spend = spend['Spend'].sum()
    
    # 3. Агрегация по Продуктам
    active_students_df = deals_calc[deals_calc['stage_normalized'] == 'Active Student']
    
    if len(active_students_df) == 0:
        return pd.DataFrame(), pd.DataFrame()
    
    # Правильный B для TOTAL (уникальные клиенты)
    TOTAL_B_CORRECT = active_students_df['Contact Name'].nunique()
    
    product_stats = active_students_df.groupby('Product').agg({
        'Contact Name': 'nunique',  # B (Buyers - Люди)
        'revenue': 'sum',           # Revenue
        'Transactions': 'sum',      # T
    }).reset_index().rename(columns={
        'Contact Name': 'B', 
        'Transactions': 'T',
        'revenue': 'Revenue'
    })
    
    # 4. Расчет Метрик
    # UA (Константа для всех)
    product_stats['UA'] = TOTAL_UA
    
    # C1 (Конверсия в покупку)
    product_stats['C1'] = product_stats['B'] / product_stats['UA']
    
    # AC (Общий бюджет школы)
    product_stats['AC'] = total_marketing_spend
    
    # APC (Частота платежей)
    product_stats['APC'] = product_stats['T'] / product_stats['B']
    
    # AOV (Средний чек транзакции)
    product_stats['AOV'] = product_stats['Revenue'] / product_stats['T']
    
    # COGS (на 1 транзакцию)
    total_cogs_amt = (product_stats['Revenue'] * COGS_PERCENT_FROM_CHECK) + (product_stats['T'] * COGS_FIXED_PER_TRANS)
    product_stats['COGS'] = total_cogs_amt / product_stats['T']
    
    # CLTV (Прибыль с Клиента)
    product_stats['CLTV'] = (product_stats['AOV'] - product_stats['COGS']) * product_stats['APC']
    
    # LTV (Прибыль с Пользователя/UA)
    product_stats['LTV'] = product_stats['CLTV'] * product_stats['C1']
    
    # CPA (Цена Лида)
    product_stats['CPA'] = product_stats['AC'] / product_stats['UA']
    
    # CAC (Цена Клиента)
    product_stats['CAC'] = product_stats['AC'] / product_stats['B']
    
    # CM (Margin)
    product_stats['CM'] = product_stats['Revenue'] - product_stats['AC'] - total_cogs_amt
    
    # ROMI
    product_stats['ROMI'] = (product_stats['CM'] / product_stats['AC']) * 100
    
    # 5. Расчет TOTAL для справки
    total_row = {
        'Product': 'TOTAL BUSINESS',
        'UA': TOTAL_UA,
        'B': TOTAL_B_CORRECT,
        'Revenue': product_stats['Revenue'].sum(),
        'AC': total_marketing_spend,
        'T': product_stats['T'].sum(),
        'COGS': 0 
    }
    total_row['C1'] = total_row['B'] / total_row['UA']
    total_row['AOV'] = total_row['Revenue'] / total_row['T'] if total_row['T'] > 0 else 0
    total_row['APC'] = total_row['T'] / total_row['B'] if total_row['B'] > 0 else 0
    total_cogs_global = (total_row['Revenue'] * COGS_PERCENT_FROM_CHECK) + (total_row['T'] * COGS_FIXED_PER_TRANS)
    total_row['COGS'] = total_cogs_global / total_row['T'] if total_row['T'] > 0 else 0
    total_row['CLTV'] = (total_row['AOV'] - total_row['COGS']) * total_row['APC']
    total_row['LTV'] = total_row['CLTV'] * total_row['C1'] 
    total_row['CPA'] = total_row['AC'] / total_row['UA']
    total_row['CAC'] = total_row['AC'] / total_row['B']
    total_row['CM'] = total_row['Revenue'] - total_row['AC'] - total_cogs_global
    total_row['ROMI'] = (total_row['CM'] / total_row['AC']) * 100
    
    total_df = pd.DataFrame([total_row])
    
    final_cols = ['Product', 'UA', 'B', 'C1', 'AOV', 'T', 'APC', 'COGS', 'Revenue', 
                  'CLTV', 'LTV', 'AC', 'CPA', 'CAC', 'CM', 'ROMI']
    
    unit_econ_products = product_stats[final_cols].sort_values(by='CM', ascending=False).reset_index(drop=True)
    
    return total_df[final_cols], unit_econ_products

# ========== ФУНКЦИЯ ТОЧЕК РОСТА (как в ячейке 25) ==========
def calculate_growth_points():
    """Анализ точек роста с sensitivity analysis (ячейка 25)"""
    
    # Настройки
    GROWTH_PCT = 0.10
    COGS_FIXED_PER_TRANS = 0
    COGS_PERCENT_FROM_CHECK = 0.0
    AC_SCALING_FACTOR = 0.8
    
    # Коэффициенты сложности
    DIFFICULTY_FACTORS = {'UA': 0.2, 'C1': 0.4, 'AOV': 0.6, 'APC': 0.5, 'CPA': 0.3}
    REALISM_WEIGHTS = {k: 1 - v for k, v in DIFFICULTY_FACTORS.items()}
    
    ACTION_INSIGHTS = {
        'UA': "Масштабирование каналов",
        'C1': "Оптимизация воронки", 
        'AOV': "Up-sell и цены",
        'APC': "Удержание и лояльность",
        'CPA': "Оптимизация рекламы"
    }
    
    def calculate_scenario_metrics(ua, c1, aov, apc, ac_base, product_name, scenario_name, growth_pct):
        b = ua * c1 if ua > 0 and c1 > 0 else 0
        t = b * apc if b > 0 and apc > 0 else 0
        revenue = t * aov if t > 0 and aov > 0 else 0
        
        if "UA" in scenario_name:
            ac = ac_base * (1 + growth_pct * AC_SCALING_FACTOR)
        elif "CPA" in scenario_name:
            ac = ac_base * (1 - growth_pct)
        else:
            ac = ac_base

        cogs_total = (revenue * COGS_PERCENT_FROM_CHECK) + (t * COGS_FIXED_PER_TRANS)
        cogs_per_trans = cogs_total / t if t > 0 else 0
        
        cltv = (aov - cogs_per_trans) * apc if aov > 0 and cogs_per_trans >= 0 and apc > 0 else 0
        ltv = cltv * c1 if cltv > 0 and c1 > 0 else 0
        
        cm = revenue - ac - cogs_total
        romi = (cm / ac * 100) if ac > 0 else 0
        cpa = ac / ua if ua > 0 else 0
        cac = ac / b if b > 0 else 0
        
        scenario_type = 'BASELINE'
        if scenario_name != 'BASELINE':
            if 'C1' in scenario_name: scenario_type = 'C1'
            elif 'AOV' in scenario_name: scenario_type = 'AOV'
            elif 'APC' in scenario_name: scenario_type = 'APC'
            elif 'CPA' in scenario_name: scenario_type = 'CPA'
            elif 'UA' in scenario_name: scenario_type = 'UA'
        
        return {
            'Scenario': scenario_name, 'Scenario_Type': scenario_type, 'Growth_Pct': growth_pct,
            'Product': product_name, 'UA': ua, 'C1': c1, 'B': b, 'AOV': aov, 'APC': apc, 
            'T': t, 'Revenue': revenue, 'AC': ac, 'CLTV': cltv, 'LTV': ltv, 
            'CPA': cpa, 'CAC': cac, 'CM': cm, 'ROMI': romi,
            'Realism_Weight': REALISM_WEIGHTS.get(scenario_type, 0.5)
        }
    
    def generate_scenarios_for_row(row, product_name):
        base_ua, base_c1, base_aov, base_apc = row['UA'], row['C1'], row['AOV'], row['APC']
        base_ac = row['AC'] if 'AC' in row else 0
        
        scenarios = []
        scenarios.append(calculate_scenario_metrics(
            base_ua, base_c1, base_aov, base_apc, base_ac, product_name, "BASELINE", 0))
        
        g = GROWTH_PCT
        scenarios.append(calculate_scenario_metrics(
            base_ua * (1 + g), base_c1, base_aov, base_apc, base_ac, product_name, f"UA +{int(g*100)}%", g))
        scenarios.append(calculate_scenario_metrics(
            base_ua, base_c1 * (1 + g), base_aov, base_apc, base_ac, product_name, f"C1 +{int(g*100)}%", g))
        scenarios.append(calculate_scenario_metrics(
            base_ua, base_c1, base_aov * (1 + g), base_apc, base_ac, product_name, f"AOV +{int(g*100)}%", g))
        scenarios.append(calculate_scenario_metrics(
            base_ua, base_c1, base_aov, base_apc * (1 + g), base_ac, product_name, f"APC +{int(g*100)}%", g))
        scenarios.append(calculate_scenario_metrics(
            base_ua, base_c1, base_aov, base_apc, base_ac, product_name, f"CPA -{int(g*100)}%", g))
        
        return pd.DataFrame(scenarios)
    
    # Получаем данные юнит-экономики
    total_df, product_econ = calculate_unit_economics()
    
    if len(product_econ) == 0:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    
    # Отбираем топ-продукты
    revenue_threshold = product_econ['Revenue'].max() * 0.1
    top_products = product_econ[product_econ['Revenue'] > revenue_threshold].copy()
    
    # Генерируем сценарии для каждого продукта
    all_scenarios_list = []
    product_scenarios_dict = {}
    
    for _, row in top_products.iterrows():
        product_name = row['Product']
        scenarios = generate_scenarios_for_row(row, product_name)
        product_scenarios_dict[product_name] = scenarios
        
        # Добавляем в общий список для сводной таблицы
        growth_scenarios = scenarios[scenarios['Scenario'] != 'BASELINE']
        if not growth_scenarios.empty:
            best = growth_scenarios.sort_values('CM', ascending=False).iloc[0]
            all_scenarios_list.append({
                'Product': product_name,
                'Best_Scenario': best['Scenario'],
                'Scenario_Type': best['Scenario_Type'],
                'Growth_CM': best['CM'] - scenarios[scenarios['Scenario'] == 'BASELINE'].iloc[0]['CM'],
                'Base_CM': scenarios[scenarios['Scenario'] == 'BASELINE'].iloc[0]['CM'],
                'Action': ACTION_INSIGHTS.get(best['Scenario_Type'], '')
            })
    
    # Сводная таблица приоритетов
    summary_df = pd.DataFrame(all_scenarios_list) if all_scenarios_list else pd.DataFrame()
    
    return total_df, product_econ, summary_df

# ========== ВКЛАДКИ ==========
tabs = st.tabs([
    "ЮНИТ-ЭКОНОМИКА",
    "ТОЧКИ РОСТА", 
    "МАРКЕТИНГ",
    "ПРОДАЖИ",
    "ПРОДУКТЫ",
    "ГЕОГРАФИЯ",
    "СТАТИСТИКА",
    "МЕТОДОЛОГИЯ",
    "ДАННЫЕ"
])

# ---------- ВКЛАДКА 1: ЮНИТ-ЭКОНОМИКА ----------
with tabs[0]:
    st.markdown('<div class="section-title">ЮНИТ-ЭКОНОМИКА БИЗНЕСА (VACUUM MODEL)</div>', unsafe_allow_html=True)
    
    # Получаем данные
    total_df, product_econ = calculate_unit_economics()
    
    if len(total_df) == 0 or len(product_econ) == 0:
        st.warning("Нет данных для отображения юнит-экономики")
    else:
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
        st.dataframe(
            format_unit_econ(total_df).background_gradient(subset=['ROMI', 'LTV'], cmap='RdYlGn'),
            use_container_width=True,
            height=150
        )
        
        st.subheader("2. ЭКОНОМИКА ПО ПРОДУКТАМ (ВАКУУМНАЯ МОДЕЛЬ)")
        st.dataframe(
            format_unit_econ(product_econ).background_gradient(subset=['ROMI', 'LTV'], cmap='RdYlGn'),
            use_container_width=True
        )
        
        # Визуализация
        col1, col2 = st.columns(2)
        
        with col1:
            if len(product_econ) > 0:
                fig = px.bar(product_econ, x='Product', y='Revenue',
                            title='Выручка по продуктам', color='LTV',
                            color_continuous_scale='RdYlGn',
                            labels={'Revenue': 'Выручка (€)', 'LTV': 'LTV (€)'})
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if len(product_econ) > 0:
                fig2 = px.scatter(product_econ, x='C1', y='LTV', size='Revenue',
                                 color='Product', hover_name='Product',
                                 title='Матрица: Конверсия vs LTV',
                                 labels={'C1': 'Конверсия (C1)', 'LTV': 'LTV (€)'})
                st.plotly_chart(fig2, use_container_width=True)
        
        # Легенда метрик
        with st.expander("СПРАВОЧНИК МЕТРИК И ФОРМУЛ"):
            st.markdown("""
            **0. ИСХОДНЫЕ ДАННЫЕ:**
            - **UA** = Уникальные контакты (CONTACTS['Id'].nunique())
            - **B** = Уникальные платящие клиенты (Contact Name со статусом Active Student)
            - **AC** = Весь маркетинговый бюджет школы (Spend['Spend'].sum())
            
            **1. БАЗОВЫЕ МЕТРИКИ:**
            - **C1** = B / UA (Конверсия из посетителя в покупателя)
            - **Revenue** = Фактически полученные деньги (First payment + Recurring payments)
            
            **2. ТРАНЗАКЦИОННЫЕ МЕТРИКИ:**
            - **T** = Количество платежей (если рассрочка = месяцы обучения, если полная = 1)
            - **AOV** = Revenue / T (Средний чек ОДНОЙ транзакции)
            - **APC** = T / B (Сколько раз в среднем платит студент)
            
            **3. ЗАТРАТЫ:**
            - **COGS** = Себестоимость ОДНОЙ транзакции (комиссии, налоги)
            - **CPA** = AC / UA (Цена одного лида)
            - **CAC** = AC / B (Цена одного покупателя)
            
            **4. ЭКОНОМИКА (ПРИБЫЛЬ):**
            - **CLTV** = (AOV - COGS) × APC (Прибыль с одного ПЛАТЯЩЕГО клиента)
            - **LTV** = CLTV × C1 (Прибыль с одного ПОСЕТИТЕЛЯ - самая важная метрика)
            - **CM** = Revenue - AC - COGS (Маржинальный вклад)
            - **ROMI** = CM / AC × 100% (Окупаемость рекламы)
            """)

# ---------- ВКЛАДКА 2: ТОЧКИ РОСТА ----------
with tabs[1]:
    st.markdown('<div class="section-title">АНАЛИЗ ТОЧЕК РОСТА (SENSITIVITY ANALYSIS)</div>', unsafe_allow_html=True)
    
    # Получаем данные
    total_df, product_econ, growth_summary = calculate_growth_points()
    
    if len(total_df) == 0:
        st.warning("Нет данных для анализа точек роста")
    else:
        st.subheader("1. СЦЕНАРИИ РОСТА ДЛЯ ВСЕГО БИЗНЕСА")
        
        # Расчет сценариев для TOTAL BUSINESS
        TOTAL_UA = contacts['Id'].nunique()
        total_marketing_spend = spend['Spend'].sum()
        active_students_df = filtered_deals[filtered_deals['stage_normalized'] == 'Active Student']
        TOTAL_B_CORRECT = active_students_df['Contact Name'].nunique()
        total_t = active_students_df['Transactions'].sum() if 'Transactions' in active_students_df.columns else 0
        total_revenue = active_students_df['revenue'].sum()
        
        global_row = {
            'UA': TOTAL_UA,
            'B': TOTAL_B_CORRECT,
            'Revenue': total_revenue,
            'T': total_t,
            'AC': total_marketing_spend,
            'C1': TOTAL_B_CORRECT / TOTAL_UA if TOTAL_UA > 0 else 0,
            'AOV': total_revenue / total_t if total_t > 0 else 0,
            'APC': total_t / TOTAL_B_CORRECT if TOTAL_B_CORRECT > 0 else 0,
        }
        
        # Функции из ячейки 25
        GROWTH_PCT = 0.10
        AC_SCALING_FACTOR = 0.8
        
        def calculate_scenario_metrics_simple(ua, c1, aov, apc, ac_base, scenario_name, growth_pct):
            b = ua * c1 if ua > 0 and c1 > 0 else 0
            t = b * apc if b > 0 and apc > 0 else 0
            revenue = t * aov if t > 0 and aov > 0 else 0
            
            if "UA" in scenario_name:
                ac = ac_base * (1 + growth_pct * AC_SCALING_FACTOR)
            elif "CPA" in scenario_name:
                ac = ac_base * (1 - growth_pct)
            else:
                ac = ac_base

            cm = revenue - ac
            romi = (cm / ac * 100) if ac > 0 else 0
            
            return {
                'Scenario': scenario_name,
                'UA': ua, 'C1': c1, 'B': b, 'AOV': aov, 'APC': apc,
                'T': t, 'Revenue': revenue, 'AC': ac, 'CM': cm, 'ROMI': romi
            }
        
        # Генерация сценариев
        scenarios_list = []
        base_ua, base_c1, base_aov, base_apc = global_row['UA'], global_row['C1'], global_row['AOV'], global_row['APC']
        base_ac = global_row['AC']
        
        scenarios_list.append(calculate_scenario_metrics_simple(
            base_ua, base_c1, base_aov, base_apc, base_ac, "BASELINE", 0))
        
        g = GROWTH_PCT
        scenarios_list.append(calculate_scenario_metrics_simple(
            base_ua * (1 + g), base_c1, base_aov, base_apc, base_ac, f"UA +{int(g*100)}%", g))
        scenarios_list.append(calculate_scenario_metrics_simple(
            base_ua, base_c1 * (1 + g), base_aov, base_apc, base_ac, f"C1 +{int(g*100)}%", g))
        scenarios_list.append(calculate_scenario_metrics_simple(
            base_ua, base_c1, base_aov * (1 + g), base_apc, base_ac, f"AOV +{int(g*100)}%", g))
        scenarios_list.append(calculate_scenario_metrics_simple(
            base_ua, base_c1, base_aov, base_apc * (1 + g), base_ac, f"APC +{int(g*100)}%", g))
        scenarios_list.append(calculate_scenario_metrics_simple(
            base_ua, base_c1, base_aov, base_apc, base_ac, f"CPA -{int(g*100)}%", g))
        
        scenarios_df = pd.DataFrame(scenarios_list)
        
        # Расчет прироста
        base_cm = scenarios_df.loc[0, 'CM']
        scenarios_df['CM_Growth'] = scenarios_df['CM'] - base_cm
        scenarios_df['CM_Growth_Pct'] = (scenarios_df['CM_Growth'] / abs(base_cm) * 100) if abs(base_cm) > 0 else 0
        
        # Отображаем таблицу
        display_cols = ['Scenario', 'UA', 'C1', 'B', 'AOV', 'APC', 'Revenue', 'AC', 'CM', 'CM_Growth', 'ROMI']
        display_df = scenarios_df[display_cols].sort_values('CM_Growth', ascending=False)
        
        st.dataframe(
            display_df.style.format({
                'UA': '{:,.0f}', 'B': '{:,.0f}', 'Revenue': '{:,.0f}', 'AC': '{:,.0f}', 
                'CM': '{:,.0f}', 'CM_Growth': '{:+,.0f}', 'ROMI': '{:.1f}%',
                'C1': '{:.2%}', 'AOV': '{:,.1f}', 'APC': '{:.2f}'
            }).background_gradient(subset=['CM_Growth', 'ROMI'], cmap='RdYlGn'),
            use_container_width=True
        )
        
        # Анализ чувствительности
        st.subheader("2. АНАЛИЗ ЧУВСТВИТЕЛЬНОСТИ (±5-10%)")
        
        sensitivity_results = []
        metrics = ['UA', 'C1', 'AOV', 'APC']
        steps = [-0.10, -0.05, 0.05, 0.10]
        
        for metric in metrics:
            for step in steps:
                u = global_row['UA'] * (1 + step) if metric == 'UA' else global_row['UA']
                c = global_row['C1'] * (1 + step) if metric == 'C1' else global_row['C1']
                a = global_row['AOV'] * (1 + step) if metric == 'AOV' else global_row['AOV']
                p = global_row['APC'] * (1 + step) if metric == 'APC' else global_row['APC']
                
                cost = global_row['AC'] * (1 + step * AC_SCALING_FACTOR) if metric == 'UA' else global_row['AC']
                
                b = u * c if u > 0 and c > 0 else 0
                t = b * p if b > 0 and p > 0 else 0
                rev = t * a if t > 0 and a > 0 else 0
                cm = rev - cost
                
                cm_impact = cm - base_cm
                cm_impact_pct = (cm_impact / abs(base_cm) * 100) if abs(base_cm) > 0 else 0
                
                sensitivity_results.append({
                    'Metric': metric, 
                    'Change': f"{step:+.0%}",
                    'New_Value': (u if metric=='UA' else c if metric=='C1' else a if metric=='AOV' else p),
                    'CM_Impact': cm_impact, 
                    'CM_Impact_Pct': cm_impact_pct
                })
        
        sensitivity_df = pd.DataFrame(sensitivity_results)
        
        if len(sensitivity_df) > 0:
            sensitivity_df = sensitivity_df.sort_values('CM_Impact', ascending=False)
            st.dataframe(
                sensitivity_df.style.format({
                    'New_Value': '{:.2f}', 
                    'CM_Impact': '{:+,.0f}', 
                    'CM_Impact_Pct': '{:+.1f}%'
                }).background_gradient(subset=['CM_Impact'], cmap='RdYlGn'),
                use_container_width=True
            )
            
            # Ключевые инсайты
            st.subheader("3. КЛЮЧЕВЫЕ ИНСАЙТЫ")
            
            insights = []
            for metric in ['UA', 'C1', 'AOV', 'APC']:
                metric_data = sensitivity_df[sensitivity_df['Metric'] == metric]
                if not metric_data.empty:
                    max_impact = metric_data.loc[metric_data['CM_Impact'].idxmax()]
                    insights.append(f"**{metric}**: {max_impact['Change']} → Влияние на CM: {max_impact['CM_Impact']:+,.0f}€")
            
            for insight in insights:
                st.write(f"• {insight}")
        
        # Сводная карта приоритетов по продуктам
        if len(growth_summary) > 0:
            st.subheader("4. СВОДНАЯ КАРТА ПРИОРИТЕТОВ ПО ПРОДУКТАМ")
            
            growth_summary['Growth_Pct'] = (growth_summary['Growth_CM'] / growth_summary['Base_CM'].abs() * 100)
            growth_summary['Growth_Pct'] = growth_summary['Growth_Pct'].apply(lambda x: x if abs(x) < 1000 else (1000 if x > 0 else -1000))
            growth_summary = growth_summary.sort_values('Growth_CM', ascending=False)
            
            st.dataframe(
                growth_summary.style.format({
                    'Growth_CM': '{:+,.0f}', 
                    'Base_CM': '{:,.0f}', 
                    'Growth_Pct': '{:+.1f}%'
                }).background_gradient(subset=['Growth_CM'], cmap='Greens', vmin=0)
                .background_gradient(subset=['Growth_Pct'], cmap='RdYlGn', vmin=-100, vmax=100),
                use_container_width=True
            )

# ---------- ВКЛАДКА 3: МАРКЕТИНГ ----------
with tabs[2]:
    st.markdown('<div class="section-title">МАРКЕТИНГОВАЯ АНАЛИТИКА</div>', unsafe_allow_html=True)
    
    # 1. МАРКЕТИНГОВАЯ ВОРОНКА (ячейка 13)
    st.subheader("1. МАРКЕТИНГОВАЯ ВОРОНКА И ЭФФЕКТИВНОСТЬ РАСХОДОВ")
    
    if 'Source' in spend.columns and 'Source' in filtered_deals.columns:
        # Агрегация Spend
        spend_agg = spend.groupby('Source').agg({
            'Impressions': 'sum',
            'Clicks': 'sum',
            'Spend': 'sum'
        }).reset_index()
        
        # Агрегация Deals
        leads_agg = filtered_deals.groupby('Source')['Id'].count().reset_index().rename(columns={'Id': 'Leads'})
        quality_filter = ['A - High', 'B - Medium']
        qual_leads_agg = filtered_deals[filtered_deals['Quality'].isin(quality_filter)].groupby('Source')['Id'].count().reset_index().rename(columns={'Id': 'Quality_Leads'})
        
        # Объединение
        funnel_df = spend_agg.merge(leads_agg, on='Source', how='left').merge(qual_leads_agg, on='Source', how='left').fillna(0)
        
        # Сортируем и берем Топ-7 по расходам
        top_funnel = funnel_df.sort_values(by='Spend', ascending=False).head(7)
        
        # График воронки
        fig1 = make_subplots(
            rows=2, cols=1,
            subplot_titles=("Воронка конверсии по каналам (Log Scale)", "Стоимость результата"),
            vertical_spacing=0.15,
            specs=[[{"type": "bar"}], [{"type": "table"}]]
        )
        
        # График 1: Группированная воронка
        stages = ['Impressions', 'Clicks', 'Leads', 'Quality_Leads']
        colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA']
        
        for i, stage in enumerate(stages):
            fig1.add_trace(
                go.Bar(
                    name=stage,
                    x=top_funnel['Source'],
                    y=top_funnel[stage],
                    text=top_funnel[stage].apply(lambda x: f"{x:,.0f}"),
                    textposition='auto',
                    marker_color=colors[i]
                ),
                row=1, col=1
            )
        
        fig1.update_yaxes(type="log", title_text="Количество (Log Scale)", row=1, col=1)
        
        # График 2: Таблица с деньгами
        top_funnel['CPM'] = (top_funnel['Spend'] / top_funnel['Impressions'] * 1000).replace([np.inf], 0).round(2)
        top_funnel['CPC'] = (top_funnel['Spend'] / top_funnel['Clicks']).replace([np.inf], 0).round(2)
        top_funnel['CPL (Lead)'] = (top_funnel['Spend'] / top_funnel['Leads']).replace([np.inf], 0).round(2)
        top_funnel['CPQ (Quality)'] = (top_funnel['Spend'] / top_funnel['Quality_Leads']).replace([np.inf], 0).round(2)
        
        fig1.add_trace(
            go.Table(
                header=dict(
                    values=['Source', 'Spend', 'CPM (1000 shows)', 'CPC (Click)', 'CPL (Lead)', 'CPQ (Quality Lead)'],
                    fill_color='paleturquoise',
                    align='left'
                ),
                cells=dict(
                    values=[
                        top_funnel['Source'],
                        top_funnel['Spend'].apply(lambda x: f"{x:,.0f}€"),
                        top_funnel['CPM'],
                        top_funnel['CPC'],
                        top_funnel['CPL (Lead)'],
                        top_funnel['CPQ (Quality)']
                    ],
                    fill_color='lavender',
                    align='left'
                )
            ),
            row=2, col=1
        )
        
        fig1.update_layout(height=800, title_text="Маркетинговая аналитика: Объемы и Деньги", barmode='group')
        st.plotly_chart(fig1, use_container_width=True)
    
    # 2. АНАЛИЗ ПЛАТНЫХ ИСТОЧНИКОВ (ячейка 14)
    st.subheader("2. АНАЛИЗ ПЛАТНЫХ ИСТОЧНИКОВ: CPC vs КАЧЕСТВО")
    
    if 'Source' in spend.columns and 'Source' in filtered_deals.columns:
        spend_metrics = spend.groupby('Source').agg({'Spend': 'sum', 'Clicks': 'sum', 'Impressions': 'sum'}).reset_index()
        deals_metrics = filtered_deals.groupby('Source').agg({
            'Id': 'count', 
            'stage_normalized': lambda x: (x == 'Active Student').sum()
        }).reset_index().rename(columns={'Id': 'Leads', 'stage_normalized': 'Buyers'})
        
        marketing_deep = spend_metrics.merge(deals_metrics, on='Source', how='inner')
        marketing_deep['CPC'] = (marketing_deep['Spend'] / marketing_deep['Clicks']).replace([np.inf], 0).fillna(0).round(2)
        marketing_deep['CTR'] = (marketing_deep['Clicks'] / marketing_deep['Impressions'] * 100).fillna(0).round(2)
        marketing_deep['CPL'] = (marketing_deep['Spend'] / marketing_deep['Leads'])
        marketing_deep['C1_Quality'] = (marketing_deep['Buyers'] / marketing_deep['Leads'] * 100)
        
        paid_marketing = marketing_deep[(marketing_deep['Spend'] > 10)].sort_values(by='Spend', ascending=False).copy()
        
        if len(paid_marketing) > 0:
            fig2 = px.scatter(
                paid_marketing,
                x='CPC',
                y='C1_Quality',
                size='Spend',
                color='Source',
                text='Source',
                title='CPC vs Качество трафика (C1)',
                labels={'CPC': 'Цена за клик (€)', 'C1_Quality': 'Конверсия в покупку (%)'},
                height=500
            )
            fig2.add_vline(x=paid_marketing['CPC'].median(), line_dash="dash", line_color="gray", annotation_text="Ср.CPC")
            fig2.add_hline(y=paid_marketing['C1_Quality'].median(), line_dash="dash", line_color="gray", annotation_text="Ср.C1")
            fig2.update_traces(textposition='top center')
            st.plotly_chart(fig2, use_container_width=True)
    
    # 3. МАТРИЦА ЭФФЕКТИВНОСТИ ИСТОЧНИКОВ (ячейка 15)
    st.subheader("3. МАТРИЦА ЭФФЕКТИВНОСТИ ИСТОЧНИКОВ: СКОРОСТЬ VS ЧЕК")
    
    if 'Source' in filtered_deals.columns:
        deals_success = filtered_deals[filtered_deals['stage_normalized'] == 'Active Student'].copy()
        
        if len(deals_success) > 0:
            source_matrix = deals_success.groupby('Source').agg({
                'Id': 'count',
                'Deal_Age_days': 'median',
                'revenue': ['mean', 'sum'],
                'Offer Total Amount': 'sum'
            }).reset_index()
            
            source_matrix.columns = ['Source', 'Student_Count', 'Median_Speed_Days', 'Mean_Check', 'Total_Revenue', 'Total_Potential']
            source_matrix = source_matrix[source_matrix['Student_Count'] >= 5]
            source_matrix['Collected_Pct'] = (source_matrix['Total_Revenue'] / source_matrix['Total_Potential'] * 100).round(1)
            
            if len(source_matrix) > 0:
                fig3 = px.scatter(
                    source_matrix,
                    x='Median_Speed_Days',
                    y='Mean_Check',
                    size='Total_Revenue',
                    color='Source',
                    text='Source',
                    title='Матрица Источников: Скорость (X) vs Средний чек (Y)',
                    labels={
                        'Median_Speed_Days': 'Медианная скорость закрытия (дни)', 
                        'Mean_Check': 'Средний чек (Revenue Mean)',
                        'Total_Revenue': 'Общая выручка'
                    },
                    height=600
                )
                
                avg_speed = source_matrix['Median_Speed_Days'].mean()
                avg_check = source_matrix['Mean_Check'].mean()
                fig3.add_vline(x=avg_speed, line_dash="dash", line_color="gray", annotation_text="Ср. скорость")
                fig3.add_hline(y=avg_check, line_dash="dash", line_color="gray", annotation_text="Ср. чек")
                fig3.update_traces(textposition='top center')
                st.plotly_chart(fig3, use_container_width=True)
    
    # 4. ROI ПО ИСТОЧНИКАМ (ячейка 16)
    st.subheader("4. ROI/ROAS ПО ИСТОЧНИКАМ ТРАФИКА")
    
    if 'Source' in spend.columns and 'Source' in filtered_deals.columns:
        marketing_costs = spend.groupby('Source').agg({'Spend': 'sum', 'Clicks': 'sum'}).reset_index()
        marketing_revenue = filtered_deals[filtered_deals['stage_normalized'] == 'Active Student'].groupby('Source').agg({
            'revenue': 'sum',
            'Id': 'count'
        }).reset_index().rename(columns={'Id': 'Students_Count'})
        
        marketing_roi = marketing_costs.merge(marketing_revenue, on='Source', how='left').fillna(0)
        marketing_roi['CAC'] = (marketing_roi['Spend'] / marketing_roi['Students_Count']).replace([np.inf], 0).round(2)
        marketing_roi['ROAS_Pct'] = (marketing_roi['revenue'] / marketing_roi['Spend'] * 100).replace([np.inf], 0).round(2)
        marketing_roi['Avg_Check'] = (marketing_roi['revenue'] / marketing_roi['Students_Count']).fillna(0).round(2)
        
        roi_analysis = marketing_roi[(marketing_roi['Spend'] > 0) & (marketing_roi['Students_Count'] > 0)].sort_values(by='ROAS_Pct', ascending=False)
        
        if len(roi_analysis) > 0:
            fig4 = px.scatter(
                roi_analysis,
                x='Spend',
                y='ROAS_Pct',
                size='revenue',
                color='Source',
                text='Source',
                title='ROAS: Окупаемость источников',
                labels={'ROAS_Pct': 'ROAS (%)', 'Spend': 'Расходы (€)'}
            )
            fig4.update_traces(textposition='bottom center')
            fig4.add_hline(y=100, line_dash="dash", line_color="red", annotation_text="Точка безубыточности")
            st.plotly_chart(fig4, use_container_width=True)

# ---------- ВКЛАДКА 4: ПРОДАЖИ ----------
with tabs[3]:
    st.markdown('<div class="section-title">ЭФФЕКТИВНОСТЬ ОТДЕЛА ПРОДАЖ (KPI 360°)</div>', unsafe_allow_html=True)
    
    # 1. ТОП МЕНЕДЖЕРОВ ПО ВЫРУЧКЕ (ячейка 17)
    st.subheader("1. ТОП МЕНЕДЖЕРОВ ПО ВЫРУЧКЕ И КОНВЕРСИИ")
    
    if 'Deal Owner Name' in filtered_deals.columns:
        # Подготовка данных (только чистые сделки)
        df_clean = filtered_deals[filtered_deals['max_stage_rank'] >= 1].copy() if 'max_stage_rank' in filtered_deals.columns else filtered_deals.copy()
        
        # Базовые метрики
        manager_stats = df_clean.groupby('Deal Owner Name').agg(
            Leads=('Id', 'count'),
            Revenue=('revenue', 'sum'),
            Sales=('stage_normalized', lambda x: (x == 'Active Student').sum())
        ).reset_index().rename(columns={'Deal Owner Name': 'Manager'})
        
        # Скорость закрытия (только успешные)
        speed_stats = df_clean[df_clean['stage_normalized'] == 'Active Student'].groupby('Deal Owner Name')['Deal_Age_days'].median().reset_index()
        speed_stats.columns = ['Manager', 'Median_Deal_Age_Days']
        
        # Сборка таблицы
        final_stats = manager_stats.merge(speed_stats, on='Manager', how='left').fillna(0)
        
        # Производные KPI
        final_stats['Win_Rate'] = (final_stats['Sales'] / final_stats['Leads'] * 100).round(2)
        final_stats['Avg_Check'] = (final_stats['Revenue'] / final_stats['Sales']).replace([np.inf], 0).fillna(0).round(0)
        
        # Фильтр: менеджеры с > 10 лидов
        top_managers = final_stats[final_stats['Leads'] >= 10].sort_values(by='Revenue', ascending=False)
        
        if len(top_managers) > 0:
            # График 1: Выручка с цветом Win Rate
            fig1 = px.bar(
                top_managers.head(15),
                x='Manager', y='Revenue', 
                color='Win_Rate',
                text_auto='.2s',
                title='ТОП-15 Менеджеров по Выручке (Цвет = Конверсия Win Rate)',
                labels={'Revenue': 'Выручка', 'Win_Rate': 'Win Rate (%)'},
                color_continuous_scale='RdYlGn',
                height=500
            )
            fig1.update_layout(xaxis={'categoryorder':'total descending'})
            st.plotly_chart(fig1, use_container_width=True)
            
            # График 2: Конверсия с цветом скорости
            efficiency_view = top_managers.sort_values(by='Win_Rate', ascending=True).tail(15)
            fig2 = px.bar(
                efficiency_view,
                x='Win_Rate', 
                y='Manager', 
                orientation='h', 
                color='Median_Deal_Age_Days',
                text_auto='.1f',
                title='ТОП по конверсии (Цвет = Скорость закрытия, дни)',
                labels={'Win_Rate': 'Конверсия (%)', 'Manager': 'Менеджер', 'Median_Deal_Age_Days': 'Ср. цикл сделки (дни)'},
                color_continuous_scale='Bluered',
                height=600
            )
            st.plotly_chart(fig2, use_container_width=True)
            
            # ТАБЛИЦА С ИСПРАВЛЕНИЯМИ (убрать is_paid, добавить лиды и SLA)
            st.subheader("2. ДЕТАЛЬНАЯ СТАТИСТИКА МЕНЕДЖЕРОВ")
            
            # Добавляем SLA метрики
            if 'SLA' in df_clean.columns:
                # Конвертируем SLA в часы для расчета
                df_clean['SLA_Hours'] = pd.to_timedelta(df_clean['SLA']).dt.total_seconds() / 3600
                sla_stats = df_clean.groupby('Deal Owner Name')['SLA_Hours'].median().reset_index()
                sla_stats.columns = ['Manager', 'Median_SLA_Hours']
                final_stats = final_stats.merge(sla_stats, on='Manager', how='left').fillna(0)
                
                display_cols = ['Manager', 'Leads', 'Sales', 'Revenue', 'Win_Rate', 
                               'Avg_Check', 'Median_Deal_Age_Days', 'Median_SLA_Hours']
                display_df = final_stats[display_cols].sort_values('Revenue', ascending=False).head(20)
                
                st.dataframe(
                    display_df.style\
                        .background_gradient(subset=['Revenue', 'Win_Rate'], cmap='Greens')\
                        .format({
                            'Revenue': '{:,.0f}', 
                            'Avg_Check': '{:,.0f}', 
                            'Median_Deal_Age_Days': '{:.0f}',
                            'Median_SLA_Hours': '{:.1f}',
                            'Win_Rate': '{:.1f}%'
                        }),
                    use_container_width=True
                )
            else:
                display_cols = ['Manager', 'Leads', 'Sales', 'Revenue', 'Win_Rate', 
                               'Avg_Check', 'Median_Deal_Age_Days']
                display_df = final_stats[display_cols].sort_values('Revenue', ascending=False).head(20)
                
                st.dataframe(
                    display_df.style\
                        .background_gradient(subset=['Revenue', 'Win_Rate'], cmap='Greens')\
                        .format({
                            'Revenue': '{:,.0f}', 
                            'Avg_Check': '{:,.0f}', 
                            'Median_Deal_Age_Days': '{:.0f}',
                            'Win_Rate': '{:.1f}%'
                        }),
                    use_container_width=True
                )
    
    # 3. АНАЛИЗ СКОРОСТИ И КАЧЕСТВА (SLA & QUALITY) - ячейка 18
    st.subheader("3. АНАЛИЗ СКОРОСТИ ОТВЕТА (SLA) И КАЧЕСТВА ЛИДОВ")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'SLA_Segment' in filtered_deals.columns:
            sla_global = filtered_deals[
                (filtered_deals['SLA_Segment'].notna()) & 
                (filtered_deals['SLA_Segment'] != 'Unknown')
            ].copy()
            
            if len(sla_global) > 0:
                sla_impact = sla_global.groupby('SLA_Segment').agg({
                    'Id': 'count',
                    'is_paid': 'mean'
                }).reset_index()
                sla_impact.columns = ['SLA_Segment', 'Total_Deals', 'Win_Rate']
                sla_impact['Win_Rate_Pct'] = (sla_impact['Win_Rate'] * 100).round(2)
                
                sla_order = ['Top Speed (< 1h)', 'Fast (1h-4h)', 'Normal (4h-24h)', 'Slow (1d-7d)', 'Too Slow (> 7d)']
                sla_impact['SLA_Segment'] = pd.Categorical(sla_impact['SLA_Segment'], categories=sla_order, ordered=True)
                sla_impact = sla_impact.sort_values('SLA_Segment')
                
                fig3 = px.bar(
                    sla_impact,
                    x='SLA_Segment',
                    y='Win_Rate_Pct',
                    color='Total_Deals',
                    text_auto='.1f',
                    title='Конверсия по сегментам скорости ответа',
                    labels={'Win_Rate_Pct': 'Конверсия (%)', 'Total_Deals': 'Кол-во сделок'},
                    color_continuous_scale='RdYlGn',
                    height=400
                )
                st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        if 'Quality' in filtered_deals.columns:
            deals_quality = filtered_deals[filtered_deals['Quality'].notna()].copy()
            
            if len(deals_quality) > 0:
                quality_stats = deals_quality.groupby('Quality').agg({
                    'Id': 'count',
                    'stage_normalized': lambda x: (x == 'Active Student').sum()
                }).reset_index()
                quality_stats.columns = ['Quality', 'Total_Leads', 'Active_Students']
                quality_stats['Win_Rate_Pct'] = (quality_stats['Active_Students'] / quality_stats['Total_Leads'] * 100).round(2)
                
                fig4 = px.bar(
                    quality_stats,
                    x='Quality',
                    y='Win_Rate_Pct',
                    color='Total_Leads',
                    text_auto='.1f',
                    title='Конверсия по качеству лидов',
                    labels={'Win_Rate_Pct': 'Конверсия (%)', 'Quality': 'Категория качества'},
                    color_continuous_scale='RdYlGn',
                    height=400
                )
                fig4.update_layout(xaxis={'categoryorder':'category ascending'})
                st.plotly_chart(fig4, use_container_width=True)
    
    # 4. ПРИЧИНЫ ОТКАЗОВ ПО МЕНЕДЖЕРАМ (ячейка 19)
    st.subheader("4. АНАЛИЗ ПРИЧИН ОТКАЗОВ ПО МЕНЕДЖЕРАМ")
    
    if 'Lost Reason' in filtered_deals.columns and 'Deal Owner Name' in filtered_deals.columns:
        lost_deals = filtered_deals[
            (filtered_deals['stage_normalized'] == 'Churned') & 
            (filtered_deals['Lost Reason'].notna()) &
            (filtered_deals['Lost Reason'] != 'unknown') &
            (filtered_deals['Lost Reason'] != 'Unknown')
        ].copy()
        
        if len(lost_deals) > 0:
            lost_reasons_stats = lost_deals.groupby(['Deal Owner Name', 'Lost Reason'])['Id'].count().reset_index()
            lost_reasons_stats.columns = ['Manager', 'Reason', 'Count']
            
            # Фильтр: менеджеры с > 10 отказов
            manager_total_lost = lost_reasons_stats.groupby('Manager')['Count'].transform('sum')
            lost_reasons_stats = lost_reasons_stats[manager_total_lost > 10]
            
            if len(lost_reasons_stats) > 0:
                fig5 = px.bar(
                    lost_reasons_stats,
                    x='Manager',
                    y='Count',
                    color='Reason',
                    title='Структура причин отказов по менеджерам',
                    labels={'Count': 'Количество отказов', 'Reason': 'Причина', 'Manager': 'Менеджер'},
                    color_discrete_sequence=px.colors.qualitative.Set2,
                    height=500
                )
                fig5.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
                st.plotly_chart(fig5, use_container_width=True)

# ---------- ВКЛАДКА 5: ПРОДУКТЫ ----------
with tabs[4]:
    st.markdown('<div class="section-title">АНАЛИЗ ПРОДУКТОВ И ПЛАТЕЖЕЙ</div>', unsafe_allow_html=True)
    
    # Подготовка данных (ячейка 20)
    deals_success = filtered_deals[filtered_deals['stage_normalized'] == 'Active Student'].copy()
    pay_col = 'Payment_Type_Recovered' if 'Payment_Type_Recovered' in deals_success.columns else 'Payment Type'
    
    if len(deals_success) > 0:
        # Рассчитываем Transactions как в юнит-экономике
        deals_success['Transactions'] = np.where(
            deals_success[pay_col] == 'one payment', 
            1, 
            deals_success['Months of study'].fillna(1)
        )
        
        # 1. ПОЛНЫЕ МЕТРИКИ ПО ПРОДУКТАМ
        st.subheader("1. ПОЛНЫЕ МЕТРИКИ ПО ПРОДУКТАМ")
        
        # Базовые метрики
        product_metrics = deals_success.groupby('Product').agg({
            'Contact Name': 'nunique',          # B (уникальные клиенты)
            'revenue': 'sum',                   # Выручка
            'Offer Total Amount': ['mean', 'sum'],  # Средний и общий контракт
            'Transactions': 'sum',              # T (транзакции)
            'Initial Amount Paid': 'mean'       # Средний первоначальный взнос
        }).round(0)
        
        product_metrics.columns = ['B', 'Revenue', 'Avg_Contract', 'Total_Contract', 'T', 'Avg_Initial']
        
        # Фильтрация: удаляем продукты с 1 клиентом
        product_metrics = product_metrics[product_metrics['B'] > 1].copy()
        
        if len(product_metrics) > 0:
            # Расчет производных метрик
            product_metrics['Avg_Check'] = (product_metrics['Revenue'] / product_metrics['B']).round(0)
            product_metrics['Collection_Ratio'] = (product_metrics['Revenue'] / product_metrics['Total_Contract'] * 100).round(1)
            product_metrics['APC'] = (product_metrics['T'] / product_metrics['B']).round(2)
            product_metrics['AOV'] = (product_metrics['Revenue'] / product_metrics['T']).round(0)
            
            # Юнит-экономика (автономные расчеты)
            TOTAL_UA = contacts['Id'].nunique()
            total_marketing_spend = spend['Spend'].sum()
            COGS_PERCENT = 0.0
            COGS_FIXED = 0
            
            product_metrics['UA'] = TOTAL_UA
            product_metrics['C1'] = (product_metrics['B'] / TOTAL_UA).round(4)
            product_metrics['AC'] = total_marketing_spend
            product_metrics['CPA'] = (total_marketing_spend / TOTAL_UA).round(2)
            product_metrics['CAC'] = (total_marketing_spend / product_metrics['B']).round(0)
            
            # COGS и прибыль
            product_metrics['COGS_per_T'] = (product_metrics['Revenue'] * COGS_PERCENT + product_metrics['T'] * COGS_FIXED) / product_metrics['T']
            product_metrics['CLTV'] = ((product_metrics['AOV'] - product_metrics['COGS_per_T']) * product_metrics['APC']).round(0)
            product_metrics['LTV'] = (product_metrics['CLTV'] * product_metrics['C1']).round(2)
            product_metrics['CM'] = (product_metrics['Revenue'] - total_marketing_spend - (product_metrics['Revenue'] * COGS_PERCENT + product_metrics['T'] * COGS_FIXED)).round(0)
            
            # Таблица для вывода
            display_cols = ['B', 'Revenue', 'Avg_Check', 'Avg_Contract', 'Collection_Ratio', 
                            'C1', 'CLTV', 'LTV', 'CAC', 'CM']
            display_df = product_metrics[display_cols].sort_values('Revenue', ascending=False)
            
            st.dataframe(
                display_df.style.format({
                    'B': '{:,.0f}',
                    'Revenue': '{:,.0f}',
                    'Avg_Check': '{:,.0f}',
                    'Avg_Contract': '{:,.0f}',
                    'Collection_Ratio': '{:.1f}%',
                    'C1': '{:.2%}',
                    'CLTV': '{:,.0f}',
                    'LTV': '{:.2f}',
                    'CAC': '{:,.0f}',
                    'CM': '{:,.0f}'
                }).background_gradient(subset=['Revenue', 'LTV', 'CM'], cmap='RdYlGn'),
                use_container_width=True
            )
            
            # 2. ВИЗУАЛИЗАЦИИ
            st.subheader("2. ВИЗУАЛИЗАЦИИ ЭФФЕКТИВНОСТИ ПРОДУКТОВ")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # График 1: Выручка по продуктам (цвет = LTV)
                fig1 = px.bar(
                    display_df.reset_index(),
                    x='Product', y='Revenue',
                    color='LTV',
                    title='Выручка по продуктам (Цвет = LTV)',
                    labels={'Revenue': 'Выручка (€)', 'LTV': 'LTV (€)'},
                    color_continuous_scale='RdYlGn',
                    height=500
                )
                fig1.update_layout(xaxis={'categoryorder': 'total descending'})
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                # График 2: Матрица продуктов (Клиенты vs Средний чек)
                fig2 = px.scatter(
                    display_df.reset_index(),
                    x='B', y='Avg_Check',
                    size='Revenue',
                    color='Collection_Ratio',
                    text='Product',
                    title='Матрица продуктов: Клиенты vs Средний чек',
                    labels={'B': 'Количество клиентов', 'Avg_Check': 'Средний чек (€)', 'Collection_Ratio': '% оплаты контракта'},
                    color_continuous_scale='Viridis',
                    height=500
                )
                fig2.update_traces(textposition='top center')
                st.plotly_chart(fig2, use_container_width=True)
            
            # 3. АНАЛИЗ ТИПОВ ОПЛАТЫ
            st.subheader("3. АНАЛИЗ ТИПОВ ОПЛАТЫ")
            
            if pay_col in deals_success.columns:
                # Фильтруем те же продукты
                deals_filtered = deals_success[deals_success['Product'].isin(display_df.index)]
                payment_split = deals_filtered.groupby(['Product', pay_col]).size().reset_index(name='Count')
                
                if len(payment_split) > 0:
                    # Stacked bar
                    fig3 = px.bar(
                        payment_split,
                        x='Product', y='Count', color=pay_col,
                        title='Распределение типов оплаты по продуктам',
                        labels={'Count': 'Количество сделок'},
                        color_discrete_sequence=px.colors.qualitative.Set3,
                        height=500
                    )
                    fig3.update_layout(xaxis={'categoryorder': 'total descending'}, barmode='stack')
                    st.plotly_chart(fig3, use_container_width=True)
            
            # 4. АНАЛИЗ ТИПОВ ОБУЧЕНИЯ
            st.subheader("4. АНАЛИЗ ТИПОВ ОБУЧЕНИЯ")
            
            if 'Education Type' in deals_success.columns:
                edu_stats = deals_success.groupby('Education Type').agg({
                    'Contact Name': 'nunique',
                    'revenue': 'sum',
                    'Offer Total Amount': 'mean'
                }).round(0)
                edu_stats.columns = ['Students', 'Revenue', 'Avg_Contract']
                edu_stats = edu_stats[edu_stats['Students'] > 1]  # Фильтр
                edu_stats['Avg_Check'] = (edu_stats['Revenue'] / edu_stats['Students']).round(0)
                
                if len(edu_stats) > 0:
                    fig4 = px.bar(
                        edu_stats.reset_index(),
                        x='Education Type', y='Revenue',
                        color='Avg_Check',
                        title='Выручка по типам обучения (Цвет = Средний чек)',
                        labels={'Revenue': 'Выручка (€)', 'Avg_Check': 'Средний чек (€)'},
                        color_continuous_scale='RdYlGn',
                        height=500
                    )
                    fig4.update_layout(xaxis={'categoryorder': 'total descending'})
                    st.plotly_chart(fig4, use_container_width=True)
    else:
        st.warning("Нет успешных сделок для анализа продуктов")

# ---------- ВКЛАДКА 6: ГЕОГРАФИЯ ----------
with tabs[5]:
    st.markdown('<div class="section-title">ГЕОГРАФИЧЕСКИЙ АНАЛИЗ</div>', unsafe_allow_html=True)
    
    # Подготовка данных (ячейка 21)
    deals_with_city = filtered_deals[
        (filtered_deals['City'].notna()) & 
        (filtered_deals['City'] != 'Unknown') &
        (filtered_deals['City'] != 'unknown')
    ].copy()
    
    if len(deals_with_city) > 0:
        city_stats = deals_with_city.groupby('City').agg({
            'Id': 'count',
            'stage_normalized': lambda x: (x == 'Active Student').sum(),
            'revenue': 'sum',
            'Source': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'Unknown'
        }).reset_index()
        
        city_stats.columns = ['City', 'Total_Deals', 'Active_Students', 'Total_Revenue', 'Top_Source']
        city_stats['Win_Rate'] = (city_stats['Active_Students'] / city_stats['Total_Deals'] * 100).round(2)
        city_stats = city_stats.sort_values('Total_Revenue', ascending=False)
        
        # 1. КАРТА ПРОДАЖ (ячейка 21)
        st.subheader("1. КАРТА ПРОДАЖ")
        
        # Подготовка геоданных
        geocoded = prepare_geodata(city_stats)
        
        if len(geocoded) > 0:
            fig_map = px.scatter_geo(
                geocoded,
                lat="lat",
                lon="lon",
                size="Total_Deals",
                color="Total_Revenue",
                hover_name="City",
                hover_data={'Total_Revenue': ':.0f', 'Total_Deals': True, 'Win_Rate': ':.1f', 'Top_Source': True},
                scope="europe",
                center={"lat": 50.0, "lon": 10.0},
                title="Карта продаж: размер = сделки, цвет = выручка",
                color_continuous_scale='RdYlGn',
                map_style="carto-positron",
                height=600
            )
            fig_map.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.info("Не удалось геокодировать города для отображения карты")
        
        # 2. ТОП ГОРОДОВ ПО ВЫРУЧКЕ (ячейка 21)
        st.subheader("2. ТОП ГОРОДОВ ПО ВЫРУЧКЕ")
        
        city_top15 = city_stats.head(15).copy()
        
        fig_bar = px.bar(
            city_top15,
            x='City',
            y='Total_Revenue',
            color='Top_Source',
            text_auto='.2s',
            title='Топ-15 городов по выручке',
            labels={'Total_Revenue': 'Выручка (€)'},
            color_discrete_sequence=px.colors.qualitative.Set3,
            height=500
        )
        fig_bar.update_layout(xaxis={'categoryorder': 'total descending'})
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # 3. АНАЛИЗ ЭФФЕКТИВНОСТИ ПО ГОРОДАМ (ячейка 22)
        st.subheader("3. АНАЛИЗ ЭФФЕКТИВНОСТИ ПО ГОРОДАМ")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # ТОП-10 ПО ВЫРУЧКЕ
            top_revenue = city_stats.head(10).sort_values('Total_Revenue', ascending=True)
            
            fig_rev = px.bar(
                top_revenue,
                x='Total_Revenue',
                y='City',
                orientation='h',
                text='Total_Revenue',
                title='Топ-10 городов по выручке',
                labels={'Total_Revenue': 'Выручка (€)', 'City': ''},
                color='Win_Rate',
                color_continuous_scale='RdYlGn',
                height=500
            )
            fig_rev.update_traces(texttemplate='%{text:,.0f}€', textposition='outside')
            fig_rev.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_rev, use_container_width=True)
        
        with col2:
            # ТОП-10 ПО КОНВЕРСИИ (минимум 5 сделок)
            min_deals = 5
            top_conversion = city_stats[city_stats['Total_Deals'] >= min_deals].sort_values('Win_Rate', ascending=False).head(10)
            
            if len(top_conversion) > 0:
                fig_conv = px.bar(
                    top_conversion,
                    x='Win_Rate',
                    y='City',
                    orientation='h',
                    text='Win_Rate',
                    title=f'Топ-10 городов по конверсии (≥{min_deals} сделок)',
                    labels={'Win_Rate': 'Win Rate (%)', 'City': ''},
                    color='Total_Revenue',
                    color_continuous_scale='RdYlGn',
                    height=500
                )
                fig_conv.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                fig_conv.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig_conv, use_container_width=True)
        
        # 4. УРОВНИ НЕМЕЦКОГО ПО ГОРОДАМ (ячейка 23)
        st.subheader("4. УРОВНИ НЕМЕЦКОГО ЯЗЫКА ПО ГОРОДАМ")
        
        if 'Level of Deutsch' in filtered_deals.columns:
            deals_lang = filtered_deals[
                (filtered_deals['max_stage_rank'] >= 1) & 
                (filtered_deals['Level of Deutsch'].notna()) &
                (filtered_deals['Level of Deutsch'] != 'Unknown') &
                (filtered_deals['Level of Deutsch'] != 'unknown')
            ].copy()
            
            if len(deals_lang) > 0:
                # Берем топ-50 городов по выручке
                city_revenue = filtered_deals.groupby('City')['revenue'].sum().nlargest(50).index.tolist()
                deals_city_lang = filtered_deals[
                    (filtered_deals['City'].isin(city_revenue)) &
                    (filtered_deals['Level of Deutsch'].notna()) &
                    (filtered_deals['Level of Deutsch'] != 'Unknown') &
                    (filtered_deals['Level of Deutsch'] != 'unknown') &
                    (filtered_deals['stage_normalized'] == 'Active Student')
                ].copy()
                
                if len(deals_city_lang) > 0:
                    city_lang_dist = deals_city_lang.groupby(['City', 'Level of Deutsch']).size().reset_index(name='Active_Students')
                    city_totals = city_lang_dist.groupby('City')['Active_Students'].sum().reset_index(name='Total_Active')
                    city_lang_dist = pd.merge(city_lang_dist, city_totals, on='City')
                    city_lang_dist['Percentage'] = (city_lang_dist['Active_Students'] / city_lang_dist['Total_Active'] * 100).round(1)
                    
                    # Создаем сводную таблицу
                    level_order = ['A0', 'A1', 'A2', 'B1', 'B2', 'C1', 'C2']
                    pivot_table = city_lang_dist.pivot_table(
                        index='City',
                        columns='Level of Deutsch',
                        values='Percentage',
                        aggfunc='first'
                    ).fillna(0)
                    
                    # Добавляем недостающие уровни
                    for level in level_order:
                        if level not in pivot_table.columns:
                            pivot_table[level] = 0
                    
                    # Упорядочиваем колонки
                    pivot_table = pivot_table[level_order]
                    
                    # Добавляем общую статистику по городам
                    city_stats_summary = filtered_deals.groupby('City').agg({
                        'Id': 'count',
                        'revenue': 'sum',
                        'stage_normalized': lambda x: (x == 'Active Student').sum()
                    }).reset_index()
                    city_stats_summary.columns = ['City', 'Total_Deals', 'Total_Revenue', 'Active_Students']
                    city_stats_summary['Win_Rate_Pct'] = (city_stats_summary['Active_Students'] / city_stats_summary['Total_Deals'] * 100).round(1)
                    
                    pivot_table = pd.merge(
                        pivot_table,
                        city_stats_summary[['City', 'Total_Deals', 'Total_Revenue', 'Win_Rate_Pct']],
                        left_index=True,
                        right_on='City'
                    )
                    
                    pivot_table = pivot_table.sort_values('Total_Revenue', ascending=False)
                    
                    # Отображаем таблицу
                    st.dataframe(
                        pivot_table.style.format({
                            'Total_Revenue': '{:,.0f}',
                            'Win_Rate_Pct': '{:.1f}%',
                            **{level: '{:.1f}%' for level in level_order}
                        }).background_gradient(subset=['Total_Revenue', 'Win_Rate_Pct'], cmap='RdYlGn'),
                        use_container_width=True,
                        height=400
                    )
        
        # 5. СВОДНАЯ СТАТИСТИКА
        st.subheader("5. СВОДНАЯ СТАТИСТИКА ПО ГЕОГРАФИИ")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Распределение городов по группам
            city_groups = pd.cut(
                city_stats['Total_Deals'],
                bins=[0, 1, 3, 10, 30, 100, float('inf')],
                labels=['1 сделка', '2-3', '4-10', '11-30', '31-100', '100+']
            )
            
            group_stats = pd.DataFrame({
                'Группа': city_groups,
                'Города': 1,
                'Выручка': city_stats['Total_Revenue']
            }).groupby('Группа', observed=False).agg({
                'Города': 'count',
                'Выручка': 'sum'
            })
            
            if len(group_stats) > 0:
                group_stats['Доля выручки'] = (group_stats['Выручка'] / group_stats['Выручка'].sum() * 100).round(1)
                group_stats['Выручка на город'] = (group_stats['Выручка'] / group_stats['Города']).astype(int)
                
                fig_groups = px.bar(
                    group_stats.reset_index(),
                    x='Группа',
                    y='Города',
                    color='Доля выручки',
                    text='Города',
                    title='Распределение городов по объему сделок',
                    color_continuous_scale='RdYlGn',
                    height=400
                )
                fig_groups.update_traces(textposition='outside')
                st.plotly_chart(fig_groups, use_container_width=True)
        
        with col2:
            # Лидерство источников в городах
            source_leadership = city_stats['Top_Source'].value_counts().head(5).reset_index()
            source_leadership.columns = ['Источник', 'Городов']
            source_leadership['Доля'] = (source_leadership['Городов'] / len(city_stats) * 100).round(1)
            
            fig_sources = px.bar(
                source_leadership,
                x='Источник',
                y='Городов',
                color='Доля',
                text='Городов',
                title='Основной источник трафика в городах',
                labels={'Городов': 'Количество городов'},
                color_continuous_scale='Blues',
                height=400
            )
            fig_sources.update_traces(texttemplate='%{text} городов', textposition='outside')
            fig_sources.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_sources, use_container_width=True)
    else:
        st.warning("Нет данных по городам для анализа")

# ---------- ВКЛАДКА 7: СТАТИСТИКА ----------
with tabs[6]:
    st.markdown('<div class="section-title">ОПИСАТЕЛЬНАЯ СТАТИСТИКА</div>', unsafe_allow_html=True)
    
    # 1. ЧИСЛОВЫЕ ПОЛЯ (как в ячейке 7)
    st.subheader("1. ЧИСЛОВЫЕ ПОЛЯ (среднее, медиана, диапазон)")
    
    numeric_cols = []
    for col in filtered_deals.columns:
        if pd.api.types.is_numeric_dtype(filtered_deals[col]) and filtered_deals[col].notna().any():
            numeric_cols.append(col)
    
    if numeric_cols:
        stats = filtered_deals[numeric_cols].describe().T[['mean', '50%', 'std', 'min', 'max']]
        stats.columns = ['Среднее', 'Медиана', 'Ст.откл', 'Минимум', 'Максимум']
        
        # Форматирование
        formatted_stats = stats.round(2)
        
        # Выделяем важные метрики
        important_metrics = ['revenue', 'Offer Total Amount', 'Initial Amount Paid', 
                            'Months of study', 'Course duration', 'Deal_Age_days']
        
        st.dataframe(
            formatted_stats.style\
                .background_gradient(subset=['Среднее', 'Медиана'], cmap='YlOrBr')\
                .apply(lambda x: ['font-weight: bold' if x.name in important_metrics else '' 
                                 for _ in x], axis=1),
            use_container_width=True
        )
    else:
        st.info("Нет числовых колонок для анализа")
    
    # 2. КАТЕГОРИАЛЬНЫЕ ПОЛЯ (как в ячейке 7)
    st.subheader("2. КАТЕГОРИАЛЬНЫЕ ПОЛЯ (топ-5 значений)")
    
    cat_cols = ['Quality', 'Stage', 'Source', 'Product', 'Education Type', 'City', 'Level of Deutsch']
    cat_cols = [col for col in cat_cols if col in filtered_deals.columns]
    
    if cat_cols:
        for col in cat_cols[:4]:  # Показываем первые 4
            st.write(f"**{col}:**")
            counts = filtered_deals[col].value_counts().head(5)
            
            # Создаем датафрейм для отображения
            counts_df = pd.DataFrame({
                'Значение': counts.index,
                'Количество': counts.values,
                'Доля': (counts.values / len(filtered_deals) * 100).round(1)
            })
            
            st.dataframe(
                counts_df.style.format({'Доля': '{:.1f}%'})\
                    .background_gradient(subset=['Количество'], cmap='Blues'),
                use_container_width=True,
                height=200
            )
    
    # 3. ВРЕМЕННЫЕ ПОЛЯ
    st.subheader("3. ВРЕМЕННЫЕ ПОЛЯ")
    
    date_cols = ['Created Time', 'Closing Date']
    date_cols = [col for col in date_cols if col in filtered_deals.columns]
    
    if date_cols:
        date_stats = []
        for col in date_cols:
            min_date = filtered_deals[col].min()
            max_date = filtered_deals[col].max()
            date_range = max_date - min_date if pd.notna(min_date) and pd.notna(max_date) else None
            
            date_stats.append({
                'Поле': col,
                'Минимум': min_date.strftime('%Y-%m-%d') if pd.notna(min_date) else '—',
                'Максимум': max_date.strftime('%Y-%m-%d') if pd.notna(max_date) else '—',
                'Диапазон': str(date_range).split('.')[0] if date_range else '—'
            })
        
        date_stats_df = pd.DataFrame(date_stats)
        st.dataframe(date_stats_df, use_container_width=True)
    
    # 4. КЛЮЧЕВЫЕ МЕТРИКИ КАК В EXECUTIVE SUMMARY (ячейка 8)
    st.subheader("4. КЛЮЧЕВЫЕ МЕТРИКИ БИЗНЕСА")
    
    # Используем уже рассчитанный summary_df
    if 'summary_df' in locals():
        st.dataframe(
            summary_df[['Metric', 'Formatted']].style.hide(axis='index'),
            use_container_width=True
        )

# ---------- ВКЛАДКА 8: МЕТОДОЛОГИЯ ----------
with tabs[7]:
    st.markdown('<div class="section-title">МЕТОДОЛОГИЯ И A/B ТЕСТИРОВАНИЕ</div>', unsafe_allow_html=True)
    
    # 1. ДЕРЕВО МЕТРИК (ячейка 26)
    st.subheader("1. ДЕРЕВО МЕТРИК БИЗНЕСА")
    
    tree_data = """
**УРОВЕНЬ 1: Ключевой показатель бизнеса**
└── Маржинальная прибыль (CM) — Revenue - AC - COGS

**УРОВЕНЬ 2: Юнит-экономика**
├── UA (User Acquisition) — Уникальные контакты → COUNTUNIQUE(CONTACTS['Id'])
├── C1 (Conversion Rate) — Конверсия в покупателя → B / UA
├── CPA (Cost Per Acquisition) — Стоимость посетителя → AC / UA
├── AOV (Average Order Value) — Средний чек → Revenue / T
├── COGS (Cost of Goods Sold) — Себестоимость (моделируемая)
├── APC (Average Payment Count) — Платежи на клиента → T / B
├── CPC (Cost Per Click) — Стоимость клика → AC / Clicks
└── CTR (Click-Through Rate) — Конверсия в клик → Clicks / Impressions

**УРОВЕНЬ 2.1: Финансовые показатели**
├── Оборот (Revenue) — Сумма поступлений → SUM(DEALS['revenue'])
└── ROMI (Return on Marketing) — Окупаемость рекламы → CM / AC

**УРОВЕНЬ 3: Продуктовые метрики**
├── B (Buyers) — Платящие клиенты → COUNT(DEALS['is_paid'])
├── AC (Advertising Cost) — Расходы на рекламу → SUM(SPEND['Spend'])
├── CAC (Customer Acquisition Cost) — Стоимость клиента → AC / B
├── CLTV (Customer Lifetime Value) — Прибыль с клиента → (AOV - COGS) × APC
├── LTV (Lifetime Value) — Ценность посетителя → CLTV × C1
└── T (Transactions) — Всего транзакций → SUM(DEALS['Transactions'])

**УРОВЕНЬ 4: Атомные метрики (ключевые данные)**
├── DEALS['Created Time'] — Дата создания лида
├── DEALS['Closing Date'] — Дата закрытия сделки
├── DEALS['Source'] / SPEND['Source'] — Источник трафика
├── DEALS['Campaign'] — Кампания
├── DEALS['Product'] — Тип курса
├── DEALS['Stage'] — Стадия воронки
├── DEALS['Quality'] — Качество лида
├── DEALS['City'] — География
├── SPEND['Clicks'] — Клики по рекламе
└── SPEND['Impressions'] — Показы рекламы

**УРОВЕНЬ 5: Ванильные метрики (мониторинг)**
├── DEALS['SLA'] — Время ответа
├── DEALS['Level of Deutsch'] — Уровень языка
├── DEALS['Course duration'] — Длительность курса
├── CALLS['Call Duration (in seconds)'] — Длительность звонков
├── CALLS['Call Type'] — Тип звонка
├── CALLS['Call Status'] — Статус звонка
├── SPEND['AdGroup'] — Группа объявлений
└── SPEND['Ad'] — Конкретное объявление

**КЛЮЧЕВЫЕ ЗАВИСИМОСТИ**
- B = UA × C1 (Клиенты = Посетители × Конверсия)
- Revenue = AOV × T (Оборот = Чек × Транзакции)
- T = B × APC (Транзакции = Клиенты × Частота)
- CAC = AC / B (Стоимость клиента = Реклама / Клиенты)
- CLTV = (AOV - COGS) × APC (Ценность клиента = (Чек - Себестоимость) × Частота)
- LTV = CLTV × C1 (Ценность посетителя = Ценность клиента × Конверсия)
- CM = Revenue - AC - COGS (Маржа = Оборот - Реклама - Себестоимость)
- ROMI = CM / AC (Окупаемость = Маржа / Реклама)

*Прибыль (Profit) не включена — нет данных о постоянных затратах*
    """
    
    st.markdown(tree_data)
    
    # 2. HADI-ЦИКЛЫ И A/B ТЕСТЫ (ячейка 27)
    st.subheader("2. HADI-ЦИКЛЫ И A/B ТЕСТИРОВАНИЕ")
    
    # Основные продукты для анализа
    main_products = ["digital marketing", "ux/ui design", "web developer"]
    
    # Подготовка данных
    if 'created_date' not in contacts.columns:
        contacts['created_date'] = pd.to_datetime(contacts['Created Time']).dt.date
    
    TOTAL_UA = contacts['Id'].nunique()
    active_students_df = filtered_deals[filtered_deals['stage_normalized'] == 'Active Student']
    buyers_per_product = active_students_df.groupby('Product')['Contact Name'].nunique()
    c1_per_product = buyers_per_product / TOTAL_UA if TOTAL_UA > 0 else 0
    
    product_stats = pd.DataFrame({
        "Продукт": buyers_per_product.index,
        "B (Покупатели)": buyers_per_product.values,
        "UA (Общий трафик)": TOTAL_UA,
        "C1 (Конверсия)": c1_per_product.values
    })
    product_stats = product_stats[product_stats["Продукт"].isin(main_products)]
    
    if len(product_stats) > 0:
        st.write("**Базовые метрики для A/B тестов:**")
        st.dataframe(
            product_stats.style.format({
                'B (Покупатели)': '{:,.0f}',
                'UA (Общий трафик)': '{:,.0f}',
                'C1 (Конверсия)': '{:.2%}'
            }),
            use_container_width=True
        )
        
        # Гипотезы для A/B тестов
        hypotheses = [
            ("HADI-1. Уведомление менеджера", 
             "Внедрение автоматического уведомления менеджера при поступлении заявки и обязательный первый звонок в течение 1 часа"),
            ("HADI-2. Автоматическая отправка материалов", 
             "Автоматическая отправка email с программой курса и видео-отзывом выпускника в течение 5 минут после заявки"),
            ("HADI-3. SMS-напоминание", 
             "Отправка SMS-напоминания о записи на курс через 1 час после пропущенного звонка менеджера")
        ]
        
        st.write("**Готовые HADI-циклы для тестирования:**")
        
        for hyp_name, hyp_text in hypotheses:
            with st.expander(f"{hyp_name}"):
                st.write(f"**Гипотеза:** {hyp_text}")
                st.write("**HADI-цикл:**")
                
                hadi_df = pd.DataFrame({
                    "Этап": ["Hypothesis (H)", "Action (A)", "Data (D)", "Insight (I)"],
                    "Формулировка": [
                        f"{hyp_text}. Ожидаемый рост конверсии на 10%.",
                        "Настроить процесс согласно гипотезе для тестовой группы (50%). Контрольная группа — текущий процесс.",
                        "Срок теста — 2 недели. Сравниваются две группы лидов. Метрика — конверсия (C1). Цель — прирост ≥ 10%.",
                        "Гипотеза подтверждается, если прирост конверсии ≥ целевого уровня и результат статистически значим."
                    ]
                })
                
                st.table(hadi_df)
                
                abtest_df = pd.DataFrame({
                    "Параметр": [
                        "Гипотеза",
                        "Нулевая гипотеза",
                        "Условия проведения A-теста",
                        "Условия проведения B-теста",
                        "Метрика для отслеживания",
                        "Граница подтверждения гипотезы",
                        "Уровень значимости"
                    ],
                    "Описание": [
                        f"{hyp_text} увеличит конверсию (C1) на 10%.",
                        "Нет различий: C1_B ≤ C1_A.",
                        "Группа A — текущий процесс. Случайное распределение 50% новых лидов. Длительность: 14 дней.",
                        f"Группа B — {hyp_text}. Случайное распределение 50% новых лидов. Длительность: 14 дней.",
                        "Основная: C1 (оплаты / лиды). Дополнительные: TTFC, дозвоны, CPA.",
                        "C1_B ≥ C1_A × 1.10 и различие статистически значимо.",
                        "α = 0.05"
                    ]
                })
                
                st.table(abtest_df)

# ---------- ВКЛАДКА 9: ДАННЫЕ ----------
with tabs[8]:
    st.markdown('<div class="section-title">ПОЛНЫЕ ДАННЫЕ</div>', unsafe_allow_html=True)
    
    dataset = st.selectbox("Выберите таблицу", ["Deals (фильтрованные)", "Spend", "Contacts", "Deals (полные)"])
    
    if dataset == "Deals (фильтрованные)":
        df = filtered_deals
        st.info(f"Отображено: {len(filtered_deals):,} из {len(deals):,} сделок (применены фильтры)")
    elif dataset == "Deals (полные)":
        df = deals
        st.info(f"Все сделки: {len(deals):,} записей")
    elif dataset == "Spend":
        df = spend
    else:
        df = contacts
    
    # Показываем данные
    st.dataframe(df, use_container_width=True, height=500)
    
    # Экспорт
    col1, col2 = st.columns(2)
    with col1:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Скачать CSV",
            data=csv,
            file_name=f"{dataset.lower().replace(' ', '_').replace('(', '').replace(')', '')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    with col2:
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Data')
        excel_buffer.seek(0)
        st.download_button(
            "📊 Скачать Excel",
            data=excel_buffer,
            file_name=f"{dataset.lower().replace(' ', '_').replace('(', '').replace(')', '')}.xlsx",
            mime="application/vnd.ms-excel",
            use_container_width=True
        )
    
    # Статистика по данным
    st.subheader("Статистика по данным")
    
    stats_data = {
        'Метрика': ['Строк', 'Столбцов', 'Пропусков', 'Заполненность'],
        'Значение': [
            len(df),
            len(df.columns),
            df.isnull().sum().sum(),
            f"{(1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100:.1f}%"
        ]
    }
    
    stats_df = pd.DataFrame(stats_data)
    st.dataframe(stats_df, use_container_width=True)

# ========== ФУТЕР ==========
st.markdown("---")
st.markdown(f"""
**Отчет создан:** {datetime.now().strftime('%d.%m.%Y %H:%M')}  
**Период данных:** {min_date} – {max_date}  
**Версия дэшборда:** 2.0 (полная интеграция анализа из Jupyter Notebook)
""")

# ========== ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ ==========
def check_data_quality():
    """Проверка качества данных (для отладки)"""
    issues = []
    
    # Проверка дубликатов
    if deals['Id'].duplicated().any():
        issues.append(f"Дубликаты ID в deals: {deals['Id'].duplicated().sum()}")
    
    # Проверка пропусков в ключевых полях
    key_fields = ['Created Time', 'Product', 'Source']
    for field in key_fields:
        if field in deals.columns:
            null_count = deals[field].isnull().sum()
            if null_count > 0:
                issues.append(f"Пропуски в {field}: {null_count}")
    
    return issues

# Скрытая панель для отладки (раскомментировать при необходимости)
# with st.sidebar.expander("Отладка"):
#     if st.button("Проверить качество данных"):
#         issues = check_data_quality()
#         if issues:
#             for issue in issues:
#                 st.warning(issue)
#         else:
#             st.success("Качество данных в порядке")