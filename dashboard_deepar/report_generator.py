import pandas as pd
import numpy as np
from datetime import datetime
import os

def generate_excel_report(csv_path, output_path=None):
    """
    Genera un reporte en Excel con las predicciones de DeepAR
    
    Args:
        csv_path (str): Ruta al archivo CSV de predicciones
        output_path (str): Ruta de salida para el archivo Excel
    """
    
    # Cargar datos
    df = pd.read_csv(csv_path)
    df['ds'] = pd.to_datetime(df['ds'])
    
    # Crear nombre de archivo por defecto
    if output_path is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = f"reporte_predicciones_deepar_{timestamp}.xlsx"
    
    # Crear writer de Excel
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        
        # Hoja 1: Datos completos
        df.to_excel(writer, sheet_name='Datos_Completos', index=False)
        
        # Hoja 2: Resumen por ItemCode
        summary = df.groupby('ItemCode').agg({
            'yhat': ['count', 'mean', 'std', 'min', 'max'],
            'q10': 'mean',
            'q50': 'mean',
            'q90': 'mean'
        }).round(3)
        
        summary.columns = ['Cantidad_Predicciones', 'Predicción_Media', 'Desv_Est', 'Min', 'Max', 'Q10_Media', 'Q50_Media', 'Q90_Media']
        summary = summary.reset_index()
        summary.to_excel(writer, sheet_name='Resumen_ItemCode', index=False)
        
        # Hoja 3: Predicciones por mes
        monthly_summary = df.groupby(['ItemCode', df['ds'].dt.to_period('M')]).agg({
            'yhat': 'mean',
            'q10': 'mean',
            'q50': 'mean',
            'q90': 'mean'
        }).round(3)
        
        monthly_summary = monthly_summary.reset_index()
        monthly_summary['ds'] = monthly_summary['ds'].astype(str)
        monthly_summary.to_excel(writer, sheet_name='Predicciones_Mensuales', index=False)
        
        # Hoja 4: Análisis de tendencias
        trend_analysis = df.groupby('ItemCode').apply(lambda x: {
            'Tendencia': 'Creciente' if x['yhat'].iloc[-1] > x['yhat'].iloc[0] else 'Decreciente',
            'Variabilidad': x['yhat'].std(),
            'Rango_Predicciones': x['yhat'].max() - x['yhat'].min(),
            'Promedio_Intervalo_Confianza': (x['q90'] - x['q10']).mean()
        }).reset_index()
        
        trend_analysis.to_excel(writer, sheet_name='Análisis_Tendencias', index=False)
        
        # Hoja 5: Top Items por predicción
        top_items = df.groupby('ItemCode')['yhat'].mean().sort_values(ascending=False).head(10)
        top_items_df = pd.DataFrame({
            'ItemCode': top_items.index,
            'Predicción_Media': top_items.values
        })
        top_items_df.to_excel(writer, sheet_name='Top_10_Items', index=False)
    
    print(f"Reporte generado exitosamente: {output_path}")
    return output_path

def generate_filtered_report(csv_path, item_codes=None, start_date=None, end_date=None, output_path=None):
    """
    Genera un reporte filtrado en Excel
    
    Args:
        csv_path (str): Ruta al archivo CSV de predicciones
        item_codes (list): Lista de ItemCodes a incluir
        start_date (str): Fecha de inicio (YYYY-MM-DD)
        end_date (str): Fecha de fin (YYYY-MM-DD)
        output_path (str): Ruta de salida para el archivo Excel
    """
    
    # Cargar datos
    df = pd.read_csv(csv_path)
    df['ds'] = pd.to_datetime(df['ds'])
    
    # Aplicar filtros
    if item_codes:
        df = df[df['ItemCode'].isin(item_codes)]
    
    if start_date:
        df = df[df['ds'] >= pd.Timestamp(start_date)]
    
    if end_date:
        df = df[df['ds'] <= pd.Timestamp(end_date)]
    
    # Crear nombre de archivo por defecto
    if output_path is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filter_info = f"filtrado_{timestamp}"
        output_path = f"reporte_predicciones_deepar_{filter_info}.xlsx"
    
    # Generar reporte con datos filtrados
    return generate_excel_report(df, output_path)

if __name__ == "__main__":
    # Ejemplo de uso
    csv_file = "../ConexionSql\predicciones_deepAR.csv"
    
    if os.path.exists(csv_file):
        # Generar reporte completo
        generate_excel_report(csv_file)
        
        # Generar reporte filtrado (ejemplo)
        # generate_filtered_report(
        #     csv_file,
        #     item_codes=['ACEI-EIFFEL-NORM-0001', 'ACEI-EIFFEL-NORM-0002'],
        #     start_date='2025-04-01',
        #     end_date='2025-06-30'
        # )
    else:
        print(f"Archivo no encontrado: {csv_file}") 