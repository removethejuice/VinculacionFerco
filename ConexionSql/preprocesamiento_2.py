import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os

def preparar_dataset_para_prophet(archivo_entrada, archivo_salida):
    if not os.path.exists(archivo_entrada):
        print(f"❌ Archivo no encontrado: {archivo_entrada}")
        return

    try:
        df = pd.read_csv(archivo_entrada)
    except Exception as e:
        print(f"❌ Error al leer {archivo_entrada}: {e}")
        return

    if df.empty:
        print(f"⚠️ El archivo {archivo_entrada} está vacío. No se procesará.")
        return

    # Crear listas de columnas
    columnas_venta = [f"Mes_{i}_venta" for i in range(1, 13)]
    columnas_inventario = [f"Mes_{i}_inventario" for i in range(1, 13)]

    # Formato largo para ventas
    ventas_largo = df.melt(
        id_vars=['ItemCode', 'ItemName'],
        value_vars=columnas_venta,
        var_name='mes',
        value_name='y'
    )

    # Formato largo para inventario
    inventario_largo = df.melt(
        id_vars=['ItemCode', 'ItemName'],
        value_vars=columnas_inventario,
        var_name='mes_inv',
        value_name='inventario'
    )

    # Asegurarse que ambas listas tengan el mismo orden
    ventas_largo = ventas_largo.sort_values(by=['ItemCode', 'mes']).reset_index(drop=True)
    inventario_largo = inventario_largo.sort_values(by=['ItemCode', 'mes_inv']).reset_index(drop=True)

    # Extraer número de mes
    ventas_largo['mes_num'] = ventas_largo['mes'].str.extract(r'Mes_(\d+)_venta').astype(int)

    # Generar fechas ficticias en base al mes actual
    hoy = datetime.today()
    ventas_largo['ds'] = ventas_largo['mes_num'].apply(lambda m: hoy - relativedelta(months=(12 - m)))
    ventas_largo['ds'] = ventas_largo['ds'].dt.to_period('M').dt.to_timestamp()

    # Añadir la columna de inventario desde el otro DataFrame
    ventas_largo['inventario'] = inventario_largo['inventario']

    # Rellenar valores faltantes
    ventas_largo['y'] = ventas_largo['y'].fillna(0)
    ventas_largo['inventario'] = ventas_largo['inventario'].fillna(0)

    # Guardar dataset final
    ventas_largo = ventas_largo[['ItemCode', 'ItemName', 'ds', 'y', 'inventario']]
    ventas_largo.to_csv(archivo_salida, index=False, encoding='utf-8-sig')
    print(f"✅ CSV generado: {archivo_salida}")

# Procesar ambos datasets
preparar_dataset_para_prophet("dataset_combinado.csv", "ventas_formato_prophet.csv")
preparar_dataset_para_prophet("dataset_combinado_aceites.csv", "ventas_formato_prophet_aceites.csv")

print("🎉 ¡Ambos archivos Prophet fueron generados!")
