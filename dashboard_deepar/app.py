import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import io

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Predicciones DeepAR",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("Dashboard de Predicciones DeepAR - Formato Aceites con Demanda y Pedido")
st.markdown("---")

@st.cache_data
def load_data():
    """Cargar los datos de predicciones"""
    try:
        df = pd.read_csv("../ConexionSql/predicciones_deepAR.csv")
        # Convertir la columna ds a datetime
        df['ds'] = pd.to_datetime(df['ds'])
        return df
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        return None

@st.cache_data
def load_reference_data():
    """Cargar los datos de referencia del archivo aceites_con_demanda_y_pedido.csv"""
    try:
        df_ref = pd.read_csv("../ConexionSql/aceites_con_demanda_y_pedido.csv")
        return df_ref
    except Exception as e:
        st.warning(f"No se pudo cargar el archivo de referencia: {e}")
        return None

def transform_deepar_to_aceites_format(deepar_df, reference_df=None):
    """Transformar las predicciones de DeepAR al formato de aceites_con_demanda_y_pedido.csv"""
    
    # Crear un DataFrame base con la estructura requerida
    result_data = []
    
    # Obtener todos los ItemCodes únicos
    item_codes = deepar_df['ItemCode'].unique()
    
    for item_code in item_codes:
        item_data = deepar_df[deepar_df['ItemCode'] == item_code].sort_values('ds')
        
        # Buscar información de referencia si está disponible
        ref_info = None
        if reference_df is not None:
            ref_matches = reference_df[reference_df['Codigo'] == item_code]
            if not ref_matches.empty:
                ref_info = ref_matches.iloc[0]
        
        # Crear filas para VENTA e INVENTARIO
        for tipo in ['VENTA', 'INVENTARIO']:
            row = {
                'Codigo': item_code,
                'Descripcion': ref_info['Descripcion'] if ref_info is not None else f"Producto {item_code}",
                'No. Fabricante': ref_info['No. Fabricante'] if ref_info is not None else "",
                'In Stock': ref_info['In Stock'] if ref_info is not None and tipo == 'INVENTARIO' else 0.0,
                'Pedido': ref_info['Pedido'] if ref_info is not None and tipo == 'VENTA' else 0.0,
                'Total': ref_info['Total'] if ref_info is not None and tipo == 'VENTA' else 0.0,
                'Tipo': tipo
            }
            
            # Agregar datos mensuales (Mes_1 a Mes_12)
            # Para simplificar, usaremos las predicciones de DeepAR para los próximos 3 meses
            # y rellenaremos con 0.0 para los meses restantes
            for i in range(1, 13):
                if i <= len(item_data):
                    if tipo == 'VENTA':
                        row[f'Mes_{i}'] = round(item_data.iloc[i-1]['yhat'], 2) if i <= len(item_data) else 0.0
                    else:  # INVENTARIO
                        # Para inventario, simular valores basados en stock actual
                        current_stock = ref_info['In Stock'] if ref_info is not None else 0.0
                        row[f'Mes_{i}'] = max(0, current_stock - sum([round(item_data.iloc[j]['yhat'], 2) for j in range(min(i, len(item_data)))]))
                else:
                    row[f'Mes_{i}'] = 0.0
            
            # Calcular demandas para 4, 5 y 6 meses
            if len(item_data) >= 4:
                row['Demanda 4 meses'] = round(sum([item_data.iloc[i]['yhat'] for i in range(4)]), 8)
            else:
                row['Demanda 4 meses'] = 0.0
                
            if len(item_data) >= 5:
                row['Demanda 5 meses'] = round(sum([item_data.iloc[i]['yhat'] for i in range(5)]), 8)
            else:
                row['Demanda 5 meses'] = 0.0
                
            if len(item_data) >= 6:
                row['Demanda 6 meses'] = round(sum([item_data.iloc[i]['yhat'] for i in range(6)]), 8)
            else:
                row['Demanda 6 meses'] = 0.0
            
            # Calcular pedidos sugeridos (solo para VENTA)
            if tipo == 'VENTA':
                current_stock = ref_info['In Stock'] if ref_info is not None else 0.0
                current_order = ref_info['Pedido'] if ref_info is not None else 0.0
                
                # Pedido sugerido = demanda - (stock actual + pedido actual)
                available = current_stock + current_order
                
                row['Pedido Sugerido 4 meses'] = max(0, row['Demanda 4 meses'] - available)
                row['Pedido Sugerido 5 meses'] = max(0, row['Demanda 5 meses'] - available)
                row['Pedido Sugerido 6 meses'] = max(0, row['Demanda 6 meses'] - available)
            else:
                row['Pedido Sugerido 4 meses'] = ""
                row['Pedido Sugerido 5 meses'] = ""
                row['Pedido Sugerido 6 meses'] = ""
            
            result_data.append(row)
    
    return pd.DataFrame(result_data)

