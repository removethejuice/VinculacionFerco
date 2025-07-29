import pandas as pd

def generar_archivo_con_demanda_y_pedido(dataset_original_path, predicciones_path, salida_path):
    # Leer datasets
    df_original = pd.read_csv(dataset_original_path)
    df_predicciones = pd.read_csv(predicciones_path)

    # Limpiar columnas clave
    df_original['ItemCode'] = df_original['ItemCode'].astype(str).str.strip()
    df_predicciones['nombrellanta'] = df_predicciones['nombrellanta'].astype(str).str.strip()

    # Renombrar para hacer merge
    df_original = df_original.rename(columns={
        'ItemCode': 'Codigo',
        'ItemName': 'Descripcion'
    })

    # Hacer inner join (solo incluir las que están en predicciones)
    df_merged = pd.merge(
        df_original,
        df_predicciones,
        left_on='Codigo',
        right_on='nombrellanta',
        how='inner'
    )

    # Calcular demanda por fila
    df_merged['Demanda 4 meses'] = df_merged['prediccion_4_meses']
    df_merged['Demanda 5 meses'] = df_merged['prediccion_5_meses']
    df_merged['Demanda 6 meses'] = df_merged['prediccion_6_meses']

    # Calcular Pedido Sugerido como Demanda - Total DE ESA FILA
    df_merged[f'Pedido Sugerido 4 meses'] = (df_merged[f'Demanda 4 meses'] - df_merged['Total']).clip(lower=0)
    df_merged[f'Pedido Sugerido 5 meses'] = ((df_merged[f'Demanda 5 meses'] + df_merged[f'Demanda 4 meses']) - df_merged['Total']).clip(lower=0)
    df_merged[f'Pedido Sugerido 6 meses'] = ((df_merged[f'Demanda 6 meses'] + df_merged[f'Demanda 5 meses']) - df_merged['Total']).clip(lower=0)


    # Columnas a dejar
    columnas_finales = [
        'Codigo', 'Descripcion', 'No. Fabricante', 'In Stock', 'Pedido', 'Total', 'Tipo'
    ] + [f'Mes_{i}' for i in range(1, 13)] + \
        ['Demanda 4 meses', 'Demanda 5 meses', 'Demanda 6 meses',
         'Pedido Sugerido 4 meses', 'Pedido Sugerido 5 meses', 'Pedido Sugerido 6 meses']

    # Validar columnas existentes
    columnas_validas = [col for col in columnas_finales if col in df_merged.columns]

    # Exportar a CSV
    df_merged[columnas_validas].to_csv(salida_path, index=False, encoding='utf-8-sig')
    print(f"✅ Archivo generado: {salida_path}")

# Llantas
generar_archivo_con_demanda_y_pedido(
    "ventas_12_meses.csv",
    "predicciones_llantas_final.csv",
    "llantas_con_demanda_y_pedido.csv"
)

# Aceites
generar_archivo_con_demanda_y_pedido(
    "ventas_12_meses_aceites.csv",
    "predicciones_aceites_final.csv",
    "aceites_con_demanda_y_pedido.csv"
)

print("🎯 Archivos creados correctamente con Pedido Sugerido basado en el Total de cada fila.")