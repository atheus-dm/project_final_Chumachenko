"""
ПОЛНЫЙ АНАЛИТИЧЕСКИЙ ДАШБОРД IT ШКОЛЫ
Версия 3.0 - Мультиязычная поддержка (русский, немецкий, английский)
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
from statsmodels.stats.power import NormalIndPower
warnings.filterwarnings('ignore')

# ========== МУЛЬТИЯЗЫЧНАЯ ПОДДЕРЖКА ==========
TRANSLATIONS = {
    # Основной интерфейс
    'ru': {
        # Заголовки и меню
        'full_it_school_analytics': 'ПОЛНЫЙ АНАЛИТИЧЕСКИЙ ОТЧЕТ IT ШКОЛЫ',
        'data_period': 'Период данных',
        'business_summary': 'СВОДНЫЕ ПОКАЗАТЕЛИ БИЗНЕСА',
        
        # Метрики бизнеса
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
        'products': 'Продукты',
        'top_product': 'Топ продукт',
        'no_data': 'Нет данных',
        
        # Названия вкладок
        'marketing_tab': 'МАРКЕТИНГ',
        'sales_tab': 'ПРОДАЖИ',
        'products_tab': 'ПРОДУКТЫ',
        'geography_tab': 'ГЕОГРАФИЯ/ЯЗЫКИ',
        'unit_economics_tab': 'ЮНИТ-ЭКОНОМИКА',
        'growth_points_tab': 'ТОЧКИ РОСТА',
        'metrics_tree_tab': 'ДЕРЕВО МЕТРИК И A/B ТЕСТЫ',
        
        # Маркетинг
        'marketing_analytics': 'МАРКЕТИНГОВАЯ АНАЛИТИКА',
        'marketing_funnel': 'МАРКЕТИНГОВАЯ ВОРОНКА И ЭФФЕКТИВНОСТЬ РАСХОДОВ',
        'paid_sources_analysis': 'АНАЛИЗ ПЛАТНЫХ ИСТОЧНИКОВ: CPC vs КАЧЕСТВО',
        'source_efficiency_matrix': 'МАТРИЦА ЭФФЕКТИВНОСТИ ИСТОЧНИКОВ: СКОРОСТЬ VS ЧЕК',
        'roas_by_sources': 'ROAS ПО ИСТОЧНИКАМ ТРАФИКА',
        'campaign_analysis': 'АНАЛИЗ КАМПАНИЙ ПО ЭФФЕКТИВНОСТИ',
        'conversion_funnel': 'Воронка конверсии по каналам (Log Scale)',
        'cost_per_result': 'Стоимость результата',
        'marketing_analytics_volumes': 'Маркетинговая аналитика: Объемы и Деньги',
        'source': 'Источник',
        'spend': 'Расходы',
        'clicks': 'Клики',
        'leads': 'Лиды',
        'students': 'Студенты',
        'cpc': 'CPC',
        'cpl': 'CPL',
        'cps': 'CPS',
        'cpc_vs_conversion': 'CPC vs Конверсия лидов в студентов',
        'cpcl': 'Цена за клик (€)',
        'conversion_percent': 'Конверсия (%)',
        'median_cpc': 'Ср.CPC',
        'median_conversion': 'Ср.Конверсия',
        'detailed_source_stats': 'Детальная статистика по источникам:',
        'speed_vs_check': 'Матрица Источников: Скорость (X) vs Средний чек (Y)',
        'median_speed_days': 'Медианная скорость закрытия (дни)',
        'avg_check_euro': 'Средний чек (€)',
        'avg_speed': 'Ср. скорость',
        'avg_check': 'Ср. чек',
        'leads_finance_details': 'Детализация по лидам и финансам:',
        'quality_leads': 'Качественные лиды',
        'quality_percent': 'Качество %',
        'conversion_percent_short': 'Конв. %',
        'avg_check_full': 'Средний чек',
        'roas_analysis': 'ROAS: Окупаемость источников',
        'roas_percent': 'ROAS (%)',
        'breakeven_point': 'Точка безубыточности',
        'top_campaigns_efficiency': 'ТОП-15 кампаний по эффективности (студенты / лиды)',
        'efficiency_ratio': 'Конверсия лидов в студентов (%)',
        'campaign': 'Кампания',
        'detailed_campaign_stats': 'Детальная статистика по кампаниям:',
        
        # Продажи
        'sales_efficiency': 'ЭФФЕКТИВНОСТЬ ОТДЕЛА ПРОДАЖ (KPI 360°)',
        'calls_dynamics_analysis': 'АНАЛИЗ ДИНАМИКИ И ВЛИЯНИЯ ЗВОНКОВ',
        'leads_calls_sales_dynamics': 'ДИНАМИКА ЛИДОВ, ЗВОНКОВ И ПРОДАЖ',
        'incoming_leads': 'Входящие Лиды',
        'sales_multiplied': 'Продажи (×50)',
        'calls': 'Звонки',
        'calls_impact_on_sales': 'Влияние звонков на продажи (по неделям)',
        'number_of_calls': 'Количество Звонков',
        'number_of_sales': 'Количество Продаж',
        'leads_volume': 'Объем Лидов',
        'weekly_conversion': 'Конверсия недели (%)',
        'correlation_analysis': 'Корреляционный анализ:',
        'calls_sales_correlation': 'Связь "Звонки → Продажи"',
        'leads_sales_correlation': 'Связь "Лиды → Продажи"',
        'correlation_insight': 'Вывод: Корреляция слабая (0.43-0.54). Нет прямой линейной связи между звонками/лидами и продажами в рамках одной недели.',
        'calls_distribution': 'РАСПРЕДЕЛЕНИЕ ЗВОНКОВ ДО ПРОДАЖИ',
        'calls_count': 'Количество звонков',
        'deals_count': 'Кол-во сделок',
        'median': 'Медиана',
        'average': 'Среднее',
        'deal_speed': 'СКОРОСТЬ ЗАКРЫТИЯ СДЕЛОК',
        'success_deal_duration': 'Распределение времени закрытия успешных сделок (Шаг = 5 дней)',
        'deal_duration_days': 'Продолжительность сделки (дни)',
        'metric': 'Метрика',
        'days': 'Дни',
        'mean': 'Среднее',
        'minimum': 'Минимум',
        'maximum': 'Максимум',
        'manager_speed': 'Скорость закрытия по менеджером (только ≥3 сделок)',
        'manager': 'Менеджер',
        'deals_count_full': 'Кол-во сделок',
        'median_full': 'Медиана',
        'monthly_dynamics': 'МЕСЯЧНАЯ ДИНАМИКА: ВЫРУЧКА, СТУДЕНТЫ И ЛИДЫ',
        'revenue_students': 'ВЫРУЧКА И АКТИВНЫЕ СТУДЕНТЫ',
        'leads_conversion': 'ЛИДЫ И КОНВЕРСИЯ',
        'revenue_euro': 'Выручка (€)',
        'active_students': 'Активные студенты',
        'total_leads': 'Всего лидов',
        'conversion_rate': 'Конверсия (%)',
        'month': 'Месяц',
        'detailed_monthly_stats': 'Детальная месячная статистика:',
        'month_year': 'Месяц-Год',
        'active_students_count': 'Активные студенты',
        'top_managers': 'ТОП МЕНЕДЖЕРОВ ПО ВЫРУЧКЕ И КОНВЕРСИИ',
        'top_managers_revenue': 'ТОП-15 Менеджеров по Выручке (Цвет = Конверсия Win Rate)',
        'win_rate': 'Win Rate (%)',
        'top_conversion': 'ТОП по конверсии (Цвет = Скорость закрытия, дни)',
        'avg_deal_cycle': 'Ср. цикл сделки (дни)',
        'detailed_manager_stats': 'ДЕТАЛЬНАЯ СТАТИСТИКА МЕНЕДЖЕРОВ',
        'speed_quality_analysis': 'АНАЛИЗ СКОРОСТИ ОТВЕТА (SLA) И КАЧЕСТВА ЛИДОВ',
        'conversion_by_speed': 'Конверсия по сегментам скорости ответа',
        'sla_segment': 'SLA_Segment',
        'conversion_by_quality': 'Конверсия по качеству лидов (только категории с >10 лидами)',
        'quality': 'Качество',
        'speed_vs_conversion': 'Скорость ответа vs Конверсия по менеджерам',
        'median_sla_hours': 'Медианное время ответа (часы)',
        'manager_sla': 'Скорость ответа по менеджерам:',
        'deals': 'Сделок',
        'median_hours': 'Медиана (ч)',
        'mean_hours': 'Среднее (ч)',
        'conversion_deciles': 'Конверсия vs Время ответа (децили)',
        'response_time_min': 'Время ответа (мин)',
        'sla_metrics': 'Ключевые метрики скорости ответа:',
        'response_time': 'Время ответа',
        'average_time': 'Среднее время',
        'median_time': 'Медианное время',
        'faster_25': '25% сделок быстрее',
        'faster_75': '75% сделок быстрее',
        'lost_reasons_analysis': 'АНАЛИЗ ПРИЧИНЫ ОТКАЗОВ ПО МЕНЕДЖЕРАМ',
        'lost_reasons_distribution': 'Распределение причин отказов по менеджерам:',
        'lost_reason': 'Причина',
        'total': 'ВСЕГО',
        'share_percent': 'Доля %',
        'total_distribution': 'Общее распределение причин отказов:',
        
        # Продукты
        'products_payments_analysis': 'АНАЛИЗ ПРОДУКТОВ И ПЛАТЕЖЕЙ',
        'full_product_metrics': 'ПОЛНЫЕ МЕТРИКИ ПО ПРОДУКТАМ',
        'product': 'Продукт',
        'clients': 'Клиенты',
        'avg_contract': 'Средний контракт',
        'collection_ratio': '% оплаты контракта',
        'cltv_full': 'CLTV',
        'ltv_full': 'LTV',
        'cac_full': 'CAC',
        'cm_full': 'CM',
        'product_efficiency': 'ВИЗУАЛИЗАЦИИ ЭФФЕКТИВНОСТИ ПРОДУКТОВ',
        'revenue_by_products': 'Выручка по продуктам (Цвет = LTV)',
        'revenue_euro_full': 'Выручка (€)',
        'product_matrix': 'Матрица продуктов: Клиенты vs Средний чек',
        'clients_count': 'Количество клиентов',
        'payment_type_analysis': 'АНАЛИЗ ТИПОВ ОПЛАТЫ',
        'payment_type_distribution': 'Распределение типов оплата по продуктам',
        'education_type_analysis': 'АНАЛИЗ ТИПОВ ОБУЧЕНИЯ',
        'education_type': 'Тип обучения',
        'revenue_by_education': 'Выручка по типам обучения (Цвет = Средний чек)',
        
        # География
        'geographical_analysis': 'ГЕОГРАФИЧЕСКИЙ АНАЛИЗ',
        'sales_map': 'КАРТА ПРОДАЖ',
        'top_cities_revenue': 'ТОП ГОРОДОВ ПО ВЫРУЧКЕ',
        'city': 'Город',
        'top_source': 'Топ источник',
        'city_efficiency_analysis': 'АНАЛИЗ ЭФФЕКТИВНОСТИ ПО ГОРОДАМ',
        'top_conversion_cities': 'Топ-10 городов по конверсии (≥5 сделок)',
        'additional_metrics': 'ДОПОЛНИТЕЛЬНЫЕ МЕТРИКИ',
        'top_volume_cities': 'Топ-10 городов по объему сделок',
        'total_deals': 'Количество сделок',
        'source_distribution': 'Топ источников по охвату городов',
        'cities_count': 'Городов',
        'traffic_source': 'Источник трафика',
        'german_levels_by_cities': 'УРОВНИ НЕМЕЦКОГО ЯЗЫКА ПО ГОРОДАМ',
        'level_of_german': 'Уровень немецкого',
        'students_count': 'Студентов',
        'german_level_analysis': 'АНАЛИЗ УРОВНЕЙ НЕМЕЦКОГО ЯЗЫКА',
        'conversion_by_level': 'Конверсия по уровням немецкого языка',
        'level': 'Уровень',
        'financial_by_level': 'Финансовые показатели по уровням языка',
        'revenue_by_level': 'Выручка по уровням',
        'avg_revenue_per_student': 'Средняя выручка на студента',
        'level_statistics': 'Статистика по уровням языка:',
        'geography_summary': 'СВОДНАЯ СТАТИСТИКА ПО ГЕОГРАФИИ',
        'city_groups_distribution': 'Распределение городов по объему сделок',
        'group': 'Группа',
        'revenue_share': 'Доля выручки',
        'revenue_per_city': 'Выручка на город',
        'key_geo_metrics': 'Ключевые метрики географии:',
        'cities_with_data': 'Всего городов с данными',
        'cities_5_deals': 'Городов с ≥5 сделками',
        'avg_win_rate_cities': 'Средний Win Rate по городам',
        'top3_revenue_share': 'Доля выручки топ-3 городов',
        'most_common_source': 'Самый частый источник',
        'cities_with_source': 'Городов с этим источником',
        'top3_students_share': 'Доля студентов топ-3 городов',
        
        # Юнит-экономика
        'unit_economics': 'ЮНИТ-ЭКОНОМИКА БИЗНЕСА',
        'total_business_economics': 'ЭКОНОМИКА ВСЕГО БИЗНЕСА',
        'product_economics': 'ЭКОНОМИКА ПО ПРОДУКТАМ',
        'revenue_by_product': 'Выручка по продуктам',
        'ltv_matrix': 'Матрица: Конверсия vs LTV',
        'conversion_c1_axis': 'Конверсия (C1)',
        'ltv_euro': 'LTV (€)',
        'metrics_guide': 'СПРАВОЧНИК МЕТРИК И ФОРМУЛ',
        'metrics_guide_text': """
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
        """,
        
        # Точки роста
        'growth_points_analysis': 'АНАЛИЗ ТОЧКИ РОСТА (SENSITIVITY ANALYSIS)',
        'total_business_analysis': 'АНАЛИЗ ВСЕГО БИЗНЕСА',
        'global_business_scenarios': 'СЦЕНАРИИ РОСТА ДЛЯ ВСЕГО БИЗНЕСА',
        'scenario': 'Сценарий',
        'scenario_type': 'Тип сценария',
        'growth_pct': 'Рост %',
        'transactions': 'Транзакции',
        'cm_growth': 'Рост CM €',
        'best_scenarios': 'Наилучшие сценарии',
        'action': 'Действие',
        'scaling_channels': 'Масштабирование каналов',
        'funnel_optimization': 'Оптимизация воронки',
        'upsell_pricing': 'Up-sell и цены',
        'retention_loyalty': 'Удержание и лояльность',
        'ad_optimization': 'Оптимизация рекламы',
        'sensitivity_analysis': 'АНАЛИЗ ЧУВСТВИТЕЛЬНОСТИ (МИКРО-ИЗМЕНЕНИЯ ±5-10%)',
        'change': 'Изменение',
        'new_value': 'Новое значение',
        'cm_impact': 'Влияние на CM',
        'cm_impact_pct': 'Влияние на CM %',
        'sensitivity_insights': 'Ключевые инсайты по чувствительности:',
        'product_analysis': 'АНАЛИЗ ПО ПРОДУКТАМ (ТОП-ПРОДУКТЫ)',
        'product_scenarios': 'Лучшие сценарии',
        'priority_map': 'СВОДНАЯ КАРТА ПРИОРИТЕТОВ ПО ПРОДУКТАМ',
        'growth_pct_column': 'Рост %',
        'key_insight': 'Ключевой вывод анализа:',
        'key_insight_text': """
        **Ключевой вывод анализа:**
        - Несколько сценариев (C1, AOV, APC) показывают **идентичный математический эффект** на прирост CM
        - Это происходит потому, что в текущей модели:
          - Revenue = UA × C1 × APC × AOV
          - Увеличение ЛЮБОЙ из этих метрик на 10% дает одинаковый рост Revenue
          - AC и COGS не меняются для этих сценариев (кроме UA)

        **Почему выбран фокус на C1 (конверсия):**
        1. **Отсутствие данных о затратах** - у нас нет информации о стоимости изменения каждой метрики
        2. **Стратегические соображения** - улучшение конверсии:
           - Дает синергетический эффект с другими метриками
           - Улучшает пользовательский опыт в целом
           - Часто требует меньших капитальных затрат vs масштабирование трафика (UA)
        3. **Практическая реализуемость** - для C1 уже разработаны:
           - Готовые HADI-циклы
           - Конкретные A/B тесты
           - Измеримые гипотезы

        **Где найти детали реализации:**
        - **Готовые HADI-циклы для тестирования** → вкладка "Дерево метрик и A/B тесты"
        """,
        
        # Методология и A/B тесты
        'methodology_ab_testing': 'МЕТОДОЛОГИЯ И A/B ТЕСТИРОВАНИЕ',
        'business_metrics_tree': 'ДЕРЕВО МЕТРИК БИЗНЕСА',
        'metrics_tree_text': """
        **УРОВЕНЬ 1: Ключевой показатель бизнеса**  
        └── **Маржинальная прибыль (CM)** — Revenue - AC - COGS

        **УРОВЕНЬ 2: Юнит-экономика**  
        ├── **UA (User Acquisition)** — Уникальные контакты → COUNTUNIQUE(CONTACTS['Id'])  
        ├── **C1 (Conversion Rate)** — Конверсия в покупателя → B / UA  
        ├── **CPA (Cost Per Acquisition)** — Стоимость посетителя → AC / UA  
        ├── **AOV (Average Order Value)** — Средний чек → Revenue / T  
        ├── **COGS (Cost of Goods Sold)** — Себестоимость (моделируемая)  
        ├── **APC (Average Payment Count)** — Платежи на клиента → T / B  
        ├── **CPC (Cost Per Click)** — Стоимость клика → AC / Clicks  
        └── **CTR (Click-Through Rate)** — Конверсия в клик → Clicks / Impressions

        **УРОВЕНЬ 2.1: Финансовые показатели**  
        ├── **Оборот (Revenue)** — Сумма поступлений → SUM(DEALS['revenue'])  
        └── **ROMI (Return on Marketing)** — Окупаемость рекламы → CM / AC

        **УРОВЕНЬ 3: Продуктовые метрики**  
        ├── **B (Buyers)** — Уникальные Contact Name со статусом Active Student  
        ├── **AC (Advertising Cost)** — Расходы на рекламу → SUM(SPEND['Spend'])  
        ├── **CAC (Customer Acquisition Cost)** — Стоимость клиента → AC / B  
        ├── **CLTV (Customer Lifetime Value)** — Прибыль с клиента → (AOV - COGS) × APC  
        ├── **LTV (Lifetime Value)** — Ценность посетителя → CLTV × C1  
        └── **T (Transactions)** — Всего транзакций → SUM(DEALS['Transactions'])

        **УРОВЕНЬ 4: Атомные метрики**  
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
        - **B = UA × C1** (Клиенты = Посетители × Конверсия)  
        - **Revenue = AOV × T** (Оборот = Чек × Транзакции)  
        - **T = B × APC** (Транзакции = Клиенты × Частота)  
        - **CAC = AC / B** (Стоимость клиента = Реклама / Клиенты)  
        - **CLTV = (AOV - COGS) × APC** (Ценность клиента = (Чек - Себестоимость) × Частота)  
        - **LTV = CLTV × C1** (Ценность посетителя = Ценность клиента × Конверсия)  
        - **CM = Revenue - AC - COGS** (Маржа = Оборот - Реклама - Себестоимость)  
        - **ROMI = CM / AC** (Окупаемость = Маржа / Реклама)  

        *Прибыль (Profit) не включена — нет данных о постоянных затратах*
        """,
        'hadi_cycles_ab_tests': 'HADI-ЦИКЛЫ И A/B ТЕСТИРОВАНИЕ',
        'ab_test_basics': 'Базовые метрики для A/B тестов:',
        'buyers': 'Покупатели',
        'traffic': 'Общий трафик',
        'conversion': 'Конверсия',
        'ready_hadi_cycles': 'Готовые HADI-циклы для тестирования:',
        'hypothesis': 'Гипотеза',
        'hadi_cycle': 'HADI-цикл:',
        'stage': 'Этап',
        'formulation': 'Формулировка',
        'hadi_cycle_stages': {
            'h': 'Hypothesis (H)',
            'a': 'Action (A)',
            'd': 'Data (D)',
            'i': 'Insight (I)'
        },
        'manager_notification': 'HADI-1. Уведомление менеджера',
        'auto_materials': 'HADI-2. Автоматическая отправка материалов',
        'sms_reminder': 'HADI-3. SMS-напоминание',
        'manager_notification_text': 'Внедрение автоматического уведомления менеджера при поступлении заявки и обязательный первый звонок в течение 1 часа',
        'auto_materials_text': 'Автоматическая отправка email с программой курса и видео-отзывом выпускника в течение 5 минут после заявки',
        'sms_reminder_text': 'Отправка SMS-напоминания о записи на курс через 1 час после пропущенного звонка менеджера',
        'ab_test_params': 'РАСЧЕТ ПАРАМЕТРОВ A/B ТЕСТОВ',
        'ab_test_calc_description': 'Расчет минимального объема выборки и времени для статистически значимых результатов при различных целевых эффектах (MDE).',
        'avg_daily_leads': 'Средний приток лидов в день (на одну группу):',
        'parameter': 'Параметр',
        'description': 'Описание',
        'null_hypothesis': 'Нулевая гипотеза',
        'test_conditions_a': 'Условия проведения A-теста',
        'test_conditions_b': 'Условия проведения B-теста',
        'tracking_metric': 'Метрика для отслеживания',
        'hypothesis_threshold': 'Граница подтверждения гипотезы',
        'significance_level': 'Уровень значимости',
        'leads_per_group': 'Лидов на группу',
        'leads_per_day': 'Лидов/день (группа)',
        'days_for_test': 'Дней для теста',
        'color_legend': 'Легенда цветов:',
        'green_test': '≤14 дней — тест реализуем в стандартном 2-недельном цикле',
        'orange_test': '15-30 дней — требуется продленный тест или увеличение трафика',
        'red_test': '>30 дней — проверка гипотезы затруднена при текущем трафике',
        
        # Сообщения и предупреждения
        'no_unit_economics_data': 'Нет данных для отображения юнит-экономики',
        'no_successful_deals': 'Нет успешных сделок для анализа продуктов',
        'no_city_data': 'Нет данных по городам для анализа',
        'insufficient_data': 'Недостаточно данных для анализа скорости закрытия',
        'no_monthly_data': 'Нет данных для месячного анализа',
        'no_data_for_display': 'Нет данных для отображения',
        
        # Кнопки и элементы
        'select_language': 'Выберите язык',
        'russian': 'Русский',
        'german': 'Немецкий',
        'english': 'English',
        
        # Footer
        'footer': 'Analytics Dashboard • Built by Dmitriy Chumachenko',
    },
    
    'de': {
        # Заголовки и меню
        'full_it_school_analytics': 'VOLLSTÄNDIGER ANALYSEBERICT IT-SCHULE',
        'data_period': 'Datenzeitraum',
        'business_summary': 'ZUSAMMENFASSENDE GESCHÄFTSKENNZAHLEN',
        
        # Метрики бизнеса
        'revenue': 'Umsatz',
        'margin': 'Marge',
        'romi': 'ROMI',
        'ltv': 'LTV',
        'conversion_c1': 'Konversion C1',
        'marketing_spend': 'Marketingausgaben',
        'ua': 'UA',
        'successful_deals': 'Erfolgreiche Deals',
        'unique_clients': 'Einzigartige Kunden',
        'aov_per_transaction': 'AOV pro Transaktion',
        'aov_per_client': 'AOV pro Kunde',
        'traffic_sources': 'Trafficquellen',
        'cities': 'Städte',
        'managers': 'Manager',
        'products': 'Produkte',
        'top_product': 'Top-Produkt',
        'no_data': 'Keine Daten',
        
        # Названия вкладок
        'marketing_tab': 'MARKETING',
        'sales_tab': 'VERTRIEB',
        'products_tab': 'PRODUKTE',
        'geography_tab': 'GEOGRAFIE/SPRACHEN',
        'unit_economics_tab': 'UNIT-ECONOMICS',
        'growth_points_tab': 'WACHSTUMSCHANCEN',
        'metrics_tree_tab': 'KENNZAHLENBAUM & A/B TESTS',
        
        # Маркетинг
        'marketing_analytics': 'MARKETINGANALYTIK',
        'marketing_funnel': 'MARKETING-TRICHTER UND AUSGABENEFFIZIENZ',
        'paid_sources_analysis': 'ANALYSE BEZAHLTER QUELLEN: CPC vs QUALITÄT',
        'source_efficiency_matrix': 'QUELLEN-EFFIZIENZ-MATRIX: GESCHWINDIGKEIT VS CHECK',
        'roas_by_sources': 'ROAS NACH TRAFFICQUELLEN',
        'campaign_analysis': 'KAMPAGNENANALYSE NACH EFFIZIENZ',
        'conversion_funnel': 'Konversionstrichter nach Kanälen (Log-Skala)',
        'cost_per_result': 'Kosten pro Ergebnis',
        'marketing_analytics_volumes': 'Marketinganalytik: Volumen und Geld',
        'source': 'Quelle',
        'spend': 'Ausgaben',
        'clicks': 'Klicks',
        'leads': 'Leads',
        'students': 'Studenten',
        'cpc': 'CPC',
        'cpl': 'CPL',
        'cps': 'CPS',
        'cpc_vs_conversion': 'CPC vs Lead-to-Student-Konversion',
        'cpcl': 'Kosten pro Klick (€)',
        'conversion_percent': 'Konversion (%)',
        'median_cpc': 'Durchschn. CPC',
        'median_conversion': 'Durchschn. Konversion',
        'detailed_source_stats': 'Detaillierte Quellenstatistiken:',
        'speed_vs_check': 'Quellenmatrix: Geschwindigkeit (X) vs Durchschn. Check (Y)',
        'median_speed_days': 'Median Schließgeschwindigkeit (Tage)',
        'avg_check_euro': 'Durchschnittlicher Check (€)',
        'avg_speed': 'Durchschn. Geschwindigkeit',
        'avg_check': 'Durchschn. Check',
        'leads_finance_details': 'Details zu Leads und Finanzen:',
        'quality_leads': 'Qualitätsleads',
        'quality_percent': 'Qualität %',
        'conversion_percent_short': 'Konv. %',
        'avg_check_full': 'Durchschnittlicher Check',
        'roas_analysis': 'ROAS: Rentabilität der Quellen',
        'roas_percent': 'ROAS (%)',
        'breakeven_point': 'Break-Even-Punkt',
        'top_campaigns_efficiency': 'TOP-15 Kampagnen nach Effizienz (Studenten / Leads)',
        'efficiency_ratio': 'Lead-zu-Student-Konversion (%)',
        'campaign': 'Kampagne',
        'detailed_campaign_stats': 'Detaillierte Kampagnenstatistiken:',
        
        # Продажи
        'sales_efficiency': 'VERTRIEBSEFFIZIENZ (KPI 360°)',
        'calls_dynamics_analysis': 'ANALYSE DER ANRUFDYNAMIK UND AUSWIRKUNGEN',
        'leads_calls_sales_dynamics': 'DYNAMIK VON LEADS, ANRUFEN UND VERKÄUFEN',
        'incoming_leads': 'Eingehende Leads',
        'sales_multiplied': 'Verkäufe (×50)',
        'calls': 'Anrufe',
        'calls_impact_on_sales': 'Einfluss von Anrufen auf Verkäufe (nach Wochen)',
        'number_of_calls': 'Anzahl Anrufe',
        'number_of_sales': 'Anzahl Verkäufe',
        'leads_volume': 'Lead-Volumen',
        'weekly_conversion': 'Wochenkonversion (%)',
        'correlation_analysis': 'Korrelationsanalyse:',
        'calls_sales_correlation': 'Korrelation "Anrufe → Verkäufe"',
        'leads_sales_correlation': 'Korrelation "Leads → Verkäufe"',
        'correlation_insight': 'Fazit: Schwache Korrelation (0,43-0,54). Kein direkter linearer Zusammenhang zwischen Anrufen/Leads und Verkäufen innerhalb einer Woche.',
        'calls_distribution': 'VERTEILUNG DER ANRUFE BIS ZUM VERKAUF',
        'calls_count': 'Anzahl Anrufe',
        'deals_count': 'Anzahl Deals',
        'median': 'Median',
        'average': 'Durchschnitt',
        'deal_speed': 'ABSCHLUSSGESCHWINDIGKEIT',
        'success_deal_duration': 'Verteilung der Abschlussdauer erfolgreicher Deals (Schritt = 5 Tage)',
        'deal_duration_days': 'Dealdauer (Tage)',
        'metric': 'Kennzahl',
        'days': 'Tage',
        'mean': 'Mittelwert',
        'minimum': 'Minimum',
        'maximum': 'Maximum',
        'manager_speed': 'Abschlussgeschwindigkeit nach Managern (nur ≥3 Deals)',
        'manager': 'Manager',
        'deals_count_full': 'Anzahl Deals',
        'median_full': 'Median',
        'monthly_dynamics': 'MONATSDYNAMIK: UMSATZ, STUDENTEN UND LEADS',
        'revenue_students': 'UMSATZ UND AKTIVE STUDENTEN',
        'leads_conversion': 'LEADS UND KONVERSION',
        'revenue_euro': 'Umsatz (€)',
        'active_students': 'Aktive Studenten',
        'total_leads': 'Gesamt Leads',
        'conversion_rate': 'Konversion (%)',
        'month': 'Monat',
        'detailed_monthly_stats': 'Detaillierte Monatsstatistiken:',
        'month_year': 'Monat-Jahr',
        'active_students_count': 'Aktive Studenten',
        'top_managers': 'TOP MANAGER NACH UMSATZ UND KONVERSION',
        'top_managers_revenue': 'TOP-15 Manager nach Umsatz (Farbe = Konversion Win Rate)',
        'win_rate': 'Win Rate (%)',
        'top_conversion': 'TOP nach Konversion (Farbe = Abschlussgeschwindigkeit, Tage)',
        'avg_deal_cycle': 'Durchschn. Deal-Zyklus (Tage)',
        'detailed_manager_stats': 'DETAILMANAGERSTATISTIKEN',
        'speed_quality_analysis': 'ANALYSE DER ANTWORTGESCHWINDIGKEIT (SLA) UND LEAD-QUALITÄT',
        'conversion_by_speed': 'Konversion nach Antwortgeschwindigkeits-Segmenten',
        'sla_segment': 'SLA_Segment',
        'conversion_by_quality': 'Konversion nach Lead-Qualität (nur Kategorien mit >10 Leads)',
        'quality': 'Qualität',
        'speed_vs_conversion': 'Antwortgeschwindigkeit vs Konversion nach Managern',
        'median_sla_hours': 'Median Antwortzeit (Stunden)',
        'manager_sla': 'Antwortgeschwindigkeit nach Managern:',
        'deals': 'Deals',
        'median_hours': 'Median (Std)',
        'mean_hours': 'Mittelwert (Std)',
        'conversion_deciles': 'Konversion vs Antwortzeit (Dezile)',
        'response_time_min': 'Antwortzeit (Min)',
        'sla_metrics': 'Schlüsselmetriken der Antwortgeschwindigkeit:',
        'response_time': 'Antwortzeit',
        'average_time': 'Durchschnittszeit',
        'median_time': 'Medianzeit',
        'faster_25': '25% Deals schneller',
        'faster_75': '75% Deals schneller',
        'lost_reasons_analysis': 'ANALYSE DER ABBRUCHGRÜNDE NACH MANAGERN',
        'lost_reasons_distribution': 'Verteilung der Abbruchgründe nach Managern:',
        'lost_reason': 'Grund',
        'total': 'GESAMT',
        'share_percent': 'Anteil %',
        'total_distribution': 'Gesamtverteilung der Abbruchgründe:',
        
        # Продукты
        'products_payments_analysis': 'PRODUKT- UND ZAHLUNGSANALYSE',
        'full_product_metrics': 'VOLLSTÄNDIGE PRODUKTMETRIKEN',
        'product': 'Produkt',
        'clients': 'Kunden',
        'avg_contract': 'Durchschn. Vertrag',
        'collection_ratio': 'Vertragsbezahlung %',
        'cltv_full': 'CLTV',
        'ltv_full': 'LTV',
        'cac_full': 'CAC',
        'cm_full': 'CM',
        'product_efficiency': 'VISUALISIERUNGEN DER PRODUKTEFFIZIENZ',
        'revenue_by_products': 'Umsatz nach Produkten (Farbe = LTV)',
        'revenue_euro_full': 'Umsatz (€)',
        'product_matrix': 'Produktmatrix: Kunden vs Durchschn. Check',
        'clients_count': 'Anzahl Kunden',
        'payment_type_analysis': 'ANALYSE DER ZAHLUNGSARTEN',
        'payment_type_distribution': 'Verteilung der Zahlungsarten nach Produkten',
        'education_type_analysis': 'ANALYSE DER BILDUNGSARTEN',
        'education_type': 'Bildungsart',
        'revenue_by_education': 'Umsatz nach Bildungsarten (Farbe = Durchschn. Check)',
        
        # География
        'geographical_analysis': 'GEOGRAFISCHE ANALYSE',
        'sales_map': 'VERKAUFSKARTE',
        'top_cities_revenue': 'TOP STÄDTE NACH UMSATZ',
        'city': 'Stadt',
        'top_source': 'Top-Quelle',
        'city_efficiency_analysis': 'EFFIZIENZANALYSE NACH STÄDTEN',
        'top_conversion_cities': 'Top-10 Städte nach Konversion (≥5 Deals)',
        'additional_metrics': 'ZUSÄTZLICHE METRIKEN',
        'top_volume_cities': 'Top-10 Städte nach Deal-Volumen',
        'total_deals': 'Anzahl Deals',
        'source_distribution': 'Top-Quellen nach Stadtabdeckung',
        'cities_count': 'Städte',
        'traffic_source': 'Trafficquelle',
        'german_levels_by_cities': 'DEUTSCHNIVEAUS NACH STÄDTEN',
        'level_of_german': 'Deutschniveau',
        'students_count': 'Studenten',
        'german_level_analysis': 'ANALYSE DER DEUTSCHNIVEAUS',
        'conversion_by_level': 'Konversion nach Deutschniveaus',
        'level': 'Niveau',
        'financial_by_level': 'Finanzkennzahlen nach Sprachniveaus',
        'revenue_by_level': 'Umsatz nach Niveaus',
        'avg_revenue_per_student': 'Durchschn. Umsatz pro Student',
        'level_statistics': 'Statistik nach Sprachniveaus:',
        'geography_summary': 'ZUSAMMENFASSENDE GEOGRAFIE-STATISTIK',
        'city_groups_distribution': 'Verteilung der Städte nach Deal-Volumen',
        'group': 'Gruppe',
        'revenue_share': 'Umsatzanteil',
        'revenue_per_city': 'Umsatz pro Stadt',
        'key_geo_metrics': 'Schlüsselmetriken der Geografie:',
        'cities_with_data': 'Gesamt Städte mit Daten',
        'cities_5_deals': 'Städte mit ≥5 Deals',
        'avg_win_rate_cities': 'Durchschn. Win Rate der Städte',
        'top3_revenue_share': 'Umsatzanteil Top-3 Städte',
        'most_common_source': 'Häufigste Quelle',
        'cities_with_source': 'Städte mit dieser Quelle',
        'top3_students_share': 'Studentenanteil Top-3 Städte',
        
        # Юнит-экономика
        'unit_economics': 'UNIT-ECONOMICS DES GESCHÄFTS',
        'total_business_economics': 'ECONOMICS DES GESAMTEN GESCHÄFTS',
        'product_economics': 'ECONOMICS NACH PRODUKTEN',
        'revenue_by_product': 'Umsatz nach Produkten',
        'ltv_matrix': 'Matrix: Konversion vs LTV',
        'conversion_c1_axis': 'Konversion (C1)',
        'ltv_euro': 'LTV (€)',
        'metrics_guide': 'METRIKEN-LEITFADEN UND FORMELN',
        'metrics_guide_text': """
        **0. AUSGANGSDATEN:**
        - **UA** = Einzigartige Kontakte (CONTACTS['Id'].nunique())
        - **B** = Einzigartige zahlende Kunden (Contact Name mit Status Active Student)
        - **AC** = Gesamtes Marketingbudget der Schule (Spend['Spend'].sum())
        
        **1. BASISMETRIKEN:**
        - **C1** = B / UA (Konversion vom Besucher zum Käufer)
        - **Revenue** = Tatsächlich erhaltenes Geld (First payment + Recurring payments)
        
        **2. TRANSAKTIONSMETRIKEN:**
        - **T** = Anzahl Zahlungen (wenn Ratenzahlung = Studienmonate, wenn einmalig = 1)
        - **AOV** = Revenue / T (Durchschn. Check EINER Transaktion)
        - **APC** = T / B (Wie oft zahlt ein Student durchschn.)
        
        **3. KOSTEN:**
        - **COGS** = Selbstkosten EINER Transaktion (Gebühren, Steuern)
        - **CPA** = AC / UA (Preis eines Leads)
        - **CAC** = AC / B (Preis eines Kunden)
        
        **4. ECONOMICS (GEWINN):**
        - **CLTV** = (AOV - COGS) × APC (Gewinn pro ZAHLENDEM Kunden)
        - **LTV** = CLTV × C1 (Gewinn pro BESUCHER - wichtigste Metrik)
        - **CM** = Revenue - AC - COGS (Deckungsbeitrag)
        - **ROMI** = CM / AC × 100% (Rentabilität der Werbung)
        """,
        
        # Точки роста
        'growth_points_analysis': 'WACHSTUMSPUNKTANALYSE (SENSITIVITY ANALYSIS)',
        'total_business_analysis': 'ANALYSE DES GESAMTEN GESCHÄFTS',
        'global_business_scenarios': 'WACHSTUMSSZENARIEN FÜR DAS GESAMTE GESCHÄFT',
        'scenario': 'Szenario',
        'scenario_type': 'Szenariotyp',
        'growth_pct': 'Wachstum %',
        'transactions': 'Transaktionen',
        'cm_growth': 'CM-Wachstum €',
        'best_scenarios': 'Beste Szenarien',
        'action': 'Aktion',
        'scaling_channels': 'Kanal-Skalierung',
        'funnel_optimization': 'Trichteroptimierung',
        'upsell_pricing': 'Up-Sell und Preise',
        'retention_loyalty': 'Bindung und Loyalität',
        'ad_optimization': 'Werbeoptimierung',
        'sensitivity_analysis': 'SENSITIVITÄTSANALYSE (MIKRO-VERÄNDERUNGEN ±5-10%)',
        'change': 'Veränderung',
        'new_value': 'Neuer Wert',
        'cm_impact': 'Auswirkung auf CM',
        'cm_impact_pct': 'Auswirkung auf CM %',
        'sensitivity_insights': 'Schlüsseleinsichten zur Sensitivität:',
        'product_analysis': 'PRODUKTANALYSE (TOP-PRODUKTE)',
        'product_scenarios': 'Beste Szenarien',
        'priority_map': 'ZUSAMMENFASSENDE PRIORITÄTENKARTE NACH PRODUKTEN',
        'growth_pct_column': 'Wachstum %',
        'key_insight': 'Schlüsselerkenntnis der Analyse:',
        'key_insight_text': """
        **Schlüsselerkenntnis der Analyse:**
        - Mehrere Szenarien (C1, AOV, APC) zeigen **identische mathematische Effekte** auf CM-Wachstum
        - Dies passiert, weil im aktuellen Modell:
          - Revenue = UA × C1 × APC × AOV
          - Eine Erhöhung JEDER dieser Metriken um 10% gibt gleichen Revenue-Wachstum
          - AC und COGS ändern sich für diese Szenarien nicht (außer UA)

        **Warum Fokus auf C1 (Konversion):**
        1. **Fehlende Kostendaten** - wir haben keine Informationen über Kosten der Veränderung jeder Metrik
        2. **Strategische Überlegungen** - Konversionsverbesserung:
           - Gibt synergetischen Effekt mit anderen Metriken
           - Verbessert gesamte Nutzererfahrung
           - Benötigt oft weniger Kapitalaufwand vs Traffic-Skalierung (UA)
        3. **Praktische Umsetzbarkeit** - für C1 bereits entwickelt:
           - Fertige HADI-Zyklen
           - Konkrete A/B Tests
           - Messbare Hypothesen

        **Wo Implementierungsdetails zu finden:**
        - **Fertige HADI-Zyklen für Tests** → Tab "Kennzahlenbaum & A/B Tests"
        """,
        
        # Методология и A/B тесты
        'methodology_ab_testing': 'METHODIK UND A/B TESTS',
        'business_metrics_tree': 'KENNZAHLENBAUM DES GESCHÄFTS',
        'metrics_tree_text': """
        **EBENE 1: Schlüsselkennzahl des Geschäfts**  
        └── **Deckungsbeitrag (CM)** — Revenue - AC - COGS

        **EBENE 2: Unit-Economics**  
        ├── **UA (User Acquisition)** — Einzigartige Kontakte → COUNTUNIQUE(CONTACTS['Id'])  
        ├── **C1 (Conversion Rate)** — Konversion zum Käufer → B / UA  
        ├── **CPA (Cost Per Acquisition)** — Besucherkosten → AC / UA  
        ├── **AOV (Average Order Value)** — Durchschn. Check → Revenue / T  
        ├── **COGS (Cost of Goods Sold)** — Selbstkosten (modelliert)  
        ├── **APC (Average Payment Count)** — Zahlungen pro Kunde → T / B  
        ├── **CPC (Cost Per Click)** — Klickkosten → AC / Clicks  
        └── **CTR (Click-Through Rate)** — Klick-Konversion → Clicks / Impressions

        **EBENE 2.1: Finanzkennzahlen**  
        ├── **Umsatz (Revenue)** — Summe Einnahmen → SUM(DEALS['revenue'])  
        └── **ROMI (Return on Marketing)** — Werberentabilität → CM / AC

        **EBENE 3: Produktmetriken**  
        ├── **B (Buyers)** — Einzigartige Contact Name mit Status Active Student  
        ├── **AC (Advertising Cost)** — Werbeausgaben → SUM(SPEND['Spend'])  
        ├── **CAC (Customer Acquisition Cost)** — Kundenakquisitionskosten → AC / B  
        ├── **CLTV (Customer Lifetime Value)** — Kundenwert → (AOV - COGS) × APC  
        ├── **LTV (Lifetime Value)** — Besucherwert → CLTV × C1  
        └── **T (Transactions)** — Gesamttransaktionen → SUM(DEALS['Transactions'])

        **EBENE 4: Atomare Metriken**  
        ├── DEALS['Created Time'] — Lead-Erstellungsdatum  
        ├── DEALS['Closing Date'] — Deal-Abschlussdatum  
        ├── DEALS['Source'] / SPEND['Source'] — Trafficquelle  
        ├── DEALS['Campaign'] — Kampagne  
        ├── DEALS['Product'] — Kursart  
        ├── DEALS['Stage'] — Trichterstadium  
        ├── DEALS['Quality'] — Lead-Qualität  
        ├── DEALS['City'] — Geografie  
        ├── SPEND['Clicks'] — Werbeklicks  
        └── SPEND['Impressions'] — Werbeeinblendungen

        **EBENE 5: Standardmetriken (Monitoring)**  
        ├── DEALS['SLA'] — Antwortzeit  
        ├── DEALS['Level of Deutsch'] — Sprachniveau  
        ├── DEALS['Course duration'] — Kursdauer  
        ├── CALLS['Call Duration (in seconds)'] — Anrufdauer  
        ├── CALLS['Call Type'] — Anruftyp  
        ├── CALLS['Call Status'] — Anrufstatus  
        ├── SPEND['AdGroup'] — Anzeigengruppe  
        └── SPEND['Ad'] — Konkrete Anzeige

        **SCHLÜSSELABHÄNGIGKEITEN**  
        - **B = UA × C1** (Kunden = Besucher × Konversion)  
        - **Revenue = AOV × T** (Umsatz = Check × Transaktionen)  
        - **T = B × APC** (Transaktionen = Kunden × Häufigkeit)  
        - **CAC = AC / B** (Kundenkosten = Werbung / Kunden)  
        - **CLTV = (AOV - COGS) × APC** (Kundenwert = (Check - Selbstkosten) × Häufigkeit)  
        - **LTV = CLTV × C1** (Besucherwert = Kundenwert × Konversion)  
        - **CM = Revenue - AC - COGS** (Deckungsbeitrag = Umsatz - Werbung - Selbstkosten)  
        - **ROMI = CM / AC** (Rentabilität = Deckungsbeitrag / Werbung)  

        *Gewinn (Profit) nicht enthalten — keine Daten zu Fixkosten*
        """,
        'hadi_cycles_ab_tests': 'HADI-ZYKLEN UND A/B TESTS',
        'ab_test_basics': 'Basis-Metriken für A/B Tests:',
        'buyers': 'Käufer',
        'traffic': 'Gesamttraffic',
        'conversion': 'Konversion',
        'ready_hadi_cycles': 'Fertige HADI-Zyklen für Tests:',
        'hypothesis': 'Hypothese',
        'hadi_cycle': 'HADI-Zyklus:',
        'stage': 'Stufe',
        'formulation': 'Formulierung',
        'hadi_cycle_stages': {
            'h': 'Hypothesis (H)',
            'a': 'Action (A)',
            'd': 'Data (D)',
            'i': 'Insight (I)'
        },
        'manager_notification': 'HADI-1. Managerbenachrichtigung',
        'auto_materials': 'HADI-2. Automatischer Materialversand',
        'sms_reminder': 'HADI-3. SMS-Erinnerung',
        'manager_notification_text': 'Einführung automatischer Managerbenachrichtigung bei Antragseingang und verbindlicher erster Anruf innerhalb 1 Stunde',
        'auto_materials_text': 'Automatischer Email-Versand mit Kursprogramm und Video-Erfahrungsbericht innerhalb 5 Minuten nach Antrag',
        'sms_reminder_text': 'SMS-Erinnerung zur Kurseinschreibung 1 Stunde nach verpasstem Manageranruf',
        'ab_test_params': 'BERECHNUNG VON A/B TEST-PARAMETERN',
        'ab_test_calc_description': 'Berechnung minimaler Stichprobenumfang und Zeit für statistisch signifikante Ergebnisse bei verschiedenen Zielwirkungen (MDE).',
        'avg_daily_leads': 'Durchschn. täglicher Lead-Zufluss (pro Gruppe):',
        'parameter': 'Parameter',
        'description': 'Beschreibung',
        'null_hypothesis': 'Nullhypothese',
        'test_conditions_a': 'Bedingungen für A-Test',
        'test_conditions_b': 'Bedingungen für B-Test',
        'tracking_metric': 'Metrik zur Verfolgung',
        'hypothesis_threshold': 'Hypothesenbestätigungsschwelle',
        'significance_level': 'Signifikanzniveau',
        'leads_per_group': 'Leads pro Gruppe',
        'leads_per_day': 'Leads/Tag (Gruppe)',
        'days_for_test': 'Tage für Test',
        'color_legend': 'Farblegende:',
        'green_test': '≤14 Tage — Test realisierbar im Standard 2-Wochen-Zyklus',
        'orange_test': '15-30 Tage — Verlängerter Test oder Traffic-Erhöhung benötigt',
        'red_test': '>30 Tage — Hypothesenprüfung schwierig bei aktuellem Traffic',
        
        # Сообщения и предупреждения
        'no_unit_economics_data': 'Keine Daten für Unit-Economics-Anzeige',
        'no_successful_deals': 'Keine erfolgreichen Deals für Produktanalyse',
        'no_city_data': 'Keine Städtendaten für Analyse',
        'insufficient_data': 'Unzureichende Daten für Abschlussgeschwindigkeitsanalyse',
        'no_monthly_data': 'Keine Daten für Monatsanalyse',
        'no_data_for_display': 'Keine Daten zur Anzeige',
        
        # Кнопки и элементы
        'select_language': 'Sprache auswählen',
        'russian': 'Russisch',
        'german': 'Deutsch',
        'english': 'Englisch',
        
        # Footer
        'footer': 'Analytics Dashboard • Erstellt von Dmitriy Chumachenko',
    },
    
    'en': {
        # Заголовки и меню
        'full_it_school_analytics': 'COMPLETE IT SCHOOL ANALYTICS REPORT',
        'data_period': 'Data period',
        'business_summary': 'BUSINESS SUMMARY METRICS',
        
        # Метрики бизнеса
        'revenue': 'Revenue',
        'margin': 'Margin',
        'romi': 'ROMI',
        'ltv': 'LTV',
        'conversion_c1': 'Conversion C1',
        'marketing_spend': 'Marketing spend',
        'ua': 'UA',
        'successful_deals': 'Successful deals',
        'unique_clients': 'Unique clients',
        'aov_per_transaction': 'AOV per transaction',
        'aov_per_client': 'AOV per client',
        'traffic_sources': 'Traffic sources',
        'cities': 'Cities',
        'managers': 'Managers',
        'products': 'Products',
        'top_product': 'Top product',
        'no_data': 'No data',
        
        # Названия вкладок
        'marketing_tab': 'MARKETING',
        'sales_tab': 'SALES',
        'products_tab': 'PRODUCTS',
        'geography_tab': 'GEOGRAPHY/LANGUAGES',
        'unit_economics_tab': 'UNIT ECONOMICS',
        'growth_points_tab': 'GROWTH POINTS',
        'metrics_tree_tab': 'METRICS TREE & A/B TESTS',
        
        # Маркетинг
        'marketing_analytics': 'MARKETING ANALYTICS',
        'marketing_funnel': 'MARKETING FUNNEL AND SPEND EFFICIENCY',
        'paid_sources_analysis': 'PAID SOURCES ANALYSIS: CPC vs QUALITY',
        'source_efficiency_matrix': 'SOURCE EFFICIENCY MATRIX: SPEED VS CHECK',
        'roas_by_sources': 'ROAS BY TRAFFIC SOURCES',
        'campaign_analysis': 'CAMPAIGN ANALYSIS BY EFFICIENCY',
        'conversion_funnel': 'Conversion funnel by channels (Log Scale)',
        'cost_per_result': 'Cost per result',
        'marketing_analytics_volumes': 'Marketing analytics: Volumes and Money',
        'source': 'Source',
        'spend': 'Spend',
        'clicks': 'Clicks',
        'leads': 'Leads',
        'students': 'Students',
        'cpc': 'CPC',
        'cpl': 'CPL',
        'cps': 'CPS',
        'cpc_vs_conversion': 'CPC vs Lead-to-Student conversion',
        'cpcl': 'Cost per click (€)',
        'conversion_percent': 'Conversion (%)',
        'median_cpc': 'Avg. CPC',
        'median_conversion': 'Avg. Conversion',
        'detailed_source_stats': 'Detailed source statistics:',
        'speed_vs_check': 'Sources Matrix: Speed (X) vs Avg. Check (Y)',
        'median_speed_days': 'Median closing speed (days)',
        'avg_check_euro': 'Average check (€)',
        'avg_speed': 'Avg. speed',
        'avg_check': 'Avg. check',
        'leads_finance_details': 'Leads and finance details:',
        'quality_leads': 'Quality leads',
        'quality_percent': 'Quality %',
        'conversion_percent_short': 'Conv. %',
        'avg_check_full': 'Average check',
        'roas_analysis': 'ROAS: Sources profitability',
        'roas_percent': 'ROAS (%)',
        'breakeven_point': 'Breakeven point',
        'top_campaigns_efficiency': 'TOP-15 campaigns by efficiency (students / leads)',
        'efficiency_ratio': 'Lead-to-student conversion (%)',
        'campaign': 'Campaign',
        'detailed_campaign_stats': 'Detailed campaign statistics:',
        
        # Продажи
        'sales_efficiency': 'SALES DEPARTMENT EFFICIENCY (KPI 360°)',
        'calls_dynamics_analysis': 'CALLS DYNAMICS AND IMPACT ANALYSIS',
        'leads_calls_sales_dynamics': 'LEADS, CALLS AND SALES DYNAMICS',
        'incoming_leads': 'Incoming Leads',
        'sales_multiplied': 'Sales (×50)',
        'calls': 'Calls',
        'calls_impact_on_sales': 'Calls impact on sales (by weeks)',
        'number_of_calls': 'Number of Calls',
        'number_of_sales': 'Number of Sales',
        'leads_volume': 'Leads volume',
        'weekly_conversion': 'Weekly conversion (%)',
        'correlation_analysis': 'Correlation analysis:',
        'calls_sales_correlation': 'Correlation "Calls → Sales"',
        'leads_sales_correlation': 'Correlation "Leads → Sales"',
        'correlation_insight': 'Conclusion: Weak correlation (0.43-0.54). No direct linear relationship between calls/leads and sales within one week.',
        'calls_distribution': 'CALLS DISTRIBUTION BEFORE SALE',
        'calls_count': 'Number of calls',
        'deals_count': 'Number of deals',
        'median': 'Median',
        'average': 'Average',
        'deal_speed': 'DEAL CLOSING SPEED',
        'success_deal_duration': 'Successful deal closing time distribution (Step = 5 days)',
        'deal_duration_days': 'Deal duration (days)',
        'metric': 'Metric',
        'days': 'Days',
        'mean': 'Mean',
        'minimum': 'Minimum',
        'maximum': 'Maximum',
        'manager_speed': 'Closing speed by managers (only ≥3 deals)',
        'manager': 'Manager',
        'deals_count_full': 'Number of deals',
        'median_full': 'Median',
        'monthly_dynamics': 'MONTHLY DYNAMICS: REVENUE, STUDENTS AND LEADS',
        'revenue_students': 'REVENUE AND ACTIVE STUDENTS',
        'leads_conversion': 'LEADS AND CONVERSION',
        'revenue_euro': 'Revenue (€)',
        'active_students': 'Active students',
        'total_leads': 'Total leads',
        'conversion_rate': 'Conversion (%)',
        'month': 'Month',
        'detailed_monthly_stats': 'Detailed monthly statistics:',
        'month_year': 'Month-Year',
        'active_students_count': 'Active students',
        'top_managers': 'TOP MANAGERS BY REVENUE AND CONVERSION',
        'top_managers_revenue': 'TOP-15 Managers by Revenue (Color = Win Rate conversion)',
        'win_rate': 'Win Rate (%)',
        'top_conversion': 'TOP by conversion (Color = Closing speed, days)',
        'avg_deal_cycle': 'Avg. deal cycle (days)',
        'detailed_manager_stats': 'DETAILED MANAGER STATISTICS',
        'speed_quality_analysis': 'RESPONSE SPEED (SLA) AND LEAD QUALITY ANALYSIS',
        'conversion_by_speed': 'Conversion by response speed segments',
        'sla_segment': 'SLA_Segment',
        'conversion_by_quality': 'Conversion by lead quality (only categories with >10 leads)',
        'quality': 'Quality',
        'speed_vs_conversion': 'Response speed vs Conversion by managers',
        'median_sla_hours': 'Median response time (hours)',
        'manager_sla': 'Response speed by managers:',
        'deals': 'Deals',
        'median_hours': 'Median (h)',
        'mean_hours': 'Mean (h)',
        'conversion_deciles': 'Conversion vs Response time (deciles)',
        'response_time_min': 'Response time (min)',
        'sla_metrics': 'Key response speed metrics:',
        'response_time': 'Response time',
        'average_time': 'Average time',
        'median_time': 'Median time',
        'faster_25': '25% deals faster',
        'faster_75': '75% deals faster',
        'lost_reasons_analysis': 'LOST REASONS ANALYSIS BY MANAGERS',
        'lost_reasons_distribution': 'Lost reasons distribution by managers:',
        'lost_reason': 'Reason',
        'total': 'TOTAL',
        'share_percent': 'Share %',
        'total_distribution': 'Total lost reasons distribution:',
        
        # Продукты
        'products_payments_analysis': 'PRODUCTS AND PAYMENTS ANALYSIS',
        'full_product_metrics': 'FULL PRODUCT METRICS',
        'product': 'Product',
        'clients': 'Clients',
        'avg_contract': 'Avg. contract',
        'collection_ratio': 'Contract payment %',
        'cltv_full': 'CLTV',
        'ltv_full': 'LTV',
        'cac_full': 'CAC',
        'cm_full': 'CM',
        'product_efficiency': 'PRODUCT EFFICIENCY VISUALIZATIONS',
        'revenue_by_products': 'Revenue by products (Color = LTV)',
        'revenue_euro_full': 'Revenue (€)',
        'product_matrix': 'Product matrix: Clients vs Avg. check',
        'clients_count': 'Number of clients',
        'payment_type_analysis': 'PAYMENT TYPES ANALYSIS',
        'payment_type_distribution': 'Payment types distribution by products',
        'education_type_analysis': 'EDUCATION TYPES ANALYSIS',
        'education_type': 'Education type',
        'revenue_by_education': 'Revenue by education types (Color = Avg. check)',
        
        # География
        'geographical_analysis': 'GEOGRAPHICAL ANALYSIS',
        'sales_map': 'SALES MAP',
        'top_cities_revenue': 'TOP CITIES BY REVENUE',
        'city': 'City',
        'top_source': 'Top source',
        'city_efficiency_analysis': 'EFFICIENCY ANALYSIS BY CITIES',
        'top_conversion_cities': 'Top-10 cities by conversion (≥5 deals)',
        'additional_metrics': 'ADDITIONAL METRICS',
        'top_volume_cities': 'Top-10 cities by deal volume',
        'total_deals': 'Number of deals',
        'source_distribution': 'Top sources by city coverage',
        'cities_count': 'Cities',
        'traffic_source': 'Traffic source',
        'german_levels_by_cities': 'GERMAN LEVELS BY CITIES',
        'level_of_german': 'German level',
        'students_count': 'Students',
        'german_level_analysis': 'GERMAN LEVELS ANALYSIS',
        'conversion_by_level': 'Conversion by German levels',
        'level': 'Level',
        'financial_by_level': 'Financial metrics by language levels',
        'revenue_by_level': 'Revenue by levels',
        'avg_revenue_per_student': 'Avg. revenue per student',
        'level_statistics': 'Statistics by language levels:',
        'geography_summary': 'GEOGRAPHY SUMMARY STATISTICS',
        'city_groups_distribution': 'Cities distribution by deal volume',
        'group': 'Group',
        'revenue_share': 'Revenue share',
        'revenue_per_city': 'Revenue per city',
        'key_geo_metrics': 'Key geography metrics:',
        'cities_with_data': 'Total cities with data',
        'cities_5_deals': 'Cities with ≥5 deals',
        'avg_win_rate_cities': 'Avg. Win Rate of cities',
        'top3_revenue_share': 'Revenue share top-3 cities',
        'most_common_source': 'Most common source',
        'cities_with_source': 'Cities with this source',
        'top3_students_share': 'Students share top-3 cities',
        
        # Юнит-экономика
        'unit_economics': 'BUSINESS UNIT ECONOMICS',
        'total_business_economics': 'TOTAL BUSINESS ECONOMICS',
        'product_economics': 'ECONOMICS BY PRODUCTS',
        'revenue_by_product': 'Revenue by products',
        'ltv_matrix': 'Matrix: Conversion vs LTV',
        'conversion_c1_axis': 'Conversion (C1)',
        'ltv_euro': 'LTV (€)',
        'metrics_guide': 'METRICS GUIDE AND FORMULAS',
        'metrics_guide_text': """
        **0. SOURCE DATA:**
        - **UA** = Unique contacts (CONTACTS['Id'].nunique())
        - **B** = Unique paying clients (Contact Name with Active Student status)
        - **AC** = Total marketing budget of school (Spend['Spend'].sum())
        
        **1. BASIC METRICS:**
        - **C1** = B / UA (Conversion from visitor to buyer)
        - **Revenue** = Actually received money (First payment + Recurring payments)
        
        **2. TRANSACTION METRICS:**
        - **T** = Number of payments (if installment = months of study, if one-time = 1)
        - **AOV** = Revenue / T (Average check of ONE transaction)
        - **APC** = T / B (How many times student pays on average)
        
        **3. COSTS:**
        - **COGS** = Cost of ONE transaction (fees, taxes)
        - **CPA** = AC / UA (Price of one lead)
        - **CAC** = AC / B (Price of one customer)
        
        **4. ECONOMICS (PROFIT):**
        - **CLTV** = (AOV - COGS) × APC (Profit per PAYING customer)
        - **LTV** = CLTV × C1 (Profit per VISITOR - most important metric)
        - **CM** = Revenue - AC - COGS (Contribution margin)
        - **ROMI** = CM / AC × 100% (Advertising profitability)
        """,
        
        # Точки роста
        'growth_points_analysis': 'GROWTH POINTS ANALYSIS (SENSITIVITY ANALYSIS)',
        'total_business_analysis': 'TOTAL BUSINESS ANALYSIS',
        'global_business_scenarios': 'GROWTH SCENARIOS FOR TOTAL BUSINESS',
        'scenario': 'Scenario',
        'scenario_type': 'Scenario type',
        'growth_pct': 'Growth %',
        'transactions': 'Transactions',
        'cm_growth': 'CM Growth €',
        'best_scenarios': 'Best scenarios',
        'action': 'Action',
        'scaling_channels': 'Channel scaling',
        'funnel_optimization': 'Funnel optimization',
        'upsell_pricing': 'Up-sell and pricing',
        'retention_loyalty': 'Retention and loyalty',
        'ad_optimization': 'Ad optimization',
        'sensitivity_analysis': 'SENSITIVITY ANALYSIS (MICRO-CHANGES ±5-10%)',
        'change': 'Change',
        'new_value': 'New value',
        'cm_impact': 'CM Impact',
        'cm_impact_pct': 'CM Impact %',
        'sensitivity_insights': 'Key sensitivity insights:',
        'product_analysis': 'PRODUCT ANALYSIS (TOP PRODUCTS)',
        'product_scenarios': 'Best scenarios',
        'priority_map': 'SUMMARY PRIORITY MAP BY PRODUCTS',
        'growth_pct_column': 'Growth %',
        'key_insight': 'Key analysis insight:',
        'key_insight_text': """
        **Key analysis insight:**
        - Several scenarios (C1, AOV, APC) show **identical mathematical effect** on CM growth
        - This happens because in current model:
          - Revenue = UA × C1 × APC × AOV
          - Increase of ANY of these metrics by 10% gives same Revenue growth
          - AC and COGS don't change for these scenarios (except UA)

        **Why focus on C1 (conversion):**
        1. **Lack of cost data** - we have no information about cost of changing each metric
        2. **Strategic considerations** - conversion improvement:
           - Gives synergistic effect with other metrics
           - Improves overall user experience
           - Often requires less capital investment vs traffic scaling (UA)
        3. **Practical feasibility** - for C1 already developed:
           - Ready HADI cycles
           - Concrete A/B tests
           - Measurable hypotheses

        **Where to find implementation details:**
        - **Ready HADI cycles for testing** → tab "Metrics tree & A/B tests"
        """,
        
        # Методология и A/B тесты
        'methodology_ab_testing': 'METHODOLOGY AND A/B TESTING',
        'business_metrics_tree': 'BUSINESS METRICS TREE',
        'metrics_tree_text': """
        **LEVEL 1: Key business indicator**  
        └── **Contribution margin (CM)** — Revenue - AC - COGS

        **LEVEL 2: Unit-economics**  
        ├── **UA (User Acquisition)** — Unique contacts → COUNTUNIQUE(CONTACTS['Id'])  
        ├── **C1 (Conversion Rate)** — Conversion to buyer → B / UA  
        ├── **CPA (Cost Per Acquisition)** — Visitor cost → AC / UA  
        ├── **AOV (Average Order Value)** — Average check → Revenue / T  
        ├── **COGS (Cost of Goods Sold)** — Cost of goods (modeled)  
        ├── **APC (Average Payment Count)** — Payments per customer → T / B  
        ├── **CPC (Cost Per Click)** — Click cost → AC / Clicks  
        └── **CTR (Click-Through Rate)** — Click conversion → Clicks / Impressions

        **LEVEL 2.1: Financial metrics**  
        ├── **Turnover (Revenue)** — Sum of receipts → SUM(DEALS['revenue'])  
        └── **ROMI (Return on Marketing)** — Advertising profitability → CM / AC

        **LEVEL 3: Product metrics**  
        ├── **B (Buyers)** — Unique Contact Name with Active Student status  
        ├── **AC (Advertising Cost)** — Advertising expenses → SUM(SPEND['Spend'])  
        ├── **CAC (Customer Acquisition Cost)** — Customer acquisition cost → AC / B  
        ├── **CLTV (Customer Lifetime Value)** — Customer value → (AOV - COGS) × APC  
        ├── **LTV (Lifetime Value)** — Visitor value → CLTV × C1  
        └── **T (Transactions)** — Total transactions → SUM(DEALS['Transactions'])

        **LEVEL 4: Atomic metrics**  
        ├── DEALS['Created Time'] — Lead creation date  
        ├── DEALS['Closing Date'] — Deal closing date  
        ├── DEALS['Source'] / SPEND['Source'] — Traffic source  
        ├── DEALS['Campaign'] — Campaign  
        ├── DEALS['Product'] — Course type  
        ├── DEALS['Stage'] — Funnel stage  
        ├── DEALS['Quality'] — Lead quality  
        ├── DEALS['City'] — Geography  
        ├── SPEND['Clicks'] — Ad clicks  
        └── SPEND['Impressions'] — Ad impressions

        **LEVEL 5: Standard metrics (monitoring)**  
        ├── DEALS['SLA'] — Response time  
        ├── DEALS['Level of Deutsch'] — Language level  
        ├── DEALS['Course duration'] — Course duration  
        ├── CALLS['Call Duration (in seconds)'] — Call duration  
        ├── CALLS['Call Type'] — Call type  
        ├── CALLS['Call Status'] — Call status  
        ├── SPEND['AdGroup'] — Ad group  
        └── SPEND['Ad'] — Specific ad

        **KEY DEPENDENCIES**  
        - **B = UA × C1** (Customers = Visitors × Conversion)  
        - **Revenue = AOV × T** (Turnover = Check × Transactions)  
        - **T = B × APC** (Transactions = Customers × Frequency)  
        - **CAC = AC / B** (Customer cost = Advertising / Customers)  
        - **CLTV = (AOV - COGS) × APC** (Customer value = (Check - Cost) × Frequency)  
        - **LTV = CLTV × C1** (Visitor value = Customer value × Conversion)  
        - **CM = Revenue - AC - COGS** (Margin = Turnover - Advertising - Cost)  
        - **ROMI = CM / AC** (Profitability = Margin / Advertising)  

        *Profit not included — no data about fixed costs*
        """,
        'hadi_cycles_ab_tests': 'HADI CYCLES AND A/B TESTS',
        'ab_test_basics': 'Basic metrics for A/B tests:',
        'buyers': 'Buyers',
        'traffic': 'Total traffic',
        'conversion': 'Conversion',
        'ready_hadi_cycles': 'Ready HADI cycles for testing:',
        'hypothesis': 'Hypothesis',
        'hadi_cycle': 'HADI cycle:',
        'stage': 'Stage',
        'formulation': 'Formulation',
        'hadi_cycle_stages': {
            'h': 'Hypothesis (H)',
            'a': 'Action (A)',
            'd': 'Data (D)',
            'i': 'Insight (I)'
        },
        'manager_notification': 'HADI-1. Manager notification',
        'auto_materials': 'HADI-2. Automatic materials sending',
        'sms_reminder': 'HADI-3. SMS reminder',
        'manager_notification_text': 'Implementation of automatic manager notification on application receipt and mandatory first call within 1 hour',
        'auto_materials_text': 'Automatic email sending with course program and graduate video review within 5 minutes after application',
        'sms_reminder_text': 'SMS reminder for course enrollment 1 hour after missed manager call',
        'ab_test_params': 'A/B TEST PARAMETERS CALCULATION',
        'ab_test_calc_description': 'Calculation of minimum sample size and time for statistically significant results at different target effects (MDE).',
        'avg_daily_leads': 'Average daily leads inflow (per group):',
        'parameter': 'Parameter',
        'description': 'Description',
        'null_hypothesis': 'Null hypothesis',
        'test_conditions_a': 'A-test conditions',
        'test_conditions_b': 'B-test conditions',
        'tracking_metric': 'Tracking metric',
        'hypothesis_threshold': 'Hypothesis confirmation threshold',
        'significance_level': 'Significance level',
        'leads_per_group': 'Leads per group',
        'leads_per_day': 'Leads/day (group)',
        'days_for_test': 'Days for test',
        'color_legend': 'Color legend:',
        'green_test': '≤14 days — test feasible in standard 2-week cycle',
        'orange_test': '15-30 days — extended test or traffic increase needed',
        'red_test': '>30 days — hypothesis checking difficult with current traffic',
        
        # Сообщения и предупреждения
        'no_unit_economics_data': 'No data to display unit economics',
        'no_successful_deals': 'No successful deals for product analysis',
        'no_city_data': 'No city data for analysis',
        'insufficient_data': 'Insufficient data for closing speed analysis',
        'no_monthly_data': 'No data for monthly analysis',
        'no_data_for_display': 'No data for display',
        
        # Кнопки и элементы
        'select_language': 'Select language',
        'russian': 'Russian',
        'german': 'German',
        'english': 'English',
        
        # Footer
        'footer': 'Analytics Dashboard • Built by Dmitriy Chumachenko',
    }
}

def t(key):
    """Функция перевода текста"""
    lang = st.session_state.get('language', 'ru')
    if lang in TRANSLATIONS and key in TRANSLATIONS[lang]:
        return TRANSLATIONS[lang][key]
    # Если нет перевода, возвращаем ключ
    return key

# ========== НАСТРОЙКА СТРАНИЦЫ ==========
st.set_page_config(
    page_title=t('full_it_school_analytics'),
    layout="wide",
    initial_sidebar_state="expanded"
)

# Инициализация языка в session_state
if 'language' not in st.session_state:
    st.session_state['language'] = 'ru'

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
    .dataframe-table {font-size: 0.9rem;}
    
    /* Убираем белую подсветку Streamlit */
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

# ========== ВЫБОР ЯЗЫКА В САЙДБАРЕ ==========
with st.sidebar:
    st.selectbox(
        t('select_language'),
        options=['ru', 'de', 'en'],
        format_func=lambda x: {'ru': t('russian'), 'de': t('german'), 'en': t('english')}[x],
        key='language',
        on_change=lambda: None  # Триггерим обновление при изменении языка
    )

# ========== ЗАГРУЗКА ДАННЫХ ==========
@st.cache_data(ttl=3600, show_spinner=False)
def load_data():
    deals = pd.read_parquet('deals_clean.parquet')
    spend = pd.read_parquet('spend_clean.parquet')
    contacts = pd.read_parquet('contacts_clean.parquet')
    calls = pd.read_parquet('calls_clean.parquet')
    
    # Конвертация дат
    for col in ['Created Time', 'Closing Date']:
        if col in deals.columns:
            deals[col] = pd.to_datetime(deals[col], errors='coerce')
    
    # СОЗДАЕМ ЧИСЛОВЫЕ ВЕРСИИ timedelta КОЛОНОК (вместо конвертации в строку)
    td_cols = deals.select_dtypes(include=['timedelta64[ns]']).columns
    for col in td_cols:
        # Создаем числовую версию в секундах для анализа
        deals[f'{col}_seconds'] = deals[col].dt.total_seconds()
        # Оригинальную колонку оставляем как есть (timedelta)
        # Её Streamlit может сконвертировать в строку, но у нас есть backup в секундах
    
    return deals, spend, contacts, calls

deals, spend, contacts, calls = load_data()

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

# ========== ДАТЫ МИНИМУМ/МАКСИМУМ ==========
min_date = deals['Created Time'].min().date()
max_date = deals['Created Time'].max().date()

# ========== ИСПРАВЛЕННАЯ ФУНКЦИЯ КЛЮЧЕВЫХ МЕТРИК ==========
def calculate_business_metrics():
    """Расчет ключевых метрик бизнеса"""
    
    # Базовые константы
    TOTAL_UA = contacts['Id'].nunique()
    total_marketing_spend = spend['Spend'].sum()
    
    # Активные студенты
    active_students_df = deals[deals['stage_normalized'] == 'Active Student']
    TOTAL_B_CORRECT = active_students_df['Contact Name'].nunique() if len(active_students_df) > 0 else 0
    successful_deals_count = len(active_students_df)
    
    # Транзакции
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
    
    # Инициализация
    total_revenue = 0
    avg_check = 0
    avg_check_per_client = 0
    win_rate_vacuum = 0
    margin = -total_marketing_spend
    romi = -100
    median_deal_age = 0
    top_product_name = t('no_data')
    ltv_vacuum_business = 0
    
    if len(active_students_df) > 0:
        total_revenue = active_students_df['revenue'].sum()
        
        # AOV на транзакцию
        total_t = active_students_calc['Transactions'].sum() if len(active_students_calc) > 0 else 0
        avg_check = total_revenue / total_t if total_t > 0 else 0
        
        # AOV на клиента
        avg_check_per_client = total_revenue / TOTAL_B_CORRECT if TOTAL_B_CORRECT > 0 else 0
        
        # Конверсия
        win_rate_vacuum = (TOTAL_B_CORRECT / TOTAL_UA * 100) if TOTAL_UA > 0 else 0
        
        # Маржа и ROMI
        margin = total_revenue - total_marketing_spend
        romi = (margin / total_marketing_spend * 100) if total_marketing_spend > 0 else 0
        
        # Цикл сделки
        closed_deals_clean = deals[
            (deals['Id'].isin(active_students_df['Id'].unique())) &
            (deals['Closing Date'].notna()) &
            (deals['Deal_Age_days'].notna()) &
            (deals['Deal_Age_days'] >= 0)
        ].copy()
        if len(closed_deals_clean) > 0:
            median_deal_age = closed_deals_clean['Deal_Age_days'].median()
        
        # LTV и топ продукт
        if len(active_students_calc) > 0:
            product_stats = active_students_calc.groupby('Product').agg({
                'Contact Name': 'nunique',
                'revenue': 'sum',
                'Transactions': 'sum',
            }).reset_index()
            
            # LTV расчет
            product_stats['AOV'] = product_stats['revenue'] / product_stats['Transactions']
            product_stats['APC'] = product_stats['Transactions'] / product_stats['Contact Name']
            COGS_FIXED_PER_TRANS = 0
            COGS_PERCENT_FROM_CHECK = 0.0
            total_cogs = (product_stats['revenue'] * COGS_PERCENT_FROM_CHECK) + (product_stats['Transactions'] * COGS_FIXED_PER_TRANS)
            product_stats['COGS'] = total_cogs / product_stats['Transactions'].replace(0, np.nan)
            product_stats['CLTV'] = (product_stats['AOV'] - product_stats['COGS']) * product_stats['APC']
            product_stats['C1_vacuum'] = product_stats['Contact Name'] / TOTAL_UA if TOTAL_UA > 0 else 0
            product_stats['LTV'] = product_stats['CLTV'] * product_stats['C1_vacuum']
            
            # Топ продукт
            top_product_row = product_stats.sort_values('revenue', ascending=False).head(1)
            top_product_name = top_product_row['Product'].iloc[0] if len(top_product_row) else t('no_data')
            
            # Бизнес-LTV
            if product_stats['Contact Name'].sum() > 0:
                cltv_weighted = (product_stats['CLTV'] * product_stats['Contact Name']).sum() / product_stats['Contact Name'].sum()
                ltv_vacuum_business = cltv_weighted * (TOTAL_B_CORRECT / TOTAL_UA) if TOTAL_UA > 0 else 0
    
    # Сводные метрики
    summary_rows = [
        (t('revenue'), total_revenue, '€'),
        (t('margin'), margin, '€'),
        (t('romi'), romi, '%'),
        (t('ltv'), ltv_vacuum_business, '€'),
        (t('conversion_c1'), win_rate_vacuum, '%'),
        (t('marketing_spend'), total_marketing_spend, '€'),
        (t('ua'), TOTAL_UA, ''),
        (t('successful_deals'), successful_deals_count, ''),
        (t('unique_clients'), TOTAL_B_CORRECT, ''),
        (t('aov_per_transaction'), avg_check, '€'),
        (t('aov_per_client'), avg_check_per_client, '€'),
        (t('traffic_sources'), spend['Source'].nunique(), ''),
        (t('cities'), deals['City'].nunique(), ''),
        (t('managers'), deals['Deal Owner Name'].nunique(), ''),
        (t('products'), deals['Product'].nunique(), ''),
        (t('top_product'), top_product_name, ''),
    ]

    summary_df = pd.DataFrame(summary_rows, columns=['Metric', 'Value', 'Unit'])
    
    return summary_df, TOTAL_UA, TOTAL_B_CORRECT, total_revenue, total_marketing_spend

# Вызов функции
summary_df, TOTAL_UA, TOTAL_B, total_revenue, marketing_spend = calculate_business_metrics()

# ========== ЗАГОЛОВОК ==========
st.markdown(f'<div class="main-title">{t("full_it_school_analytics")}</div>', unsafe_allow_html=True)
st.markdown(f"*{t('data_period')}: {min_date} - {max_date}*")
st.markdown("---")

# ========== КЛЮЧЕВЫЕ МЕТРИКИ ==========
st.markdown(f'<div class="section-title">{t("business_summary")}</div>', unsafe_allow_html=True)

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
    deals_calc = deals.copy()
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

# ========== ФУНКЦИЯ ТОЧЕК РОСТА ==========
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
        'UA': t('scaling_channels'),
        'C1': t('funnel_optimization'), 
        'AOV': t('upsell_pricing'),
        'APC': t('retention_loyalty'),
        'CPA': t('ad_optimization')
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
            'Scenario': scenario_name,  # ← Английский ключ
            'Scenario_Type': scenario_type,  # ← Английский ключ
            'Growth_Pct': growth_pct,
            'Product': product_name,
            'UA': ua,
            'C1': c1,
            'B': b,
            'AOV': aov,
            'APC': apc,
            'T': t,
            'Revenue': revenue,
            'AC': ac,
            'CLTV': cltv,
            'LTV': ltv,
            'CPA': cpa,
            'CAC': cac,
            'CM': cm,
            'ROMI': romi
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
    t('marketing_tab'),
    t('sales_tab'),
    t('products_tab'),
    t('geography_tab'),
    t('unit_economics_tab'),
    t('growth_points_tab'), 
    t('metrics_tree_tab'),
])

# ---------- ВКЛАДКА 1: МАРКЕТИНГ ----------
with tabs[0]:
    st.markdown(f'<div class="section-title">{t("marketing_analytics")}</div>', unsafe_allow_html=True)
    
    # ========== 0. ПОДГОТОВКА ЕДИНЫХ ДАННЫХ ==========
    # Студенты по источникам (единый расчет)
    students_by_source = deals[deals['stage_normalized'] == 'Active Student'].groupby('Source')['Id'].count().reset_index()
    students_by_source.columns = ['Source', 'Students']
    
    # Лиды по источникам
    leads_by_source = deals.groupby('Source')['Id'].count().reset_index()
    leads_by_source.columns = ['Source', 'Leads']
    
    # Качественные лиды (A-B)
    quality_filter = ['A - High', 'B - Medium']
    quality_leads_by_source = deals[deals['Quality'].isin(quality_filter)].groupby('Source')['Id'].count().reset_index()
    quality_leads_by_source.columns = ['Source', 'Quality_Leads']
    
    # Выручка по источникам
    revenue_by_source = deals[deals['stage_normalized'] == 'Active Student'].groupby('Source')['revenue'].sum().reset_index()
    revenue_by_source.columns = ['Source', 'Revenue']
    
    # Расходы по источникам
    spend_by_source = spend.groupby('Source').agg({
        'Spend': 'sum',
        'Clicks': 'sum',
        'Impressions': 'sum'
    }).reset_index()
    
    # ========== 1. МАРКЕТИНГОВАЯ ВОРОНКА ==========
    st.subheader(t("marketing_funnel"))
    
    if 'Source' in spend.columns and 'Source' in deals.columns:
        # Объединение всех метрик
        funnel_df = spend_by_source.merge(leads_by_source, on='Source', how='left')\
                                   .merge(quality_leads_by_source, on='Source', how='left')\
                                   .merge(students_by_source, on='Source', how='left')\
                                   .merge(revenue_by_source, on='Source', how='left').fillna(0)
        
        # Дополнительные расчеты
        funnel_df['CPC'] = (funnel_df['Spend'] / funnel_df['Clicks']).replace([np.inf, 0], np.nan).fillna(0).round(2)
        funnel_df['CPL'] = (funnel_df['Spend'] / funnel_df['Leads']).replace([np.inf, 0], np.nan).fillna(0).round(2)
        funnel_df['CPS'] = (funnel_df['Spend'] / funnel_df['Students']).replace([np.inf, 0], np.nan).fillna(0).round(2)
        funnel_df['CPQ'] = (funnel_df['Spend'] / funnel_df['Quality_Leads']).replace([np.inf, 0], np.nan).fillna(0).round(2)
        funnel_df['CTR'] = (funnel_df['Clicks'] / funnel_df['Impressions'] * 100).fillna(0).round(2)
        
        # Топ-7 по расходам
        top_funnel = funnel_df.sort_values(by='Spend', ascending=False).head(7)
        
        # График воронки
        fig1 = make_subplots(
            rows=2, cols=1,
            subplot_titles=(t('conversion_funnel'), t('cost_per_result')),
            vertical_spacing=0.15,
            specs=[[{"type": "bar"}], [{"type": "table"}]]
        )
        
        # График 1: Группированная воронка
        stages = ['Impressions', 'Clicks', 'Leads', 'Students']
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
        
        fig1.update_yaxes(type="log", title_text=f"{t('quantity')} (Log Scale)", row=1, col=1)
        
        # График 2: Таблица с деньгами
        fig1.add_trace(
            go.Table(
                header=dict(
                    values=[t('source'), t('spend'), t('clicks'), t('leads'), t('students'), t('cpc'), t('cpl'), t('cps')],
                    fill_color="#0235C4",
                    font_color='white',
                    align='left',
                    font_size=12
                ),
                cells=dict(
                    values=[
                        top_funnel['Source'],
                        top_funnel['Spend'].apply(lambda x: f"{x:,.0f}€"),
                        top_funnel['Clicks'].apply(lambda x: f"{x:,.0f}"),
                        top_funnel['Leads'].apply(lambda x: f"{x:,.0f}"),
                        top_funnel['Students'].apply(lambda x: f"{x:,.0f}"),
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

        fig1.update_layout(height=800, title_text=t('marketing_analytics_volumes'), barmode='group')
        st.plotly_chart(fig1, use_container_width=True)
    
    # ========== 2. АНАЛИЗ ПЛАТНЫХ ИСТОЧНИКОВ ==========
    st.subheader(t("paid_sources_analysis"))
    
    if 'Source' in spend.columns and 'Source' in deals.columns:
        # Объединение данных
        marketing_deep = spend_by_source.merge(leads_by_source, on='Source', how='left')\
                                        .merge(students_by_source, on='Source', how='left')\
                                        .merge(revenue_by_source, on='Source', how='left').fillna(0)
        
        # Расчет метрик
        marketing_deep['CPC'] = (marketing_deep['Spend'] / marketing_deep['Clicks']).replace([np.inf], 0).fillna(0).round(2)
        marketing_deep['Conversion'] = (marketing_deep['Students'] / marketing_deep['Leads'] * 100).fillna(0).round(2)
        marketing_deep['CAC'] = (marketing_deep['Spend'] / marketing_deep['Students']).replace([np.inf, 0], np.nan).fillna(0).round(2)
        marketing_deep['Avg_Check'] = (marketing_deep['Revenue'] / marketing_deep['Students']).replace([np.inf, 0], np.nan).fillna(0).round(2)
        marketing_deep['ROAS'] = (marketing_deep['Revenue'] / marketing_deep['Spend'] * 100).replace([np.inf, 0], np.nan).fillna(0).round(2)
        
        # Фильтр платных источников
        paid_marketing = marketing_deep[(marketing_deep['Spend'] > 10)].sort_values(by='Spend', ascending=False).copy()
        
        if len(paid_marketing) > 0:
            # График CPC vs Конверсия
            fig2 = px.scatter(
                paid_marketing,
                x='CPC',
                y='Conversion',
                size='Spend',
                color='Source',
                text='Source',
                title=t('cpc_vs_conversion'),
                labels={'CPC': t('cpcl'), 'Conversion': t('conversion_percent')},
                height=500
            )
            fig2.add_vline(x=paid_marketing['CPC'].median(), line_dash="dash", line_color="gray", annotation_text=t('median_cpc'))
            fig2.add_hline(y=paid_marketing['Conversion'].median(), line_dash="dash", line_color="gray", annotation_text=t('median_conversion'))
            fig2.update_traces(textposition='top center')
            st.plotly_chart(fig2, use_container_width=True)
            
            # Таблица по источникам
            st.markdown(f"**{t('detailed_source_stats')}**")
            
            display_cols = ['Source', 'Spend', 'Leads', 'Students', 'Conversion', 
                           'CAC', 'Avg_Check', 'ROAS']
            
            st.dataframe(
                paid_marketing[display_cols].sort_values('Spend', ascending=False).style.format({
                    'Spend': '{:,.0f}',
                    'Leads': '{:,.0f}',
                    'Students': '{:,.0f}',
                    'Conversion': '{:.1f}%',
                    'CAC': '{:.0f}',
                    'Avg_Check': '{:,.0f}',
                    'ROAS': '{:.0f}%'
                }).background_gradient(subset=['Conversion', 'ROAS'], cmap='RdYlGn'),
                use_container_width=True,
                height=300
            )
    
    # ========== 3. МАТРИЦА ЭФФЕКТИВНОСТИ ИСТОЧНИКОВ ==========
    st.subheader(t("source_efficiency_matrix"))
    
    if 'Source' in deals.columns:
        # Подготовка данных
        source_matrix = spend_by_source.merge(leads_by_source, on='Source', how='left')\
                                       .merge(quality_leads_by_source, on='Source', how='left')\
                                       .merge(students_by_source, on='Source', how='left')\
                                       .merge(revenue_by_source, on='Source', how='left').fillna(0)
        
        # Качественные метрики
        source_matrix['Quality_Pct'] = (source_matrix['Quality_Leads'] / source_matrix['Leads'] * 100).round(1)
        source_matrix['Conversion_Pct'] = (source_matrix['Students'] / source_matrix['Leads'] * 100).round(1)
        source_matrix['Avg_Check'] = (source_matrix['Revenue'] / source_matrix['Students']).replace([np.inf, 0], np.nan).fillna(0).round(0)
        source_matrix['ROAS'] = (source_matrix['Revenue'] / source_matrix['Spend'] * 100).replace([np.inf, 0], np.nan).fillna(0).round(1)
        
        # Скорость сделок по источникам
        deals_success = deals[deals['stage_normalized'] == 'Active Student'].copy()
        speed_by_source = deals_success.groupby('Source')['Deal_Age_days'].median().reset_index()
        speed_by_source.columns = ['Source', 'Median_Speed_Days']
        
        source_matrix = source_matrix.merge(speed_by_source, on='Source', how='left').fillna(0)
        
        # Фильтр по минимальному количеству студентов
        source_matrix_filtered = source_matrix[source_matrix['Students'] >= 5].copy()
        
        if len(source_matrix_filtered) > 0:
            # График матрицы
            fig3 = px.scatter(
                source_matrix_filtered,
                x='Median_Speed_Days',
                y='Avg_Check',
                size='Revenue',
                color='Source',
                text='Source',
                title=t('speed_vs_check'),
                labels={
                    'Median_Speed_Days': t('median_speed_days'), 
                    'Avg_Check': t('avg_check_euro'),
                    'Revenue': t('revenue')
                },
                height=600
            )
            
            avg_speed = source_matrix_filtered['Median_Speed_Days'].mean()
            avg_check = source_matrix_filtered['Avg_Check'].mean()
            fig3.add_vline(x=avg_speed, line_dash="dash", line_color="gray", annotation_text=t('avg_speed'))
            fig3.add_hline(y=avg_check, line_dash="dash", line_color="gray", annotation_text=t('avg_check'))
            fig3.update_traces(textposition='top center')
            st.plotly_chart(fig3, use_container_width=True)
            
            # Таблица с лидами
            st.markdown(f"**{t('leads_finance_details')}**")
            
            display_cols = ['Source', 'Leads', 'Quality_Leads', 'Quality_Pct', 'Students', 
                           'Conversion_Pct', 'Revenue', 'Avg_Check', 'ROAS']
            
            st.dataframe(
                source_matrix_filtered[display_cols].sort_values('Revenue', ascending=False).style.format({
                    'Leads': '{:,.0f}',
                    'Quality_Leads': '{:,.0f}',
                    'Quality_Pct': '{:.1f}%',
                    'Students': '{:,.0f}',
                    'Conversion_Pct': '{:.1f}%',
                    'Revenue': '{:,.0f}',
                    'Avg_Check': '{:,.0f}',
                    'ROAS': '{:.1f}%'
                }).background_gradient(subset=['Conversion_Pct', 'ROAS'], cmap='RdYlGn'),
                use_container_width=True,
                height=300
            )
    
    # ========== 4. ROAS ПО ИСТОЧНИКАМ ==========
    st.subheader(t("roas_by_sources"))
    
    if 'Source' in spend.columns and 'Source' in deals.columns:
        # Используем уже подготовленные данные
        roi_analysis = marketing_deep[(marketing_deep['Spend'] > 0) & (marketing_deep['Students'] > 0)].copy()
        roi_analysis = roi_analysis.sort_values(by='ROAS', ascending=False)
        
        if len(roi_analysis) > 0:
            # График ROAS
            fig4 = px.scatter(
                roi_analysis,
                x='Spend',
                y='ROAS',
                size='Revenue',
                color='Source',
                text='Source',
                title=t('roas_analysis'),
                labels={'ROAS': t('roas_percent'), 'Spend': t('spend')}
            )
            fig4.update_traces(textposition='bottom center')
            fig4.add_hline(y=100, line_dash="dash", line_color="red", annotation_text=t('breakeven_point'))
            st.plotly_chart(fig4, use_container_width=True)
            
            # Таблица ROI
            st.markdown(f"**{t('roas_by_sources')}**")
            
            display_cols = ['Source', 'Spend', 'Students', 'Revenue', 'CAC', 'ROAS']
            
            st.dataframe(
                roi_analysis[display_cols].style.format({
                    'Spend': '{:,.0f}',
                    'Students': '{:,.0f}',
                    'Revenue': '{:,.0f}',
                    'CAC': '{:.0f}',
                    'ROAS': '{:.0f}%'
                }).background_gradient(subset=['ROAS'], cmap='RdYlGn'),
                use_container_width=True,
                height=250
            )
    
    # ========== 5. АНАЛИЗ КАМПАНИЙ ==========
    st.subheader(t("campaign_analysis"))
    
    if 'Campaign' in deals.columns:
        # Efficiency Ratio кампаний
        lead_counts = deals[deals['stage_normalized'] == 'Lead'].groupby('Campaign')['Id'].nunique().reset_index()
        lead_counts.columns = ['Campaign', 'Count_Leads']
        active_counts = deals[deals['stage_normalized'] == 'Active Student'].groupby('Campaign')['Id'].nunique().reset_index()
        active_counts.columns = ['Campaign', 'Count_Active_Students']
        
        campaign_df = lead_counts.merge(active_counts, on='Campaign', how='outer').fillna(0)
        campaign_df['Efficiency_Ratio'] = (campaign_df['Count_Active_Students'] / campaign_df['Count_Leads'] * 100).replace([np.inf, -np.inf], 0).fillna(0).round(2)
        campaign_efficiency = campaign_df[(campaign_df['Count_Leads'] + campaign_df['Count_Active_Students']) > 20].copy()
        
        if len(campaign_efficiency) > 0:
            # График
            fig5 = px.bar(
                campaign_efficiency.sort_values('Efficiency_Ratio', ascending=False).head(15),
                x='Campaign', 
                y='Efficiency_Ratio', 
                color='Efficiency_Ratio',
                title=t('top_campaigns_efficiency'),
                labels={'Efficiency_Ratio': t('efficiency_ratio'), 'Campaign': t('campaign')},
                color_continuous_scale='RdYlGn',
                height=500
            )
            fig5.update_layout(xaxis={'categoryorder': 'total descending'})
            st.plotly_chart(fig5, use_container_width=True)
            
            # Таблица
            st.markdown(f"**{t('detailed_campaign_stats')}**")
            st.dataframe(
                campaign_efficiency.sort_values('Efficiency_Ratio', ascending=False).head(15).style.format({
                    'Count_Leads': '{:,.0f}',
                    'Count_Active_Students': '{:,.0f}',
                    'Efficiency_Ratio': '{:.2f}%'
                }).background_gradient(subset=['Efficiency_Ratio'], cmap='RdYlGn'),
                use_container_width=True,
                height=350
            )

# ---------- ВКЛАДКА 2: ПРОДАЖИ ----------
with tabs[1]:
    st.markdown(f'<div class="section-title">{t("sales_efficiency")}</div>', unsafe_allow_html=True)
    
    # ========== 0. АНАЛИЗ ЗВОНКОВ И ДИНАМИКИ ==========
    st.subheader(t("calls_dynamics_analysis"))
    
    # --- Подготовка данных для трендов ---
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
    
    # 1. ГРАФИК ДИНАМИКИ ЛИДОВ, ЗВОНКОВ И ПРОДАЖ
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
            name=t('sales_multiplied'),
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

    fig_trend.update_yaxes(
        title_text=f"<b>{t('incoming_leads')} (реальные)</b>", 
        secondary_y=False,
        title_font=dict(color='white', size=14),
        showgrid=True
    )

    fig_trend.update_yaxes(
        title_text=f"<b>{t('calls')}</b>", 
        secondary_y=True,
        title_font=dict(color='white', size=14),
        showgrid=False
    )

    fig_trend.data[0].hovertemplate = f"{t('week')}: %{{x}}<br>{t('leads')}: %{{y:.0f}}<extra></extra>"
    fig_trend.data[1].hovertemplate = f"{t('week')}: %{{x}}<br>{t('sales')}: %{{customdata:.0f}}<extra></extra>"
    fig_trend.data[1].customdata = weekly_stats['Success_Count']
    fig_trend.data[2].hovertemplate = f"{t('week')}: %{{x}}<br>{t('calls')}: %{{y:.0f}}<extra></extra>"

    fig_trend.update_layout(
        title_text=f"<b>{t('leads_calls_sales_dynamics')}</b><br><span style='font-size:12px'>Продажи искусственно увеличены для наглядности</span>",
        hovermode="x unified",
        height=450
    )

    st.plotly_chart(fig_trend, use_container_width=True)
    
    # 2. ГРАФИК ВЛИЯНИЯ ЗВОНКОВ НА ПРОДАЖИ
    fig_impact = px.scatter(
        weekly_stats,
        x='Calls_Count',
        y='Success_Count',
        size='Leads_Count',
        color='Conversion_Rate',
        hover_data=['Week', 'Calls_Per_Lead'],
        title=t('calls_impact_on_sales'),
        labels={
            'Calls_Count': t('number_of_calls'),
            'Success_Count': t('number_of_sales'),
            'Leads_Count': t('leads_volume'),
            'Conversion_Rate': t('weekly_conversion')
        },
        color_continuous_scale='Viridis',
        height=400
    )
    fig_impact.add_traces(
        px.scatter(weekly_stats, x='Calls_Count', y='Success_Count', trendline="ols").data[1]
    )
    st.plotly_chart(fig_impact, use_container_width=True)
    
    # КОРРЕЛЯЦИОННЫЙ АНАЛИЗ
    corr_calls_sales = weekly_stats['Calls_Count'].corr(weekly_stats['Success_Count'])
    corr_leads_sales = weekly_stats['Leads_Count'].corr(weekly_stats['Success_Count'])
    
    st.markdown(f"**{t('correlation_analysis')}**")
    st.markdown(f"- {t('calls_sales_correlation')}: **{corr_calls_sales:.2f}**")
    st.markdown(f"- {t('leads_sales_correlation')}: **{corr_leads_sales:.2f}**")
    
    # ИСПРАВЛЕННЫЙ ВЫВОД
    st.info(t('correlation_insight'))
    
    # 3. РАСПРЕДЕЛЕНИЕ ЗВОНКОВ ДО ПРОДАЖИ
    st.subheader(t("calls_distribution"))
    
    success_deals = deals[
        (deals['stage_normalized'] == 'Active Student') & 
        (deals['Closing Date'].notna()) &
        (deals['Contact Name'].notna()) & 
        (deals['Contact Name'] != '')
    ][['Id', 'Contact Name', 'Closing Date', 'Deal Owner Name']].copy()
    
    calls_dates = calls[
        (calls['CONTACTID'].notna()) & 
        (calls['CONTACTID'] != '')
    ][['CONTACTID', 'Call Start Time']].copy()
    
    merged_calls = success_deals.merge(
        calls_dates, 
        left_on='Contact Name', 
        right_on='CONTACTID', 
        how='left'
    )
    
    valid_calls = merged_calls[
        (merged_calls['Call Start Time'].notna()) &
        (merged_calls['Call Start Time'].dt.normalize() <= merged_calls['Closing Date'].dt.normalize())
    ]
    
    calls_per_deal = valid_calls.groupby('Id')['Call Start Time'].count().reset_index()
    calls_per_deal.columns = ['Id', 'Calls_Count']
    
    final_calls_stats = pd.DataFrame(success_deals[['Id', 'Deal Owner Name']]).merge(calls_per_deal, on='Id', how='left').fillna(0)
    
    percentile_95 = final_calls_stats['Calls_Count'].quantile(0.95)
    calls_for_histogram = final_calls_stats[final_calls_stats['Calls_Count'] <= percentile_95].copy()
    
    avg_calls = final_calls_stats['Calls_Count'].mean()
    median_calls = final_calls_stats['Calls_Count'].median()
    total_deals = len(final_calls_stats)
    
    fig_calls_dist = px.histogram(
        calls_for_histogram, 
        x='Calls_Count',
        title=f"{t('calls_distribution')} (показано {len(calls_for_histogram)} из {total_deals} сделок, до {int(percentile_95)} звонков)",
        labels={'Calls_Count': t('calls_count'), 'count': t('deals_count')},
        text_auto=True,
        color_discrete_sequence=['#FFA15A'],
        nbins=int(percentile_95) + 1
    )
    
    fig_calls_dist.update_xaxes(dtick=1, title_text=t('calls_count'))
    fig_calls_dist.update_yaxes(title_text=t('deals_count'))

    
    fig_calls_dist.add_vline(
        x=median_calls, 
        line_dash="dash", 
        line_color="green", 
        annotation_text=f"{t('median')}: {median_calls}",
        annotation_position="top left",
        annotation_y=0.95
    )
    
    fig_calls_dist.add_vline(
        x=avg_calls, 
        line_dash="dash", 
        line_color="blue", 
        annotation_text=f"{t('average')}: {avg_calls:.1f}",
        annotation_position="top right",
        annotation_y=0.85
    )
    
    fig_calls_dist.update_layout(bargap=0.1, height=400, showlegend=False)
    st.plotly_chart(fig_calls_dist, use_container_width=True)

    # ========== 3. СКОРОСТЬ ЗАКРЫТИЯ СДЕЛОК ==========
    st.subheader(t("deal_speed"))

    # Фильтрация (только успешные сделки)
    active_student_ids = deals[deals['stage_normalized'] == 'Active Student']['Id'].unique()
    closed_deals_clean = deals[
        (deals['Id'].isin(active_student_ids)) & 
        (deals['Closing Date'].notna()) & 
        (deals['Deal_Age_days'].notna()) & 
        (deals['Deal_Age_days'] >= 0)
    ].copy()

    if len(closed_deals_clean) > 0:
        # --- Статистика ---
        mean_age = closed_deals_clean['Deal_Age_days'].mean()
        median_age = closed_deals_clean['Deal_Age_days'].median()
        min_age = closed_deals_clean['Deal_Age_days'].min()
        max_age = closed_deals_clean['Deal_Age_days'].max()
        
        # --- Таблица статистик ---
        stats_df = pd.DataFrame({
            t('metric'): [t('mean'), t('median'), t('minimum'), t('maximum')],
            t('days'): [mean_age, median_age, min_age, max_age]
        })
        st.dataframe(stats_df, use_container_width=True)
        
        # --- ГРАФИК БЕЗ БОКСПЛОТА ---
        fig = px.histogram(
            closed_deals_clean, 
            x='Deal_Age_days', 
            title=t('success_deal_duration'),
            color_discrete_sequence=['#FFA15A'],
            opacity=0.75
        )
        
        # Настройка бинов
        fig.update_traces(xbins=dict(start=0, size=5), selector=dict(type='histogram'))
        
        # Линии медианы и среднего
        fig.add_vline(
            x=median_age, line_width=2, line_dash="dash", line_color="red",
            annotation_text=f"{t('median')}: {median_age:.1f}", annotation_position="top left"
        )
        fig.add_vline(
            x=mean_age, line_width=2, line_dash="dash", line_color="green",
            annotation_text=f"{t('mean')}: {mean_age:.1f}", annotation_position="top right"
        )
        
        # Настройки осей
        fig.update_xaxes(range=[-1, 120], title_text=t('deal_duration_days'))
        fig.update_layout(
            yaxis_title=t('deals_count'), 
            showlegend=False, 
            bargap=0.1,
            height=550
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # --- ТАБЛИЦА ПО МЕНЕДЖЕРАМ ---
        if 'Deal Owner Name' in closed_deals_clean.columns:
            manager_stats = closed_deals_clean.groupby('Deal Owner Name').agg({
                'Id': 'count',
                'Deal_Age_days': ['min', 'median', 'mean', 'max']
            }).reset_index()
            
            # Выравниваем колонки
            manager_stats.columns = [t('manager'), t('deals_count_full'), t('minimum'), t('median_full'), t('mean'), t('maximum')]
            
            # Фильтруем менеджеров с >=3 сделками
            manager_stats = manager_stats[manager_stats[t('deals_count_full')] >= 3]
            
            if len(manager_stats) > 0:
                st.subheader(t('manager_speed'))
                
                # Сортируем по медиане (быстрее → медленнее)
                manager_stats = manager_stats.sort_values(t('median_full'), ascending=True)
                
                st.dataframe(
                    manager_stats.style\
                        .background_gradient(subset=[t('median_full')], cmap='RdYlGn_r')\
                        .background_gradient(subset=[t('mean')], cmap='RdYlGn_r')\
                        .format({
                            t('minimum'): '{:.0f}',
                            t('median_full'): '{:.1f}',
                            t('mean'): '{:.1f}',
                            t('maximum'): '{:.0f}'
                        }),
                    use_container_width=True,
                    height=400
                )
    else:
        st.info(t('insufficient_data'))

    # 4. МЕСЯЧНАЯ ДИНАМИКА ВЫРУЧКИ, ЛИДОВ И СТУДЕНТОВ
    st.subheader(t("monthly_dynamics"))

    # Работаем с копией, не трогаем оригинал
    deals_monthly = deals.copy()
    deals_monthly['Created_Month'] = deals_monthly['Created Time'].dt.to_period('M').dt.to_timestamp()

    monthly_stats = deals_monthly.groupby('Created_Month').agg({
        'Id': 'count',
        'stage_normalized': lambda x: (x == 'Active Student').sum(),
        'revenue': 'sum'
    }).reset_index()

    monthly_stats.columns = ['Month', 'Total_Deals', 'Active_Students', 'Total_Revenue']

    if len(monthly_stats) > 0:
        monthly_stats['Month_Year'] = monthly_stats['Month'].dt.strftime('%b %Y')
        monthly_stats['Conversion_Rate_%'] = (monthly_stats['Active_Students'] / monthly_stats['Total_Deals'] * 100).round(1)
        
        # Разделенный график: 2 строки, 1 колонка
        fig_split = make_subplots(
            rows=2, cols=1,
            subplot_titles=(
                f"<b>{t('revenue_students')}</b>",
                f"<b>{t('leads_conversion')}</b>"
            ),
            vertical_spacing=0.2,
            shared_xaxes=True,
            specs=[[{"secondary_y": True}], [{"secondary_y": True}]]
        )
        
        # ========== ВЕРХНИЙ ГРАФИК (ОРАНЖЕВЫЙ) ==========
        # Выручка (столбцы, левая ось) - ОРАНЖЕВЫЙ
        fig_split.add_trace(
            go.Bar(
                x=monthly_stats['Month_Year'],
                y=monthly_stats['Total_Revenue'],
                name=t('revenue_euro'),
                marker_color='#FFA15A',
                opacity=0.9,
                text=monthly_stats['Total_Revenue'].apply(lambda x: f'{x:,.0f}'),
                textposition='inside',
                textfont=dict(color='white', size=10),
                insidetextanchor='start'
            ),
            secondary_y=False,
            row=1, col=1
        )
        
        # Активные студенты (линия, правая ось) - СИНИЙ
        fig_split.add_trace(
            go.Scatter(
                x=monthly_stats['Month_Year'],
                y=monthly_stats['Active_Students'],
                name=t('active_students'),
                mode='lines+markers+text',
                line=dict(color='#2E86AB', width=3),
                marker=dict(size=10, symbol='diamond'),
                text=monthly_stats['Active_Students'],
                textposition='top center',
            ),
            secondary_y=True,
            row=1, col=1
        )
        
        # ========== НИЖНИЙ ГРАФИК ==========
        # Всего лидов (столбцы, левая ось) - ЗЕЛЕНЫЙ
        fig_split.add_trace(
            go.Bar(
                x=monthly_stats['Month_Year'],
                y=monthly_stats['Total_Deals'],
                name=t('total_leads'),
                marker_color='#00CC96',
                opacity=0.9,
                text=monthly_stats['Total_Deals'],
                textposition='inside',
                textfont=dict(color='white', size=10),
                insidetextanchor='start'
            ),
            secondary_y=False,
            row=2, col=1
        )
        
        # Конверсия (линия, правая ось) - ФИОЛЕТОВЫЙ
        fig_split.add_trace(
            go.Scatter(
                x=monthly_stats['Month_Year'],
                y=monthly_stats['Conversion_Rate_%'],
                name=t('conversion_rate'),
                mode='lines+markers+text',
                line=dict(color='#AB63FA', width=3),
                marker=dict(size=10, symbol='square'),
                text=monthly_stats['Conversion_Rate_%'].apply(lambda x: f'{x:.1f}%'),
                textposition='top center',
            ),
            secondary_y=True,
            row=2, col=1
        )
        
        # ========== НАСТРОЙКА ОСЕЙ ==========
        # Верхний график: левая ось (выручка)
        fig_split.update_yaxes(
            title_text=f"<b>{t('revenue_euro')}</b>",
            secondary_y=False,
            row=1, col=1,
            showgrid=False,
        )
        
        # Верхний график: правая ось (студенты)
        fig_split.update_yaxes(
            title_text=f"<b>{t('students')} (шт)</b>",
            secondary_y=True,
            row=1, col=1,
            showgrid=False,
            rangemode='tozero'
        )
        
        # Нижний график: левая ось (лиды)
        fig_split.update_yaxes(
            title_text=f"<b>{t('leads')} (шт)</b>",
            secondary_y=False,
            row=2, col=1,
            showgrid=False,
            rangemode='tozero'
        )
        
        # Нижний график: правая ось (конверсия)
        fig_split.update_yaxes(
            title_text=f"<b>{t('conversion_rate')}</b>",
            secondary_y=True,
            row=2, col=1,
            showgrid=False,
            range=[0, min(100, monthly_stats['Conversion_Rate_%'].max() * 1.5)]
        )
        
        # Общая настройка
        fig_split.update_xaxes(
            title_text=t('month'),
            row=2, col=1
        )
        
        fig_split.update_layout(
            height=800,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            hovermode="x unified",
            bargap=0.3,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_split, use_container_width=True)
        
        # Статистика по месяцам
        st.markdown(f"**{t('detailed_monthly_stats')}**")
        
        month_summary = monthly_stats.copy()
        month_summary['Avg_Check'] = (month_summary['Total_Revenue'] / month_summary['Active_Students']).replace([np.inf, 0], np.nan).fillna(0).round(0)
        
        # Сортируем по Month, но отображаем Month_Year
        month_summary = month_summary.sort_values('Month', ascending=False)
        
        display_cols = ['Month_Year', 'Total_Deals', 'Active_Students', 'Conversion_Rate_%', 
                    'Total_Revenue', 'Avg_Check']
        
        st.dataframe(
            month_summary[display_cols].style.format({
                'Total_Deals': '{:,.0f}',
                'Active_Students': '{:,.0f}',
                'Total_Revenue': '{:,.0f}',
                'Avg_Check': '{:,.0f}',
                'Conversion_Rate_%': '{:.1f}%'
            }).background_gradient(subset=['Total_Revenue', 'Conversion_Rate_%'], cmap='RdYlGn'),
            use_container_width=True,
            height=300
        )
    else:
        st.info(t('no_monthly_data'))

    # ========== 1. ТОП МЕНЕДЖЕРОВ ПО ВЫРУЧКЕ И КОНВЕРСИИ ==========
    st.subheader(t("top_managers"))
    
    if 'Deal Owner Name' in deals.columns:
        # Подготовка данных
        df_clean = deals.copy()
        
        # Базовые метрики
        manager_stats = df_clean.groupby('Deal Owner Name').agg(
            Leads=('Id', 'count'),
            Revenue=('revenue', 'sum'),
            Sales=('stage_normalized', lambda x: (x == 'Active Student').sum())
        ).reset_index().rename(columns={'Deal Owner Name': 'Manager'})
        
        # Скорость закрытия
        speed_stats = df_clean[df_clean['stage_normalized'] == 'Active Student'].groupby('Deal Owner Name')['Deal_Age_days'].median().reset_index()
        speed_stats.columns = ['Manager', 'Median_Deal_Age_Days']
        
        # Звонки (ТОЛЬКО по успешным сделкам)
        if 'calls' in locals() and len(calls) > 0:
            calls_agg = calls.groupby('CONTACTID')['Id'].count().reset_index().rename(columns={'Id': 'Calls_Count', 'CONTACTID': 'Contact Name'})
            successful_deals = df_clean[df_clean['stage_normalized'] == 'Active Student']
            deals_with_calls = successful_deals[['Id', 'Deal Owner Name', 'Contact Name']].merge(calls_agg, on='Contact Name', how='left').fillna(0)
            calls_stats = deals_with_calls.groupby('Deal Owner Name')['Calls_Count'].mean().reset_index()
            calls_stats.columns = ['Manager', 'Avg_Calls_Per_Deal']
        else:
            calls_stats = pd.DataFrame({'Manager': manager_stats['Manager'], 'Avg_Calls_Per_Deal': 0})
        
        # Сборка
        final_stats = manager_stats.merge(speed_stats, on='Manager', how='left').fillna(0)
        final_stats = final_stats.merge(calls_stats, on='Manager', how='left').fillna(0)
        
        # KPI
        final_stats['Win_Rate'] = (final_stats['Sales'] / final_stats['Leads'] * 100).round(2)
        final_stats['Avg_Check'] = (final_stats['Revenue'] / final_stats['Sales']).replace([np.inf], 0).fillna(0).round(0)
        
        # Фильтр
        top_managers = final_stats[final_stats['Leads'] >= 10].sort_values(by='Revenue', ascending=False)
        
        if len(top_managers) > 0:
            fig1 = px.bar(
                top_managers.head(15),
                x='Manager', y='Revenue', 
                color='Win_Rate',
                text_auto='.2s',
                title=t('top_managers_revenue'),
                labels={'Revenue': t('revenue'), 'Win_Rate': t('win_rate')},
                color_continuous_scale='RdYlGn',
                height=500
            )
            fig1.update_layout(xaxis={'categoryorder':'total descending'})
            st.plotly_chart(fig1, use_container_width=True)
            
            efficiency_view = top_managers.sort_values(by='Win_Rate', ascending=True).tail(15)
            fig2 = px.bar(
                efficiency_view,
                x='Win_Rate', 
                y='Manager', 
                orientation='h', 
                color='Median_Deal_Age_Days',
                text_auto='.1f',
                title=t('top_conversion'),
                labels={'Win_Rate': t('win_rate'), 'Manager': t('manager'), 'Median_Deal_Age_Days': t('avg_deal_cycle')},
                color_continuous_scale='Bluered',
                height=600
            )
            st.plotly_chart(fig2, use_container_width=True)
            
            st.subheader(t("detailed_manager_stats"))
            
            display_cols = ['Manager', 'Leads', 'Sales', 'Revenue', 'Win_Rate', 
                           'Avg_Check', 'Median_Deal_Age_Days', 'Avg_Calls_Per_Deal']
            display_df = final_stats[display_cols].sort_values('Revenue', ascending=False).head(20)
            
            st.dataframe(
                display_df.style\
                    .background_gradient(subset=['Revenue', 'Win_Rate'], cmap='Greens')\
                    .format({
                        'Revenue': '{:,.0f}', 
                        'Avg_Check': '{:,.0f}', 
                        'Median_Deal_Age_Days': '{:.0f}',
                        'Win_Rate': '{:.1f}%',
                        'Avg_Calls_Per_Deal': '{:.1f}'
                    }),
                use_container_width=True
            )
    
    # ========== 2. АНАЛИЗ СКОРОСТИ И КАЧЕСТВА ==========
    st.subheader(t("speed_quality_analysis"))
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'SLA_Segment' in deals.columns:
            sla_global = deals[
                (deals['SLA_Segment'].notna()) & 
                (deals['SLA_Segment'] != 'Unknown')
            ].copy()
            
            if len(sla_global) > 0:
                sla_impact = sla_global.groupby('SLA_Segment').agg({
                    'Id': 'count',
                    'is_paid': 'mean'
                }).reset_index()
                sla_impact.columns = ['SLA_Segment', 'Total_Deals', 'Win_Rate_Pct']
                sla_impact['Win_Rate_Pct'] = (sla_impact['Win_Rate_Pct'] * 100).round(2)
                
                sla_order = ['Top Speed (< 1h)', 'Fast (1h-4h)', 'Normal (4h-24h)', 'Slow (1d-7d)', 'Too Slow (> 7d)']
                sla_impact['SLA_Segment'] = pd.Categorical(sla_impact['SLA_Segment'], categories=sla_order, ordered=True)
                sla_impact = sla_impact.sort_values('SLA_Segment')
                
                fig3 = px.bar(
                    sla_impact,
                    x='SLA_Segment',
                    y='Win_Rate_Pct',
                    color='Total_Deals',
                    text_auto='.1f',
                    title=t('conversion_by_speed'),
                    labels={'Win_Rate_Pct': t('conversion_percent'), 'Total_Deals': t('deals_count')},
                    color_continuous_scale='RdYlGn',
                    height=400
                )
                st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        if 'Quality' in deals.columns:
            deals_quality = deals[deals['Quality'].notna()].copy()
            
            if len(deals_quality) > 0:
                quality_stats = deals_quality.groupby('Quality').agg({
                    'Id': 'count',
                    'stage_normalized': lambda x: (x == 'Active Student').sum()
                }).reset_index()
                quality_stats.columns = ['Quality', 'Total_Leads', 'Active_Students']
                quality_stats['Win_Rate_Pct'] = (quality_stats['Active_Students'] / quality_stats['Total_Leads'] * 100).round(2)
                
                # Фильтр: показываем только категории с >10 лидами
                quality_stats = quality_stats[quality_stats['Total_Leads'] > 10].copy()
                
                fig4 = px.bar(
                    quality_stats,
                    x='Quality',
                    y='Win_Rate_Pct',
                    color='Total_Leads',
                    text_auto='.1f',
                    title=t('conversion_by_quality'),
                    labels={'Win_Rate_Pct': t('conversion_percent'), 'Quality': t('quality')},
                    color_continuous_scale='RdYlGn',
                    height=400
                )
                fig4.update_layout(xaxis={'categoryorder':'category ascending'})
                st.plotly_chart(fig4, use_container_width=True)
    
    st.markdown(f"**{t('detailed_analysis_response_speed')}**")
    
    if 'SLA_seconds' in deals.columns:
        deals_sla = deals[deals['SLA_seconds'].notna()].copy()
        deals_sla['SLA_Hours'] = deals_sla['SLA_seconds'] / 3600
        
        manager_sla_stats = deals_sla.groupby('Deal Owner Name').agg({
            'Id': 'count',
            'SLA_Hours': 'median',
            'is_paid': 'mean'
        }).reset_index()
        manager_sla_stats.columns = ['Manager', 'Deals_Count', 'Median_SLA_Hours', 'Win_Rate_Pct']
        manager_sla_stats['Win_Rate_Pct'] = (manager_sla_stats['Win_Rate_Pct'] * 100).round(2)
        manager_sla_stats = manager_sla_stats[manager_sla_stats['Deals_Count'] > 10]
        
        if len(manager_sla_stats) > 0:
            fig5 = px.scatter(
                manager_sla_stats,
                x='Median_SLA_Hours',
                y='Win_Rate_Pct',
                size='Deals_Count',
                color='Win_Rate_Pct',
                hover_name='Manager',
                title=t('speed_vs_conversion'),
                labels={'Median_SLA_Hours': t('median_sla_hours'), 'Win_Rate_Pct': t('conversion_percent')},
                color_continuous_scale='RdYlGn',
                height=600
            )
            
            avg_sla = manager_sla_stats['Median_SLA_Hours'].median()
            avg_win = manager_sla_stats['Win_Rate_Pct'].median()
            fig5.add_vline(x=avg_sla, line_dash="dash", line_color="gray", annotation_text="Ср.SLA")
            fig5.add_hline(y=avg_win, line_dash="dash", line_color="gray", annotation_text="Ср.конверсия")
            st.plotly_chart(fig5, use_container_width=True)
            
        # ========== ТАБЛИЦА SLA ПО МЕНЕДЖЕРАМ ==========
    st.markdown(f"**{t('manager_sla')}**")

    # Используем ВСЕ сделки как в графике
    all_deals_with_sla = deals.copy()
    all_deals_with_sla['SLA_Hours'] = all_deals_with_sla['SLA_seconds'] / 3600

    manager_table = all_deals_with_sla.groupby('Deal Owner Name').agg({
        'Id': 'count',
        'SLA_Hours': ['median', 'mean'],
        'stage_normalized': lambda x: (x == 'Active Student').sum()
    }).reset_index()

    manager_table.columns = ['Manager', 'Deals_Count', 'Median_SLA_Hours', 'Mean_SLA_Hours', 'Active_Students']
    manager_table['Win_Rate_Pct'] = (manager_table['Active_Students'] / manager_table['Deals_Count'] * 100).round(2)
    manager_table = manager_table[manager_table['Deals_Count'] > 10]

    if len(manager_table) > 0:
        manager_table = manager_table.sort_values('Median_SLA_Hours', ascending=True)
        
        display_df = manager_table[['Manager', 'Deals_Count', 'Median_SLA_Hours', 'Mean_SLA_Hours', 'Win_Rate_Pct']]
        display_df.columns = [t('manager'), t('deals'), t('median_hours'), t('mean_hours'), t('conversion_percent_short')]
        
        st.dataframe(
            display_df.style\
                .background_gradient(subset=[t('median_hours')], cmap='RdYlGn_r')\
                .background_gradient(subset=[t('mean_hours')], cmap='RdYlGn_r')\
                .background_gradient(subset=[t('conversion_percent_short')], cmap='RdYlGn')\
                .format({
                    t('median_hours'): '{:.1f} ч',
                    t('mean_hours'): '{:.1f} ч',
                    t('conversion_percent_short'): '{:.1f}%'
                }),
            use_container_width=True,
            height=300
        )
    
    if 'SLA_seconds' in deals.columns:
        sla_clean = deals[deals['SLA_seconds'].notna()].copy()
        sla_clean['SLA_Minutes'] = sla_clean['SLA_seconds'] / 60
        sla_clean = sla_clean[(sla_clean['SLA_Minutes'] > 0) & (sla_clean['SLA_Minutes'] < 43200)]
        
        if len(sla_clean) > 0:
            sla_clean['SLA_Decile'] = pd.qcut(sla_clean['SLA_Minutes'], q=10, labels=False)
            conversion_by_speed = sla_clean.groupby('SLA_Decile').agg({
                'SLA_Minutes': 'median',
                'stage_normalized': lambda x: (x == 'Active Student').mean() * 100
            }).reset_index()
            conversion_by_speed['Time_Label'] = conversion_by_speed['SLA_Minutes'].apply(
                lambda m: f"{m/60:.1f} ч" if m >= 60 else f"{m:.0f} мин"
            )
            conversion_by_speed.columns = ['Decile', 'SLA_Minutes', 'Win_Rate_Pct', 'Time_Label']
            
            if len(conversion_by_speed) > 0:
                fig6 = px.line(
                    conversion_by_speed,
                    x='SLA_Minutes',
                    y='Win_Rate_Pct',
                    markers=True,
                    text='Time_Label',
                    title=t('conversion_deciles'),
                    labels={'SLA_Minutes': t('response_time_min'), 'Win_Rate_Pct': t('conversion_percent')},
                    height=400
                )
                fig6.update_traces(textposition="top center")
                st.plotly_chart(fig6, use_container_width=True)
                
                def format_time(minutes):
                    if minutes < 60: return f"{minutes:.1f} мин"
                    if minutes < 1440: return f"{minutes/60:.1f} ч"
                    return f"{minutes/1440:.1f} дн"
                
                mean_sla = sla_clean['SLA_Minutes'].mean()
                median_sla = sla_clean['SLA_Minutes'].median()
                q25 = sla_clean['SLA_Minutes'].quantile(0.25)
                q75 = sla_clean['SLA_Minutes'].quantile(0.75)
                
                metrics_df = pd.DataFrame({
                    t('metric'): [t('average_time'), t('median_time'), t('faster_25'), t('faster_75')],
                    t('value'): [format_time(mean_sla), format_time(median_sla), format_time(q25), format_time(q75)]
                })
                
                st.markdown(f"**{t('sla_metrics')}**")
                st.dataframe(
                    metrics_df.style.set_table_styles([
                        {'selector': 'thead th', 'props': [('background-color', '#0235C4'), ('color', 'white')]},
                        {'selector': 'tbody td', 'props': [('background-color', '#f8fafc')]},
                    ]).hide(axis='index'),
                    use_container_width=True,
                    height=200
                )
    
    # ========== 3. ПРИЧИНЫ ОТКАЗОВ ПО МЕНЕДЖЕРАМ ==========
    st.subheader(t("lost_reasons_analysis"))

    if 'Lost Reason' in deals.columns and 'Deal Owner Name' in deals.columns:
        lost_deals = deals[
            (deals['stage_normalized'] == 'Churned') & 
            (deals['Lost Reason'].notna()) &
            (deals['Lost Reason'] != 'unknown') &
            (deals['Lost Reason'] != 'Unknown')
        ].copy()
        
        if len(lost_deals) > 0:
            # Основная таблица БЕЗ итогов
            pivot_table = lost_deals.pivot_table(
                index='Deal Owner Name',
                columns='Lost Reason',
                values='Id',
                aggfunc='count',
                fill_value=0
            )
            
            # Сортируем менеджеров по общему числу отказов
            pivot_table_sorted = pivot_table.loc[pivot_table.sum(axis=1).sort_values(ascending=False).index]
            
            # Добавляем строку "ВСЕГО" ВНИЗУ
            pivot_table_with_total = pivot_table_sorted.copy()
            pivot_table_with_total.loc[t('total')] = pivot_table_sorted.sum()
            
            # Добавляем колонку "ВСЕГО" СПРАВА
            pivot_table_with_total[t('total')] = pivot_table_with_total.sum(axis=1)
            
            # Создаем стиль
            styled_table = pivot_table_with_total.style.format("{:.0f}")
            
            # 1. МЕНЕДЖЕРЫ: построчное окрашивание (кроме колонки "ВСЕГО")
            reason_columns = [col for col in pivot_table_with_total.columns if col != t('total')]
            for idx in pivot_table_with_total.index:
                if idx != t('total'):
                    styled_table = styled_table.background_gradient(
                        subset=pd.IndexSlice[idx, reason_columns],
                        cmap='YlOrBr', 
                        vmin=0,
                        axis=1
                    )
            
            # 2. СТРОКА "ВСЕГО": горизонтальное окрашивание ВСЕЙ строки
            styled_table = styled_table.background_gradient(
                subset=pd.IndexSlice[t('total'), :],
                cmap='YlOrBr',
                vmin=0,
                axis=1
            )
            
            # 3. КОЛОНКА "ВСЕГО": вертикальное окрашивание (кроме строки "ВСЕГО")
            styled_table = styled_table.background_gradient(
                subset=pd.IndexSlice[pivot_table_with_total.index.drop(t('total')), t('total')],
                cmap='Reds',
                vmin=0,
                axis=0
            )
            
            # 4. ЯЧЕЙКА ПЕРЕСЕЧЕНИЯ ('ВСЕГО', 'ВСЕГО'): убираем цвет
            styled_table = styled_table.map(
                lambda val: 'background-color: transparent !important',
                subset=pd.IndexSlice[t('total'), t('total')]
            )
            
            st.markdown(f"**{t('lost_reasons_distribution')}**")
            st.dataframe(
                styled_table,
                use_container_width=True,
                height=600
            )
            
            # Общее распределение причин
            st.markdown(f"**{t('total_distribution')}**")
            reason_total = lost_deals['Lost Reason'].value_counts().reset_index()
            reason_total.columns = [t('lost_reason'), t('quantity')]
            reason_total[t('share_percent')] = (reason_total[t('quantity')] / len(lost_deals) * 100).round(1)
            
            st.dataframe(
                reason_total.style\
                    .background_gradient(subset=[t('share_percent')], cmap='YlOrBr')\
                    .format({t('share_percent'): '{:.1f}%'}),
                use_container_width=True,
                height=300
            )

# ---------- ВКЛАДКА 3: ПРОДУКТЫ ----------
with tabs[2]:
    st.markdown(f'<div class="section-title">{t("products_payments_analysis")}</div>', unsafe_allow_html=True)
    
    # Подготовка данных
    deals_success = deals[deals['stage_normalized'] == 'Active Student'].copy()
    pay_col = 'Payment_Type_Recovered' if 'Payment_Type_Recovered' in deals_success.columns else 'Payment Type'
    
    if len(deals_success) > 0:
        # Рассчитываем Transactions как в юнит-экономике
        deals_success['Transactions'] = np.where(
            deals_success[pay_col] == 'one payment', 
            1, 
            deals_success['Months of study'].fillna(1)
        )
        
        # 1. ПОЛНЫЕ МЕТРИКИ ПО ПРОДУКТАМ
        st.subheader(t("full_product_metrics"))
        
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
            st.subheader(t("product_efficiency"))
            
            col1, col2 = st.columns(2)
            
            with col1:
                # График 1: Выручка по продуктам (цвет = LTV)
                fig1 = px.bar(
                    display_df.reset_index(),
                    x='Product', y='Revenue',
                    color='LTV',
                    title=t('revenue_by_products'),
                    labels={'Revenue': t('revenue_euro_full'), 'LTV': t('ltv_full')},
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
                    title=t('product_matrix'),
                    labels={'B': t('clients_count'), 'Avg_Check': t('avg_check_full'), 'Collection_Ratio': t('collection_ratio')},
                    color_continuous_scale='Viridis',
                    height=500
                )
                fig2.update_traces(textposition='top center')
                st.plotly_chart(fig2, use_container_width=True)
            
            # 3. АНАЛИЗ ТИПОВ ОПЛАТЫ
            st.subheader(t("payment_type_analysis"))
            
            if pay_col in deals_success.columns:
                # Фильтруем те же продукты
                deals_filtered = deals_success[deals_success['Product'].isin(display_df.index)]
                payment_split = deals_filtered.groupby(['Product', pay_col]).size().reset_index(name='Count')
                
                if len(payment_split) > 0:
                    # Stacked bar
                    fig3 = px.bar(
                        payment_split,
                        x='Product', y='Count', color=pay_col,
                        title=t('payment_type_distribution'),
                        labels={'Count': t('deals_count')},
                        color_discrete_sequence=px.colors.qualitative.Set3,
                        height=500
                    )
                    fig3.update_layout(xaxis={'categoryorder': 'total descending'}, barmode='stack')
                    st.plotly_chart(fig3, use_container_width=True)
            
            # 4. АНАЛИЗ ТИПОВ ОБУЧЕНИЯ
            st.subheader(t("education_type_analysis"))
            
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
                        title=t('revenue_by_education'),
                        labels={'Revenue': t('revenue_euro'), 'Avg_Check': t('avg_check_full')},
                        color_continuous_scale='RdYlGn',
                        height=500
                    )
                    fig4.update_layout(xaxis={'categoryorder': 'total descending'})
                    st.plotly_chart(fig4, use_container_width=True)
    else:
        st.warning(t('no_successful_deals'))

# ---------- ВКЛАДКА 4: ГЕОГРАФИЯ ----------
with tabs[3]:
    st.markdown(f'<div class="section-title">{t("geographical_analysis")}</div>', unsafe_allow_html=True)
    
    # Подготовка данных
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
        
        city_stats.columns = ['City', 'Total_Deals', 'Active_Students', 'Total_Revenue', 'Top_Source']
        city_stats['Win_Rate'] = (city_stats['Active_Students'] / city_stats['Total_Deals'] * 100).round(2)
        city_stats = city_stats.sort_values('Total_Revenue', ascending=False)
        
        # 1. КАРТА ПРОДАЖ
        geocoded = prepare_geodata(city_stats)
        geocoded_count = len(geocoded)
        total_cities = len(city_stats)
        
        st.subheader(f"{t('sales_map')} (Топ-{geocoded_count} из {total_cities} {t('cities')})")

        if len(geocoded) > 0:
            fig_map = px.scatter_mapbox(
                geocoded,
                lat="lat",
                lon="lon",
                size="Total_Deals",
                color="Total_Revenue",
                hover_name="City",
                hover_data={
                    'Total_Revenue': ':.0f',
                    'Total_Deals': True,
                    'Win_Rate': ':.1f',
                    'Top_Source': True
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
            st.info(t('no_data_for_display'))

        
        # 2. ТОП ГОРОДОВ ПО ВЫРУЧКЕ
        top_n = 15
        st.subheader(f"{t('top_cities_revenue')} (Топ-{top_n})")
        
        city_top15 = city_stats.head(top_n).copy()
        
        fig_bar = px.bar(
            city_top15,
            x='City',
            y='Total_Revenue',
            color='Top_Source',
            text_auto='.2s',
            title=f'Топ-{top_n} {t('cities').lower()} по {t('revenue').lower()}',
            labels={'Total_Revenue': t('revenue_euro')},
            color_discrete_sequence=px.colors.qualitative.Set3,
            height=500
        )
        fig_bar.update_layout(xaxis={'categoryorder': 'total descending'})
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # 3. АНАЛИЗ ЭФФЕКТИВНОСТИ ПО ГОРОДАМ
        st.subheader(t("city_efficiency_analysis"))

        
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
                title=t('top_conversion_cities'),
                labels={'Win_Rate': t('win_rate'), 'City': ''},
                color='Total_Revenue',
                color_continuous_scale='RdYlGn',
                height=500
            )
            fig_conv.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig_conv.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'},
                                  margin=dict(r=100))
            st.plotly_chart(fig_conv, use_container_width=True)
        
        # 4. ДОПОЛНИТЕЛЬНЫЕ ГРАФИКИ
        st.subheader(t("additional_metrics"))
        
        # ТОП-10 ПО ОБЪЕМУ СДЕЛОК
        top_volume = city_stats.head(10).sort_values('Total_Deals', ascending=True)
        
        fig_volume = px.bar(
            top_volume,
            x='Total_Deals',
            y='City',
            orientation='h',
            text='Total_Deals',
            title=t('top_volume_cities'),
            labels={'Total_Deals': t('total_deals'), 'City': ''},
            color='Win_Rate',
            color_continuous_scale='RdYlGn',
            height=500
        )
        fig_volume.update_traces(textposition='outside')
        fig_volume.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'},
                                margin=dict(r=80))
        st.plotly_chart(fig_volume, use_container_width=True)
        
        # РАСПРЕДЕЛЕНИЕ ИСТОЧНИКОВ - НА ВСЮ ШИРИНУ
        source_dist = city_stats.groupby('Top_Source').agg({
            'City': 'count',
            'Total_Revenue': 'sum'
        }).reset_index()
        source_dist.columns = ['Source', 'Cities_Count', 'Total_Revenue']
        source_dist = source_dist.sort_values('Cities_Count', ascending=False).head(15)
        
        fig_sources = px.bar(
            source_dist,
            x='Source',
            y='Cities_Count',
            color='Total_Revenue',
            text='Cities_Count',
            title=t('source_distribution'),
            labels={'Cities_Count': t('cities_count')},
            color_continuous_scale='Viridis',
            height=500
        )
        fig_sources.update_traces(texttemplate='%{text} городов', textposition='outside')
        fig_sources.update_layout(
            xaxis_tickangle=-45,
            xaxis_title=t('traffic_source'),
            yaxis_title=t('cities_count')
        )
        st.plotly_chart(fig_sources, use_container_width=True)
        
        # 5. УРОВНИ НЕМЕЦКОГО ПО ГОРОДАМ
        st.subheader(t("german_levels_by_cities"))
        
        if 'Level of Deutsch' in deals.columns:
            deals_lang = deals[
                (deals['max_stage_rank'] >= 1) & 
                (deals['Level of Deutsch'].notna()) &
                (deals['Level of Deutsch'] != 'Unknown') &
                (deals['Level of Deutsch'] != 'unknown')
            ].copy()
            
            if len(deals_lang) > 0:
                # Берем топ-50 городов по выручке
                city_revenue = deals.groupby('City')['revenue'].sum().nlargest(50).index.tolist()
                deals_city_lang = deals[
                    (deals['City'].isin(city_revenue)) &
                    (deals['Level of Deutsch'].notna()) &
                    (deals['Level of Deutsch'] != 'Unknown') &
                    (deals['Level of Deutsch'] != 'unknown') &
                    (deals['stage_normalized'] == 'Active Student')
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
                    city_stats_summary = deals.groupby('City').agg({
                        'Id': 'count',
                        'revenue': 'sum',
                        'stage_normalized': lambda x: (x == 'Active Student').sum()
                    }).reset_index()
                    city_stats_summary.columns = ['City', 'Total_Deals', 'Total_Revenue', 'Active_Students']
                    city_stats_summary['Win_Rate_Pct'] = (city_stats_summary['Active_Students'] / city_stats_summary['Total_Deals'] * 100).round(1)
                    city_stats_summary['Avg_Check_City'] = (city_stats_summary['Total_Revenue'] / city_stats_summary['Active_Students']).round(0)
                    
                    pivot_table = pd.merge(
                        pivot_table,
                        city_stats_summary[['City', 'Total_Deals', 'Total_Revenue', 'Active_Students', 'Win_Rate_Pct', 'Avg_Check_City']],
                        left_index=True,
                        right_on='City'
                    )
                    
                    pivot_table = pivot_table.sort_values('Total_Revenue', ascending=False)
                    
                    # Отображаем таблицу
                    st.dataframe(
                        pivot_table.style.format({
                            'Total_Revenue': '{:,.0f}',
                            'Active_Students': '{:,.0f}',
                            'Avg_Check_City': '{:,.0f}',
                            'Win_Rate_Pct': '{:.1f}%',
                            **{level: '{:.1f}%' for level in level_order}
                        }).background_gradient(subset=['Total_Revenue', 'Avg_Check_City', 'Win_Rate_Pct'], cmap='RdYlGn'),
                        use_container_width=True,
                        height=400
                    )
        
        # 6. АНАЛИЗ УРОВНЕЙ ЯЗЫКА
        st.subheader(t("german_level_analysis"))
        
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
                
                lang_stats.columns = ['Level', 'Total_Deals', 'Active_Students', 'Total_Revenue']
                lang_stats['Win_Rate'] = (lang_stats['Active_Students'] / lang_stats['Total_Deals'] * 100).round(2)
                lang_stats['Avg_Revenue_per_Student'] = (lang_stats['Total_Revenue'] / lang_stats['Active_Students']).round(0)
                
                level_order = ['A0', 'A1', 'A2', 'B1', 'B2', 'C1', 'C2']
                lang_stats['Level'] = pd.Categorical(lang_stats['Level'], categories=level_order, ordered=True)
                lang_stats = lang_stats.sort_values('Level').dropna()
                
                # График конверсии по уровням
                fig_lang1 = px.bar(
                    lang_stats,
                    x='Level',
                    y='Win_Rate',
                    color='Total_Deals',
                    text_auto='.1f',
                    title=t('conversion_by_level'),
                    labels={'Win_Rate': t('win_rate'), 'Level': t('level')},
                    color_continuous_scale='Teal',
                    height=400
                )
                fig_lang1.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': level_order})
                st.plotly_chart(fig_lang1, use_container_width=True)
                
                # Финансовые показатели по уровням
                fig_lang2 = make_subplots(
                    rows=1, cols=2,
                    subplot_titles=[t('revenue_by_level'), t('avg_revenue_per_student')],
                    horizontal_spacing=0.15
                )
                
                fig_lang2.add_trace(
                    go.Bar(
                        x=lang_stats['Level'],
                        y=lang_stats['Total_Revenue'],
                        text=lang_stats['Total_Revenue'].apply(lambda x: f'{x:,.0f}'),
                        textposition='auto',
                        marker_color='#636EFA',
                        name=t('revenue')
                    ),
                    row=1, col=1
                )
                
                fig_lang2.add_trace(
                    go.Bar(
                        x=lang_stats['Level'],
                        y=lang_stats['Avg_Revenue_per_Student'],
                        text=lang_stats['Avg_Revenue_per_Student'].apply(lambda x: f'{x:,.0f}'),
                        textposition='auto',
                        marker_color='#00CC96',
                        name=t('avg_revenue_per_student')
                    ),
                    row=1, col=2
                )
                
                fig_lang2.update_xaxes(title_text=t('level'), row=1, col=1)
                fig_lang2.update_xaxes(title_text=t('level'), row=1, col=2)
                fig_lang2.update_yaxes(title_text=t('revenue_euro'), row=1, col=1)
                fig_lang2.update_yaxes(title_text=t('avg_revenue_per_student'), row=1, col=2)
                fig_lang2.update_layout(showlegend=False, height=400, title_text=t('financial_by_level'))
                st.plotly_chart(fig_lang2, use_container_width=True)
                
                # Таблица статистики по уровням
                st.markdown(f"**{t('level_statistics')}**")
                st.dataframe(
                    lang_stats.style.format({
                        'Total_Revenue': '{:,.0f}',
                        'Avg_Revenue_per_Student': '{:,.0f}',
                        'Win_Rate': '{:.1f}%'
                    }).background_gradient(subset=['Win_Rate', 'Total_Revenue'], cmap='RdYlGn'),
                    use_container_width=True,
                    height=300
                )
        
        # 7. СВОДНАЯ СТАТИСТИКА ПО ГЕОГРАФИИ
        st.subheader(t("geography_summary"))
        
        # Распределение городов по группам
        city_groups = pd.cut(
            city_stats['Total_Deals'],
            bins=[0, 1, 3, 10, 30, 100, float('inf')],
            labels=['1 сделка', '2-3', '4-10', '11-30', '31-100', '100+']
        )
        
        group_stats = pd.DataFrame({
            t('group'): city_groups,
            t('cities'): 1,
            t('revenue'): city_stats['Total_Revenue']
        }).groupby(t('group'), observed=False).agg({
            t('cities'): 'count',
            t('revenue'): 'sum'
        })
        
        if len(group_stats) > 0:
            group_stats[t('revenue_share')] = (group_stats[t('revenue')] / group_stats[t('revenue')].sum() * 100).round(1)
            group_stats[t('revenue_per_city')] = (group_stats[t('revenue')] / group_stats[t('cities')].replace(0, np.nan)).fillna(0).astype(int)
            
            fig_groups = px.bar(
                group_stats.reset_index(),
                x=t('group'),
                y=t('cities'),
                color=t('revenue_share'),
                text=t('cities'),
                title=t('city_groups_distribution'),
                labels={t('cities'): t('cities_count')},
                color_continuous_scale='RdYlGn',
                height=400
            )
            fig_groups.update_traces(textposition='outside')
            st.plotly_chart(fig_groups, use_container_width=True)
        
        # Ключевые метрики географии - отдельно под графиком
        source_leadership = city_stats['Top_Source'].value_counts().head(5).reset_index()
        source_leadership.columns = [t('source'), t('cities_count')]
        source_leadership[t('share')] = (source_leadership[t('cities_count')] / len(city_stats) * 100).round(1)
        
        # Общее количество студентов по всем городам
        total_students_all_cities = city_stats['Active_Students'].sum()
        
        geo_summary_data = {
            t('metric'): [
                t('cities_with_data'),
                t('cities_5_deals'),
                t('avg_win_rate_cities'),
                t('top3_revenue_share'),
                t('most_common_source'),
                t('cities_with_source'),
                t('top3_students_share')
            ],
            t('value'): [
                f"{len(city_stats)}",
                f"{len(city_stats[city_stats['Total_Deals'] >= 5])}",
                f"{city_stats['Win_Rate'].mean():.1f}%",
                f"{city_stats.head(3)['Total_Revenue'].sum() / city_stats['Total_Revenue'].sum() * 100:.1f}%",
                f"{source_leadership.iloc[0][t('source')]}",
                f"{source_leadership.iloc[0][t('cities_count')]} ({source_leadership.iloc[0][t('share')]}%)",
                f"{(city_stats.head(3)['Active_Students'].sum() / total_students_all_cities * 100):.1f}%"
            ]
        }
        
        geo_summary_df = pd.DataFrame(geo_summary_data)
        st.markdown(f"**{t('key_geo_metrics')}**")
        st.dataframe(
            geo_summary_df.style.set_table_styles([
                {'selector': 'thead th', 'props': [('background-color', '#0235C4'), ('color', 'white')]},
                {'selector': 'tbody td', 'props': [('background-color', '#f8fafc')]},
            ]).hide(axis='index'),
            use_container_width=True,
            height=300
        )
    else:
        st.warning(t('no_city_data'))

# ---------- ВКЛАДКА 5: ЮНИТ-ЭКОНОМИКА ----------
with tabs[4]:
    st.markdown(f'<div class="section-title">{t("unit_economics")}</div>', unsafe_allow_html=True)
    
    # Получаем данные
    total_df, product_econ = calculate_unit_economics()
    product_econ = product_econ[product_econ['B'] > 1].copy()
    
    if len(total_df) == 0 or len(product_econ) == 0:
        st.warning(t('no_unit_economics_data'))
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
        
        st.subheader(t("total_business_economics"))
        st.dataframe(
            format_unit_econ(total_df).background_gradient(subset=['ROMI', 'LTV'], cmap='Greens'),
            use_container_width=True,
            height=150
        )
        
        st.subheader(t("product_economics"))
        st.dataframe(
            format_unit_econ(product_econ).background_gradient(subset=['ROMI', 'LTV'], cmap='RdYlGn'),
            use_container_width=True
        )
        
        # Визуализация
        col1, col2 = st.columns(2)
        
        with col1:
            if len(product_econ) > 0:
                fig = px.bar(
                    product_econ, x='Product', y='Revenue',
                    title=t('revenue_by_product'), color='LTV',
                    color_continuous_scale='RdYlGn',
                    labels={'Revenue': t('revenue_euro'), 'LTV': t('ltv_euro')}
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if len(product_econ) > 0:
                fig2 = px.scatter(
                    product_econ, x='C1', y='LTV', size='Revenue',
                    color='Product', hover_name='Product',
                    title=t('ltv_matrix'),
                    labels={'C1': t('conversion_c1_axis'), 'LTV': t('ltv_euro')}
                )
                st.plotly_chart(fig2, use_container_width=True)
        
        # Легенда метрик
        with st.expander(t("metrics_guide")):
            st.markdown(t('metrics_guide_text'))

# ---------- ВКЛАДКА 6: ТОЧКИ РОСТА ----------
with tabs[5]:
    st.markdown(f'<div class="section-title">{t("growth_points_analysis")}</div>', unsafe_allow_html=True)
    
    # --- НАСТРОЙКИ ---
    GROWTH_PCT = 0.10
    COGS_FIXED_PER_TRANS = 0
    COGS_PERCENT_FROM_CHECK = 0.0
    
    ACTION_INSIGHTS = {
        'UA': t('scaling_channels'),
        'C1': t('funnel_optimization'), 
        'AOV': t('upsell_pricing'),
        'APC': t('retention_loyalty'),
        'CPA': t('ad_optimization')
    }
    
    # --- ФУНКЦИИ ---
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
            t('scenario'): scenario_name, t('scenario_type'): scenario_type, t('growth_pct'): growth_pct,
            t('product'): product_name, 'UA': ua, 'C1': c1, 'B': b, 'AOV': aov, 'APC': apc, 
            t('transactions'): t, t('revenue'): revenue, 'AC': ac, 'CLTV': cltv, 'LTV': ltv, 
            'CPA': cpa, 'CAC': cac, 'CM': cm, 'ROMI': romi
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

    def run_sensitivity_analysis(row, product_name):
        base_cm = row['CM'] if 'CM' in row else 0
        results = []
        
        metrics = ['UA', 'C1', 'AOV', 'APC']
        steps = [-0.10, -0.05, 0.05, 0.10]
        
        for metric in metrics:
            for step in steps:
                u = row['UA'] * (1 + step) if metric == 'UA' else row['UA']
                c = row['C1'] * (1 + step) if metric == 'C1' else row['C1']
                a = row['AOV'] * (1 + step) if metric == 'AOV' else row['AOV']
                p = row['APC'] * (1 + step) if metric == 'APC' else row['APC']
                
                cost = row['AC'] * (1 + step) if metric == 'UA' else row['AC']
                
                b = u * c if u > 0 and c > 0 else 0
                t = b * p if b > 0 and p > 0 else 0
                rev = t * a if t > 0 and a > 0 else 0
                cogs = (rev * COGS_PERCENT_FROM_CHECK) + (t * COGS_FIXED_PER_TRANS)
                cm = rev - cost - cogs
                
                cm_impact = cm - base_cm
                cm_impact_pct = (cm_impact / abs(base_cm) * 100) if abs(base_cm) > 0 else 0
                
                results.append({
                    t('metric'): metric, t('change'): f"{step:+.0%}",
                    t('new_value'): (u if metric=='UA' else c if metric=='C1' else a if metric=='AOV' else p),
                    t('cm_impact'): cm_impact, t('cm_impact_pct'): cm_impact_pct
                })
        
        return pd.DataFrame(results)
    
    # --- РАСЧЕТ TOTAL BUSINESS ---
    st.subheader(t("total_business_analysis"))
    
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
        'Revenue': total_revenue,
        'T': total_t,
        'AC': total_marketing_spend,
        'C1': TOTAL_B_CORRECT / TOTAL_UA if TOTAL_UA > 0 else 0,
        'AOV': total_revenue / total_t if total_t > 0 else 0,
        'APC': total_t / TOTAL_B_CORRECT if TOTAL_B_CORRECT > 0 else 0,
        'CM': total_revenue - total_marketing_spend - cogs_global
    }
    
    global_scenarios = generate_scenarios_for_row(global_row, "TOTAL BUSINESS")
    
    if not global_scenarios.empty:
        base_scenario = global_scenarios[global_scenarios['Scenario'] == 'BASELINE']  # 'Scenario' вместо t('scenario')
        if not base_scenario.empty:
            base_cm = base_scenario.iloc[0]['CM']
            global_scenarios['CM_Growth_€'] = global_scenarios['CM'] - base_cm  # 'CM_Growth_€' вместо t('cm_growth')
    
    st.subheader(t("global_business_scenarios"))
    
    format_dict = {
        'UA': '{:,.0f}', 'B': '{:,.0f}', 'T': '{:,.0f}', 'Revenue': '{:,.0f}', 
        'C1': '{:.2%}', 'ROMI': '{:.0f}%', 'AOV': '{:,.1f}', 'APC': '{:.2f}', 
        'CLTV': '{:,.0f}', 'LTV': '{:,.1f}', 'AC': '{:,.0f}', 'CPA': '{:,.2f}', 
        'CAC': '{:,.1f}', 'CM': '{:,.0f}', 'CM_Growth_€': '{:+,.0f}'  # ← 'CM_Growth_€' вместо t('cm_growth')
    }
    
    cols = [t('scenario'), 'UA', 'C1', 'B', 'T', 'AOV', 'APC', t('revenue'), 'AC', 
            'CPA', 'CAC', 'CLTV', 'LTV', 'CM', t('cm_growth'), 'ROMI']
    
    if 'CM_Growth_€' in global_scenarios.columns:
        sorted_df = global_scenarios[cols].sort_values('CM_Growth_€', ascending=False)  # Английское название
    else:
        sorted_df = global_scenarios[cols]
    
    st.dataframe(
        sorted_df.style.format(format_dict).background_gradient(
            subset=['CM_Growth_€' if 'CM_Growth_€' in global_scenarios.columns else 'CM'],  # Английские названия
            cmap='Greens', vmin=0),
        use_container_width=True
    )
    
    growth_scenarios = global_scenarios[global_scenarios['Scenario'] != 'BASELINE']
    if not growth_scenarios.empty and t('cm_growth') in growth_scenarios.columns:
        # Округляем для корректного сравнения
        growth_scenarios['CM_Growth_Rounded'] = growth_scenarios[t('cm_growth')].round(0)
        max_growth = growth_scenarios['CM_Growth_Rounded'].max()
        best_scenarios = growth_scenarios[growth_scenarios['CM_Growth_Rounded'] == max_growth]
        
        st.write(f"**{t('best_scenarios')} ({len(best_scenarios)} с одинаковым эффектом):**")
        for _, scenario in best_scenarios.iterrows():
            st.write(f"- **{scenario['Scenario']}**: {t('profit_growth')} {scenario['CM_Growth_€']:+,.0f} €")
            st.write(f"  ROMI: {scenario['ROMI']:.1f}%")
            st.write(f"  {t('action')}: {ACTION_INSIGHTS.get(scenario['Scenario_Type'], '')}")
    
    # Анализ чувствительности
    st.subheader(t("sensitivity_analysis"))
    
    sens_df = run_sensitivity_analysis(global_row, "TOTAL")
    if not sens_df.empty:
        sens_df = sens_df.sort_values(t('cm_impact'), ascending=False)
        
        st.dataframe(
            sens_df.style.format({
                t('new_value'): '{:.2f}', t('cm_impact'): '{:+,.0f}', t('cm_impact_pct'): '{:+.1f}%'
            }).background_gradient(subset=[t('cm_impact')], cmap='RdYlGn'),
            use_container_width=True
        )
        
        st.write(f"**{t('sensitivity_insights')}**")
        for metric in ['UA', 'C1', 'AOV', 'APC']:
            metric_data = sens_df[sens_df[t('metric')] == metric]
            if not metric_data.empty:
                max_impact = metric_data.loc[metric_data[t('cm_impact')].idxmax()]
                st.write(f"- **{metric}**: {max_impact[t('change')]} → {t('cm_impact')}: {max_impact[t('cm_impact')]:+,.0f} €")
    
    # --- АНАЛИЗ ПО ПРОДУКТАМ ---
    st.subheader(t("product_analysis"))
    
    product_stats = active_students_df.groupby('Product').agg({
        'Contact Name': 'nunique', 'revenue': 'sum', 'Transactions': 'sum'
    }).reset_index().rename(columns={'Contact Name': 'B', 'Transactions': 'T', 'revenue': 'Revenue'})

    product_stats['UA'] = TOTAL_UA
    product_stats['AC'] = total_marketing_spend
    product_stats['C1'] = product_stats['B'] / product_stats['UA']
    product_stats['AOV'] = product_stats['Revenue'] / product_stats['T']
    product_stats['APC'] = product_stats['T'] / product_stats['B']

    total_cogs_amt = (product_stats['Revenue'] * COGS_PERCENT_FROM_CHECK) + (product_stats['T'] * COGS_FIXED_PER_TRANS)
    product_stats['COGS'] = total_cogs_amt / product_stats['T']
    product_stats['CLTV'] = (product_stats['AOV'] - product_stats['COGS']) * product_stats['APC']
    product_stats['LTV'] = product_stats['CLTV'] * product_stats['C1']
    product_stats['CPA'] = product_stats['AC'] / product_stats['UA']
    product_stats['CAC'] = product_stats['AC'] / product_stats['B']
    product_stats['CM'] = product_stats['Revenue'] - product_stats['AC'] - total_cogs_amt
    product_stats['ROMI'] = (product_stats['CM'] / product_stats['AC']) * 100

    revenue_threshold = product_stats['Revenue'].max() * 0.1
    top_products = product_stats[product_stats['Revenue'] > revenue_threshold].copy()
    
    if len(top_products) > 0:
        all_scenarios = []
        
        for _, row in top_products.iterrows():
            product_name = row['Product']
            
            with st.expander(f"**{product_name.upper()}**"):
                scenarios = generate_scenarios_for_row(row, product_name)
                if not scenarios.empty:
                    # 1. Исправляем обращения к столбцам
                    base_scenario = scenarios[scenarios['Scenario'] == 'BASELINE']  # 'Scenario' вместо t('scenario')
                    if not base_scenario.empty:
                        base_cm = base_scenario.iloc[0]['CM']
                        scenarios['CM_Growth_€'] = scenarios['CM'] - base_cm  # 'CM_Growth_€' вместо t('cm_growth')
                    
                    # 2. Английские названия столбцов
                    display_cols = ['Scenario', 'UA', 'C1', 'B', 'AOV', 'APC', 'Revenue', 'CM', 'CM_Growth_€', 'ROMI']  # Английские!
                    
                    # 3. Проверка и сортировка по английским названиям
                    if 'CM_Growth_€' in scenarios.columns:
                        display_df = scenarios[display_cols].sort_values('CM_Growth_€', ascending=False)  # Английское
                    else:
                        display_df = scenarios[display_cols]
                    
                    # 4. Форматирование с английскими ключами
                    st.dataframe(
                        display_df.style.format({
                            'UA': '{:,.0f}', 'B': '{:,.0f}', 'Revenue': '{:,.0f}',  # 'Revenue' вместо t('revenue')
                            'CM': '{:,.0f}', 'CM_Growth_€': '{:+,.0f}' if 'CM_Growth_€' in scenarios.columns else '{}',  # Английское
                            'ROMI': '{:.1f}%',
                            'C1': '{:.2%}', 'AOV': '{:,.1f}', 'APC': '{:.2f}'
                        }).background_gradient(
                            subset=['CM_Growth_€' if 'CM_Growth_€' in scenarios.columns else 'CM', 'ROMI'],  # Английские
                            cmap='RdYlGn'),
                        use_container_width=True
                    )
                    
                    # 5. Английские названия столбцов
                    growth_scenarios = scenarios[scenarios['Scenario'] != 'BASELINE']  # 'Scenario' вместо t('scenario')
                    if not growth_scenarios.empty and 'CM_Growth_€' in growth_scenarios.columns:  # 'CM_Growth_€' вместо t('cm_growth')
                        growth_scenarios['CM_Growth_Rounded'] = growth_scenarios['CM_Growth_€'].round(0)  # Английское
                        max_growth = growth_scenarios['CM_Growth_Rounded'].max()
                        best_scenarios = growth_scenarios[growth_scenarios['CM_Growth_Rounded'] == max_growth]
                        
                        st.write(f"**{t('product_scenarios')} ({len(best_scenarios)} с одинаковым эффектом):**")
                        for _, scenario in best_scenarios.iterrows():
                            st.write(f"- **{scenario['Scenario']}**: {t('profit_growth')} {scenario['CM_Growth_€']:+,.0f} €")
                            st.write(f"  {t('action')}: {ACTION_INSIGHTS.get(scenario['Scenario_Type'], '')}")
                    
            # Сводная карта приоритетов
            if all_scenarios:
                st.subheader(t("priority_map"))
                
                summary = pd.DataFrame(all_scenarios)
                summary['Growth_Pct'] = (summary['CM_Growth_€'] / summary['Base_CM'].abs() * 100)  # Английские ключи
                summary['Growth_Pct'] = summary['Growth_Pct'].apply(lambda x: x if abs(x) < 1000 else (1000 if x > 0 else -1000))
                summary = summary.sort_values(['CM_Growth_€', 'Product'], ascending=[False, True])  # Английские
                
                st.dataframe(
                    summary.style.format({
                        'CM_Growth_€': '{:+,.0f}',  # Английское
                        'Base_CM': '{:,.0f}', 
                        'Growth_Pct': '{:+.1f}%'  # Английское
                    }).background_gradient(subset=['CM_Growth_€'], cmap='Greens', vmin=0)
                    .background_gradient(subset=['Growth_Pct'], cmap='RdYlGn', vmin=-100, vmax=100),
                    use_container_width=True
                )
# ---------- ВКЛАДКА 7: Дерево метрик и A/B тесты ----------
with tabs[6]:
    st.markdown(f'<div class="section-title">{t("methodology_ab_testing")}</div>', unsafe_allow_html=True)
    
    # 1. ДЕРЕВО МЕТРИК
    st.subheader(t("business_metrics_tree"))
    st.markdown(t('metrics_tree_text'))
    
    # 2. HADI-ЦИКЛЫ И A/B ТЕСТЫ
    st.subheader(t("hadi_cycles_ab_tests"))
    
    # Основные продукты для анализа
    main_products = ["digital marketing", "ux/ui design", "web developer"]
    
    # Подготовка данных
    contacts_local = contacts.copy()
    if 'created_date' not in contacts_local.columns:
        contacts_local['created_date'] = pd.to_datetime(contacts_local['Created Time']).dt.date
    
    TOTAL_UA = contacts_local['Id'].nunique()
    active_students_df = deals[deals['stage_normalized'] == 'Active Student']
    buyers_per_product = active_students_df.groupby('Product')['Contact Name'].nunique()
    c1_per_product = buyers_per_product / TOTAL_UA if TOTAL_UA > 0 else 0
    
    product_stats = pd.DataFrame({
        t('product'): buyers_per_product.index,
        t('buyers'): buyers_per_product.values,
        t('traffic'): TOTAL_UA,
        t('conversion'): c1_per_product.values
    })
    product_stats = product_stats[product_stats[t('product')].isin(main_products)]
    
    if len(product_stats) > 0:
        st.write(f"**{t('ab_test_basics')}**")
        st.dataframe(
            product_stats.style.format({
                t('buyers'): '{:,.0f}',
                t('traffic'): '{:,.0f}',
                t('conversion'): '{:.2%}'
            }),
            use_container_width=True
        )
        
        # Гипотезы для A/B тестов
        hypotheses = [
            (t('manager_notification'), t('manager_notification_text')),
            (t('auto_materials'), t('auto_materials_text')),
            (t('sms_reminder'), t('sms_reminder_text'))
        ]
        
        st.write(f"**{t('ready_hadi_cycles')}**")
        
        for hyp_name, hyp_text in hypotheses:
            with st.expander(f"{hyp_name}"):
                st.write(f"**{t('hypothesis')}:** {hyp_text}")
                st.write(f"**{t('hadi_cycle')}**")
                
                hadi_df = pd.DataFrame({
                    t('stage'): [
                        t('hadi_cycle_stages')['h'],
                        t('hadi_cycle_stages')['a'],
                        t('hadi_cycle_stages')['d'],
                        t('hadi_cycle_stages')['i']
                    ],
                    t('formulation'): [
                        f"{hyp_text}. Ожидаемый рост конверсии на 10%.",
                        "Настроить процесс согласно гипотезе для тестовой группы (50%). Контрольная группа — текущий процесс.",
                        "Срок теста — 2 недели. Сравниваются две группы лидов. Метрика — конверсия (C1). Цель — прирост ≥ 10%.",
                        "Гипотеза подтверждается, если прирост конверсии ≥ целевого уровня и результат статистически значим."
                    ]
                })
                
                st.table(hadi_df)
                
                abtest_df = pd.DataFrame({
                    t('parameter'): [
                        t('hypothesis'),
                        t('null_hypothesis'),
                        t('test_conditions_a'),
                        t('test_conditions_b'),
                        t('tracking_metric'),
                        t('hypothesis_threshold'),
                        t('significance_level')
                    ],
                    t('description'): [
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
    
    # 3. РАСЧЕТ ПАРАМЕТРОВ A/B ТЕСТОВ
    st.subheader(t("ab_test_params"))
    
    st.markdown(t('ab_test_calc_description'))
    
    if len(product_stats) > 0:
        # Параметры эксперимента
        ALPHA = 0.05
        POWER = 0.8
        MDE_LIST = [0.10, 0.20, 0.30]  # +10%, +20%, +30%
        
        # Расчет среднего количества лидов в день (на одну группу)
        daily_leads = contacts_local.groupby('created_date')['Id'].nunique().mean()
        DAILY_LEADS_PER_GROUP = daily_leads / 2 if daily_leads > 0 else 10
        
        # Функция для расчетов
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
        
        # Генерация таблицы расчетов
        results = []
        
        for _, row in product_stats.iterrows():
            product_name = row[t('product')]
            p = row[t('conversion')]
            
            for mde in MDE_LIST:
                n_required = required_sample(p, mde)
                days_needed = required_days(n_required, DAILY_LEADS_PER_GROUP)
                
                for hyp_name, _ in hypotheses:
                    results.append({
                        t('product'): product_name,
                        t('hypothesis'): hyp_name,
                        t('conversion'): f"{p:.2%}",
                        t('growth_pct'): f"{mde*100:.0f}%",
                        t('leads_per_group'): int(np.ceil(n_required)),
                        t('leads_per_day'): f"{DAILY_LEADS_PER_GROUP:.1f}",
                        t('days_for_test'): days_needed
                    })
        
        results_df = pd.DataFrame(results)
        
        # Цветовое кодирование для столбца "Дней для теста"
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
        
        # Отображение таблицы
        st.markdown(f"**{t('avg_daily_leads')}** {DAILY_LEADS_PER_GROUP:.1f}")
        
        styled_df = results_df.style.applymap(highlight_days, subset=[t('days_for_test')])
        
        st.dataframe(
            styled_df.format({
                t('leads_per_group'): "{:,.0f}",
                t('days_for_test'): "{:,.0f}"
            }),
            use_container_width=True,
            height=400
        )
        
        # Легенда цветов
        st.markdown(f"**{t('color_legend')}**")
        st.markdown(f"🟩 **{t('green_test')}**")
        st.markdown(f"🟧 **{t('orange_test')}**")
        st.markdown(f"🟥 **{t('red_test')}**")
    else:
        st.info(t('no_data_for_display'))

# ---------- ФУТЕР ----------
st.markdown(
    f"""
    <div style='text-align: center; color: #ffffff; font-size: 0.9rem; padding: 2rem 0;'>
        {t('footer')}
    </div>
    """, 
    unsafe_allow_html=True
)