def main():
    # Cargar datos
    df = load_data()
    df_ref = load_reference_data()
    
    if df is None:
        st.error("No se pudieron cargar los datos. Verifique que el archivo existe.")
        return
    
    # Transformar datos al formato requerido
    st.subheader("Transformando datos al formato de Aceites con Demanda y Pedido...")
    transformed_df = transform_deepar_to_aceites_format(df, df_ref)
    
    # Sidebar para filtros
    st.sidebar.header("Filtros")
    
    # Filtro por Código
    codigos = sorted(transformed_df['Codigo'].unique())
    selected_codigos = st.sidebar.multiselect(
        "Seleccionar Código:",
        options=codigos,
        default=codigos[:5] if len(codigos) > 5 else codigos
    )
    
    # Filtro por Tipo
    tipos = ['VENTA', 'INVENTARIO']
    selected_tipos = st.sidebar.multiselect(
        "Seleccionar Tipo:",
        options=tipos,
        default=tipos
    )
    
    # Aplicar filtros
    filtered_df = transformed_df.copy()
    
    if selected_codigos:
        filtered_df = filtered_df[filtered_df['Codigo'].isin(selected_codigos)]
    
    if selected_tipos:
        filtered_df = filtered_df[filtered_df['Tipo'].isin(selected_tipos)]
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total de Productos",
            len(selected_codigos) if selected_codigos else len(codigos)
        )
    
    with col2:
        total_ventas = filtered_df[filtered_df['Tipo'] == 'VENTA']['Demanda 6 meses'].sum()
        st.metric(
            "Demanda Total 6 meses",
            f"{total_ventas:.2f}"
        )
    
    with col3:
        total_pedidos = filtered_df[filtered_df['Tipo'] == 'VENTA']['Pedido Sugerido 6 meses'].sum()
        st.metric(
            "Pedidos Sugeridos 6 meses",
            f"{total_pedidos:.2f}"
        )
    
    with col4:
        total_stock = filtered_df[filtered_df['Tipo'] == 'INVENTARIO']['In Stock'].sum()
        st.metric(
            "Stock Total",
            f"{total_stock:.2f}"
        )
    
    # Mostrar tabla principal en formato de aceites con demanda y pedido
    st.subheader("Datos en Formato de Aceites con Demanda y Pedido")
    
    if not filtered_df.empty:
        # Agregar botón para descargar datos filtrados
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Descargar datos filtrados (CSV)",
            data=csv,
            file_name=f"predicciones_deepar_formato_aceites_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        
        # Mostrar tabla con paginación
        st.dataframe(
            filtered_df,
            use_container_width=True,
            height=600
        )
        
        # Gráfico de barras para comparar demandas
        st.subheader("Comparación de Demandas por Producto")
        
        # Filtrar solo datos de VENTA para el gráfico
        venta_data = filtered_df[filtered_df['Tipo'] == 'VENTA'].copy()
        
        if not venta_data.empty:
            fig_bar = px.bar(
                venta_data,
                x='Codigo',
                y='Demanda 6 meses',
                title='Demanda 6 meses por Producto',
                labels={'Demanda 6 meses': 'Demanda 6 meses', 'Codigo': 'Código de Producto'}
            )
            fig_bar.update_layout(height=500)
            fig_bar.update_xaxes(tickangle=45)
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Gráfico de pedidos sugeridos
        st.subheader("Pedidos Sugeridos por Producto")
        
        if not venta_data.empty:
            fig_pedidos = px.bar(
                venta_data,
                x='Codigo',
                y='Pedido Sugerido 6 meses',
                title='Pedidos Sugeridos 6 meses por Producto',
                labels={'Pedido Sugerido 6 meses': 'Pedido Sugerido 6 meses', 'Codigo': 'Código de Producto'}
            )
            fig_pedidos.update_layout(height=500)
            fig_pedidos.update_xaxes(tickangle=45)
            st.plotly_chart(fig_pedidos, use_container_width=True)
        
        # Resumen por tipo
        st.subheader("Resumen por Tipo")
        
        resumen_tipo = filtered_df.groupby('Tipo').agg({
            'In Stock': 'sum',
            'Pedido': 'sum',
            'Total': 'sum',
            'Demanda 4 meses': 'sum',
            'Demanda 5 meses': 'sum',
            'Demanda 6 meses': 'sum',
            'Pedido Sugerido 4 meses': 'sum',
            'Pedido Sugerido 5 meses': 'sum',
            'Pedido Sugerido 6 meses': 'sum'
        }).round(2)
        
        st.dataframe(resumen_tipo, use_container_width=True)
        
    else:
        st.warning("No hay datos que coincidan con los filtros seleccionados.")

if __name__ == "__main__":
    main() 