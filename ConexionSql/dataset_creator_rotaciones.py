import pandas as pd
from conexion_2 import conectorcito

# Conexión
conn = conectorcito()
if conn is None:
    exit("❌ No se pudo conectar a la base de datos.")

query = r"""
WITH Movs AS (
    SELECT
        CAST(T0.DocDate AS date)      AS Fecha,
        T0.ItemCode                   AS ItemCode,
        SUM(T0.InQty)                 AS InQty,
        SUM(T0.OutQty)                AS OutQty
    FROM OINM T0
    INNER JOIN OITM T1 ON T1.ItemCode = T0.ItemCode
    WHERE T1.ItemCode LIKE 'LLA%'         -- sin rango: trae todo
    GROUP BY CAST(T0.DocDate AS date), T0.ItemCode
),
Ventas AS (
    SELECT
        CAST(H.DocDate AS date)       AS Fecha,
        L.ItemCode                    AS ItemCode,
        SUM(L.LineTotal)              AS Ingresos,
        SUM(L.Quantity * L.Price)     AS CostoTotal
    FROM INV1 L
    INNER JOIN OINV H ON H.DocEntry = L.DocEntry   -- fecha viene del header
    WHERE L.ItemCode LIKE 'LLA%'
    GROUP BY CAST(H.DocDate AS date), L.ItemCode
),
J AS (
    SELECT
        COALESCE(M.Fecha, V.Fecha)            AS [Fecha],
        COALESCE(M.ItemCode, V.ItemCode)      AS [Código del Artículo],
        I.ItemName                             AS [Nombre del Artículo],
        ISNULL(M.InQty, 0)                     AS [Total Comprado],
        ISNULL(M.OutQty, 0)                    AS [Total Vendido],
        CASE 
            WHEN ISNULL(M.InQty, 0) = 0 THEN 0
            ELSE CAST(ISNULL(M.OutQty, 0) AS float) / NULLIF(M.InQty, 0)
        END                                    AS [Rotación],
        ISNULL(V.Ingresos, 0)                  AS [Ingresos],
        ISNULL(V.CostoTotal, 0)                AS [Costo Total],
        ISNULL(V.Ingresos, 0) - ISNULL(V.CostoTotal, 0) AS [Ganancia Bruta],
        CASE 
            WHEN ISNULL(V.Ingresos, 0) = 0 THEN 0
            ELSE CAST(ISNULL(V.Ingresos, 0) - ISNULL(V.CostoTotal, 0) AS float) / NULLIF(V.Ingresos, 0)
        END                                    AS [Margen de Ganancia]
    FROM Movs M
    FULL OUTER JOIN Ventas V
        ON M.Fecha = V.Fecha AND M.ItemCode = V.ItemCode
    LEFT JOIN OITM I
        ON I.ItemCode = COALESCE(M.ItemCode, V.ItemCode)
    WHERE COALESCE(M.ItemCode, V.ItemCode) IS NOT NULL
)
SELECT *
FROM J
WHERE
    ([Rotación] < 8)
    AND ([Margen de Ganancia] < 10.00)   -- si esto es %, cámbialo a 0.10
ORDER BY
    [Fecha] ASC, [Rotación] ASC, [Margen de Ganancia] ASC;
"""

try:
    cursor = conn.cursor()
    cursor.execute(query)

    # Avanza a primer resultset útil (por si el driver devuelve info previa)
    while cursor.description is None and cursor.nextset():
        pass

    if cursor.description is None:
        print("⚠️ La consulta no retornó ningún resultado (SELECT).")
    else:
        cols = [c[0] for c in cursor.description]
        rows = cursor.fetchall()
        df = pd.DataFrame.from_records(rows, columns=cols)

        # Formato fecha
        if "Fecha" in df.columns:
            try:
                df["Fecha"] = pd.to_datetime(df["Fecha"]).dt.strftime("%Y-%m-%d")
            except Exception:
                pass

        df.to_csv("rotaciones_completas.csv", index=False, encoding="utf-8-sig")
        print("✅ Archivo CSV generado: rotaciones_completas.csv")

except Exception as e:
    print(f"❌ Error ejecutando la consulta: {e}")

finally:
    conn.close()
