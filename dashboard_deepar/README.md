# Dashboard de Predicciones DeepAR

Este dashboard permite visualizar y analizar las predicciones generadas por el modelo DeepAR de manera interactiva.

## Características

- Visualización de predicciones por ItemCode con valores redondeados
- Intervalos de confianza (q10, q50, q90) integrados en el mismo gráfico
- Filtros por ItemCode y rango de fechas
- Gráficos interactivos con Plotly
- Exportación de datos filtrados
- Estadísticas detalladas por ItemCode con nombres de columnas significativos
- Interfaz limpia sin emojis para uso profesional

## Instalación

### Opción 1: Ejecución automática (Recomendada)
```bash
python run_dashboard.py
```

### Opción 2: Instalación manual
1. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar el dashboard:
```bash
streamlit run app.py
```

## Uso

1. **Filtros**: Utiliza la barra lateral para filtrar por:
   - ItemCode específicos
   - Rango de fechas

2. **Visualizaciones**:
   - Gráfico integrado con predicciones e intervalos de confianza
   - Valores redondeados para mejor legibilidad
   - Gráfico de barras comparativo

3. **Exportación**: Descarga los datos filtrados en formato CSV con valores redondeados

4. **Tablas**: Nombres de columnas significativos y valores enteros

## Estructura de Datos

El dashboard espera un archivo CSV con las siguientes columnas:
- `ItemCode`: Código del item
- `ds`: Fecha de predicción
- `yhat`: Valor de predicción
- `q10`: Percentil 10 (límite inferior del intervalo)
- `q50`: Percentil 50 (mediana)
- `q90`: Percentil 90 (límite superior del intervalo)

## Generación de Reportes

El dashboard incluye un generador de reportes en Excel que puede ejecutarse independientemente:

```bash
python report_generator.py
```

Este script genera un archivo Excel con múltiples hojas:
- **Datos_Completos**: Todas las predicciones
- **Resumen_ItemCode**: Estadísticas por ItemCode
- **Predicciones_Mensuales**: Resumen mensual
- **Análisis_Tendencias**: Análisis de tendencias y variabilidad
- **Top_10_Items**: Los 10 items con mayores predicciones

## Notas

- El archivo de datos debe estar ubicado en `../ConexionSql/predicciones_deepAR.csv`
- El dashboard se actualiza automáticamente al cambiar los filtros
- Los gráficos son interactivos y permiten zoom, pan y hover
- Los reportes se guardan con timestamp automático
- Todos los valores se muestran redondeados a enteros para mejor legibilidad
- Los intervalos de confianza están integrados en el gráfico principal 