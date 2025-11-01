import pandas as pd
from conexion import conectorcito

# Conexión a la base de datos
conn = conectorcito()
if conn is None:
    exit("❌ No se pudo establecer conexión con la base de datos.")

# Consulta SQL que genera columnas mes 1 al 12 por artículo
query = """
DECLARE @FechaFinal date = DATEFROMPARTS(YEAR(GETDATE()), MONTH(GETDATE()), 1);

WITH MesesCalendario AS (
    SELECT 
        DATEFROMPARTS(YEAR(DATEADD(MONTH, n.number - 12, @FechaFinal)), MONTH(DATEADD(MONTH, n.number - 12, @FechaFinal)), 1) AS Mes,
        n.number AS MesNum  
    FROM master..spt_values n
    WHERE n.type = 'P' AND n.number BETWEEN 0 AND 12
),

Movimientos AS (
    SELECT 
        T0.ItemCode,
        T1.ItemName,
        DATEFROMPARTS(YEAR(T0.DocDate), MONTH(T0.DocDate), 1) AS Mes,
        ISNULL(T0.InQty, 0) AS Entrada,
        ISNULL(T0.OutQty, 0) AS Salida
    FROM dbo.OINM T0
    INNER JOIN dbo.OITM T1 ON T0.ItemCode = T1.ItemCode
    WHERE T0.DocDate >= DATEADD(MONTH, -12, @FechaFinal)
      AND T0.DocDate < DATEADD(MONTH, 1, @FechaFinal)
      AND T1.ItmsGrpCod = 110
),

SumaMes AS (
    SELECT
        ItemCode,
        ItemName,
        Mes,
        SUM(Entrada) - SUM(Salida) AS SaldoMes
    FROM Movimientos
    GROUP BY ItemCode, ItemName, Mes
),

SaldoInicial AS (
    SELECT
        T0.ItemCode,
        T1.ItemName,
        SUM(ISNULL(T0.InQty, 0) - ISNULL(T0.OutQty, 0)) AS SaldoInicial
    FROM dbo.OINM T0
    INNER JOIN dbo.OITM T1 ON T0.ItemCode = T1.ItemCode
    WHERE T1.ItmsGrpCod = 110
      AND T0.DocDate < DATEFROMPARTS(YEAR(DATEADD(MONTH, -12, @FechaFinal)), MONTH(DATEADD(MONTH, -12, @FechaFinal)), 1)
    GROUP BY T0.ItemCode, T1.ItemName
),

TodosLosArticulos AS (
    SELECT ItemCode, ItemName FROM SumaMes
    UNION
    SELECT ItemCode, ItemName FROM SaldoInicial
),

ArticulosMeses AS (
    SELECT
        a.ItemCode,
        a.ItemName,
        m.Mes,
        m.MesNum
    FROM TodosLosArticulos a
    CROSS JOIN MesesCalendario m
),

MovMesCompleto AS (
    SELECT
        am.ItemCode,
        am.ItemName,
        am.Mes,
        am.MesNum,
        COALESCE(sm.SaldoMes, 0) AS SaldoMes
    FROM ArticulosMeses am
    LEFT JOIN SumaMes sm ON sm.ItemCode = am.ItemCode AND sm.Mes = am.Mes
),

SaldoAcumulado AS (
    SELECT
        amc.ItemCode,
        amc.ItemName,
        amc.MesNum,
        amc.Mes,
        COALESCE(si.SaldoInicial, 0) +
        SUM(amc.SaldoMes) OVER (PARTITION BY amc.ItemCode ORDER BY amc.MesNum ROWS UNBOUNDED PRECEDING) AS InventarioAcumulado
    FROM MovMesCompleto amc
    LEFT JOIN SaldoInicial si ON amc.ItemCode = si.ItemCode
    WHERE amc.MesNum BETWEEN 0 AND 12
)

SELECT
    ItemCode,
    ItemName AS Descripcion,
    MAX(CASE WHEN MesNum = 0 THEN InventarioAcumulado END) AS [1],
    MAX(CASE WHEN MesNum = 1 THEN InventarioAcumulado END) AS [2],
    MAX(CASE WHEN MesNum = 2 THEN InventarioAcumulado END) AS [3],
    MAX(CASE WHEN MesNum = 3 THEN InventarioAcumulado END) AS [4],
    MAX(CASE WHEN MesNum = 4 THEN InventarioAcumulado END) AS [5],
    MAX(CASE WHEN MesNum = 5 THEN InventarioAcumulado END) AS [6],
    MAX(CASE WHEN MesNum = 6 THEN InventarioAcumulado END) AS [7],
    MAX(CASE WHEN MesNum = 7 THEN InventarioAcumulado END) AS [8],
    MAX(CASE WHEN MesNum = 8 THEN InventarioAcumulado END) AS [9],
    MAX(CASE WHEN MesNum = 9 THEN InventarioAcumulado END) AS [10],
    MAX(CASE WHEN MesNum = 10 THEN InventarioAcumulado END) AS [11],
    MAX(CASE WHEN MesNum = 11 THEN InventarioAcumulado END) AS [12]
FROM SaldoAcumulado
GROUP BY ItemCode, ItemName
ORDER BY ItemCode;
"""

try:
    df_sql = pd.read_sql(query, conn)
    df_sql.to_csv("dataset_inventario.csv", index=False, encoding='utf-8-sig')
    print("✅ CSV generado exitosamente: dataset_inventario.csv")
except Exception as e:
    print(f"❌ Error al ejecutar la consulta o guardar el CSV: {e}")
finally:
    conn.close()
