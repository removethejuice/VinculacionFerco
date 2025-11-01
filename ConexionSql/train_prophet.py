import pandas as pd
from prophet import Prophet
import os
from joblib import dump

def entrenar_y_predecir(dataset_path, carpeta_salida):
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

    # Asegurarse de que no hay valores NaN en el regresor
    df["inventario"] = df["inventario"].fillna(0)

    # Crear carpeta de salida
    os.makedirs(carpeta_salida, exist_ok=True)

    # Obtener todos los productos únicos
    productos = df["ItemCode"].unique()

    for codigo in productos:
        df_producto = df[df["ItemCode"] == codigo][["ds", "y", "inventario"]].copy()
        df_producto = df_producto.dropna(subset=["ds", "y", "inventario"])

        if df_producto.shape[0] < 2:
            print(f"⛔ Saltando {codigo} por datos insuficientes")
            continue

        # Inicializar y entrenar modelo Prophet
        modelo = Prophet()
        modelo.add_regressor("inventario")
        modelo.fit(df_producto)

        # Crear fechas futuras (6 meses)
        futuro = modelo.make_future_dataframe(periods=6, freq='MS')
        futuro["inventario"] = 0  # se puede ajustar si tienes proyecciones de inventario

        forecast = modelo.predict(futuro)

        # Guardar predicciones
        forecast_path = os.path.join(carpeta_salida, f"forecast_{codigo}.csv")
        forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].to_csv(forecast_path, index=False)

        # Guardar modelo
        modelo_path = os.path.join(carpeta_salida, f"modelo_{codigo}.joblib")
        dump(modelo, modelo_path)

        print(f"✅ Forecast y modelo guardados para {codigo} en {carpeta_salida}/")

# Ejecutar para ambos datasets
entrenar_y_predecir("ventas_formato_prophet.csv", "modelos_y_predicciones_llantas")
entrenar_y_predecir("ventas_formato_prophet_aceites.csv", "modelos_y_predicciones_aceites")

print("🎯 Todo el proceso de entrenamiento y predicción ha finalizado.")
