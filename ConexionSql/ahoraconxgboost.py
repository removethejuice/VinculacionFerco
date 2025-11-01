import pandas as pd
import os
from joblib import dump
import xgboost as xgb
from datetime import datetime
from dateutil.relativedelta import relativedelta

def entrenar_y_predecir_xgb(dataset_path, carpeta_salida):
    if not os.path.exists(dataset_path):
        print(f"❌ Archivo no encontrado: {dataset_path}")
        return

    try:
        df = pd.read_csv(dataset_path)
    except Exception as e:
        print(f"❌ Error al leer {dataset_path}: {e}")
        return

    if df.empty:
        print(f"⚠️ El archivo {dataset_path} está vacío.")
        return

    # Asegurar que la columna ds es datetime
    df['ds'] = pd.to_datetime(df['ds'])

    # Crear carpeta de salida
    os.makedirs(carpeta_salida, exist_ok=True)

    productos = df['ItemCode'].unique()

    for codigo in productos:
        df_producto = df[df['ItemCode'] == codigo].copy()

        if df_producto.shape[0] < 3:
            print(f"⛔ Saltando {codigo} por datos insuficientes")
            continue

        df_producto = df_producto.sort_values('ds')
        df_producto['mes'] = df_producto['ds'].dt.month
        df_producto['año'] = df_producto['ds'].dt.year

        features = ['mes', 'año']
        if 'inventario' in df_producto.columns:
            features.append('inventario')
            df_producto['inventario'] = df_producto['inventario'].fillna(0)

        X = df_producto[features]
        y = df_producto['y']

        modelo = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100)
        modelo.fit(X, y)

        # Guardar modelo
        modelo_path = os.path.join(carpeta_salida, f"modelo_{codigo}.joblib")
        dump(modelo, modelo_path)

        # Predecir siguientes 6 meses
        fechas_futuras = [df_producto['ds'].max() + relativedelta(months=i) for i in range(1, 7)]
        df_futuro = pd.DataFrame({
            'ds': fechas_futuras,
            'mes': [d.month for d in fechas_futuras],
            'año': [d.year for d in fechas_futuras],
        })

        if 'inventario' in features:
            df_futuro['inventario'] = 0

        X_futuro = df_futuro[features]
        df_futuro['yhat'] = modelo.predict(X_futuro)

        # Guardar predicción
        forecast_path = os.path.join(carpeta_salida, f"forecast_{codigo}.csv")
        df_futuro[['ds', 'yhat']].to_csv(forecast_path, index=False)

        print(f"✅ Forecast XGB guardado para {codigo} en {carpeta_salida}/")

# Procesar ambos datasets
entrenar_y_predecir_xgb("ventas_formato_prophet.csv", "modelos_y_predicciones_xgb_llantas")
entrenar_y_predecir_xgb("ventas_formato_prophet_aceites.csv", "modelos_y_predicciones_xgb_aceites")

print("🎯 Modelos XGBoost y predicciones generadas exitosamente.")
