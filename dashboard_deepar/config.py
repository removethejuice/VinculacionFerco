"""
Configuración del Dashboard de Predicciones DeepAR
"""

# Configuración de la aplicación
APP_CONFIG = {
    'page_title': 'Dashboard Predicciones DeepAR',
    'page_icon': '📊',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

# Configuración de colores para los gráficos
COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'success': '#2ca02c',
    'warning': '#d62728',
    'info': '#9467bd',
    'light': '#8c564b',
    'dark': '#e377c2'
}

# Configuración de gráficos
CHART_CONFIG = {
    'height': 500,
    'template': 'plotly_white',
    'font_family': 'Arial, sans-serif',
    'font_size': 12
}

# Configuración de filtros
FILTER_CONFIG = {
    'max_items_display': 10,
    'default_items_count': 5
}

# Configuración de exportación
EXPORT_CONFIG = {
    'csv_encoding': 'utf-8',
    'excel_engine': 'openpyxl',
    'date_format': '%Y%m%d_%H%M%S'
}

# Configuración de métricas
METRICS_CONFIG = {
    'decimal_places': 2,
    'thousands_separator': ','
}

# Configuración de intervalos de confianza
CONFIDENCE_INTERVALS = {
    'q10': 'Percentil 10 (Límite Inferior)',
    'q50': 'Percentil 50 (Mediana)',
    'q90': 'Percentil 90 (Límite Superior)'
}

# Configuración de columnas del dataset
COLUMN_MAPPING = {
    'ItemCode': 'Código del Item',
    'ds': 'Fecha',
    'yhat': 'Predicción',
    'q10': 'Límite Inferior (10%)',
    'q50': 'Mediana (50%)',
    'q90': 'Límite Superior (90%)'
} 