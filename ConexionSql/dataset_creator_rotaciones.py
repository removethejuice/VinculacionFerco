import pandas as pd
from conexion_2 import conectorcito

# Conexión
conn = conectorcito()
if conn is None:
    exit("❌ No se pudo conectar a la base de datos.")

# Reemplaza esto con tu query completa (sin omitir nada)
query = """
SELECT 
    T1.ItemCode AS 'Código del Artículo',
    T1.ItemName AS 'Nombre del Artículo',
    SUM(T0.InQty) AS 'Total Comprado',
    SUM(T0.OutQty) AS 'Total Vendido',
    CASE 
        WHEN SUM(T0.InQty) = 0 THEN 0
        ELSE SUM(T0.OutQty) / SUM(T0.InQty) 
    END AS 'Rotación',
    SUM(T2.LineTotal) AS 'Ingresos',
    SUM(T2.Quantity * T2.Price) AS 'Costo Total',
    SUM(T2.LineTotal) - SUM(T2.Quantity * T2.Price) AS 'Ganancia Bruta',
    CASE 
        WHEN SUM(T2.LineTotal) = 0 THEN 0
        ELSE (SUM(T2.LineTotal) - SUM(T2.Quantity * T2.Price)) / SUM(T2.LineTotal) 
    END AS 'Margen de Ganancia'
FROM 
    OINM T0
INNER JOIN 
    OITM T1 ON T0.ItemCode = T1.ItemCode
INNER JOIN 
    INV1 T2 ON T1.ItemCode = T2.ItemCode
WHERE 
    T0.DocDate BETWEEN '2025-01-01' AND '2025-04-01'
    AND T2.DocDate BETWEEN '2025-01-01' AND '2025-04-01'
    AND T1.ItemCode like 'LLA%'
GROUP BY 
    T1.ItemCode, T1.ItemName
HAVING 
    (SUM(T0.OutQty) / NULLIF(SUM(T0.InQty), 0) < 8)
    AND ((SUM(T2.LineTotal) - SUM(T2.Quantity * T2.Price)) / NULLIF(SUM(T2.LineTotal), 0) < 10.00)
ORDER BY 
    'Rotación' ASC, 'Margen de Ganancia' ASC
"""

try:
    cursor = conn.cursor()
    cursor.execute(query)

    # Avanzar hasta encontrar el primer conjunto de resultados válido
    while cursor.description is None and cursor.nextset():
        pass

    if cursor.description is None:
        print("⚠️ La consulta no retornó ningún resultado (SELECT).")
    else:
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        df = pd.DataFrame.from_records(rows, columns=columns)
        df.to_csv("rotaciones_12_meses.csv", index=False, encoding="utf-8-sig")
        print("✅ Archivo CSV generado exitosamente: rotaciones_12_meses.csv")

except Exception as e:
    print(f"❌ Error ejecutando la consulta: {e}")

finally:
    conn.close()
