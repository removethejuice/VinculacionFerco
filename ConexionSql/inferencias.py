import pandas as pd
from prophet import Prophet
from joblib import load
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Cargar modelo específico
codigo_producto = "LLA-TOYO-TBRHR-0034"  # ← cambia esto según el producto
modelo = load(f"modelos_y_predicciones/modelo_{codigo_producto}.joblib")

# Crear nuevo dataframe con fechas futuras
ultimo_mes = datetime.today().replace(day=1)
futuro = pd.date_range(start=ultimo_mes, periods=6, freq='MS')
df_futuro = pd.DataFrame({'ds': futuro})

# Generar predicción
forecast = modelo.predict(df_futuro)

# Mostrar resultados
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])
