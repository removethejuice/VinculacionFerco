import os
import pandas as pd

def procesar_forecasts(carpeta, archivo_salida):
    resultados = []

    for archivo in os.listdir(carpeta):
        if archivo.startswith("forecast_") and archivo.endswith(".csv"):
            ruta = os.path.join(carpeta, archivo)
            try:
                df = pd.read_csv(ruta)
                df = df.sort_values(by='ds')

                # Asegurarse que hay al menos 6 filas
                if df.shape[0] >= 6:
                    pred_6 = df['yhat'].tail(6).sum()
                    pred_5 = df['yhat'].tail(5).sum()
                    pred_4 = df['yhat'].tail(4).sum()
                else:
                    pred_6 = pred_5 = pred_4 = None

                nombre_producto = archivo.replace("forecast_", "").replace(".csv", "")
                fecha_final = df['ds'].iloc[-1]

                resultados.append({
                    'nombrellanta': nombre_producto,
                    'fecha': fecha_final,
                    'prediccion_6_meses': pred_6,
                    'prediccion_5_meses': pred_5,
                    'prediccion_4_meses': pred_4
                })

            except Exception as e:
                print(f"❌ Error procesando {archivo}: {e}")

    # Guardar CSV final
    df_resultado = pd.DataFrame(resultados)
    df_resultado.to_csv(archivo_salida, index=False, encoding='utf-8-sig')
    print(f"✅ Archivo generado: {archivo_salida}")

# Ejecutar para llantas y aceites
procesar_forecasts("modelos_y_predicciones_xgb_llantas", "predicciones_llantas_final.csv")
procesar_forecasts("modelos_y_predicciones_xgb_aceites", "predicciones_aceites_final.csv")

print("🎉 Consolidación de predicciones XGBoost finalizada.")
