import pandas as pd
import os

def procesar_dataset(archivo_entrada, archivo_salida):
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

    # Asegurar que las columnas de meses están ordenadas
    meses = [f"Mes_{i}" for i in range(1, 13)]

    # Lista para almacenar las filas combinadas
    filas_combinadas = []

    # Iterar por índice
    i = 0
    while i < len(df) - 1:
        fila_actual = df.iloc[i]
        fila_siguiente = df.iloc[i + 1]

        # Comprobar si las filas son del mismo ItemCode y tienen tipos alternados VENTA/INVENTARIO
        if (fila_actual["ItemCode"] == fila_siguiente["ItemCode"] and
            fila_actual["Tipo"] == "VENTA" and fila_siguiente["Tipo"] == "INVENTARIO"):

            nueva_fila = {}

            # Copiar campos generales de la fila de VENTA
            for col in ["ItemCode", "ItemName", "No. Fabricante", "In Stock", "Qty Ordered by", "Qty Ordered from", "Pedido", "Total"]:
                nueva_fila[col] = fila_actual.get(col, None)

            # Agregar columnas de venta e inventario con sufijos
            for mes in meses:
                nueva_fila[f"{mes}_venta"] = fila_actual.get(mes, None)
                nueva_fila[f"{mes}_inventario"] = fila_siguiente.get(mes, None)

            filas_combinadas.append(nueva_fila)
            i += 2  # Saltarse la siguiente fila porque ya fue emparejada
        else:
            i += 1

    # Crear DataFrame final
    df_final = pd.DataFrame(filas_combinadas)

    if df_final.empty:
        print(f"⚠️ No se encontraron pares VENTA/INVENTARIO en {archivo_entrada}.")
    else:
        df_final.to_csv(archivo_salida, index=False, encoding="utf-8-sig")
        print(f"✅ CSV combinado generado: {archivo_salida}")

# Procesar los dos datasets
procesar_dataset("ventas_12_meses.csv", "dataset_combinado.csv")
procesar_dataset("ventas_12_meses_aceites.csv", "dataset_combinado_aceites.csv")

print("🎉 ¡Proceso finalizado!")
