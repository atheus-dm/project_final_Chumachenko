import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import io
import warnings
from statsmodels.stats.power import NormalIndPower
warnings.filterwarnings('ignore')

st.set_page_config(page_title="IT School Analytics", layout="wide", initial_sidebar_state="expanded")

if 'language' not in st.session_state:
    st.session_state.language = 'RU'

TRANSLATIONS = {
    'RU': {
        'main_title': 'ПОЛНЫЙ АНАЛИТИЧЕСКИЙ ОТЧЕТ IT ШКОЛЫ',
        'summary_metrics': 'СВОДНЫЕ ПОКАЗАТЕЛИ БИЗНЕСА',
        'marketing': 'МАРКЕТИНГ',
        'sales': 'ПРОДАЖИ',
        'products': 'ПРОДУКТЫ',
        'geography': 'ГЕОГРАФИЯ/ЯЗЫКИ',
        'unit_economics': 'ЮНИТ-ЭКОНОМИКА',
        'growth_points': 'ТОЧКИ РОСТА',
        'metrics_tree': 'ДЕРЕВО МЕТРИК И A/B ТЕСТЫ',
        'revenue': 'Выручка',
        'margin': 'Маржа',
        'romi': 'ROMI',
        'ltv': 'LTV',
        'conversion_c1': 'Конверсия C1',
        'marketing_spend': 'Маркетинг расходы',
        'ua': 'UA',
        'successful_deals': 'Успешные сделки',
        'unique_clients': 'Уникальные клиенты',
        'aov_per_transaction': 'AOV на транзакцию',
        'aov_per_client': 'AOV на клиента',
        'traffic_sources': 'Источники трафика',
        'cities': 'Города',
        'managers': 'Менеджеры',
        'products_count': 'Продукты',
        'top_product': 'Топ продукт',
        'data_period': 'Период данных',
        'no_data': 'Нет данных для отображения',
        'switch_to_german': 'Немецкий',
        'switch_to_russian': 'Русский',
        'currency': '€',
        'percent': '%',
        'days': 'дн',
        'scenario': 'Сценарий',
        'product': 'Продукт',
        'city': 'Город',
        'source': 'Источник',
        'manager': 'Менеджер',
        'metric': 'Метрика',
        'value': 'Значение',
        'unit': 'Ед. изм.',
        'about_dashboard': 'О дашборде',
        'about_dashboard_text': 'Полный аналитический отчет IT-школы',
        'current_language': 'Текущий язык',
        'marketing_funnel': 'Маркетинговая воронка',
        'conversion_funnel_by_channels': 'Воронка конверсии по каналам',
        'result_cost': 'Стоимость результата',
        'marketing_analytics': 'Маркетинговая аналитика',
        'source_analysis': 'Анализ платных источников',
        'cpc_vs_conversion': 'CPC vs Конверсия',
        'cpc_vs_conversion_title': 'CPC vs Конверсия',
        'cpc': 'Цена за клик',
        'conversion': 'Конверсия',
        'clicks': 'Клики',
        'leads': 'Лиды',
        'students': 'Студенты',
        'spend': 'Расходы',
        'impressions': 'Показы',
        'paid_sources': 'Платные источники',
        'quality_leads': 'Качественные лиды',
        'analysis_dynamics': 'Анализ динамики',
        'leads_trend': 'Динамика лидов, звонков и продаж',
        'incoming_leads': 'Входящие Лиды',
        'sales_scaled': 'Продажи',
        'calls': 'Звонки',
        'impact_calls_on_sales': 'Влияние звонков на продажи',
        'calls_count': 'Количество Звонков',
        'sales_count': 'Количество Продаж',
        'deal_closing_speed': 'Скорость закрытия сделок',
        'deal_duration_distribution': 'Распределение времени закрытия сделок',
        'deal_duration_days': 'Продолжительность сделки (дни)',
        'deal_count': 'Кол-во сделок',
        'median': 'Медиана',
        'mean': 'Среднее',
        'closing_speed_by_managers': 'Скорость закрытия по менеджерам',
        'not_enough_data': 'Недостаточно данных',
        'top_managers_revenue_conversion': 'Топ менеджеров по выручке и конверсии',
        'top_15_managers_revenue': 'ТОП-15 Менеджеров по Выручке',
        'top_conversion': 'ТОП по конверсии',
        'sla_analysis': 'Анализ скорости ответа (SLA)',
        'response_speed_vs_conversion': 'Скорость ответа vs Конверсия',
        'median_response_time_hours': 'Медианное время ответа (часы)',
        'product_metrics': 'Полные метрики по продуктам',
        'product_efficiency_visualizations': 'Визуализации эффективности продуктов',
        'revenue_by_products': 'Выручка по продуктам',
        'product_matrix': 'Матрица продуктов: Клиенты vs Средний чек',
        'client_count': 'Количество клиентов',
        'average_check': 'Средний чек',
        'payment_type_analysis': 'Анализ типов оплаты',
        'payment_type_distribution': 'Распределение типов оплата по продуктам',
        'deal_count_2': 'Количество сделок',
        'education_type_analysis': 'Анализ типов обучения',
        'revenue_by_education_type': 'Выручка по типам обучения',
        'sales_map': 'Карта продаж',
        'top_cities_revenue': 'Топ городов по выручке',
        'city_efficiency_analysis': 'Анализ эффективности по городам',
        'top_cities_conversion': 'Топ городов по конверсии',
        'german_level_analysis': 'Анализ уровней немецкого языка',
        'conversion_by_german_level': 'Конверсия по уровням немецкого языка',
        'german_level': 'Уровень',
        'revenue_by_level': 'Выручка по уровням',
        'avg_revenue_per_student': 'Средняя выручка на студента',
        'no_city_data': 'Нет данных по городам для анализа',
        'no_successful_deals': 'Нет успешных сделок для анализа продуктов',
        'business_analysis': 'Анализ всего бизнеса',
        'growth_scenarios_total_business': 'Сценарии роста для всего бизнеса',
        'best_scenarios': 'Наилучшие сценарии',
        'growth_scenario': 'Сценарий роста',
        'profit_growth': 'Прирост CM',
        'action': 'Действие',
        'business_metrics_tree': 'Дерево метрик бизнеса',
        'level_1': 'УРОВЕНЬ 1: Ключевой показатель бизнеса',
        'level_2': 'УРОВЕНЬ 2: Юнит-экономика',
        'level_2_1': 'УРОВЕНЬ 2.1: Финансовые показатели',
        'level_3': 'УРОВЕНЬ 3: Продуктовые метрики',
        'level_4': 'УРОВЕНЬ 4: Атомные метрики',
        'key_dependencies': 'КЛЮЧЕВЫЕ ЗАВИСИМОСТИ',
        'hadi_cycles_ab_testing': 'HADI-циклы и A/B тестирование',
        'base_metrics_ab_tests': 'Базовые метрики для A/B тестов',
        'ready_hadi_cycles': 'Готовые HADI-циклы для тестирования',
        'hypothesis': 'Гипотеза',
        'hadi_cycle': 'HADI-цикл',
        'stage': 'Этап',
        'formulation': 'Формулировка',
        'ab_test_parameters': 'Расчет параметров A/B тестов',
        'avg_leads_per_day': 'Средний приток лидов в день (на одну группу)',
        'legend': 'Легенда',
        'test_feasible': 'тест реализуем в стандартном 2-недельном цикле',
        'extended_test_needed': 'требуется продленный тест или увеличение трафика',
        'test_difficult': 'проверка гипотезы затруднена при текущем трафике',
        'channels_scaling': 'Масштабирование каналов',
        'funnel_optimization': 'Оптимизация воронки',
        'upsell_prices': 'Up-sell и цены',
        'retention_loyalty': 'Удержание и лояльность',
        'ad_optimization': 'Оптимизация рекламы',
        'total_business': 'TOTAL BUSINESS',
        'product_economics': 'ЭКОНОМИКА ПО ПРОДУКТАМ',
        'total_business_economics': 'ЭКОНОМИКА ВСЕГО БИЗНЕСА',
        'footer': 'Analytics Dashboard • Built by Dmitriy Chumachenko',
        'avg_sla': 'Ср.SLA',
        'avg_conversion': 'Ср.конверсия',
        'months': 'мес',
        'city_name': 'Название города',
        'total_deals': 'Всего сделок',
        'active_students': 'Активные студенты',
        'total_revenue': 'Общая выручка',
        'top_source': 'Топ источник',
        'win_rate': 'Win Rate',
        'german_level_2': 'Уровень немецкого',
        'total_deals_2': 'Всего сделок',
        'avg_revenue_per_student_2': 'Средняя выручка на студента',
        'minimum': 'Минимум',
        'maximum': 'Максимум',
        'count': 'Количество',
        'average': 'Среднее',
        'sales_2': 'Продажи',
        'avg_check_2': 'Средний чек',
        'median_deal_age_days': 'Медиана возраста сделки (дни)',
        'avg_calls_per_deal': 'Среднее звонков на сделку',
        'deal_age_hours': 'Возраст сделки (часы)',
        'win_rate_pct': 'Конверсия %',
        'avg_response_time': 'Среднее время ответа',
        'manager_name': 'Менеджер',
        'deals_count': 'Количество сделок',
        'avg_contract': 'Средний контракт',
        'total_contract': 'Общий контракт',
        'collection_ratio': 'Коэффициент сбора',
        'revenue_per_student': 'Выручка на студента',
        'education_type': 'Тип обучения',
        'level': 'Уровень',
        'avg_initial': 'Средний начальный платеж',
        'transactions': 'Транзакции',
        'ac': 'Рекламные расходы',
        'cpa': 'CPA',
        'cac': 'CAC',
        'cogs_per_t': 'COGS на транзакцию',
        'cm': 'Маржинальная прибыль',
        'apc': 'APC',
        'cltv': 'CLTV',
        'ltv_2': 'LTV',
        'cm_growth': 'Рост CM',
        'ua_count': 'Количество UA',
        'b_count': 'Количество B',
        't_count': 'Количество T',
        'daily_leads': 'Лидов в день',
        'test_days': 'Дней для теста',
        'target_effect': 'Целевой эффект',
        'base_c1': 'Базовый C1',
        'leads_per_group': 'Лидов на группу',
        'leads_per_day_group': 'Лидов/день (группа)',
        'test_days_2': 'Дней для теста',
        'product_name': 'Название продукта',
        'buyers': 'Покупатели',
        'total_traffic': 'Общий трафик',
    },
    'DE': {
        'main_title': 'VOLLSTÄNDIGER ANALYTIKBERICHT DER IT-SCHULE',
        'summary_metrics': 'ZUSAMMENFASSENDE GESCHÄFTSKENNZAHLEN',
        'marketing': 'MARKETING',
        'sales': 'VERTRIEB',
        'products': 'PRODUKTE',
        'geography': 'GEOGRAFIE/SPRACHEN',
        'unit_economics': 'UNIT-ECONOMICS',
        'growth_points': 'WACHSTUMSHEBEL',
        'metrics_tree': 'KENNZAHLENBAUM UND A/B-TESTS',
        'revenue': 'Umsatz',
        'margin': 'Marge',
        'romi': 'ROMI',
        'ltv': 'LTV',
        'conversion_c1': 'Konversion C1',
        'marketing_spend': 'Marketingausgaben',
        'ua': 'UA',
        'successful_deals': 'Erfolgreiche Deals',
        'unique_clients': 'Eindeutige Kunden',
        'aov_per_transaction': 'AOV pro Transaktion',
        'aov_per_client': 'AOV pro Kunde',
        'traffic_sources': 'Trafficquellen',
        'cities': 'Städte',
        'managers': 'Manager',
        'products_count': 'Produkte',
        'top_product': 'Top-Produkt',
        'data_period': 'Datenzeitraum',
        'no_data': 'Keine Daten zur Anzeige',
        'switch_to_german': 'Deutsch',
        'switch_to_russian': 'Russisch',
        'currency': '€',
        'percent': '%',
        'days': 'Tage',
        'scenario': 'Szenario',
        'product': 'Produkt',
        'city': 'Stadt',
        'source': 'Quelle',
        'manager': 'Manager',
        'metric': 'Kennzahl',
        'value': 'Wert',
        'unit': 'Einheit',
        'about_dashboard': 'Über das Dashboard',
        'about_dashboard_text': 'Vollständiger Analytikbericht der IT-Schule',
        'current_language': 'Aktuelle Sprache',
        'marketing_funnel': 'Marketing-Trichter',
        'conversion_funnel_by_channels': 'Konversionstrichter nach Kanälen',
        'result_cost': 'Kosten des Ergebnisses',
        'marketing_analytics': 'Marketing-Analytik',
        'source_analysis': 'Analyse kostenpflichtiger Quellen',
        'cpc_vs_conversion': 'CPC vs Konversion',
        'cpc_vs_conversion_title': 'CPC vs Konversion',
        'cpc': 'Kosten pro Klick',
        'conversion': 'Konversion',
        'clicks': 'Klicks',
        'leads': 'Leads',
        'students': 'Studenten',
        'spend': 'Ausgaben',
        'impressions': 'Impressionen',
        'paid_sources': 'Bezahlte Quellen',
        'quality_leads': 'Qualitäts-Leads',
        'analysis_dynamics': 'Analyse der Dynamik',
        'leads_trend': 'Trend von Leads, Anrufen und Verkäufen',
        'incoming_leads': 'Eingehende Leads',
        'sales_scaled': 'Verkäufe',
        'calls': 'Anrufe',
        'impact_calls_on_sales': 'Einfluss von Anrufen auf Verkäufe',
        'calls_count': 'Anzahl der Anrufe',
        'sales_count': 'Anzahl der Verkäufe',
        'deal_closing_speed': 'Geschwindigkeit des Deal-Abschlusses',
        'deal_duration_distribution': 'Verteilung der Deal-Abschlusszeit',
        'deal_duration_days': 'Deal-Dauer (Tage)',
        'deal_count': 'Anzahl der Deals',
        'median': 'Median',
        'mean': 'Durchschnitt',
        'closing_speed_by_managers': 'Abschlussgeschwindigkeit nach Managern',
        'not_enough_data': 'Nicht genügend Daten',
        'top_managers_revenue_conversion': 'Top Manager nach Umsatz und Konversion',
        'top_15_managers_revenue': 'TOP-15 Manager nach Umsatz',
        'top_conversion': 'TOP nach Konversion',
        'sla_analysis': 'Analyse der Antwortgeschwindigkeit (SLA)',
        'response_speed_vs_conversion': 'Antwortgeschwindigkeit vs Konversion',
        'median_response_time_hours': 'Median Antwortzeit (Stunden)',
        'product_metrics': 'Vollständige Produktkennzahlen',
        'product_efficiency_visualizations': 'Visualisierungen der Produkteffizienz',
        'revenue_by_products': 'Umsatz nach Produkten',
        'product_matrix': 'Produktmatrix: Kunden vs Durchschnittsscheck',
        'client_count': 'Anzahl der Kunden',
        'average_check': 'Durchschnittsscheck',
        'payment_type_analysis': 'Analyse der Zahlungsarten',
        'payment_type_distribution': 'Verteilung der Zahlungsarten nach Produkten',
        'deal_count_2': 'Anzahl der Deals',
        'education_type_analysis': 'Analyse der Ausbildungstypen',
        'revenue_by_education_type': 'Umsatz nach Ausbildungstypen',
        'sales_map': 'Verkaufskarte',
        'top_cities_revenue': 'Top Städte nach Umsatz',
        'city_efficiency_analysis': 'Analyse der Stadteffizienz',
        'top_cities_conversion': 'Top Städte nach Konversion',
        'german_level_analysis': 'Analyse der Deutschkenntnisse',
        'conversion_by_german_level': 'Konversion nach Deutschlevel',
        'german_level': 'Level',
        'revenue_by_level': 'Umsatz nach Level',
        'avg_revenue_per_student': 'Durchschnittsumsatz pro Student',
        'no_city_data': 'Keine Stadtdaten für Analyse verfügbar',
        'no_successful_deals': 'Keine erfolgreichen Deals für Produktanalyse',
        'business_analysis': 'Gesamtgeschäftsanalyse',
        'growth_scenarios_total_business': 'Wachstumsszenarien für das Gesamtgeschäft',
        'best_scenarios': 'Beste Szenarien',
        'growth_scenario': 'Wachstumsszenario',
        'profit_growth': 'CM-Wachstum',
        'action': 'Aktion',
        'business_metrics_tree': 'Geschäftskennzahlenbaum',
        'level_1': 'EBENE 1: Hauptgeschäftskennzahl',
        'level_2': 'EBENE 2: Unit-Economics',
        'level_2_1': 'EBENE 2.1: Finanzkennzahlen',
        'level_3': 'EBENE 3: Produktkennzahlen',
        'level_4': 'EBENE 4: Atomare Kennzahlen',
        'key_dependencies': 'SCHLÜSSELABHÄNGIGKEITEN',
        'hadi_cycles_ab_testing': 'HADI-Zyklen und A/B-Tests',
        'base_metrics_ab_tests': 'Basis-Kennzahlen für A/B-Tests',
        'ready_hadi_cycles': 'Fertige HADI-Zyklen zum Testen',
        'hypothesis': 'Hypothese',
        'hadi_cycle': 'HADI-Zyklus',
        'stage': 'Stufe',
        'formulation': 'Formulierung',
        'ab_test_parameters': 'Berechnung der A/B-Test-Parameter',
        'avg_leads_per_day': 'Durchschnittlicher Lead-Zufluss pro Tag (pro Gruppe)',
        'legend': 'Legende',
        'test_feasible': 'Test im standardmäßigen 2-wöchigen Zyklus durchführbar',
        'extended_test_needed': 'verlängerter Test oder mehr Traffic benötigt',
        'test_difficult': 'Hypothesentest bei aktuellem Traffic schwierig',
        'channels_scaling': 'Kanal-Skalierung',
        'funnel_optimization': 'Trichter-Optimierung',
        'upsell_prices': 'Up-Sell und Preise',
        'retention_loyalty': 'Kundenbindung und Loyalität',
        'ad_optimization': 'Werbeoptimierung',
        'total_business': 'GESAMTGESCHÄFT',
        'product_economics': 'ÖKONOMIE NACH PRODUKTEN',
        'total_business_economics': 'ÖKONOMIE DES GESAMTEN GESCHÄFTS',
        'footer': 'Analytics Dashboard • Erstellt von Dmitriy Chumachenko',
        'avg_sla': 'Durchschn. SLA',
        'avg_conversion': 'Durchschn. Konversion',
        'months': 'Monate',
        'city_name': 'Stadtname',
        'total_deals': 'Gesamt Deals',
        'active_students': 'Aktive Studenten',
        'total_revenue': 'Gesamtumsatz',
        'top_source': 'Top Quelle',
        'win_rate': 'Gewinnrate',
        'german_level_2': 'Deutschlevel',
        'total_deals_2': 'Gesamt Deals',
        'avg_revenue_per_student_2': 'Durchschnittsumsatz pro Student',
        'minimum': 'Minimum',
        'maximum': 'Maximum',
        'count': 'Anzahl',
        'average': 'Durchschnitt',
        'sales_2': 'Verkäufe',
        'avg_check_2': 'Durchschnittsscheck',
        'median_deal_age_days': 'Median Deal-Alter (Tage)',
        'avg_calls_per_deal': 'Durchschn. Anrufe pro Deal',
        'deal_age_hours': 'Deal-Alter (Stunden)',
        'win_rate_pct': 'Konversion %',
        'avg_response_time': 'Durchschnittliche Antwortzeit',
        'manager_name': 'Manager',
        'deals_count': 'Anzahl Deals',
        'avg_contract': 'Durchschnittsvertrag',
        'total_contract': 'Gesamtvertrag',
        'collection_ratio': 'Einzugsquote',
        'revenue_per_student': 'Umsatz pro Student',
        'education_type': 'Ausbildungstyp',
        'level': 'Level',
        'avg_initial': 'Durchschnittliche Anfangszahlung',
        'transactions': 'Transaktionen',
        'ac': 'Werbekosten',
        'cpa': 'CPA',
        'cac': 'CAC',
        'cogs_per_t': 'COGS pro Transaktion',
        'cm': 'Deckungsbeitrag',
        'apc': 'APC',
        'cltv': 'CLTV',
        'ltv_2': 'LTV',
        'cm_growth': 'CM-Wachstum',
        'ua_count': 'UA-Anzahl',
        'b_count': 'B-Anzahl',
        't_count': 'T-Anzahl',
        'daily_leads': 'Leads pro Tag',
        'test_days': 'Testtage',
        'target_effect': 'Zieleffekt',
        'base_c1': 'Basis C1',
        'leads_per_group': 'Leads pro Gruppe',
        'leads_per_day_group': 'Leads/Tag (Gruppe)',
        'test_days_2': 'Testtage',
        'product_name': 'Produktname',
        'buyers': 'Käufer',
        'total_traffic': 'Gesamttraffic',
    }
}

