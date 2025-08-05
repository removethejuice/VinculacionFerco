# SQLManagement.py
import pandas as pd  # Para trabajar con DataFrames
from ConexionSql.conexion import conectorcito  # Asegúrate de que conexion.py esté en el mismo directorio

class SQLManagement:

    def __init__(self):
        pass

    def conect(self):
        return conectorcito()  # Llama directamente a la función importada

    # Versión con manejo seguro de recursos
    def VentasPorMesSinFiltroLlantas(self, conn):
        try:
            consulta = """
            SET NOCOUNT ON;
            /* VENTAS DE LOS ULTIMOS 12 MESES*/

                DECLARE @ItemCode as nvarchar(40)
                DECLARE @Vta1 as float
                DECLARE @Vta2 as float
                DECLARE @Vta3 as float
                DECLARE @Vta4 as float
                DECLARE @Vta5 as float
                DECLARE @Vta6 as float
                DECLARE @Vta7 as float
                DECLARE @Vta8 as float
                DECLARE @Vta9 as float
                DECLARE @Vta10 as float
                DECLARE @Vta11 as float
                DECLARE @Vta12 as float

                DECLARE @TempTable TABLE
                (
                ItemCode nvarchar(40),
                Vta1 float,
                Vta2 float,
                Vta3 float,
                Vta4 float,
                Vta5 float, 
                Vta6 float,
                Vta7 float,
                Vta8 float,
                Vta9 float,
                Vta10 float,
                Vta11 float,
                Vta12 float)

                INSERT @TempTable (ItemCode)
                SELECT ItemCode 
                FROM OITM
                WHERE [ItmsGrpCod] = 110
                AND ValidFor = 'Y'

                DECLARE Saldo CURSOR FOR
                SELECT T0.ItemCode, T0.Vta1, T0.Vta2, T0.Vta3, T0.Vta4, T0.Vta5, T0.Vta6, T0.Vta7, T0.Vta8, T0.Vta9, T0.Vta10, T0.Vta11, T0.Vta12
                FROM @TempTable T0

                OPEN Saldo
                FETCH NEXT FROM Saldo
                INTO @ItemCode, @Vta1, @Vta2, @Vta3, @Vta4, @Vta5, @Vta6, @Vta7, @Vta8, @Vta9, @Vta10, @Vta11, @Vta12
                WHILE @@FETCH_STATUS = 0
                BEGIN
                        UPDATE @TempTable
                        SET Vta1 = (SELECT SUM(Cantidad)
                            FROM 
                                (SELECT INV1.Quantity as Cantidad
                                FROM INV1 
                                    INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                                WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 1
                                    AND OINV.Canceled = 'N'
                                    AND INV1.ItemCode = @ItemCode
                                UNION ALL
                                SELECT RIN1.Quantity*-1
                                FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                                WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 1
                                    AND ORIN.Canceled = 'N'
                                    AND RIN1.ItemCode = @ItemCode) Ventas)
                , Vta2 = (SELECT SUM(Cantidad)
                            FROM 
                                (SELECT INV1.Quantity as Cantidad
                                FROM INV1 
                                    INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                                WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 2
                                    AND OINV.Canceled = 'N'
                                    AND INV1.ItemCode = @ItemCode
                                UNION ALL
                                SELECT RIN1.Quantity*-1
                                FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                                WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 2
                                    AND ORIN.Canceled = 'N'
                                    AND RIN1.ItemCode = @ItemCode) Ventas)
                , Vta3 = (SELECT SUM(Cantidad)
                            FROM 
                                (SELECT INV1.Quantity as Cantidad
                                FROM INV1 
                                    INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                                WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 3
                                    AND OINV.Canceled = 'N'
                                    AND INV1.ItemCode = @ItemCode
                                UNION ALL
                                SELECT RIN1.Quantity*-1
                                FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                                WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 3
                                    AND ORIN.Canceled = 'N'
                                    AND RIN1.ItemCode = @ItemCode) Ventas)
                , Vta4 = (SELECT SUM(Cantidad)
                            FROM 
                                (SELECT INV1.Quantity as Cantidad
                                FROM INV1 
                                    INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                                WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 4
                                    AND OINV.Canceled = 'N'
                                    AND INV1.ItemCode = @ItemCode
                                UNION ALL
                                SELECT RIN1.Quantity*-1
                                FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                                WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 4
                                    AND ORIN.Canceled = 'N'
                                    AND RIN1.ItemCode = @ItemCode) Ventas)
                , Vta5 = (SELECT SUM(Cantidad)
                            FROM 
                                (SELECT INV1.Quantity as Cantidad
                                FROM INV1 
                                    INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                                WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 5
                                    AND OINV.Canceled = 'N'
                                    AND INV1.ItemCode = @ItemCode
                                UNION ALL
                                SELECT RIN1.Quantity*-1
                                FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                                WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 5
                                    AND ORIN.Canceled = 'N'
                                    AND RIN1.ItemCode = @ItemCode) Ventas)
                , Vta6 = (SELECT SUM(Cantidad)
                            FROM 
                                (SELECT INV1.Quantity as Cantidad
                                FROM INV1 
                                    INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                                WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 6
                                    AND OINV.Canceled = 'N'
                                    AND INV1.ItemCode = @ItemCode
                                UNION ALL
                                SELECT RIN1.Quantity*-1
                                FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                                WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 6
                                    AND ORIN.Canceled = 'N'
                                    AND RIN1.ItemCode = @ItemCode) Ventas)
                , Vta7 = (SELECT SUM(Cantidad)
                            FROM 
                                (SELECT INV1.Quantity as Cantidad
                                FROM INV1 
                                    INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                                WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 7
                                    AND OINV.Canceled = 'N'
                                    AND INV1.ItemCode = @ItemCode
                                UNION ALL
                                SELECT RIN1.Quantity*-1
                                FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                                WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 7
                                    AND ORIN.Canceled = 'N'
                                    AND RIN1.ItemCode = @ItemCode) Ventas)
                , Vta8 = (SELECT SUM(Cantidad)
                            FROM 
                                (SELECT INV1.Quantity as Cantidad
                                FROM INV1 
                                    INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                                WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 8
                                    AND OINV.Canceled = 'N'
                                    AND INV1.ItemCode = @ItemCode
                                UNION ALL
                                SELECT RIN1.Quantity*-1
                                FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                                WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 8
                                    AND ORIN.Canceled = 'N'
                                    AND RIN1.ItemCode = @ItemCode) Ventas)
                , Vta9 = (SELECT SUM(Cantidad)
                            FROM 
                                (SELECT INV1.Quantity as Cantidad
                                FROM INV1 
                                    INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                                WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 9
                                    AND OINV.Canceled = 'N'
                                    AND INV1.ItemCode = @ItemCode
                                UNION ALL
                                SELECT RIN1.Quantity*-1
                                FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                                WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 9
                                    AND ORIN.Canceled = 'N'
                                    AND RIN1.ItemCode = @ItemCode) Ventas)
                , Vta10 = (SELECT SUM(Cantidad)
                            FROM 
                                (SELECT INV1.Quantity as Cantidad
                                FROM INV1 
                                    INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                                WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 10
                                    AND OINV.Canceled = 'N'
                                    AND INV1.ItemCode = @ItemCode
                                UNION ALL
                                SELECT RIN1.Quantity*-1
                                FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                                WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 10
                                    AND ORIN.Canceled = 'N'
                                    AND RIN1.ItemCode = @ItemCode) Ventas)
                , Vta11 = (SELECT SUM(Cantidad)
                            FROM 
                                (SELECT INV1.Quantity as Cantidad
                                FROM INV1 
                                    INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                                WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 11
                                    AND OINV.Canceled = 'N'
                                    AND INV1.ItemCode = @ItemCode
                                UNION ALL
                                SELECT RIN1.Quantity*-1
                                FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                                WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 11
                                    AND ORIN.Canceled = 'N'
                                    AND RIN1.ItemCode = @ItemCode) Ventas)
                , Vta12 = (SELECT SUM(Cantidad)
                            FROM 
                                (SELECT INV1.Quantity as Cantidad
                                FROM INV1 
                                    INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                                WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 12
                                    AND OINV.Canceled = 'N'
                                    AND INV1.ItemCode = @ItemCode
                                UNION ALL
                                SELECT RIN1.Quantity*-1
                                FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                                WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 12
                                    AND ORIN.Canceled = 'N'
                                    AND RIN1.ItemCode = @ItemCode) Ventas)

                WHERE ItemCode = @ItemCode
                FETCH NEXT FROM Saldo
                INTO @ItemCode, @Vta1, @Vta2, @Vta3, @Vta4, @Vta5, @Vta6, @Vta7, @Vta8, @Vta9, @Vta10, @Vta11, @Vta12 
                END
                CLOSE Saldo
                DEALLOCATE Saldo

                /************************************************************************************/
                declare @GroupCode as NVARCHAR(150)
                set @GroupCode = 110

                SELECT T0.[ItemCode]
                    , T0.[ItemName]
                    , T0.[SuppCatNum] as 'No. Fabricante'
                    , T0.[OnHand]
                    , T0.[IsCommited]
                    , T0.[OnOrder]
                    , ISNULL((SELECT sum(T1.[Quantity]) 
                    FROM OPQT OFERTA INNER JOIN PQT1 T1 ON OFERTA.DocEntry = T1.DocEntry 
                    WHERE T1.[LineStatus] = 'O' AND T1.ItemCode=T0.ItemCode GROUP BY T1.[ItemCode]), 0.0) as [Pedido]
                    ,  ISNULL( T0.[OnHand]+ T0.[OnOrder]-T0.[IsCommited] + ISNULL(ISNULL((SELECT sum(T1.[Quantity]) 
                    FROM OPQT OFERTA INNER JOIN PQT1 T1 ON OFERTA.DocEntry = T1.DocEntry 
                    WHERE T1.[LineStatus] = 'O' AND T1.ItemCode=T0.ItemCode GROUP BY T1.[ItemCode]), 0.0), 0.0), 0.0) [Total]
                    , isnull((SELECT Vta12 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '1'
                    , isnull((SELECT Vta11 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '2'
                    , isnull((SELECT Vta10 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '3'
                    , isnull((SELECT Vta9 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '4'
                    , isnull((SELECT Vta8 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '5'
                    , isnull((SELECT Vta7 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '6'
                    , isnull((SELECT Vta6 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '7'
                    , isnull((SELECT Vta5 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '8'
                    , isnull((SELECT Vta4 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '9'
                    , isnull((SELECT Vta3 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '10'
                    , isnull((SELECT Vta2 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '11'
                    , isnull((SELECT Vta1 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '12'
                    , ((isnull((SELECT Vta12 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                    isnull((SELECT Vta11 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                    isnull((SELECT Vta10 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                    isnull((SELECT Vta9 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                    isnull((SELECT Vta8 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                    isnull((SELECT Vta7 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                    isnull((SELECT Vta6 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                    isnull((SELECT Vta5 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                    isnull((SELECT Vta4 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                    isnull((SELECT Vta3 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                    isnull((SELECT Vta2 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                    isnull((SELECT Vta1 FROM @Temptable WHERE ItemCode = T0.ItemCode),0))/12 )  [Promedio Mensual]
                FROM OITM T0, OITB T1
                WHERE T0.ItmsGrpCod = T1.ItmsGrpCod
                AND T1.ItmsGrpCod = 110
                AND T0.[validFor] = 'Y'
            """
            
            # Usar read_sql que maneja automáticamente las columnas
            model = pd.read_sql(consulta, conn)
            print(f"✅ Datos obtenidos correctamente. Forma: {model.shape}")
            return model
        
        except Exception as e:
            print(f"❌ Error al realizar la consulta: {str(e)}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()
    def VentasPorMesFiltroLlantasMarca(self, conn, marca):
        try:
            consulta = f"""
            SET NOCOUNT ON;
            DECLARE @ItemCode as nvarchar(40)
            DECLARE @Vta1 as float
            DECLARE @Vta2 as float
            DECLARE @Vta3 as float
            DECLARE @Vta4 as float
            DECLARE @Vta5 as float
            DECLARE @Vta6 as float
            DECLARE @Vta7 as float
            DECLARE @Vta8 as float
            DECLARE @Vta9 as float
            DECLARE @Vta10 as float
            DECLARE @Vta11 as float
            DECLARE @Vta12 as float

            DECLARE @TempTable TABLE
            (
            ItemCode nvarchar(40),
            Vta1 float,
            Vta2 float,
            Vta3 float,
            Vta4 float,
            Vta5 float, 
            Vta6 float,
            Vta7 float,
            Vta8 float,
            Vta9 float,
            Vta10 float,
            Vta11 float,
            Vta12 float)

            INSERT @TempTable (ItemCode)
            SELECT ItemCode 
            FROM OITM
            WHERE [ItmsGrpCod] = 110
            AND ValidFor = 'Y'

            DECLARE Saldo CURSOR FOR
            SELECT T0.ItemCode, T0.Vta1, T0.Vta2, T0.Vta3, T0.Vta4, T0.Vta5, T0.Vta6, T0.Vta7, T0.Vta8, T0.Vta9, T0.Vta10, T0.Vta11, T0.Vta12
            FROM @TempTable T0

            OPEN Saldo
            FETCH NEXT FROM Saldo
            INTO @ItemCode, @Vta1, @Vta2, @Vta3, @Vta4, @Vta5, @Vta6, @Vta7, @Vta8, @Vta9, @Vta10, @Vta11, @Vta12
            WHILE @@FETCH_STATUS = 0
            BEGIN
                    UPDATE @TempTable
                    SET Vta1 = (SELECT SUM(Cantidad)
                        FROM 
                            (SELECT INV1.Quantity as Cantidad
                            FROM INV1 
                                INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 1
                                AND OINV.Canceled = 'N'
                                AND INV1.ItemCode = @ItemCode
                            UNION ALL
                            SELECT RIN1.Quantity*-1
                            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 1
                                AND ORIN.Canceled = 'N'
                                AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta2 = (SELECT SUM(Cantidad)
                        FROM 
                            (SELECT INV1.Quantity as Cantidad
                            FROM INV1 
                                INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 2
                                AND OINV.Canceled = 'N'
                                AND INV1.ItemCode = @ItemCode
                            UNION ALL
                            SELECT RIN1.Quantity*-1
                            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 2
                                AND ORIN.Canceled = 'N'
                                AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta3 = (SELECT SUM(Cantidad)
                        FROM 
                            (SELECT INV1.Quantity as Cantidad
                            FROM INV1 
                                INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 3
                                AND OINV.Canceled = 'N'
                                AND INV1.ItemCode = @ItemCode
                            UNION ALL
                            SELECT RIN1.Quantity*-1
                            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 3
                                AND ORIN.Canceled = 'N'
                                AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta4 = (SELECT SUM(Cantidad)
                        FROM 
                            (SELECT INV1.Quantity as Cantidad
                            FROM INV1 
                                INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 4
                                AND OINV.Canceled = 'N'
                                AND INV1.ItemCode = @ItemCode
                            UNION ALL
                            SELECT RIN1.Quantity*-1
                            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 4
                                AND ORIN.Canceled = 'N'
                                AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta5 = (SELECT SUM(Cantidad)
                        FROM 
                            (SELECT INV1.Quantity as Cantidad
                            FROM INV1 
                                INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 5
                                AND OINV.Canceled = 'N'
                                AND INV1.ItemCode = @ItemCode
                            UNION ALL
                            SELECT RIN1.Quantity*-1
                            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 5
                                AND ORIN.Canceled = 'N'
                                AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta6 = (SELECT SUM(Cantidad)
                        FROM 
                            (SELECT INV1.Quantity as Cantidad
                            FROM INV1 
                                INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 6
                                AND OINV.Canceled = 'N'
                                AND INV1.ItemCode = @ItemCode
                            UNION ALL
                            SELECT RIN1.Quantity*-1
                            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 6
                                AND ORIN.Canceled = 'N'
                                AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta7 = (SELECT SUM(Cantidad)
                        FROM 
                            (SELECT INV1.Quantity as Cantidad
                            FROM INV1 
                                INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 7
                                AND OINV.Canceled = 'N'
                                AND INV1.ItemCode = @ItemCode
                            UNION ALL
                            SELECT RIN1.Quantity*-1
                            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 7
                                AND ORIN.Canceled = 'N'
                                AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta8 = (SELECT SUM(Cantidad)
                        FROM 
                            (SELECT INV1.Quantity as Cantidad
                            FROM INV1 
                                INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 8
                                AND OINV.Canceled = 'N'
                                AND INV1.ItemCode = @ItemCode
                            UNION ALL
                            SELECT RIN1.Quantity*-1
                            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 8
                                AND ORIN.Canceled = 'N'
                                AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta9 = (SELECT SUM(Cantidad)
                        FROM 
                            (SELECT INV1.Quantity as Cantidad
                            FROM INV1 
                                INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 9
                                AND OINV.Canceled = 'N'
                                AND INV1.ItemCode = @ItemCode
                            UNION ALL
                            SELECT RIN1.Quantity*-1
                            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 9
                                AND ORIN.Canceled = 'N'
                                AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta10 = (SELECT SUM(Cantidad)
                        FROM 
                            (SELECT INV1.Quantity as Cantidad
                            FROM INV1 
                                INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 10
                                AND OINV.Canceled = 'N'
                                AND INV1.ItemCode = @ItemCode
                            UNION ALL
                            SELECT RIN1.Quantity*-1
                            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 10
                                AND ORIN.Canceled = 'N'
                                AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta11 = (SELECT SUM(Cantidad)
                        FROM 
                            (SELECT INV1.Quantity as Cantidad
                            FROM INV1 
                                INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 11
                                AND OINV.Canceled = 'N'
                                AND INV1.ItemCode = @ItemCode
                            UNION ALL
                            SELECT RIN1.Quantity*-1
                            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 11
                                AND ORIN.Canceled = 'N'
                                AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta12 = (SELECT SUM(Cantidad)
                        FROM 
                            (SELECT INV1.Quantity as Cantidad
                            FROM INV1 
                                INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 12
                                AND OINV.Canceled = 'N'
                                AND INV1.ItemCode = @ItemCode
                            UNION ALL
                            SELECT RIN1.Quantity*-1
                            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 12
                                AND ORIN.Canceled = 'N'
                                AND RIN1.ItemCode = @ItemCode) Ventas)

            WHERE ItemCode = @ItemCode
            FETCH NEXT FROM Saldo
            INTO @ItemCode, @Vta1, @Vta2, @Vta3, @Vta4, @Vta5, @Vta6, @Vta7, @Vta8, @Vta9, @Vta10, @Vta11, @Vta12 
            END
            CLOSE Saldo
            DEALLOCATE Saldo

            /************************************************************************************/
            declare @GroupCode as NVARCHAR(150)
            set @GroupCode = 110

            SELECT T0.[ItemCode]
                , T0.[ItemName]
                , T0.[SuppCatNum] as 'No. Fabricante'
                , T0.[OnHand]
                , T0.[IsCommited]
                , T0.[OnOrder]
                , ISNULL((SELECT sum(T1.[Quantity]) 
                FROM OPQT OFERTA INNER JOIN PQT1 T1 ON OFERTA.DocEntry = T1.DocEntry 
                WHERE T1.[LineStatus] = 'O' AND T1.ItemCode=T0.ItemCode GROUP BY T1.[ItemCode]), 0.0) as [Pedido]
                ,  ISNULL( T0.[OnHand]+ T0.[OnOrder]-T0.[IsCommited] + ISNULL(ISNULL((SELECT sum(T1.[Quantity]) 
                FROM OPQT OFERTA INNER JOIN PQT1 T1 ON OFERTA.DocEntry = T1.DocEntry 
                WHERE T1.[LineStatus] = 'O' AND T1.ItemCode=T0.ItemCode GROUP BY T1.[ItemCode]), 0.0), 0.0), 0.0) [Total]
                , isnull((SELECT Vta12 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '1'
                , isnull((SELECT Vta11 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '2'
                , isnull((SELECT Vta10 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '3'
                , isnull((SELECT Vta9 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '4'
                , isnull((SELECT Vta8 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '5'
                , isnull((SELECT Vta7 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '6'
                , isnull((SELECT Vta6 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '7'
                , isnull((SELECT Vta5 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '8'
                , isnull((SELECT Vta4 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '9'
                , isnull((SELECT Vta3 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '10'
                , isnull((SELECT Vta2 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '11'
                , isnull((SELECT Vta1 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '12'
                , ((isnull((SELECT Vta12 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                isnull((SELECT Vta11 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                isnull((SELECT Vta10 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                isnull((SELECT Vta9 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                isnull((SELECT Vta8 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                isnull((SELECT Vta7 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                isnull((SELECT Vta6 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                isnull((SELECT Vta5 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                isnull((SELECT Vta4 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                isnull((SELECT Vta3 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                isnull((SELECT Vta2 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                isnull((SELECT Vta1 FROM @Temptable WHERE ItemCode = T0.ItemCode),0))/12 )  [Promedio Mensual]
            FROM OITM T0, OITB T1
            WHERE T0.ItmsGrpCod = T1.ItmsGrpCod
            AND T1.ItmsGrpCod = 110
            AND T0.[validFor] = 'Y'
            AND T0.ItemName LIKE '%{marca}%'
            """
            
            # Usar read_sql que maneja automáticamente las columnas
            model = pd.read_sql(consulta, conn)
            print(f"✅ Datos obtenidos correctamente para la marca '{marca}'. Forma: {model.shape}")
            return model
        
        except Exception as e:
            print(f"❌ Error al realizar la consulta: {str(e)}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()
    
    def VentasPorMesSinFiltroAceites(self, conn):
        try:
            consulta = """
            SET NOCOUNT ON;
            /* VENTAS DE LOS ULTIMOS 12 MESES*/

                /* VENTAS DE LOS ULTIMOS 12 MESES*/

                DECLARE @ItemCode as nvarchar(40)
                DECLARE @Vta1 as float
                DECLARE @Vta2 as float
                DECLARE @Vta3 as float
                DECLARE @Vta4 as float
                DECLARE @Vta5 as float
                DECLARE @Vta6 as float
                DECLARE @Vta7 as float
                DECLARE @Vta8 as float
                DECLARE @Vta9 as float
                DECLARE @Vta10 as float
                DECLARE @Vta11 as float
                DECLARE @Vta12 as float

                DECLARE @TempTable TABLE
                (
                ItemCode nvarchar(40),
                Vta1 float,
                Vta2 float,
                Vta3 float,
                Vta4 float,
                Vta5 float, 
                Vta6 float,
                Vta7 float,
                Vta8 float,
                Vta9 float,
                Vta10 float,
                Vta11 float,
                Vta12 float)

                INSERT @TempTable (ItemCode)
                SELECT ItemCode 
                FROM OITM
                WHERE [ItmsGrpCod] = 125
                AND ValidFor = 'Y'

                DECLARE Saldo CURSOR FOR
                SELECT T0.ItemCode, T0.Vta1, T0.Vta2, T0.Vta3, T0.Vta4, T0.Vta5, T0.Vta6, T0.Vta7, T0.Vta8, T0.Vta9, T0.Vta10, T0.Vta11, T0.Vta12
                FROM @TempTable T0

                OPEN Saldo
                FETCH NEXT FROM Saldo
                INTO @ItemCode, @Vta1, @Vta2, @Vta3, @Vta4, @Vta5, @Vta6, @Vta7, @Vta8, @Vta9, @Vta10, @Vta11, @Vta12
                WHILE @@FETCH_STATUS = 0
                BEGIN
                        UPDATE @TempTable
                        SET Vta1 = (SELECT SUM(Cantidad)
                            FROM 
                                (SELECT INV1.Quantity as Cantidad
                                FROM INV1 
                                    INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                                WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 1
                                    AND OINV.Canceled = 'N'
                                    AND INV1.ItemCode = @ItemCode
                                UNION ALL
                                SELECT RIN1.Quantity*-1
                                FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                                WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 1
                                    AND ORIN.Canceled = 'N'
                                    AND RIN1.ItemCode = @ItemCode) Ventas)
                , Vta2 = (SELECT SUM(Cantidad)
                            FROM 
                                (SELECT INV1.Quantity as Cantidad
                                FROM INV1 
                                    INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                                WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 2
                                    AND OINV.Canceled = 'N'
                                    AND INV1.ItemCode = @ItemCode
                                UNION ALL
                                SELECT RIN1.Quantity*-1
                                FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                                WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 2
                                    AND ORIN.Canceled = 'N'
                                    AND RIN1.ItemCode = @ItemCode) Ventas)
                , Vta3 = (SELECT SUM(Cantidad)
                            FROM 
                                (SELECT INV1.Quantity as Cantidad
                                FROM INV1 
                                    INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                                WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 3
                                    AND OINV.Canceled = 'N'
                                    AND INV1.ItemCode = @ItemCode
                                UNION ALL
                                SELECT RIN1.Quantity*-1
                                FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                                WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 3
                                    AND ORIN.Canceled = 'N'
                                    AND RIN1.ItemCode = @ItemCode) Ventas)
                , Vta4 = (SELECT SUM(Cantidad)
                            FROM 
                                (SELECT INV1.Quantity as Cantidad
                                FROM INV1 
                                    INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                                WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 4
                                    AND OINV.Canceled = 'N'
                                    AND INV1.ItemCode = @ItemCode
                                UNION ALL
                                SELECT RIN1.Quantity*-1
                                FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                                WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 4
                                    AND ORIN.Canceled = 'N'
                                    AND RIN1.ItemCode = @ItemCode) Ventas)
                , Vta5 = (SELECT SUM(Cantidad)
                            FROM 
                                (SELECT INV1.Quantity as Cantidad
                                FROM INV1 
                                    INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                                WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 5
                                    AND OINV.Canceled = 'N'
                                    AND INV1.ItemCode = @ItemCode
                                UNION ALL
                                SELECT RIN1.Quantity*-1
                                FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                                WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 5
                                    AND ORIN.Canceled = 'N'
                                    AND RIN1.ItemCode = @ItemCode) Ventas)
                , Vta6 = (SELECT SUM(Cantidad)
                            FROM 
                                (SELECT INV1.Quantity as Cantidad
                                FROM INV1 
                                    INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                                WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 6
                                    AND OINV.Canceled = 'N'
                                    AND INV1.ItemCode = @ItemCode
                                UNION ALL
                                SELECT RIN1.Quantity*-1
                                FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                                WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 6
                                    AND ORIN.Canceled = 'N'
                                    AND RIN1.ItemCode = @ItemCode) Ventas)
                , Vta7 = (SELECT SUM(Cantidad)
                            FROM 
                                (SELECT INV1.Quantity as Cantidad
                                FROM INV1 
                                    INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                                WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 7
                                    AND OINV.Canceled = 'N'
                                    AND INV1.ItemCode = @ItemCode
                                UNION ALL
                                SELECT RIN1.Quantity*-1
                                FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                                WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 7
                                    AND ORIN.Canceled = 'N'
                                    AND RIN1.ItemCode = @ItemCode) Ventas)
                , Vta8 = (SELECT SUM(Cantidad)
                            FROM 
                                (SELECT INV1.Quantity as Cantidad
                                FROM INV1 
                                    INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                                WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 8
                                    AND OINV.Canceled = 'N'
                                    AND INV1.ItemCode = @ItemCode
                                UNION ALL
                                SELECT RIN1.Quantity*-1
                                FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                                WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 8
                                    AND ORIN.Canceled = 'N'
                                    AND RIN1.ItemCode = @ItemCode) Ventas)
                , Vta9 = (SELECT SUM(Cantidad)
                            FROM 
                                (SELECT INV1.Quantity as Cantidad
                                FROM INV1 
                                    INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                                WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 9
                                    AND OINV.Canceled = 'N'
                                    AND INV1.ItemCode = @ItemCode
                                UNION ALL
                                SELECT RIN1.Quantity*-1
                                FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                                WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 9
                                    AND ORIN.Canceled = 'N'
                                    AND RIN1.ItemCode = @ItemCode) Ventas)
                , Vta10 = (SELECT SUM(Cantidad)
                            FROM 
                                (SELECT INV1.Quantity as Cantidad
                                FROM INV1 
                                    INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                                WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 10
                                    AND OINV.Canceled = 'N'
                                    AND INV1.ItemCode = @ItemCode
                                UNION ALL
                                SELECT RIN1.Quantity*-1
                                FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                                WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 10
                                    AND ORIN.Canceled = 'N'
                                    AND RIN1.ItemCode = @ItemCode) Ventas)
                , Vta11 = (SELECT SUM(Cantidad)
                            FROM 
                                (SELECT INV1.Quantity as Cantidad
                                FROM INV1 
                                    INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                                WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 11
                                    AND OINV.Canceled = 'N'
                                    AND INV1.ItemCode = @ItemCode
                                UNION ALL
                                SELECT RIN1.Quantity*-1
                                FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                                WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 11
                                    AND ORIN.Canceled = 'N'
                                    AND RIN1.ItemCode = @ItemCode) Ventas)
                , Vta12 = (SELECT SUM(Cantidad)
                            FROM 
                                (SELECT INV1.Quantity as Cantidad
                                FROM INV1 
                                    INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                                WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 12
                                    AND OINV.Canceled = 'N'
                                    AND INV1.ItemCode = @ItemCode
                                UNION ALL
                                SELECT RIN1.Quantity*-1
                                FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                                WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 12
                                    AND ORIN.Canceled = 'N'
                                    AND RIN1.ItemCode = @ItemCode) Ventas)

                WHERE ItemCode = @ItemCode
                FETCH NEXT FROM Saldo
                INTO @ItemCode, @Vta1, @Vta2, @Vta3, @Vta4, @Vta5, @Vta6, @Vta7, @Vta8, @Vta9, @Vta10, @Vta11, @Vta12 
                END
                CLOSE Saldo
                DEALLOCATE Saldo

                /************************************************************************************/
                declare @GroupCode as NVARCHAR(150)
                set @GroupCode = 125

                SELECT T0.[ItemCode]
                    , T0.[ItemName]
                    , T0.[OnHand]
                    , T0.[IsCommited]
                    , T0.[OnOrder]
                    , ISNULL((SELECT sum(T1.[Quantity]) 
                    FROM OPQT OFERTA INNER JOIN PQT1 T1 ON OFERTA.DocEntry = T1.DocEntry 
                    WHERE T1.[LineStatus] = 'O' AND T1.ItemCode=T0.ItemCode GROUP BY T1.[ItemCode]), 0.0) as [Pedido]
                    ,  ISNULL( T0.[OnHand]+ T0.[OnOrder]-T0.[IsCommited] + ISNULL(ISNULL((SELECT sum(T1.[Quantity]) 
                    FROM OPQT OFERTA INNER JOIN PQT1 T1 ON OFERTA.DocEntry = T1.DocEntry 
                    WHERE T1.[LineStatus] = 'O' AND T1.ItemCode=T0.ItemCode GROUP BY T1.[ItemCode]), 0.0), 0.0), 0.0) [Total]
                    , isnull((SELECT Vta12 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '1'
                    , isnull((SELECT Vta11 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '2'
                    , isnull((SELECT Vta10 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '3'
                    , isnull((SELECT Vta9 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '4'
                    , isnull((SELECT Vta8 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '5'
                    , isnull((SELECT Vta7 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '6'
                    , isnull((SELECT Vta6 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '7'
                    , isnull((SELECT Vta5 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '8'
                    , isnull((SELECT Vta4 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '9'
                    , isnull((SELECT Vta3 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '10'
                    , isnull((SELECT Vta2 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '11'
                    , isnull((SELECT Vta1 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '12'
                    , ((isnull((SELECT Vta12 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                    isnull((SELECT Vta11 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                    isnull((SELECT Vta10 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                    isnull((SELECT Vta9 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                    isnull((SELECT Vta8 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                    isnull((SELECT Vta7 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                    isnull((SELECT Vta6 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                    isnull((SELECT Vta5 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                    isnull((SELECT Vta4 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                    isnull((SELECT Vta3 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                    isnull((SELECT Vta2 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                    isnull((SELECT Vta1 FROM @Temptable WHERE ItemCode = T0.ItemCode),0))/12 )  [Promedio Mensual]
                FROM OITM T0, OITB T1
                WHERE T0.ItmsGrpCod = T1.ItmsGrpCod
                AND T1.ItmsGrpCod = 125
                AND T0.[validFor] = 'Y'
            """
            
            # Usar read_sql que maneja automáticamente las columnas
            model = pd.read_sql(consulta, conn)
            print(f"✅ Datos obtenidos correctamente. Forma: {model.shape}")
            return model
        
        except Exception as e:
            print(f"❌ Error al realizar la consulta: {str(e)}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()
        
    def VentasPorMesFiltroAceitesMarca(self, conn, marca):
        try:
            consulta = f"""
            SET NOCOUNT ON;
            DECLARE @ItemCode as nvarchar(40)
            DECLARE @Vta1 as float
            DECLARE @Vta2 as float
            DECLARE @Vta3 as float
            DECLARE @Vta4 as float
            DECLARE @Vta5 as float
            DECLARE @Vta6 as float
            DECLARE @Vta7 as float
            DECLARE @Vta8 as float
            DECLARE @Vta9 as float
            DECLARE @Vta10 as float
            DECLARE @Vta11 as float
            DECLARE @Vta12 as float

            DECLARE @TempTable TABLE
            (
            ItemCode nvarchar(40),
            Vta1 float,
            Vta2 float,
            Vta3 float,
            Vta4 float,
            Vta5 float, 
            Vta6 float,
            Vta7 float,
            Vta8 float,
            Vta9 float,
            Vta10 float,
            Vta11 float,
            Vta12 float)

            INSERT @TempTable (ItemCode)
            SELECT ItemCode 
            FROM OITM
            WHERE [ItmsGrpCod] = 125
            AND ValidFor = 'Y'

            DECLARE Saldo CURSOR FOR
            SELECT T0.ItemCode, T0.Vta1, T0.Vta2, T0.Vta3, T0.Vta4, T0.Vta5, T0.Vta6, T0.Vta7, T0.Vta8, T0.Vta9, T0.Vta10, T0.Vta11, T0.Vta12
            FROM @TempTable T0

            OPEN Saldo
            FETCH NEXT FROM Saldo
            INTO @ItemCode, @Vta1, @Vta2, @Vta3, @Vta4, @Vta5, @Vta6, @Vta7, @Vta8, @Vta9, @Vta10, @Vta11, @Vta12
            WHILE @@FETCH_STATUS = 0
            BEGIN
                    UPDATE @TempTable
                    SET Vta1 = (SELECT SUM(Cantidad)
                        FROM 
                            (SELECT INV1.Quantity as Cantidad
                            FROM INV1 
                                INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 1
                                AND OINV.Canceled = 'N'
                                AND INV1.ItemCode = @ItemCode
                            UNION ALL
                            SELECT RIN1.Quantity*-1
                            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 1
                                AND ORIN.Canceled = 'N'
                                AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta2 = (SELECT SUM(Cantidad)
                        FROM 
                            (SELECT INV1.Quantity as Cantidad
                            FROM INV1 
                                INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 2
                                AND OINV.Canceled = 'N'
                                AND INV1.ItemCode = @ItemCode
                            UNION ALL
                            SELECT RIN1.Quantity*-1
                            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 2
                                AND ORIN.Canceled = 'N'
                                AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta3 = (SELECT SUM(Cantidad)
                        FROM 
                            (SELECT INV1.Quantity as Cantidad
                            FROM INV1 
                                INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 3
                                AND OINV.Canceled = 'N'
                                AND INV1.ItemCode = @ItemCode
                            UNION ALL
                            SELECT RIN1.Quantity*-1
                            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 3
                                AND ORIN.Canceled = 'N'
                                AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta4 = (SELECT SUM(Cantidad)
                        FROM 
                            (SELECT INV1.Quantity as Cantidad
                            FROM INV1 
                                INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 4
                                AND OINV.Canceled = 'N'
                                AND INV1.ItemCode = @ItemCode
                            UNION ALL
                            SELECT RIN1.Quantity*-1
                            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 4
                                AND ORIN.Canceled = 'N'
                                AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta5 = (SELECT SUM(Cantidad)
                        FROM 
                            (SELECT INV1.Quantity as Cantidad
                            FROM INV1 
                                INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 5
                                AND OINV.Canceled = 'N'
                                AND INV1.ItemCode = @ItemCode
                            UNION ALL
                            SELECT RIN1.Quantity*-1
                            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 5
                                AND ORIN.Canceled = 'N'
                                AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta6 = (SELECT SUM(Cantidad)
                        FROM 
                            (SELECT INV1.Quantity as Cantidad
                            FROM INV1 
                                INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 6
                                AND OINV.Canceled = 'N'
                                AND INV1.ItemCode = @ItemCode
                            UNION ALL
                            SELECT RIN1.Quantity*-1
                            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 6
                                AND ORIN.Canceled = 'N'
                                AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta7 = (SELECT SUM(Cantidad)
                        FROM 
                            (SELECT INV1.Quantity as Cantidad
                            FROM INV1 
                                INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 7
                                AND OINV.Canceled = 'N'
                                AND INV1.ItemCode = @ItemCode
                            UNION ALL
                            SELECT RIN1.Quantity*-1
                            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 7
                                AND ORIN.Canceled = 'N'
                                AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta8 = (SELECT SUM(Cantidad)
                        FROM 
                            (SELECT INV1.Quantity as Cantidad
                            FROM INV1 
                                INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 8
                                AND OINV.Canceled = 'N'
                                AND INV1.ItemCode = @ItemCode
                            UNION ALL
                            SELECT RIN1.Quantity*-1
                            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 8
                                AND ORIN.Canceled = 'N'
                                AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta9 = (SELECT SUM(Cantidad)
                        FROM 
                            (SELECT INV1.Quantity as Cantidad
                            FROM INV1 
                                INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 9
                                AND OINV.Canceled = 'N'
                                AND INV1.ItemCode = @ItemCode
                            UNION ALL
                            SELECT RIN1.Quantity*-1
                            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 9
                                AND ORIN.Canceled = 'N'
                                AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta10 = (SELECT SUM(Cantidad)
                        FROM 
                            (SELECT INV1.Quantity as Cantidad
                            FROM INV1 
                                INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 10
                                AND OINV.Canceled = 'N'
                                AND INV1.ItemCode = @ItemCode
                            UNION ALL
                            SELECT RIN1.Quantity*-1
                            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 10
                                AND ORIN.Canceled = 'N'
                                AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta11 = (SELECT SUM(Cantidad)
                        FROM 
                            (SELECT INV1.Quantity as Cantidad
                            FROM INV1 
                                INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 11
                                AND OINV.Canceled = 'N'
                                AND INV1.ItemCode = @ItemCode
                            UNION ALL
                            SELECT RIN1.Quantity*-1
                            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 11
                                AND ORIN.Canceled = 'N'
                                AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta12 = (SELECT SUM(Cantidad)
                        FROM 
                            (SELECT INV1.Quantity as Cantidad
                            FROM INV1 
                                INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 12
                                AND OINV.Canceled = 'N'
                                AND INV1.ItemCode = @ItemCode
                            UNION ALL
                            SELECT RIN1.Quantity*-1
                            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 12
                                AND ORIN.Canceled = 'N'
                                AND RIN1.ItemCode = @ItemCode) Ventas)

            WHERE ItemCode = @ItemCode
            FETCH NEXT FROM Saldo
            INTO @ItemCode, @Vta1, @Vta2, @Vta3, @Vta4, @Vta5, @Vta6, @Vta7, @Vta8, @Vta9, @Vta10, @Vta11, @Vta12 
            END
            CLOSE Saldo
            DEALLOCATE Saldo

            /************************************************************************************/
            declare @GroupCode as NVARCHAR(150)
            set @GroupCode = 125

            SELECT T0.[ItemCode]
                , T0.[ItemName]
                , T0.[OnHand]
                , T0.[IsCommited]
                , T0.[OnOrder]
                , ISNULL((SELECT sum(T1.[Quantity]) 
                FROM OPQT OFERTA INNER JOIN PQT1 T1 ON OFERTA.DocEntry = T1.DocEntry 
                WHERE T1.[LineStatus] = 'O' AND T1.ItemCode=T0.ItemCode GROUP BY T1.[ItemCode]), 0.0) as [Pedido]
                ,  ISNULL( T0.[OnHand]+ T0.[OnOrder]-T0.[IsCommited] + ISNULL(ISNULL((SELECT sum(T1.[Quantity]) 
                FROM OPQT OFERTA INNER JOIN PQT1 T1 ON OFERTA.DocEntry = T1.DocEntry 
                WHERE T1.[LineStatus] = 'O' AND T1.ItemCode=T0.ItemCode GROUP BY T1.[ItemCode]), 0.0), 0.0), 0.0) [Total]
                , isnull((SELECT Vta12 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '1'
                , isnull((SELECT Vta11 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '2'
                , isnull((SELECT Vta10 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '3'
                , isnull((SELECT Vta9 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '4'
                , isnull((SELECT Vta8 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '5'
                , isnull((SELECT Vta7 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '6'
                , isnull((SELECT Vta6 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '7'
                , isnull((SELECT Vta5 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '8'
                , isnull((SELECT Vta4 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '9'
                , isnull((SELECT Vta3 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '10'
                , isnull((SELECT Vta2 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '11'
                , isnull((SELECT Vta1 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) AS '12'
                , ((isnull((SELECT Vta12 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                isnull((SELECT Vta11 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                isnull((SELECT Vta10 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                isnull((SELECT Vta9 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                isnull((SELECT Vta8 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                isnull((SELECT Vta7 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                isnull((SELECT Vta6 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                isnull((SELECT Vta5 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                isnull((SELECT Vta4 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                isnull((SELECT Vta3 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                isnull((SELECT Vta2 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
                isnull((SELECT Vta1 FROM @Temptable WHERE ItemCode = T0.ItemCode),0))/12 )  [Promedio Mensual]
            FROM OITM T0, OITB T1
            WHERE T0.ItmsGrpCod = T1.ItmsGrpCod
            AND T1.ItmsGrpCod = 125
            AND T0.[validFor] = 'Y'
            AND T0.ItemName LIKE '%{marca}%'
            """
            
            # Usar read_sql que maneja automáticamente las columnas
            model = pd.read_sql(consulta, conn)
            print(f"✅ Datos obtenidos correctamente para la marca '{marca}'. Forma: {model.shape}")
            return model
        
        except Exception as e:
            print(f"❌ Error al realizar la consulta: {str(e)}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()
    def AnalisisInventarioLlantas(self, conn):
        try:
            consulta = """SET NOCOUNT ON;
            /* VENTAS DE LOS ULTIMOS 12 MESES*/
            DECLARE @FechaFinal date = DATEFROMPARTS(YEAR(GETDATE()), MONTH(GETDATE()), 1);
            DECLARE @ItemCode as nvarchar(40)
            DECLARE @Vta1 as float
            DECLARE @Vta2 as float
            DECLARE @Vta3 as float
            DECLARE @Vta4 as float
            DECLARE @Vta5 as float
            DECLARE @Vta6 as float
            DECLARE @Vta7 as float
            DECLARE @Vta8 as float
            DECLARE @Vta9 as float
            DECLARE @Vta10 as float
            DECLARE @Vta11 as float
            DECLARE @Vta12 as float
            DECLARE @TempTable TABLE
            (
            ItemCode nvarchar(40),
            Vta1 float,
            Vta2 float,
            Vta3 float,
            Vta4 float,
            Vta5 float,
            Vta6 float,
            Vta7 float,
            Vta8 float,
            Vta9 float,
            Vta10 float,
            Vta11 float,
            Vta12 float)
            INSERT @TempTable (ItemCode)
            SELECT ItemCode
            FROM OITM
            WHERE [ItmsGrpCod] = 110
            AND ValidFor = 'Y'
            DECLARE Saldo CURSOR FOR
            SELECT T0.ItemCode, T0.Vta1, T0.Vta2, T0.Vta3, T0.Vta4, T0.Vta5, T0.Vta6, T0.Vta7,
            T0.Vta8, T0.Vta9, T0.Vta10, T0.Vta11, T0.Vta12
            FROM @TempTable T0
            OPEN Saldo
            FETCH NEXT FROM Saldo
            INTO @ItemCode, @Vta1, @Vta2, @Vta3, @Vta4, @Vta5, @Vta6, @Vta7, @Vta8, @Vta9,
            @Vta10, @Vta11, @Vta12
            WHILE @@FETCH_STATUS = 0
            BEGIN
            UPDATE @TempTable
            SET Vta1 = (SELECT SUM(Cantidad)
            FROM
            (SELECT INV1.Quantity as Cantidad
            FROM INV1
            INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 1
            AND OINV.Canceled = 'N'
            AND INV1.ItemCode = @ItemCode
            UNION ALL
            SELECT RIN1.Quantity*-1
            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 1
            AND ORIN.Canceled = 'N'
            AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta2 = (SELECT SUM(Cantidad)
            FROM
            (SELECT INV1.Quantity as Cantidad
            FROM INV1
            INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 2
            AND OINV.Canceled = 'N'
            AND INV1.ItemCode = @ItemCode
            UNION ALL
            SELECT RIN1.Quantity*-1
            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 2
            AND ORIN.Canceled = 'N'
            AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta3 = (SELECT SUM(Cantidad)
            FROM
            (SELECT INV1.Quantity as Cantidad
            FROM INV1
            INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 3
            AND OINV.Canceled = 'N'
            AND INV1.ItemCode = @ItemCode
            UNION ALL
            SELECT RIN1.Quantity*-1
            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 3
            AND ORIN.Canceled = 'N'
            AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta4 = (SELECT SUM(Cantidad)
            FROM
            (SELECT INV1.Quantity as Cantidad
            FROM INV1
            INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 4
            AND OINV.Canceled = 'N'
            AND INV1.ItemCode = @ItemCode
            UNION ALL
            SELECT RIN1.Quantity*-1
            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 4
            AND ORIN.Canceled = 'N'
            AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta5 = (SELECT SUM(Cantidad)
            FROM
            (SELECT INV1.Quantity as Cantidad
            FROM INV1
            INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 5
            AND OINV.Canceled = 'N'
            AND INV1.ItemCode = @ItemCode
            UNION ALL
            SELECT RIN1.Quantity*-1
            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 5
            AND ORIN.Canceled = 'N'
            AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta6 = (SELECT SUM(Cantidad)
            FROM
            (SELECT INV1.Quantity as Cantidad
            FROM INV1
            INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 6
            AND OINV.Canceled = 'N'
            AND INV1.ItemCode = @ItemCode
            UNION ALL
            SELECT RIN1.Quantity*-1
            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 6
            AND ORIN.Canceled = 'N'
            AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta7 = (SELECT SUM(Cantidad)
            FROM
            (SELECT INV1.Quantity as Cantidad
            FROM INV1
            INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 7
            AND OINV.Canceled = 'N'
            AND INV1.ItemCode = @ItemCode
            UNION ALL
            SELECT RIN1.Quantity*-1
            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 7
            AND ORIN.Canceled = 'N'
            AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta8 = (SELECT SUM(Cantidad)
            FROM
            (SELECT INV1.Quantity as Cantidad
            FROM INV1
            INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 8
            AND OINV.Canceled = 'N'
            AND INV1.ItemCode = @ItemCode
            UNION ALL
            SELECT RIN1.Quantity*-1
            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 8
            AND ORIN.Canceled = 'N'
            AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta9 = (SELECT SUM(Cantidad)
            FROM
            (SELECT INV1.Quantity as Cantidad
            FROM INV1
            INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 9
            AND OINV.Canceled = 'N'
            AND INV1.ItemCode = @ItemCode
            UNION ALL
            SELECT RIN1.Quantity*-1
            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 9
            AND ORIN.Canceled = 'N'
            AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta10 = (SELECT SUM(Cantidad)
            FROM
            (SELECT INV1.Quantity as Cantidad
            FROM INV1
            INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 10
            AND OINV.Canceled = 'N'
            AND INV1.ItemCode = @ItemCode
            UNION ALL
            SELECT RIN1.Quantity*-1
            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 10
            AND ORIN.Canceled = 'N'
            AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta11 = (SELECT SUM(Cantidad)
            FROM
            (SELECT INV1.Quantity as Cantidad
            FROM INV1
            INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 11
            AND OINV.Canceled = 'N'
            AND INV1.ItemCode = @ItemCode
            UNION ALL
            SELECT RIN1.Quantity*-1
            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 11
            AND ORIN.Canceled = 'N'
            AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta12 = (SELECT SUM(Cantidad)
            FROM
            (SELECT INV1.Quantity as Cantidad
            FROM INV1
            INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 12
            AND OINV.Canceled = 'N'
            AND INV1.ItemCode = @ItemCode
            UNION ALL
            SELECT RIN1.Quantity*-1
            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 12
            AND ORIN.Canceled = 'N'
            AND RIN1.ItemCode = @ItemCode) Ventas)
            WHERE ItemCode = @ItemCode
            FETCH NEXT FROM Saldo
            INTO @ItemCode, @Vta1, @Vta2, @Vta3, @Vta4, @Vta5, @Vta6, @Vta7, @Vta8, @Vta9,
            @Vta10, @Vta11, @Vta12
            END
            CLOSE Saldo
            DEALLOCATE Saldo

            declare @GroupCode as NVARCHAR(150)
            set @GroupCode = 110


            ;WITH VentasFinal AS (
                SELECT 
                    T0.[ItemCode]
            , T0.[ItemName]
            , T0.[SuppCatNum] as 'No. Fabricante'
            , T0.[OnHand] as [In Stock]
            , T0.[IsCommited] as [Qty Ordered by]
            , T0.[OnOrder] AS [Qty Ordered from]
            , ISNULL((SELECT sum(T1.[Quantity])
            FROM OPQT OFERTA INNER JOIN PQT1 T1 ON OFERTA.DocEntry = T1.DocEntry
            WHERE T1.[LineStatus] = 'O' AND T1.ItemCode=T0.ItemCode GROUP BY T1.
            [ItemCode]), 0.0) as [Pedido]
            , ISNULL( T0.[OnHand]+ T0.[OnOrder]-T0.[IsCommited] + ISNULL(ISNULL((SELECT
            sum(T1.[Quantity])
            FROM OPQT OFERTA INNER JOIN PQT1 T1 ON OFERTA.DocEntry = T1.DocEntry
            WHERE T1.[LineStatus] = 'O' AND T1.ItemCode=T0.ItemCode GROUP BY T1.
            [ItemCode]), 0.0), 0.0), 0.0) [Total],
                    'VENTA' AS Tipo,
                    ISNULL((SELECT Vta12 FROM @TempTable WHERE ItemCode = T0.ItemCode), 0) AS Mes_1,
                    ISNULL((SELECT Vta11 FROM @TempTable WHERE ItemCode = T0.ItemCode), 0) AS Mes_2,
                    ISNULL((SELECT Vta10 FROM @TempTable WHERE ItemCode = T0.ItemCode), 0) AS Mes_3,
                    ISNULL((SELECT Vta9 FROM @TempTable WHERE ItemCode = T0.ItemCode), 0) AS Mes_4,
                    ISNULL((SELECT Vta8 FROM @TempTable WHERE ItemCode = T0.ItemCode), 0) AS Mes_5,
                    ISNULL((SELECT Vta7 FROM @TempTable WHERE ItemCode = T0.ItemCode), 0) AS Mes_6,
                    ISNULL((SELECT Vta6 FROM @TempTable WHERE ItemCode = T0.ItemCode), 0) AS Mes_7,
                    ISNULL((SELECT Vta5 FROM @TempTable WHERE ItemCode = T0.ItemCode), 0) AS Mes_8,
                    ISNULL((SELECT Vta4 FROM @TempTable WHERE ItemCode = T0.ItemCode), 0) AS Mes_9,
                    ISNULL((SELECT Vta3 FROM @TempTable WHERE ItemCode = T0.ItemCode), 0) AS Mes_10,
                    ISNULL((SELECT Vta2 FROM @TempTable WHERE ItemCode = T0.ItemCode), 0) AS Mes_11,
                    ISNULL((SELECT Vta1 FROM @TempTable WHERE ItemCode = T0.ItemCode), 0) AS Mes_12,
                    ((isnull((SELECT Vta12 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
            isnull((SELECT Vta11 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
            isnull((SELECT Vta10 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
            isnull((SELECT Vta9 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
            isnull((SELECT Vta8 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
            isnull((SELECT Vta7 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
            isnull((SELECT Vta6 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
            isnull((SELECT Vta5 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
            isnull((SELECT Vta4 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
            isnull((SELECT Vta3 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
            isnull((SELECT Vta2 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
            isnull((SELECT Vta1 FROM @Temptable WHERE ItemCode = T0.ItemCode),0))/12 )
            [Promedio Mensual], (
            SELECT AVG(Cantidad)
            FROM (
                SELECT INV1.Quantity as Cantidad
                FROM INV1
                INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) BETWEEN 0 AND 2
                AND OINV.Canceled = 'N'
                AND INV1.ItemCode = T0.ItemCode
                UNION ALL
                SELECT RIN1.Quantity * -1
                FROM RIN1
                INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) BETWEEN 0 AND 2
                AND ORIN.Canceled = 'N'
                AND RIN1.ItemCode = T0.ItemCode
            ) AS VM
            ) AS [Prom 3 meses]

            , (
            SELECT AVG(Cantidad)
            FROM (
                SELECT INV1.Quantity as Cantidad
                FROM INV1
                INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) BETWEEN 0 AND 5
                AND OINV.Canceled = 'N'
                AND INV1.ItemCode = T0.ItemCode
                UNION ALL
                SELECT RIN1.Quantity * -1
                FROM RIN1
                INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) BETWEEN 0 AND 5
                AND ORIN.Canceled = 'N'
                AND RIN1.ItemCode = T0.ItemCode
            ) AS VM
            ) AS [Prom 6 meses]
                FROM OITM T0
                WHERE T0.ItmsGrpCod = 110 AND T0.ValidFor = 'Y'
            ),


            MesesCalendario AS (
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
            ),
            InventarioFinal AS (
                SELECT 
                    ItemCode,
                    ItemName,
                    '0' AS [No. Fabricante],
                    '0' AS [In Stock],
                    '0' AS [Qty Ordered by],
                    '0' AS [Qty Ordered from],
                    '0' AS [Pedido],
                    '0' AS [Total],
                    'INVENTARIO' as Tipo,
                    MAX(CASE WHEN MesNum = 0 THEN InventarioAcumulado END) AS Mes_1,
                    MAX(CASE WHEN MesNum = 1 THEN InventarioAcumulado END) AS Mes_2,
                    MAX(CASE WHEN MesNum = 2 THEN InventarioAcumulado END) AS Mes_3,
                    MAX(CASE WHEN MesNum = 3 THEN InventarioAcumulado END) AS Mes_4,
                    MAX(CASE WHEN MesNum = 4 THEN InventarioAcumulado END) AS Mes_5,
                    MAX(CASE WHEN MesNum = 5 THEN InventarioAcumulado END) AS Mes_6,
                    MAX(CASE WHEN MesNum = 6 THEN InventarioAcumulado END) AS Mes_7,
                    MAX(CASE WHEN MesNum = 7 THEN InventarioAcumulado END) AS Mes_8,
                    MAX(CASE WHEN MesNum = 8 THEN InventarioAcumulado END) AS Mes_9,
                    MAX(CASE WHEN MesNum = 9 THEN InventarioAcumulado END) AS Mes_10,
                    MAX(CASE WHEN MesNum = 10 THEN InventarioAcumulado END) AS Mes_11,
                    MAX(CASE WHEN MesNum = 11 THEN InventarioAcumulado END) AS Mes_12,
                    '0' AS [Promedio Mensual],
                    '0' AS [Prom 3 meses],
                    '0' AS [Prom 6 meses]
                FROM SaldoAcumulado
                GROUP BY ItemCode, ItemName
            )

            SELECT *
            FROM (
                SELECT *, ROW_NUMBER() OVER (PARTITION BY ItemCode ORDER BY Tipo DESC) AS Orden
                FROM (
                    SELECT * FROM VentasFinal
                    UNION ALL
                    SELECT * FROM InventarioFinal
                ) AS Todo
            ) AS ResultadoFinal
            ORDER BY ItemCode, Orden;
            """
            
            # Usar read_sql que maneja automáticamente las columnas
            model = pd.read_sql(consulta, conn)
            print(f"✅ Datos obtenidos correctamente. Forma: {model.shape}")
            return model
        
        except Exception as e:
            print(f"❌ Error al realizar la consulta: {str(e)}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()
    def InventarioAceites(self, conn):
        try:
            consulta = """
            SET NOCOUNT ON;
            /* VENTAS DE LOS ULTIMOS 12 MESES*/
            DECLARE @FechaFinal date = DATEFROMPARTS(YEAR(GETDATE()), MONTH(GETDATE()), 1);
            DECLARE @ItemCode as nvarchar(40)
            DECLARE @Vta1 as float
            DECLARE @Vta2 as float
            DECLARE @Vta3 as float
            DECLARE @Vta4 as float
            DECLARE @Vta5 as float
            DECLARE @Vta6 as float
            DECLARE @Vta7 as float
            DECLARE @Vta8 as float
            DECLARE @Vta9 as float
            DECLARE @Vta10 as float
            DECLARE @Vta11 as float
            DECLARE @Vta12 as float
            DECLARE @TempTable TABLE
            (
            ItemCode nvarchar(40),
            Vta1 float,
            Vta2 float,
            Vta3 float,
            Vta4 float,
            Vta5 float,
            Vta6 float,
            Vta7 float,
            Vta8 float,
            Vta9 float,
            Vta10 float,
            Vta11 float,
            Vta12 float)
            INSERT @TempTable (ItemCode)
            SELECT ItemCode
            FROM OITM
            WHERE [ItmsGrpCod] = 125
            AND ValidFor = 'Y'
            DECLARE Saldo CURSOR FOR
            SELECT T0.ItemCode, T0.Vta1, T0.Vta2, T0.Vta3, T0.Vta4, T0.Vta5, T0.Vta6, T0.Vta7,
            T0.Vta8, T0.Vta9, T0.Vta10, T0.Vta11, T0.Vta12
            FROM @TempTable T0
            OPEN Saldo
            FETCH NEXT FROM Saldo
            INTO @ItemCode, @Vta1, @Vta2, @Vta3, @Vta4, @Vta5, @Vta6, @Vta7, @Vta8, @Vta9,
            @Vta10, @Vta11, @Vta12
            WHILE @@FETCH_STATUS = 0
            BEGIN
            UPDATE @TempTable
            SET Vta1 = (SELECT SUM(Cantidad)
            FROM
            (SELECT INV1.Quantity as Cantidad
            FROM INV1
            INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 1
            AND OINV.Canceled = 'N'
            AND INV1.ItemCode = @ItemCode
            UNION ALL
            SELECT RIN1.Quantity*-1
            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 1
            AND ORIN.Canceled = 'N'
            AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta2 = (SELECT SUM(Cantidad)
            FROM
            (SELECT INV1.Quantity as Cantidad
            FROM INV1
            INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 2
            AND OINV.Canceled = 'N'
            AND INV1.ItemCode = @ItemCode
            UNION ALL
            SELECT RIN1.Quantity*-1
            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 2
            AND ORIN.Canceled = 'N'
            AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta3 = (SELECT SUM(Cantidad)
            FROM
            (SELECT INV1.Quantity as Cantidad
            FROM INV1
            INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 3
            AND OINV.Canceled = 'N'
            AND INV1.ItemCode = @ItemCode
            UNION ALL
            SELECT RIN1.Quantity*-1
            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 3
            AND ORIN.Canceled = 'N'
            AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta4 = (SELECT SUM(Cantidad)
            FROM
            (SELECT INV1.Quantity as Cantidad
            FROM INV1
            INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 4
            AND OINV.Canceled = 'N'
            AND INV1.ItemCode = @ItemCode
            UNION ALL
            SELECT RIN1.Quantity*-1
            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 4
            AND ORIN.Canceled = 'N'
            AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta5 = (SELECT SUM(Cantidad)
            FROM
            (SELECT INV1.Quantity as Cantidad
            FROM INV1
            INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 5
            AND OINV.Canceled = 'N'
            AND INV1.ItemCode = @ItemCode
            UNION ALL
            SELECT RIN1.Quantity*-1
            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 5
            AND ORIN.Canceled = 'N'
            AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta6 = (SELECT SUM(Cantidad)
            FROM
            (SELECT INV1.Quantity as Cantidad
            FROM INV1
            INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 6
            AND OINV.Canceled = 'N'
            AND INV1.ItemCode = @ItemCode
            UNION ALL
            SELECT RIN1.Quantity*-1
            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 6
            AND ORIN.Canceled = 'N'
            AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta7 = (SELECT SUM(Cantidad)
            FROM
            (SELECT INV1.Quantity as Cantidad
            FROM INV1
            INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 7
            AND OINV.Canceled = 'N'
            AND INV1.ItemCode = @ItemCode
            UNION ALL
            SELECT RIN1.Quantity*-1
            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 7
            AND ORIN.Canceled = 'N'
            AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta8 = (SELECT SUM(Cantidad)
            FROM
            (SELECT INV1.Quantity as Cantidad
            FROM INV1
            INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 8
            AND OINV.Canceled = 'N'
            AND INV1.ItemCode = @ItemCode
            UNION ALL
            SELECT RIN1.Quantity*-1
            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 8
            AND ORIN.Canceled = 'N'
            AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta9 = (SELECT SUM(Cantidad)
            FROM
            (SELECT INV1.Quantity as Cantidad
            FROM INV1
            INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 9
            AND OINV.Canceled = 'N'
            AND INV1.ItemCode = @ItemCode
            UNION ALL
            SELECT RIN1.Quantity*-1
            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 9
            AND ORIN.Canceled = 'N'
            AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta10 = (SELECT SUM(Cantidad)
            FROM
            (SELECT INV1.Quantity as Cantidad
            FROM INV1
            INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 10
            AND OINV.Canceled = 'N'
            AND INV1.ItemCode = @ItemCode
            UNION ALL
            SELECT RIN1.Quantity*-1
            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 10
            AND ORIN.Canceled = 'N'
            AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta11 = (SELECT SUM(Cantidad)
            FROM
            (SELECT INV1.Quantity as Cantidad
            FROM INV1
            INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 11
            AND OINV.Canceled = 'N'
            AND INV1.ItemCode = @ItemCode
            UNION ALL
            SELECT RIN1.Quantity*-1
            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 11
            AND ORIN.Canceled = 'N'
            AND RIN1.ItemCode = @ItemCode) Ventas)
            , Vta12 = (SELECT SUM(Cantidad)
            FROM
            (SELECT INV1.Quantity as Cantidad
            FROM INV1
            INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
            WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) = 12
            AND OINV.Canceled = 'N'
            AND INV1.ItemCode = @ItemCode
            UNION ALL
            SELECT RIN1.Quantity*-1
            FROM RIN1 INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
            WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) = 12
            AND ORIN.Canceled = 'N'
            AND RIN1.ItemCode = @ItemCode) Ventas)
            WHERE ItemCode = @ItemCode
            FETCH NEXT FROM Saldo
            INTO @ItemCode, @Vta1, @Vta2, @Vta3, @Vta4, @Vta5, @Vta6, @Vta7, @Vta8, @Vta9,
            @Vta10, @Vta11, @Vta12
            END
            CLOSE Saldo
            DEALLOCATE Saldo

            declare @GroupCode as NVARCHAR(150)
            set @GroupCode = 125


            ;WITH VentasFinal AS (
                SELECT 
                    T0.[ItemCode]
            , T0.[ItemName]
            , T0.[SuppCatNum] as 'No. Fabricante'
            , T0.[OnHand] as [In Stock]
            , T0.[IsCommited] as [Qty Ordered by]
            , T0.[OnOrder] AS [Qty Ordered from]
            , ISNULL((SELECT sum(T1.[Quantity])
            FROM OPQT OFERTA INNER JOIN PQT1 T1 ON OFERTA.DocEntry = T1.DocEntry
            WHERE T1.[LineStatus] = 'O' AND T1.ItemCode=T0.ItemCode GROUP BY T1.
            [ItemCode]), 0.0) as [Pedido]
            , ISNULL( T0.[OnHand]+ T0.[OnOrder]-T0.[IsCommited] + ISNULL(ISNULL((SELECT
            sum(T1.[Quantity])
            FROM OPQT OFERTA INNER JOIN PQT1 T1 ON OFERTA.DocEntry = T1.DocEntry
            WHERE T1.[LineStatus] = 'O' AND T1.ItemCode=T0.ItemCode GROUP BY T1.
            [ItemCode]), 0.0), 0.0), 0.0) [Total],
                    'VENTA' AS Tipo,
                    ISNULL((SELECT Vta12 FROM @TempTable WHERE ItemCode = T0.ItemCode), 0) AS Mes_1,
                    ISNULL((SELECT Vta11 FROM @TempTable WHERE ItemCode = T0.ItemCode), 0) AS Mes_2,
                    ISNULL((SELECT Vta10 FROM @TempTable WHERE ItemCode = T0.ItemCode), 0) AS Mes_3,
                    ISNULL((SELECT Vta9 FROM @TempTable WHERE ItemCode = T0.ItemCode), 0) AS Mes_4,
                    ISNULL((SELECT Vta8 FROM @TempTable WHERE ItemCode = T0.ItemCode), 0) AS Mes_5,
                    ISNULL((SELECT Vta7 FROM @TempTable WHERE ItemCode = T0.ItemCode), 0) AS Mes_6,
                    ISNULL((SELECT Vta6 FROM @TempTable WHERE ItemCode = T0.ItemCode), 0) AS Mes_7,
                    ISNULL((SELECT Vta5 FROM @TempTable WHERE ItemCode = T0.ItemCode), 0) AS Mes_8,
                    ISNULL((SELECT Vta4 FROM @TempTable WHERE ItemCode = T0.ItemCode), 0) AS Mes_9,
                    ISNULL((SELECT Vta3 FROM @TempTable WHERE ItemCode = T0.ItemCode), 0) AS Mes_10,
                    ISNULL((SELECT Vta2 FROM @TempTable WHERE ItemCode = T0.ItemCode), 0) AS Mes_11,
                    ISNULL((SELECT Vta1 FROM @TempTable WHERE ItemCode = T0.ItemCode), 0) AS Mes_12,
                    ((isnull((SELECT Vta12 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
            isnull((SELECT Vta11 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
            isnull((SELECT Vta10 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
            isnull((SELECT Vta9 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
            isnull((SELECT Vta8 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
            isnull((SELECT Vta7 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
            isnull((SELECT Vta6 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
            isnull((SELECT Vta5 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
            isnull((SELECT Vta4 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
            isnull((SELECT Vta3 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
            isnull((SELECT Vta2 FROM @Temptable WHERE ItemCode = T0.ItemCode),0) +
            isnull((SELECT Vta1 FROM @Temptable WHERE ItemCode = T0.ItemCode),0))/12 )
            [Promedio Mensual], (
            SELECT AVG(Cantidad)
            FROM (
                SELECT INV1.Quantity as Cantidad
                FROM INV1
                INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) BETWEEN 0 AND 2
                AND OINV.Canceled = 'N'
                AND INV1.ItemCode = T0.ItemCode
                UNION ALL
                SELECT RIN1.Quantity * -1
                FROM RIN1
                INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) BETWEEN 0 AND 2
                AND ORIN.Canceled = 'N'
                AND RIN1.ItemCode = T0.ItemCode
            ) AS VM
            ) AS [Prom 3 meses]

            , (
            SELECT AVG(Cantidad)
            FROM (
                SELECT INV1.Quantity as Cantidad
                FROM INV1
                INNER JOIN OINV ON INV1.DocEntry = OINV.DocEntry
                WHERE DATEDIFF(month, OINV.DocDate, GETDATE()) BETWEEN 0 AND 5
                AND OINV.Canceled = 'N'
                AND INV1.ItemCode = T0.ItemCode
                UNION ALL
                SELECT RIN1.Quantity * -1
                FROM RIN1
                INNER JOIN ORIN ON RIN1.DocEntry = ORIN.DocEntry
                WHERE DATEDIFF(month, ORIN.DocDate, GETDATE()) BETWEEN 0 AND 5
                AND ORIN.Canceled = 'N'
                AND RIN1.ItemCode = T0.ItemCode
            ) AS VM
            ) AS [Prom 6 meses]
                FROM OITM T0
                WHERE T0.ItmsGrpCod = 125 AND T0.ValidFor = 'Y'
            ),


            MesesCalendario AS (
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
                AND T1.ItmsGrpCod = 125
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
            ),
            InventarioFinal AS (
                SELECT 
                    ItemCode,
                    ItemName,
                    '0' AS [No. Fabricante],
                    '0' AS [In Stock],
                    '0' AS [Qty Ordered by],
                    '0' AS [Qty Ordered from],
                    '0' AS [Pedido],
                    '0' AS [Total],
                    'INVENTARIO' as Tipo,
                    MAX(CASE WHEN MesNum = 0 THEN InventarioAcumulado END) AS Mes_1,
                    MAX(CASE WHEN MesNum = 1 THEN InventarioAcumulado END) AS Mes_2,
                    MAX(CASE WHEN MesNum = 2 THEN InventarioAcumulado END) AS Mes_3,
                    MAX(CASE WHEN MesNum = 3 THEN InventarioAcumulado END) AS Mes_4,
                    MAX(CASE WHEN MesNum = 4 THEN InventarioAcumulado END) AS Mes_5,
                    MAX(CASE WHEN MesNum = 5 THEN InventarioAcumulado END) AS Mes_6,
                    MAX(CASE WHEN MesNum = 6 THEN InventarioAcumulado END) AS Mes_7,
                    MAX(CASE WHEN MesNum = 7 THEN InventarioAcumulado END) AS Mes_8,
                    MAX(CASE WHEN MesNum = 8 THEN InventarioAcumulado END) AS Mes_9,
                    MAX(CASE WHEN MesNum = 9 THEN InventarioAcumulado END) AS Mes_10,
                    MAX(CASE WHEN MesNum = 10 THEN InventarioAcumulado END) AS Mes_11,
                    MAX(CASE WHEN MesNum = 11 THEN InventarioAcumulado END) AS Mes_12,
                    '0' AS [Promedio Mensual],
                    '0' AS [Prom 3 meses],
                    '0' AS [Prom 6 meses]
                FROM SaldoAcumulado
                GROUP BY ItemCode, ItemName
            )



            -- Suponiendo que ya tienes cargadas las tablas temporales o subconsultas necesarias como @TempTable para ventas y los CTEs para inventario...




            SELECT *
            FROM (
                SELECT *, ROW_NUMBER() OVER (PARTITION BY ItemCode ORDER BY Tipo DESC) AS Orden
                FROM (
                    SELECT * FROM VentasFinal
                    UNION ALL
                    SELECT * FROM InventarioFinal
                ) AS Todo
            ) AS ResultadoFinal
            ORDER BY ItemCode, Orden;
            """
            
            # Usar read_sql que maneja automáticamente las columnas
            model = pd.read_sql(consulta, conn)
            print(f"✅ Datos obtenidos correctamente. Forma: {model.shape}")
            return model
        
        except Exception as e:
            print(f"❌ Error al realizar la consulta: {str(e)}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()


