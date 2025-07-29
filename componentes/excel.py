import pandas as pd
import numpy as np

def exportar_excel_bonito(df, nombre_archivo="tabla_bonita_datos.xlsx"):
    # Reemplazar NaN e infinitos por string vacío o lo que quieras mostrar
    df = df.replace([np.nan, np.inf, -np.inf], "")

    writer = pd.ExcelWriter(nombre_archivo, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Datos')

    workbook = writer.book
    worksheet = writer.sheets['Datos']

    # Formato de encabezado
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#D7E4BC',
        'border': 1})

    # Formato de celdas
    cell_format = workbook.add_format({
        'text_wrap': True,
        'valign': 'top',
        'border': 1})

    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)

    for row in range(1, len(df) + 1):
        for col in range(len(df.columns)):
            worksheet.write(row, col, df.iloc[row - 1, col], cell_format)

    for i, column in enumerate(df.columns):
        max_len = max(df[column].astype(str).map(len).max(), len(str(column))) + 2
        worksheet.set_column(i, i, max_len)

    writer.close()