def t(key):
    return TRANSLATIONS[st.session_state.language].get(key, key)

st.markdown("""
<style>
    .main-title {font-size: 2rem; color: #1E3A8A; font-weight: 700; margin-bottom: 0.5rem;}
    .section-title {font-size: 1.3rem; color: #374151; font-weight: 600; margin-top: 1.5rem; padding-bottom: 0.3rem; border-bottom: 2px solid #3B82F6;}
    .metric-box {
        background: #f8fafc; 
        padding: 1rem; 
        border-radius: 0.5rem; 
        margin: 0.3rem 0; 
        border: 1px solid #e5e7eb;
        color: #000000 !important;
        font-weight: 600;
    }
    div[data-testid="stMetric"] {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    div[data-testid="stMetricValue"] {
        background-color: transparent !important;
        color: #000000 !important;
        font-weight: 700 !important;
    }
    div[data-testid="stMetricLabel"] {
        background-color: transparent !important;
        color: #374151 !important;
    }
    div[data-testid="stMetricDelta"] {
        background-color: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600, show_spinner=False)
def load_data():
    deals = pd.read_parquet('deals_clean.parquet')
    spend = pd.read_parquet('spend_clean.parquet')
    contacts = pd.read_parquet('contacts_clean.parquet')
    calls = pd.read_parquet('calls_clean.parquet')
    
    for col in ['Created Time', 'Closing Date']:
        if col in deals.columns:
            deals[col] = pd.to_datetime(deals[col], errors='coerce')
    
    td_cols = deals.select_dtypes(include=['timedelta64[ns]']).columns
    for col in td_cols:
        deals[f'{col}_seconds'] = deals[col].dt.total_seconds()
    
    return deals, spend, contacts, calls

deals, spend, contacts, calls = load_data()

COORD_DB = {
    'Berlin': (52.5200, 13.4050), 'München': (48.1351, 11.5820), 'Hamburg': (53.5511, 9.9937),
    'Köln': (50.9375, 6.9603), 'Frankfurt': (50.1109, 8.6821), 'Leipzig': (51.3397, 12.3731),
    'Düsseldorf': (51.2277, 6.7735), 'Dortmund': (51.5136, 7.4653), 'Essen': (51.4556, 7.0116),
    'Bremen': (53.0793, 8.8017), 'Dresden': (51.0504, 13.7373), 'Hannover': (52.3759, 9.7320),
    'Nürnberg': (49.4521, 11.0767), 'Duisburg': (51.4344, 6.7623), 'Bochum': (51.4818, 7.2162),
    'Wuppertal': (51.2562, 7.1508), 'Bielefeld': (52.0302, 8.5325), 'Bonn': (50.7374, 7.0982),
    'Münster': (51.9607, 7.6261), 'Karlsruhe': (49.0069, 8.4037), 'Mannheim': (49.4875, 8.4660),
    'Augsburg': (48.3705, 10.8978), 'Wiesbaden': (50.0826, 8.2493), 'Gelsenkirchen': (51.5177, 7.0857),
}

def geocode_city(city_name):
    if pd.isna(city_name):
        return None
    
    city_clean = str(city_name).strip()
    
    for db_city, coords in COORD_DB.items():
        if db_city.lower() in city_clean.lower() or city_clean.lower() in db_city.lower():
            return coords
    
    return None

def prepare_geodata(city_stats):
    top_cities = city_stats.head(50).copy()
    
    coordinates = []
    for city in top_cities[t('city')]:
        coords = geocode_city(city)
        coordinates.append(coords)
    
    top_cities[['lat', 'lon']] = pd.DataFrame(coordinates, index=top_cities.index, columns=['lat', 'lon'])
    geocoded = top_cities.dropna(subset=['lat', 'lon'])
    
    return geocoded

min_date = deals['Created Time'].min().date()
max_date = deals['Created Time'].max().date()

with st.sidebar:
    st.markdown(f"### {t('current_language')} / Sprache")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(t('switch_to_german')):
            st.session_state.language = 'DE'
            st.rerun()
    with col2:
        if st.button(t('switch_to_russian')):
            st.session_state.language = 'RU'
            st.rerun()
    
    current_lang = "Deutsch" if st.session_state.language == 'DE' else "Русский"
    st.markdown(f"**{t('current_language')}:** {current_lang}")
    st.markdown("---")
    
    st.markdown(f"### {t('about_dashboard')}")
    st.markdown(f"{t('about_dashboard_text')}")

def calculate_business_metrics():
    TOTAL_UA = contacts['Id'].nunique()
    total_marketing_spend = spend['Spend'].sum()
    
    active_students_df = deals[deals['stage_normalized'] == 'Active Student']
    TOTAL_B_CORRECT = active_students_df['Contact Name'].nunique() if len(active_students_df) > 0 else 0
    successful_deals_count = len(active_students_df)
    
    deals_calc = deals.copy()
    if 'Payment_Type_Recovered' in deals_calc.columns:
        deals_calc['Transactions'] = np.where(
            deals_calc['Payment_Type_Recovered'] == 'one payment',
            1,
            deals_calc.get('Months of study', pd.Series(index=deals_calc.index, dtype='float')).fillna(1)
        )
    else:
        deals_calc['Transactions'] = deals_calc.get('Months of study', pd.Series(index=deals_calc.index, data=1))
    
    deals_calc.loc[deals_calc['stage_normalized'] != 'Active Student', 'Transactions'] = 0
    active_students_calc = deals_calc[deals_calc['stage_normalized'] == 'Active Student']
    
    total_revenue = 0
    avg_check = 0
    avg_check_per_client = 0
    win_rate_vacuum = 0
    margin = -total_marketing_spend
    romi = -100
    median_deal_age = 0
    top_product_name = "N/A"
    ltv_vacuum_business = 0
    
    if len(active_students_df) > 0:
        total_revenue = active_students_df['revenue'].sum()
        
        total_t = active_students_calc['Transactions'].sum() if len(active_students_calc) > 0 else 0
        avg_check = total_revenue / total_t if total_t > 0 else 0
        
        avg_check_per_client = total_revenue / TOTAL_B_CORRECT if TOTAL_B_CORRECT > 0 else 0
        
        win_rate_vacuum = (TOTAL_B_CORRECT / TOTAL_UA * 100) if TOTAL_UA > 0 else 0
        
        margin = total_revenue - total_marketing_spend
        romi = (margin / total_marketing_spend * 100) if total_marketing_spend > 0 else 0
        
        closed_deals_clean = deals[
            (deals['Id'].isin(active_students_df['Id'].unique())) &
            (deals['Closing Date'].notna()) &
            (deals['Deal_Age_days'].notna()) &
            (deals['Deal_Age_days'] >= 0)
        ].copy()
        if len(closed_deals_clean) > 0:
            median_deal_age = closed_deals_clean['Deal_Age_days'].median()
        
        if len(active_students_calc) > 0:
            product_stats = active_students_calc.groupby('Product').agg({
                'Contact Name': 'nunique',
                'revenue': 'sum',
                'Transactions': 'sum',
            }).reset_index()
            
            product_stats['AOV'] = product_stats['revenue'] / product_stats['Transactions']
            product_stats['APC'] = product_stats['Transactions'] / product_stats['Contact Name']
            COGS_FIXED_PER_TRANS = 0
            COGS_PERCENT_FROM_CHECK = 0.0
            total_cogs = (product_stats['revenue'] * COGS_PERCENT_FROM_CHECK) + (product_stats['Transactions'] * COGS_FIXED_PER_TRANS)
            product_stats['COGS'] = total_cogs / product_stats['Transactions'].replace(0, np.nan)
            product_stats['CLTV'] = (product_stats['AOV'] - product_stats['COGS']) * product_stats['APC']
            product_stats['C1_vacuum'] = product_stats['Contact Name'] / TOTAL_UA if TOTAL_UA > 0 else 0
            product_stats['LTV'] = product_stats['CLTV'] * product_stats['C1_vacuum']
            
            top_product_row = product_stats.sort_values('revenue', ascending=False).head(1)
            top_product_name = top_product_row['Product'].iloc[0] if len(top_product_row) else "N/A"
            
            if product_stats['Contact Name'].sum() > 0:
                cltv_weighted = (product_stats['CLTV'] * product_stats['Contact Name']).sum() / product_stats['Contact Name'].sum()
                ltv_vacuum_business = cltv_weighted * (TOTAL_B_CORRECT / TOTAL_UA) if TOTAL_UA > 0 else 0
    
    summary_rows = [
        (t('revenue'), total_revenue, t('currency')),
        (t('margin'), margin, t('currency')),
        (t('romi'), romi, t('percent')),
        (t('ltv'), ltv_vacuum_business, t('currency')),
        (t('conversion_c1'), win_rate_vacuum, t('percent')),
        (t('marketing_spend'), total_marketing_spend, t('currency')),
        (t('ua'), TOTAL_UA, ''),
        (t('successful_deals'), successful_deals_count, ''),
        (t('unique_clients'), TOTAL_B_CORRECT, ''),
        (t('aov_per_transaction'), avg_check, t('currency')),
        (t('aov_per_client'), avg_check_per_client, t('currency')),
        (t('traffic_sources'), spend['Source'].nunique(), ''),
        (t('cities'), deals['City'].nunique(), ''),
        (t('managers'), deals['Deal Owner Name'].nunique(), ''),
        (t('products_count'), deals['Product'].nunique(), ''),
        (t('top_product'), top_product_name, ''),
    ]

    summary_df = pd.DataFrame(summary_rows, columns=['Metric', 'Value', 'Unit'])
    
    return summary_df, TOTAL_UA, TOTAL_B_CORRECT, total_revenue, total_marketing_spend

summary_df, TOTAL_UA, TOTAL_B, total_revenue, marketing_spend = calculate_business_metrics()

st.markdown(f'<div class="main-title">{t("main_title")}</div>', unsafe_allow_html=True)
st.markdown(f"*{t('data_period')}: {min_date} - {max_date}*")
st.markdown("---")

st.markdown(f'<div class="section-title">{t("summary_metrics")}</div>', unsafe_allow_html=True)

def format_value(val, unit):
    if pd.isna(val):
        return '—'
    if isinstance(val, (pd.Timestamp,)):
        return str(val.date())
    if isinstance(val, str):
        return val
    if unit == t('percent'):
        return f"{val:,.1f}%"
    if unit == t('currency'):
        return f"{val:,.0f} {t('currency')}"
    if unit == t('days'):
        return f"{val:,.0f} {t('days')}"
    return f"{val:,.0f}"

summary_df['Formatted'] = summary_df.apply(lambda r: format_value(r['Value'], r['Unit']), axis=1)

metrics_display = summary_df[['Metric', 'Formatted']].values.tolist()
cols = st.columns(4)
for idx, (label, value) in enumerate(metrics_display):
    with cols[idx % 4]:
        st.markdown(f'<div class="metric-box"><b>{label}</b><br>{value}</div>', unsafe_allow_html=True)

st.markdown("---")

tabs = st.tabs([
    t("marketing"),
    t("sales"),
    t("products"),
    t("geography"),
    t("unit_economics"),
    t("growth_points"),
    t("metrics_tree"),
])

def calculate_unit_economics():
    COGS_FIXED_PER_TRANS = 0       
    COGS_PERCENT_FROM_CHECK = 0.0 
    
    deals_calc = deals.copy()
    deals_calc['Transactions'] = np.where(
        deals_calc['Payment_Type_Recovered'] == 'one payment', 
        1, 
        deals_calc['Months of study'].fillna(1)
    )
    deals_calc.loc[deals_calc['stage_normalized'] != 'Active Student', 'Transactions'] = 0
    
    TOTAL_UA = contacts['Id'].nunique()
    total_marketing_spend = spend['Spend'].sum()
    
    active_students_df = deals_calc[deals_calc['stage_normalized'] == 'Active Student']
    
    if len(active_students_df) == 0:
        return pd.DataFrame(), pd.DataFrame()
    
    TOTAL_B_CORRECT = active_students_df['Contact Name'].nunique()
    
    product_stats = active_students_df.groupby('Product').agg({
        'Contact Name': 'nunique',
        'revenue': 'sum',
        'Transactions': 'sum',
    }).reset_index().rename(columns={
        'Contact Name': 'B', 
        'Transactions': 'T',
        'revenue': 'Revenue'
    })
    
    product_stats['UA'] = TOTAL_UA
    product_stats['C1'] = product_stats['B'] / product_stats['UA']
    product_stats['AC'] = total_marketing_spend
    product_stats['APC'] = product_stats['T'] / product_stats['B']
    product_stats['AOV'] = product_stats['Revenue'] / product_stats['T']
    
    total_cogs_amt = (product_stats['Revenue'] * COGS_PERCENT_FROM_CHECK) + (product_stats['T'] * COGS_FIXED_PER_TRANS)
    product_stats['COGS'] = total_cogs_amt / product_stats['T']
    product_stats['CLTV'] = (product_stats['AOV'] - product_stats['COGS']) * product_stats['APC']
    product_stats['LTV'] = product_stats['CLTV'] * product_stats['C1']
    product_stats['CPA'] = product_stats['AC'] / product_stats['UA']
    product_stats['CAC'] = product_stats['AC'] / product_stats['B']
    product_stats['CM'] = product_stats['Revenue'] - product_stats['AC'] - total_cogs_amt
    product_stats['ROMI'] = (product_stats['CM'] / product_stats['AC']) * 100
    
    total_row = {
        'Product': t('total_business'),
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

with tabs[4]:
    st.markdown(f'<div class="section-title">{t("unit_economics")}</div>', unsafe_allow_html=True)
    
    total_df, product_econ = calculate_unit_economics()
    product_econ = product_econ[product_econ['B'] > 1].copy()
    
    if len(total_df) == 0 or len(product_econ) == 0:
        st.warning(t('no_data'))
    else:
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
        
        st.subheader(t('total_business_economics'))
        st.dataframe(
            format_unit_econ(total_df).background_gradient(subset=['ROMI', 'LTV'], cmap='Greens'),
            use_container_width=True,
            height=150
        )
        
        st.subheader(t('product_economics'))
        st.dataframe(
            format_unit_econ(product_econ).background_gradient(subset=['ROMI', 'LTV'], cmap='RdYlGn'),
            use_container_width=True
        )

with tabs[0]:
    st.markdown(f'<div class="section-title">{t("marketing")}</div>', unsafe_allow_html=True)
    
    students_by_source = deals[deals['stage_normalized'] == 'Active Student'].groupby('Source')['Id'].count().reset_index()
    students_by_source.columns = ['Source', t('students')]
    
    leads_by_source = deals.groupby('Source')['Id'].count().reset_index()
    leads_by_source.columns = ['Source', t('leads')]
    
    quality_filter = ['A - High', 'B - Medium']
    quality_leads_by_source = deals[deals['Quality'].isin(quality_filter)].groupby('Source')['Id'].count().reset_index()
    quality_leads_by_source.columns = ['Source', t('quality_leads')]
    
    revenue_by_source = deals[deals['stage_normalized'] == 'Active Student'].groupby('Source')['revenue'].sum().reset_index()
    revenue_by_source.columns = ['Source', t('revenue')]
    
    spend_by_source = spend.groupby('Source').agg({
        'Spend': 'sum',
        'Clicks': 'sum',
        'Impressions': 'sum'
    }).reset_index()
    
    st.subheader(t('marketing_funnel'))
    
    if 'Source' in spend.columns and 'Source' in deals.columns:
        funnel_df = spend_by_source.merge(leads_by_source, on='Source', how='left')\
                                   .merge(quality_leads_by_source, on='Source', how='left')\
                                   .merge(students_by_source, on='Source', how='left')\
                                   .merge(revenue_by_source, on='Source', how='left').fillna(0)
        
        funnel_df['CPC'] = (funnel_df['Spend'] / funnel_df['Clicks']).replace([np.inf, 0], np.nan).fillna(0).round(2)
        funnel_df['CPL'] = (funnel_df['Spend'] / funnel_df[t('leads')]).replace([np.inf, 0], np.nan).fillna(0).round(2)
        funnel_df['CPS'] = (funnel_df['Spend'] / funnel_df[t('students')]).replace([np.inf, 0], np.nan).fillna(0).round(2)
        funnel_df['CPQ'] = (funnel_df['Spend'] / funnel_df[t('quality_leads')]).replace([np.inf, 0], np.nan).fillna(0).round(2)
        funnel_df['CTR'] = (funnel_df['Clicks'] / funnel_df['Impressions'] * 100).fillna(0).round(2)
        
        top_funnel = funnel_df.sort_values(by='Spend', ascending=False).head(7)
        
        fig1 = make_subplots(
            rows=2, cols=1,
            subplot_titles=(t('conversion_funnel_by_channels'), t('result_cost')),
            vertical_spacing=0.15,
            specs=[[{"type": "bar"}], [{"type": "table"}]]
        )
        
        stages = ['Impressions', 'Clicks', t('leads'), t('students')]
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
        
        fig1.update_yaxes(type="log", title_text=t('count'), row=1, col=1)
        
        fig1.add_trace(
            go.Table(
                header=dict(
                    values=[t('source'), t('spend'), t('clicks'), t('leads'), t('students'), 'CPC', 'CPL', 'CPS'],
                    fill_color="#0235C4",
                    font_color='white',
                    align='left',
                    font_size=12
                ),
                cells=dict(
                    values=[
                        top_funnel['Source'],
                        top_funnel['Spend'].apply(lambda x: f"{x:,.0f}{t('currency')}"),
                        top_funnel['Clicks'].apply(lambda x: f"{x:,.0f}"),
                        top_funnel[t('leads')].apply(lambda x: f"{x:,.0f}"),
                        top_funnel[t('students')].apply(lambda x: f"{x:,.0f}"),
                        top_funnel['CPC'].apply(lambda x: f"{x:.2f}"),
                        top_funnel['CPL'].apply(lambda x: f"{x:.2f}"),
                        top_funnel['CPS'].apply(lambda x: f"{x:.2f}")
                    ],
                    fill_color="#456AD3",
                    font_color='white',
                    align='left',
                    font_size=11
                )
            ),
            row=2, col=1
        )

        fig1.update_layout(height=800, title_text=t('marketing_analytics'), barmode='group')
        st.plotly_chart(fig1, use_container_width=True)
    
    st.subheader(t('source_analysis'))
    
    if 'Source' in spend.columns and 'Source' in deals.columns:
        marketing_deep = spend_by_source.merge(leads_by_source, on='Source', how='left')\
                                        .merge(students_by_source, on='Source', how='left')\
                                        .merge(revenue_by_source, on='Source', how='left').fillna(0)
        
        marketing_deep['CPC'] = (marketing_deep['Spend'] / marketing_deep['Clicks']).replace([np.inf], 0).fillna(0).round(2)
        marketing_deep[t('conversion')] = (marketing_deep[t('students')] / marketing_deep[t('leads')] * 100).fillna(0).round(2)
        marketing_deep['CAC'] = (marketing_deep['Spend'] / marketing_deep[t('students')]).replace([np.inf, 0], np.nan).fillna(0).round(2)
        marketing_deep[t('average_check')] = (marketing_deep[t('revenue')] / marketing_deep[t('students')]).replace([np.inf, 0], np.nan).fillna(0).round(2)
        marketing_deep['ROAS'] = (marketing_deep[t('revenue')] / marketing_deep['Spend'] * 100).replace([np.inf, 0], np.nan).fillna(0).round(2)
        
        paid_marketing = marketing_deep[(marketing_deep['Spend'] > 10)].sort_values(by='Spend', ascending=False).copy()
        
        if len(paid_marketing) > 0:
            fig2 = px.scatter(
                paid_marketing,
                x='CPC',
                y=t('conversion'),
                size='Spend',
                color='Source',
                text='Source',
                title=t('cpc_vs_conversion_title'),
                labels={'CPC': f"{t('cpc')} ({t('currency')})", t('conversion'): f"{t('conversion')} ({t('percent')})"},
                height=500
            )
            fig2.add_vline(x=paid_marketing['CPC'].median(), line_dash="dash", line_color="gray")
            fig2.add_hline(y=paid_marketing[t('conversion')].median(), line_dash="dash", line_color="gray")
            fig2.update_traces(textposition='top center')
            st.plotly_chart(fig2, use_container_width=True)
            
            display_cols = ['Source', 'Spend', t('leads'), t('students'), t('conversion'), 'CAC', t('average_check'), 'ROAS']
            
            st.dataframe(
                paid_marketing[display_cols].sort_values('Spend', ascending=False).style.format({
                    'Spend': '{:,.0f}',
                    t('leads'): '{:,.0f}',
                    t('students'): '{:,.0f}',
                    t('conversion'): '{:.1f}%',
                    'CAC': '{:.0f}',
                    t('average_check'): '{:,.0f}',
                    'ROAS': '{:.0f}%'
                }).background_gradient(subset=[t('conversion'), 'ROAS'], cmap='RdYlGn'),
                use_container_width=True,
                height=300
            )

with tabs[1]:
    st.markdown(f'<div class="section-title">{t("sales")}</div>', unsafe_allow_html=True)
    
    st.subheader(t('analysis_dynamics'))
    
    weekly_deals = deals.set_index('Created Time').resample('W').agg({
        'Id': 'count',
        'stage_normalized': lambda x: (x == 'Active Student').sum()
    }).reset_index()
    weekly_deals.columns = ['Week', 'Leads_Count', 'Success_Count']
    
    weekly_calls = calls.set_index('Call Start Time').resample('W')['Id'].count().reset_index()
    weekly_calls.columns = ['Week', 'Calls_Count']
    
    weekly_stats = weekly_deals.merge(weekly_calls, on='Week', how='inner').fillna(0)
    weekly_stats['Conversion_Rate'] = (weekly_stats['Success_Count'] / weekly_stats['Leads_Count'] * 100).round(1)
    weekly_stats['Calls_Per_Lead'] = (weekly_stats['Calls_Count'] / weekly_stats['Leads_Count']).round(1)
    
    fig_trend = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig_trend.add_trace(
        go.Scatter(
            x=weekly_stats['Week'], 
            y=weekly_stats['Leads_Count'], 
            name=t('incoming_leads'), 
            line=dict(color='blue', width=3),
            fill='tozeroy',
            fillcolor='rgba(0, 0, 255, 0.1)'
        ),
        secondary_y=False,
    )
    
    multiplier = 50
    success_scaled = weekly_stats['Success_Count'] * multiplier
    
    fig_trend.add_trace(
        go.Scatter(
            x=weekly_stats['Week'], 
            y=success_scaled, 
            name=f"{t('sales_scaled')} (×{multiplier})",
            line=dict(color='green', width=3),
            fill='tozeroy',
            fillcolor='rgba(0, 255, 0, 0.3)'
        ),
        secondary_y=True,
    )
    
    fig_trend.add_trace(
        go.Scatter(
            x=weekly_stats['Week'], 
            y=weekly_stats['Calls_Count'], 
            name=t('calls'), 
            line=dict(dash='dot', color='red', width=2)
        ),
        secondary_y=True,
    )
    
    fig_trend.update_yaxes(title_text=t('incoming_leads'), secondary_y=False)
    fig_trend.update_yaxes(title_text=t('calls'), secondary_y=True)
    
    fig_trend.update_layout(
        title_text=t('leads_trend'),
        hovermode="x unified",
        height=450
    )
    
    st.plotly_chart(fig_trend, use_container_width=True)
    
    fig_impact = px.scatter(
        weekly_stats,
        x='Calls_Count',
        y='Success_Count',
        size='Leads_Count',
        color='Conversion_Rate',
        hover_data=['Week', 'Calls_Per_Lead'],
        title=t('impact_calls_on_sales'),
        labels={'Calls_Count': t('calls_count'), 'Success_Count': t('sales_count')},
        color_continuous_scale='Viridis',
        height=400
    )
    fig_impact.add_traces(
        px.scatter(weekly_stats, x='Calls_Count', y='Success_Count', trendline="ols").data[1]
    )
    st.plotly_chart(fig_impact, use_container_width=True)
    
    st.subheader(t('deal_closing_speed'))
    
    active_student_ids = deals[deals['stage_normalized'] == 'Active Student']['Id'].unique()
    closed_deals_clean = deals[
        (deals['Id'].isin(active_student_ids)) & 
        (deals['Closing Date'].notna()) & 
        (deals['Deal_Age_days'].notna()) & 
        (deals['Deal_Age_days'] >= 0)
    ].copy()
    
    if len(closed_deals_clean) > 0:
        mean_age = closed_deals_clean['Deal_Age_days'].mean()
        median_age = closed_deals_clean['Deal_Age_days'].median()
        
        fig = px.histogram(
            closed_deals_clean, 
            x='Deal_Age_days', 
            title=t('deal_duration_distribution'),
            color_discrete_sequence=['#FFA15A'],
            opacity=0.75
        )
        
        fig.update_traces(xbins=dict(start=0, size=5), selector=dict(type='histogram'))
        
        fig.add_vline(
            x=median_age, line_width=2, line_dash="dash", line_color="red",
            annotation_text=f"{t('median')}: {median_age:.1f}", annotation_position="top left"
        )
        fig.add_vline(
            x=mean_age, line_width=2, line_dash="dash", line_color="green",
            annotation_text=f"{t('mean')}: {mean_age:.1f}", annotation_position="top right"
        )
        
        fig.update_xaxes(range=[-1, 120], title_text=t('deal_duration_days'))
        fig.update_layout(
            yaxis_title=t('deal_count'), 
            showlegend=False, 
            bargap=0.1,
            height=550
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        if 'Deal Owner Name' in closed_deals_clean.columns:
            manager_stats = closed_deals_clean.groupby('Deal Owner Name').agg({
                'Id': 'count',
                'Deal_Age_days': ['min', 'median', 'mean', 'max']
            }).reset_index()
            
            manager_stats.columns = [t('manager'), t('deal_count'), t('minimum'), t('median'), t('mean'), t('maximum')]
            manager_stats = manager_stats[manager_stats[t('deal_count')] >= 3]
            
            if len(manager_stats) > 0:
                st.subheader(t('closing_speed_by_managers'))
                manager_stats = manager_stats.sort_values(t('median'), ascending=True)
                
                st.dataframe(
                    manager_stats.style\
                        .background_gradient(subset=[t('median')], cmap='RdYlGn_r')\
                        .format({
                            t('minimum'): '{:.0f}',
                            t('median'): '{:.1f}',
                            t('mean'): '{:.1f}',
                            t('maximum'): '{:.0f}'
                        }),
                    use_container_width=True,
                    height=400
                )
    else:
        st.info(t('not_enough_data'))

st.subheader(t('top_managers_revenue_conversion'))

if 'Deal Owner Name' in deals.columns:
    df_clean = deals.copy()
    
    manager_stats = df_clean.groupby('Deal Owner Name').agg(
        Leads=('Id', 'count'),
        Revenue=('revenue', 'sum'),
        Sales=('stage_normalized', lambda x: (x == 'Active Student').sum())
    ).reset_index().rename(columns={'Deal Owner Name': t('manager')})
    
    speed_stats = df_clean[df_clean['stage_normalized'] == 'Active Student'].groupby('Deal Owner Name')['Deal_Age_days'].median().reset_index()
    speed_stats.columns = [t('manager'), t('median_deal_age_days')]
    
    if 'calls' in locals() and len(calls) > 0:
        calls_agg = calls.groupby('CONTACTID')['Id'].count().reset_index().rename(columns={'Id': 'Calls_Count', 'CONTACTID': 'Contact Name'})
        successful_deals = df_clean[df_clean['stage_normalized'] == 'Active Student']
        deals_with_calls = successful_deals[['Id', 'Deal Owner Name', 'Contact Name']].merge(calls_agg, on='Contact Name', how='left').fillna(0)
        calls_stats = deals_with_calls.groupby('Deal Owner Name')['Calls_Count'].mean().reset_index()
        calls_stats.columns = [t('manager'), t('avg_calls_per_deal')]
    else:
        calls_stats = pd.DataFrame({t('manager'): manager_stats[t('manager')], t('avg_calls_per_deal'): 0})
    
    final_stats = manager_stats.merge(speed_stats, on=t('manager'), how='left').fillna(0)
    final_stats = final_stats.merge(calls_stats, on=t('manager'), how='left').fillna(0)
    
    final_stats[t('win_rate')] = (final_stats['Sales'] / final_stats['Leads'] * 100).round(2)
    final_stats[t('avg_check_2')] = (final_stats['Revenue'] / final_stats['Sales']).replace([np.inf], 0).fillna(0).round(0)
    
    top_managers = final_stats[final_stats['Leads'] >= 10].sort_values(by='Revenue', ascending=False)
    
    if len(top_managers) > 0:
        fig1 = px.bar(
            top_managers.head(15),
            x=t('manager'), y='Revenue', 
            color=t('win_rate'),
            text_auto='.2s',
            title=t('top_15_managers_revenue'),
            labels={'Revenue': f"{t('revenue')} ({t('currency')})", t('win_rate'): f"{t('win_rate')} ({t('percent')})"},
            color_continuous_scale='RdYlGn',
            height=500
        )
        fig1.update_layout(xaxis={'categoryorder':'total descending'})
        st.plotly_chart(fig1, use_container_width=True)
        
        efficiency_view = top_managers.sort_values(by=t('win_rate'), ascending=True).tail(15)
        fig2 = px.bar(
            efficiency_view,
            x=t('win_rate'), 
            y=t('manager'), 
            orientation='h', 
            color=t('median_deal_age_days'),
            text_auto='.1f',
            title=t('top_conversion'),
            labels={t('win_rate'): f"{t('win_rate')} ({t('percent')})", t('manager'): t('manager')},
            color_continuous_scale='Bluered',
            height=600
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        display_cols = [t('manager'), 'Leads', 'Sales', 'Revenue', t('win_rate'), 
                        t('avg_check_2'), t('median_deal_age_days'), t('avg_calls_per_deal')]
        display_df = final_stats[display_cols].sort_values('Revenue', ascending=False).head(20)
        
        st.dataframe(
            display_df.style\
                .background_gradient(subset=['Revenue', t('win_rate')], cmap='Greens')\
                .format({
                    'Revenue': '{:,.0f}', 
                    t('avg_check_2'): '{:,.0f}', 
                    t('median_deal_age_days'): '{:.0f}',
                    t('win_rate'): '{:.1f}%',
                    t('avg_calls_per_deal'): '{:.1f}'
                }),
            use_container_width=True
        )

st.subheader(t('sla_analysis'))

if 'SLA_seconds' in deals.columns:
    deals_sla = deals[deals['SLA_seconds'].notna()].copy()
    deals_sla['SLA_Hours'] = deals_sla['SLA_seconds'] / 3600
    
    manager_sla_stats = deals_sla.groupby('Deal Owner Name').agg({
        'Id': 'count',
        'SLA_Hours': 'median',
        'is_paid': 'mean'
    }).reset_index()
    manager_sla_stats.columns = [t('manager'), t('deals_count'), t('deal_age_hours'), t('win_rate_pct')]
    manager_sla_stats[t('win_rate_pct')] = (manager_sla_stats[t('win_rate_pct')] * 100).round(2)
    manager_sla_stats = manager_sla_stats[manager_sla_stats[t('deals_count')] > 10]
    
    if len(manager_sla_stats) > 0:
        fig5 = px.scatter(
            manager_sla_stats,
            x=t('deal_age_hours'),
            y=t('win_rate_pct'),
            size=t('deals_count'),
            color=t('win_rate_pct'),
            hover_name=t('manager'),
            title=t('response_speed_vs_conversion'),
            labels={t('deal_age_hours'): t('median_response_time_hours'), t('win_rate_pct'): f"{t('win_rate')} ({t('percent')})"},
            color_continuous_scale='RdYlGn',
            height=600
        )
        
        avg_sla = manager_sla_stats[t('deal_age_hours')].median()
        avg_win = manager_sla_stats[t('win_rate_pct')].median()
        fig5.add_vline(x=avg_sla, line_dash="dash", line_color="gray", annotation_text=t('avg_sla'))
        fig5.add_hline(y=avg_win, line_dash="dash", line_color="gray", annotation_text=t('avg_conversion'))
        st.plotly_chart(fig5, use_container_width=True)
        
        manager_table = deals_sla.groupby('Deal Owner Name').agg({
            'Id': 'count',
            'SLA_Hours': ['median', 'mean'],
            'stage_normalized': lambda x: (x == 'Active Student').sum()
        }).reset_index()
        
        manager_table.columns = [t('manager'), t('deals_count'), t('deal_age_hours'), t('avg_response_time'), t('active_students')]
        manager_table[t('win_rate_pct')] = (manager_table[t('active_students')] / manager_table[t('deals_count')] * 100).round(2)
        manager_table = manager_table[manager_table[t('deals_count')] > 10]
        
        if len(manager_table) > 0:
            manager_table = manager_table.sort_values(t('deal_age_hours'), ascending=True)
            display_df = manager_table[[t('manager'), t('deals_count'), t('deal_age_hours'), t('avg_response_time'), t('win_rate_pct')]]
            display_df.columns = [t('manager'), t('deal_count'), t('median'), t('average'), t('win_rate_pct')]
            
            st.dataframe(
                display_df.style\
                    .background_gradient(subset=[t('median')], cmap='RdYlGn_r')\
                    .background_gradient(subset=[t('average')], cmap='RdYlGn_r')\
                    .background_gradient(subset=[t('win_rate_pct')], cmap='RdYlGn')\
                    .format({
                        t('median'): '{:.1f} ' + t('days'),
                        t('average'): '{:.1f} ' + t('days'),
                        t('win_rate_pct'): '{:.1f}%'
                    }),
                use_container_width=True,
                height=300
            )

with tabs[2]:
    st.markdown(f'<div class="section-title">{t("products")}</div>', unsafe_allow_html=True)
    
    deals_success = deals[deals['stage_normalized'] == 'Active Student'].copy()
    pay_col = 'Payment_Type_Recovered' if 'Payment_Type_Recovered' in deals_success.columns else 'Payment Type'
    
    if len(deals_success) > 0:
        deals_success['Transactions'] = np.where(
            deals_success[pay_col] == 'one payment', 
            1, 
            deals_success['Months of study'].fillna(1)
        )
        
        st.subheader(t('product_metrics'))
        
        product_metrics = deals_success.groupby('Product').agg({
            'Contact Name': 'nunique',
            'revenue': 'sum',
            'Offer Total Amount': ['mean', 'sum'],
            'Transactions': 'sum',
            'Initial Amount Paid': 'mean'
        }).round(0)
        
        product_metrics.columns = ['B', 'Revenue', 'Avg_Contract', 'Total_Contract', 'T', 'Avg_Initial']
        product_metrics = product_metrics[product_metrics['B'] > 1].copy()
        
        if len(product_metrics) > 0:
            product_metrics['Avg_Check'] = (product_metrics['Revenue'] / product_metrics['B']).round(0)
            product_metrics['Collection_Ratio'] = (product_metrics['Revenue'] / product_metrics['Total_Contract'] * 100).round(1)
            product_metrics['APC'] = (product_metrics['T'] / product_metrics['B']).round(2)
            product_metrics['AOV'] = (product_metrics['Revenue'] / product_metrics['T']).round(0)
            
            TOTAL_UA = contacts['Id'].nunique()
            total_marketing_spend = spend['Spend'].sum()
            COGS_PERCENT = 0.0
            COGS_FIXED = 0
            
            product_metrics['UA'] = TOTAL_UA
            product_metrics['C1'] = (product_metrics['B'] / TOTAL_UA).round(4)
            product_metrics['AC'] = total_marketing_spend
            product_metrics['CPA'] = (total_marketing_spend / TOTAL_UA).round(2)
            product_metrics['CAC'] = (total_marketing_spend / product_metrics['B']).round(0)
            
            product_metrics['COGS_per_T'] = (product_metrics['Revenue'] * COGS_PERCENT + product_metrics['T'] * COGS_FIXED) / product_metrics['T']
            product_metrics['CLTV'] = ((product_metrics['AOV'] - product_metrics['COGS_per_T']) * product_metrics['APC']).round(0)
            product_metrics['LTV'] = (product_metrics['CLTV'] * product_metrics['C1']).round(2)
            product_metrics['CM'] = (product_metrics['Revenue'] - total_marketing_spend - (product_metrics['Revenue'] * COGS_PERCENT + product_metrics['T'] * COGS_FIXED)).round(0)
            
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
            
            st.subheader(t('product_efficiency_visualizations'))
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig1 = px.bar(
                    display_df.reset_index(),
                    x='Product', y='Revenue',
                    color='LTV',
                    title=t('revenue_by_products'),
                    labels={'Revenue': f"{t('revenue')} ({t('currency')})", 'LTV': f"{t('ltv_2')} ({t('currency')})"},
                    color_continuous_scale='RdYlGn',
                    height=500
                )
                fig1.update_layout(xaxis={'categoryorder': 'total descending'})
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                fig2 = px.scatter(
                    display_df.reset_index(),
                    x='B', y='Avg_Check',
                    size='Revenue',
                    color='Collection_Ratio',
                    text='Product',
                    title=t('product_matrix'),
                    labels={'B': t('client_count'), 'Avg_Check': f"{t('average_check')} ({t('currency')})"},
                    color_continuous_scale='Viridis',
                    height=500
                )
                fig2.update_traces(textposition='top center')
                st.plotly_chart(fig2, use_container_width=True)
            
            st.subheader(t('payment_type_analysis'))
            
            if pay_col in deals_success.columns:
                deals_filtered = deals_success[deals_success['Product'].isin(display_df.index)]
                payment_split = deals_filtered.groupby(['Product', pay_col]).size().reset_index(name='Count')
                
                if len(payment_split) > 0:
                    fig3 = px.bar(
                        payment_split,
                        x='Product', y='Count', color=pay_col,
                        title=t('payment_type_distribution'),
                        labels={'Count': t('deal_count_2')},
                        color_discrete_sequence=px.colors.qualitative.Set3,
                        height=500
                    )
                    fig3.update_layout(xaxis={'categoryorder': 'total descending'}, barmode='stack')
                    st.plotly_chart(fig3, use_container_width=True)
            
            st.subheader(t('education_type_analysis'))
            
            if 'Education Type' in deals_success.columns:
                edu_stats = deals_success.groupby('Education Type').agg({
                    'Contact Name': 'nunique',
                    'revenue': 'sum',
                    'Offer Total Amount': 'mean'
                }).round(0)
                edu_stats.columns = [t('students'), t('revenue'), 'Avg_Contract']
                edu_stats = edu_stats[edu_stats[t('students')] > 1]
                edu_stats['Avg_Check'] = (edu_stats[t('revenue')] / edu_stats[t('students')]).round(0)
                
                if len(edu_stats) > 0:
                    fig4 = px.bar(
                        edu_stats.reset_index(),
                        x='Education Type', y=t('revenue'),
                        color='Avg_Check',
                        title=t('revenue_by_education_type'),
                        labels={t('revenue'): f"{t('revenue')} ({t('currency')})", 'Avg_Check': f"{t('average_check')} ({t('currency')})"},
                        color_continuous_scale='RdYlGn',
                        height=500
                    )
                    fig4.update_layout(xaxis={'categoryorder': 'total descending'})
                    st.plotly_chart(fig4, use_container_width=True)
    else:
        st.warning(t('no_successful_deals'))

with tabs[3]:
    st.markdown(f'<div class="section-title">{t("geography")}</div>', unsafe_allow_html=True)
    
    deals_with_city = deals[
        (deals['City'].notna()) & 
        (deals['City'] != 'Unknown') &
        (deals['City'] != 'unknown')
    ].copy()
    
    if len(deals_with_city) > 0:
        city_stats = deals_with_city.groupby('City').agg({
            'Id': 'count',
            'stage_normalized': lambda x: (x == 'Active Student').sum(),
            'revenue': 'sum',
            'Source': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'Unknown'
        }).reset_index()
        
        city_stats.columns = [t('city'), t('total_deals'), t('active_students'), t('total_revenue'), t('top_source')]
        city_stats[t('win_rate')] = (city_stats[t('active_students')] / city_stats[t('total_deals')] * 100).round(2)
        city_stats = city_stats.sort_values(t('total_revenue'), ascending=False)
        
        geocoded = prepare_geodata(city_stats)
        geocoded_count = len(geocoded)
        total_cities = len(city_stats)
        
        st.subheader(f"{t('sales_map')} (Top-{geocoded_count} из {total_cities} {t('cities').lower()})")
        
        if len(geocoded) > 0:
            fig_map = px.scatter_mapbox(
                geocoded,
                lat="lat",
                lon="lon",
                size=t('total_deals'),
                color=t('total_revenue'),
                hover_name=t('city'),
                hover_data={
                    t('total_revenue'): ':.0f',
                    t('total_deals'): True,
                    t('win_rate'): ':.1f',
                    t('top_source'): True
                },
                zoom=4,
                height=600,
                mapbox_style="open-street-map"
            )
            
            fig_map.update_layout(
                margin=dict(l=0, r=0, t=30, b=0),
                coloraxis_colorbar=dict(title=t('revenue')),
            )
            
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.info("Не удалось геокодировать города")
        
        top_n = 15
        st.subheader(f"{t('top_cities_revenue')} (Top-{top_n})")
        
        city_top15 = city_stats.head(top_n).copy()
        
        fig_bar = px.bar(
            city_top15,
            x=t('city'),
            y=t('total_revenue'),
            color=t('top_source'),
            text_auto='.2s',
            title=f"{t('top_cities_revenue')} (Top-{top_n})",
            labels={t('total_revenue'): f"{t('revenue')} ({t('currency')})"},
            color_discrete_sequence=px.colors.qualitative.Set3,
            height=500
        )
        fig_bar.update_layout(xaxis={'categoryorder': 'total descending'})
        st.plotly_chart(fig_bar, use_container_width=True)
        
        st.subheader(t('city_efficiency_analysis'))
        
        min_deals = 5
        top_conversion = city_stats[city_stats[t('total_deals')] >= min_deals].sort_values(t('win_rate'), ascending=False).head(10)
        
        if len(top_conversion) > 0:
            fig_conv = px.bar(
                top_conversion,
                x=t('win_rate'),
                y=t('city'),
                orientation='h',
                text=t('win_rate'),
                title=f"{t('top_cities_conversion')} (≥{min_deals} {t('deal_count_2').lower()})",
                labels={t('win_rate'): f"{t('win_rate')} ({t('percent')})", t('city'): ''},
                color=t('total_revenue'),
                color_continuous_scale='RdYlGn',
                height=500
            )
            fig_conv.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig_conv.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_conv, use_container_width=True)
        
        st.subheader(t('german_level_analysis'))
        
        if 'Level of Deutsch' in deals.columns:
            deals_lang = deals[
                (deals['max_stage_rank'] >= 1) & 
                (deals['Level of Deutsch'].notna()) &
                (deals['Level of Deutsch'] != 'Unknown') &
                (deals['Level of Deutsch'] != 'unknown')
            ].copy()
            
            if len(deals_lang) > 0:
                lang_stats = deals_lang.groupby('Level of Deutsch').agg({
                    'Id': 'count',
                    'stage_normalized': lambda x: (x == 'Active Student').sum(),
                    'revenue': 'sum'
                }).reset_index()
                
                lang_stats.columns = [t('level'), t('total_deals_2'), t('active_students'), t('total_revenue')]
                lang_stats[t('win_rate')] = (lang_stats[t('active_students')] / lang_stats[t('total_deals_2')] * 100).round(2)
                lang_stats[t('avg_revenue_per_student_2')] = (lang_stats[t('total_revenue')] / lang_stats[t('active_students')]).round(0)
                
                level_order = ['A0', 'A1', 'A2', 'B1', 'B2', 'C1', 'C2']
                lang_stats[t('level')] = pd.Categorical(lang_stats[t('level')], categories=level_order, ordered=True)
                lang_stats = lang_stats.sort_values(t('level')).dropna()
                
                fig_lang1 = px.bar(
                    lang_stats,
                    x=t('level'),
                    y=t('win_rate'),
                    color=t('total_deals_2'),
                    text_auto='.1f',
                    title=t('conversion_by_german_level'),
                    labels={t('win_rate'): f"{t('win_rate')} ({t('percent')})", t('level'): t('german_level')},
                    color_continuous_scale='Teal',
                    height=400
                )
                fig_lang1.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': level_order})
                st.plotly_chart(fig_lang1, use_container_width=True)
                
                fig_lang2 = make_subplots(
                    rows=1, cols=2,
                    subplot_titles=[t('revenue_by_level'), t('avg_revenue_per_student')],
                    horizontal_spacing=0.15
                )
                
                fig_lang2.add_trace(
                    go.Bar(
                        x=lang_stats[t('level')],
                        y=lang_stats[t('total_revenue')],
                        text=lang_stats[t('total_revenue')].apply(lambda x: f'{x:,.0f}'),
                        textposition='auto',
                        marker_color='#636EFA',
                        name=t('revenue')
                    ),
                    row=1, col=1
                )
                
                fig_lang2.add_trace(
                    go.Bar(
                        x=lang_stats[t('level')],
                        y=lang_stats[t('avg_revenue_per_student_2')],
                        text=lang_stats[t('avg_revenue_per_student_2')].apply(lambda x: f'{x:,.0f}'),
                        textposition='auto',
                        marker_color='#00CC96',
                        name=t('avg_revenue_per_student_2')
                    ),
                    row=1, col=2
                )
                
                fig_lang2.update_xaxes(title_text=t('german_level'), row=1, col=1)
                fig_lang2.update_xaxes(title_text=t('german_level'), row=1, col=2)
                fig_lang2.update_yaxes(title_text=f"{t('revenue')} ({t('currency')})", row=1, col=1)
                fig_lang2.update_yaxes(title_text=f"{t('avg_revenue_per_student_2')} ({t('currency')})", row=1, col=2)
                fig_lang2.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig_lang2, use_container_width=True)
    else:
        st.warning(t('no_city_data'))

with tabs[5]:
    st.markdown(f'<div class="section-title">{t("growth_points")}</div>', unsafe_allow_html=True)
    
    GROWTH_PCT = 0.10
    COGS_FIXED_PER_TRANS = 0
    COGS_PERCENT_FROM_CHECK = 0.0
    
    ACTION_INSIGHTS = {
        'UA': t('channels_scaling'),
        'C1': t('funnel_optimization'), 
        'AOV': t('upsell_prices'),
        'APC': t('retention_loyalty'),
        'CPA': t('ad_optimization')
    }
    
    def calculate_scenario_metrics(ua, c1, aov, apc, ac_base, product_name, scenario_name, growth_pct):
        b = ua * c1 if ua > 0 and c1 > 0 else 0
        t = b * apc if b > 0 and apc > 0 else 0
        revenue = t * aov if t > 0 and aov > 0 else 0
        
        if "UA" in scenario_name:
            ac = ac_base * (1 + growth_pct)
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
            t('scenario'): scenario_name, 'Scenario_Type': scenario_type, 'Growth_Pct': growth_pct,
            t('product'): product_name, 'UA': ua, 'C1': c1, 'B': b, 'AOV': aov, 'APC': apc, 
            'T': t, t('revenue'): revenue, 'AC': ac, 'CLTV': cltv, 'LTV': ltv, 
            'CPA': cpa, 'CAC': cac, 'CM': cm, 'ROMI': romi
        }

    st.subheader(t('business_analysis'))
    
    TOTAL_UA = contacts['Id'].nunique()
    total_marketing_spend = spend['Spend'].sum()
    active_students_df = deals[deals['stage_normalized'] == 'Active Student']
    TOTAL_B_CORRECT = active_students_df['Contact Name'].nunique()
    total_t = active_students_df['Transactions'].sum() if 'Transactions' in active_students_df.columns else 0
    total_revenue = active_students_df['revenue'].sum()

    cogs_global = (total_revenue * COGS_PERCENT_FROM_CHECK) + (total_t * COGS_FIXED_PER_TRANS)
    
    global_row = {
        'UA': TOTAL_UA,
        'B': TOTAL_B_CORRECT,
        t('revenue'): total_revenue,
        'T': total_t,
        'AC': total_marketing_spend,
        'C1': TOTAL_B_CORRECT / TOTAL_UA if TOTAL_UA > 0 else 0,
        'AOV': total_revenue / total_t if total_t > 0 else 0,
        'APC': total_t / TOTAL_B_CORRECT if TOTAL_B_CORRECT > 0 else 0,
        'CM': total_revenue - total_marketing_spend - cogs_global
    }
    
    global_scenarios = []
    g = GROWTH_PCT
    
    global_scenarios.append(calculate_scenario_metrics(
        global_row['UA'], global_row['C1'], global_row['AOV'], global_row['APC'], 
        global_row['AC'], t('total_business'), "BASELINE", 0))
    global_scenarios.append(calculate_scenario_metrics(
        global_row['UA'] * (1 + g), global_row['C1'], global_row['AOV'], global_row['APC'], 
        global_row['AC'], t('total_business'), f"UA +{int(g*100)}%", g))
    global_scenarios.append(calculate_scenario_metrics(
        global_row['UA'], global_row['C1'] * (1 + g), global_row['AOV'], global_row['APC'], 
        global_row['AC'], t('total_business'), f"C1 +{int(g*100)}%", g))
    global_scenarios.append(calculate_scenario_metrics(
        global_row['UA'], global_row['C1'], global_row['AOV'] * (1 + g), global_row['APC'], 
        global_row['AC'], t('total_business'), f"AOV +{int(g*100)}%", g))
    global_scenarios.append(calculate_scenario_metrics(
        global_row['UA'], global_row['C1'], global_row['AOV'], global_row['APC'] * (1 + g), 
        global_row['AC'], t('total_business'), f"APC +{int(g*100)}%", g))
    global_scenarios.append(calculate_scenario_metrics(
        global_row['UA'], global_row['C1'], global_row['AOV'], global_row['APC'], 
        global_row['AC'], t('total_business'), f"CPA -{int(g*100)}%", g))
    
    global_scenarios_df = pd.DataFrame(global_scenarios)
    
    if not global_scenarios_df.empty:
        base_scenario = global_scenarios_df[global_scenarios_df[t('scenario')] == 'BASELINE']
        if not base_scenario.empty:
            base_cm = base_scenario.iloc[0]['CM']
            global_scenarios_df['CM_Growth_€'] = global_scenarios_df['CM'] - base_cm
    
    st.subheader(t('growth_scenarios_total_business'))
    
    format_dict = {
        'UA': '{:,.0f}', 'B': '{:,.0f}', 'T': '{:,.0f}', t('revenue'): '{:,.0f}', 
        'C1': '{:.2%}', 'ROMI': '{:.0f}%', 'AOV': '{:,.1f}', 'APC': '{:.2f}', 
        'CLTV': '{:,.0f}', 'LTV': '{:,.1f}', 'AC': '{:,.0f}', 'CPA': '{:,.2f}', 
        'CAC': '{:,.1f}', 'CM': '{:,.0f}', 'CM_Growth_€': '{:+,.0f}'
    }
    
    cols = [t('scenario'), 'UA', 'C1', 'B', 'T', 'AOV', 'APC', t('revenue'), 'AC', 
            'CPA', 'CAC', 'CLTV', 'LTV', 'CM', 'CM_Growth_€', 'ROMI']
    
    if 'CM_Growth_€' in global_scenarios_df.columns:
        sorted_df = global_scenarios_df[cols].sort_values('CM_Growth_€', ascending=False)
    else:
        sorted_df = global_scenarios_df[cols]
    
    st.dataframe(
        sorted_df.style.format(format_dict).background_gradient(
            subset=['CM_Growth_€' if 'CM_Growth_€' in global_scenarios_df.columns else 'CM'], 
            cmap='Greens', vmin=0),
        use_container_width=True
    )
    
    growth_scenarios = global_scenarios_df[global_scenarios_df[t('scenario')] != 'BASELINE']
    if not growth_scenarios.empty and 'CM_Growth_€' in growth_scenarios.columns:
        growth_scenarios['CM_Growth_Rounded'] = growth_scenarios['CM_Growth_€'].round(0)
        max_growth = growth_scenarios['CM_Growth_Rounded'].max()
        best_scenarios = growth_scenarios[growth_scenarios['CM_Growth_Rounded'] == max_growth]
        
        st.write(f"**{t('best_scenarios')}:**")
        for _, scenario in best_scenarios.iterrows():
            st.write(f"- **{scenario[t('scenario')]}**: {t('profit_growth')} {scenario['CM_Growth_€']:+,.0f} {t('currency')}")
            st.write(f"  ROMI: {scenario['ROMI']:.1f}%")
            st.write(f"  {t('action')}: {ACTION_INSIGHTS.get(scenario['Scenario_Type'], '')}")

with tabs[6]:
    st.markdown(f'<div class="section-title">{t("metrics_tree")}</div>', unsafe_allow_html=True)
    
    st.subheader(t('business_metrics_tree'))
    
    st.markdown(f"""
**{t('level_1')}**  
└── **{t('cm')}** — {t('revenue')} - AC - COGS

**{t('level_2')}**  
├── **UA (User Acquisition)** — {t('unique_clients')} → COUNTUNIQUE(CONTACTS['Id'])  
├── **C1 ({t('conversion_c1')})** — {t('conversion')} в покупателя → B / UA  
├── **CPA (Cost Per Acquisition)** — {t('cpc')} посетителя → AC / UA  
├── **AOV (Average Order Value)** — {t('average_check')} → {t('revenue')} / T  
├── **COGS (Cost of Goods Sold)** — {t('margin')} (моделируемая)  
├── **APC (Average Payment Count)** — {t('transactions')} на клиента → T / B  
├── **CPC (Cost Per Click)** — {t('cpc')} клика → AC / {t('clicks')}  
└── **CTR (Click-Through Rate)** — {t('conversion')} в клик → {t('clicks')} / {t('impressions')}

**{t('level_2_1')}**  
├── **{t('revenue')}** — Сумма поступлений → SUM(DEALS['revenue'])  
└── **ROMI (Return on Marketing)** — Окупаемость рекламы → CM / AC

**{t('level_3')}**  
├── **B ({t('buyers')})** — {t('unique_clients')} со статусом Active Student  
├── **AC (Advertising Cost)** — {t('marketing_spend')} → SUM(SPEND['Spend'])  
├── **CAC (Customer Acquisition Cost)** — {t('cac')} клиента → AC / B  
├── **CLTV (Customer Lifetime Value)** — {t('cm')} с клиента → (AOV - COGS) × APC  
├── **LTV (Lifetime Value)** — Ценность посетителя → CLTV × C1  
└── **T ({t('transactions')})** — Всего транзакций → SUM(DEALS['Transactions'])

**{t('level_4')}**  
├── DEALS['Created Time'] — Дата создания лида  
├── DEALS['Closing Date'] — Дата закрытия сделки  
├── DEALS['Source'] / SPEND['Source'] — {t('source')} трафика  
├── DEALS['Campaign'] — Кампания  
├── DEALS['Product'] — {t('product')} курса  
├── DEALS['Stage'] — Стадия воронки  
├── DEALS['Quality'] — Качество лида  
├── DEALS['City'] — {t('geography')}  
├── SPEND['Clicks'] — {t('clicks')} по рекламе  
└── SPEND['Impressions'] — {t('impressions')} рекламы

**{t('key_dependencies')}**  
- **B = UA × C1** ({t('buyers')} = Посетители × {t('conversion')})  
- **{t('revenue')} = AOV × T** (Оборот = Чек × {t('transactions')})  
- **T = B × APC** ({t('transactions')} = Клиенты × Частота)  
- **CAC = AC / B** ({t('cac')} клиента = Реклама / Клиенты)  
- **CLTV = (AOV - COGS) × APC** (Ценность клиента = (Чек - Себестоимость) × Частота)  
- **LTV = CLTV × C1** (Ценность посетителя = Ценность клиента × {t('conversion')})  
- **CM = {t('revenue')} - AC - COGS** ({t('margin')} = Оборот - Реклама - Себестоимость)  
- **ROMI = CM / AC** (Окупаемость = {t('margin')} / Реклама)  
""")
    
    st.subheader(t('hadi_cycles_ab_testing'))
    
    main_products = ["digital marketing", "ux/ui design", "web developer"]
    
    contacts_local = contacts.copy()
    if 'created_date' not in contacts_local.columns:
        contacts_local['created_date'] = pd.to_datetime(contacts_local['Created Time']).dt.date
    
    TOTAL_UA = contacts_local['Id'].nunique()
    active_students_df = deals[deals['stage_normalized'] == 'Active Student']
    buyers_per_product = active_students_df.groupby('Product')['Contact Name'].nunique()
    c1_per_product = buyers_per_product / TOTAL_UA if TOTAL_UA > 0 else 0
    
    product_stats = pd.DataFrame({
        t('product'): buyers_per_product.index,
        "B (Покупатели)": buyers_per_product.values,
        "UA (Общий трафик)": TOTAL_UA,
        "C1 (Конверсия)": c1_per_product.values
    })
    product_stats = product_stats[product_stats[t('product')].isin(main_products)]
    
    if len(product_stats) > 0:
        st.write(f"**{t('base_metrics_ab_tests')}:**")
        st.dataframe(
            product_stats.style.format({
                'B (Покупатели)': '{:,.0f}',
                'UA (Общий трафик)': '{:,.0f}',
                'C1 (Конверсия)': '{:.2%}'
            }),
            use_container_width=True
        )
        
        hypotheses = [
            ("HADI-1. Уведомление менеджера", 
             "Внедрение автоматического уведомления менеджера при поступлении заявки и обязательный первый звонок в течение 1 часа"),
            ("HADI-2. Автоматическая отправка материалов", 
             "Автоматическая отправка email с программой курса и видео-отзывом выпускника в течение 5 минут после заявки"),
            ("HADI-3. SMS-напоминание", 
             "Отправка SMS-напоминания о записи на курс через 1 час после пропущенного звонка менеджера")
        ]
        
        st.write(f"**{t('ready_hadi_cycles')}:**")
        
        for hyp_name, hyp_text in hypotheses:
            with st.expander(f"{hyp_name}"):
                st.write(f"**{t('hypothesis')}:** {hyp_text}")
                st.write(f"**{t('hadi_cycle')}:**")
                
                hadi_df = pd.DataFrame({
                    t('stage'): ["Hypothesis (H)", "Action (A)", "Data (D)", "Insight (I)"],
                    t('formulation'): [
                        f"{hyp_text}. Ожидаемый рост конверсии на 10%.",
                        "Настроить процесс согласно гипотезе для тестовой группы (50%). Контрольная группа — текущий процесс.",
                        "Срок теста — 2 недели. Сравниваются две группы лидов. Метрика — конверсия (C1). Цель — прирост ≥ 10%.",
                        "Гипотеза подтверждается, если прирост конверсии ≥ целевого уровня и результат статистически значим."
                    ]
                })
                
                st.table(hadi_df)
    
    st.subheader(t('ab_test_parameters'))
    
    if len(product_stats) > 0:
        ALPHA = 0.05
        POWER = 0.8
        MDE_LIST = [0.10, 0.20, 0.30]
        
        daily_leads = contacts_local.groupby('created_date')['Id'].nunique().mean()
        DAILY_LEADS_PER_GROUP = daily_leads / 2 if daily_leads > 0 else 10
        
        def required_sample(p, mde, alpha=ALPHA, power=POWER):
            p1 = p
            p2 = p * (1 + mde)
            diff = abs(p2 - p1)
            pooled_var = (p1*(1-p1) + p2*(1-p2)) / 2
            effect_size = diff / np.sqrt(pooled_var)
            
            n_required = NormalIndPower().solve_power(
                effect_size=effect_size,
                nobs1=None,
                alpha=alpha,
                power=power,
                ratio=1.0,
                alternative='two-sided'
            )
            return n_required
        
        def required_days(n_required, daily_leads):
            return int(np.ceil(n_required / daily_leads)) if daily_leads > 0 else 999
        
        results = []
        
        for _, row in product_stats.iterrows():
            product_name = row[t('product')]
            p = row["C1 (Конверсия)"]
            
            for mde in MDE_LIST:
                n_required = required_sample(p, mde)
                days_needed = required_days(n_required, DAILY_LEADS_PER_GROUP)
                
                for hyp_name, _ in hypotheses:
                    results.append({
                        t('product'): product_name,
                        t('hypothesis'): hyp_name,
                        t('base_c1'): f"{p:.2%}",
                        t('target_effect'): f"{mde*100:.0f}%",
                        t('leads_per_group'): int(np.ceil(n_required)),
                        t('leads_per_day_group'): f"{DAILY_LEADS_PER_GROUP:.1f}",
                        t('test_days_2'): days_needed
                    })
        
        results_df = pd.DataFrame(results)
        
        def highlight_days(val):
            try:
                val_int = int(val)
                if val_int <= 14:
                    return 'background-color: #006400; color: white'
                elif val_int <= 30:
                    return 'background-color: #FFA500; color: black'
                else:
                    return 'background-color: #8B0000; color: white'
            except:
                return ''
        
        st.markdown(f"**{t('avg_leads_per_day')}:** {DAILY_LEADS_PER_GROUP:.1f}")
        
        styled_df = results_df.style.applymap(highlight_days, subset=[t('test_days_2')])
        
        st.dataframe(
            styled_df.format({
                t('leads_per_group'): "{:,.0f}",
                t('test_days_2'): "{:,.0f}"
            }),
            use_container_width=True,
            height=400
        )
        
        st.markdown(f"""
**{t('legend')}:**  
🟩 **≤14 {t('days').lower()}** — {t('test_feasible')}  
🟧 **15-30 {t('days').lower()}** — {t('extended_test_needed')}  
🟥 **>30 {t('days').lower()}** — {t('test_difficult')}  
""")
        
st.markdown("---")

st.markdown(
    f"""
    <div style='text-align: center; color: #666; font-size: 0.9rem; padding: 2rem 0;'>
        {t('footer')}
    </div>
    """, 
    unsafe_allow_html=True
)