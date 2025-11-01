from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QStatusBar, 
    QApplication, QInputDialog
)
from PySide6.QtCore import QTimer, Slot
import time
import pandas as pd  # 👈 necesario para leer CSV
import os
from componentes.tabla import TablaDatos
from componentes.boton import BotonReporte
from componentes.navbar import NavBar
from ConexionSql.conexion import conectorcito
from ConexionSql.SQLManagement import SQLManagement
from componentes.excel import exportar_excel_bonito
from PySide6.QtWidgets import QMessageBox




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Ventas")
        self.resize(1000, 600)
        self.conn = None
        self.manager = SQLManagement()
        self.initialize_connection()
        self.setup_ui()
        self.connect_signals()
        self.ultimo_dataframe = None
        self.data_original = None  # 👈 esto es nuevo



    def initialize_connection(self):
        try:
            self.conn = conectorcito()
            print("✅ ¡Conexión exitosa!" if self.conn else "❌ No se pudo conectar a la BD")
        except Exception as e:
            print(f"❌ Error en conexión: {str(e)}")

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)

        self.navbar = NavBar()
        self.main_layout.addWidget(self.navbar)

        self.content_area = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_area.setLayout(self.content_layout)

        self.main_layout.addWidget(self.content_area, stretch=1)

        self.reporte_sin_filtros_llantas_btn = BotonReporte("Reporte Sin Filtros - Llantas", self.LlenarLlantas)
        self.reporte_con_filtros_llantas_btn = BotonReporte("Reporte Con Filtros por Marca - Llantas", self.LlenarLlantasConFiltros)
        self.reporte_sin_filtros_aceites_btn = BotonReporte("Reporte Sin Filtros - Aceites", self.LlenarAceitesSinFiltros)
        self.reporte_con_filtros_aceites_btn = BotonReporte("Reporte Con Filtros por Marca - Aceites", self.LlenarAceitesConFiltros)
        self.inventario_llantas_btn = BotonReporte("Llantas", self.mostrar_inventario_llantas)
        self.inventario_aceites_btn = BotonReporte("Aceites", self.mostrar_inventario_aceites)

        # Ocúltalos por defecto
        self.inventario_llantas_btn.hide()
        self.inventario_aceites_btn.hide()
        self.reporte_con_filtros_llantas_btn.hide()
        self.reporte_con_filtros_aceites_btn.hide()
        self.reporte_sin_filtros_llantas_btn.hide()
        self.reporte_sin_filtros_aceites_btn.hide()

        self.main_layout.addWidget(self.inventario_llantas_btn)
        self.main_layout.addWidget(self.inventario_aceites_btn)

        for btn in [self.reporte_sin_filtros_llantas_btn, self.reporte_con_filtros_llantas_btn,
                    self.reporte_sin_filtros_aceites_btn, self.reporte_con_filtros_aceites_btn]:
            self.main_layout.addWidget(btn)

        self.status_bar = QStatusBar()
        #esto es para los botones de prediccion
        self.setStatusBar(self.status_bar)
        self.prediccion_llantas_btn = BotonReporte("Llantas", self.mostrar_prediccion_llantas)
        self.prediccion_aceites_btn = BotonReporte("Aceites", self.mostrar_prediccion_aceites)

        self.prediccion_llantas_btn.hide()
        self.prediccion_aceites_btn.hide()

        self.main_layout.addWidget(self.prediccion_llantas_btn)
        self.main_layout.addWidget(self.prediccion_aceites_btn)
        # Botones para reporte de pedidos
        self.reporte_pedido_llantas_btn = BotonReporte("Llantas", self.mostrar_reporte_pedido_llantas)
        self.reporte_pedido_aceites_btn = BotonReporte("Aceites", self.mostrar_reporte_pedido_aceites)

        self.reporte_pedido_llantas_btn.hide()
        self.reporte_pedido_aceites_btn.hide()

        self.main_layout.addWidget(self.reporte_pedido_llantas_btn)
        self.main_layout.addWidget(self.reporte_pedido_aceites_btn)

    
    def mostrar_botones_prediccion_demanda(self):
        self.ocultar_todos_los_botones()
        self.prediccion_llantas_btn.show()
        self.prediccion_aceites_btn.show()



    def connect_signals(self):
        self.navbar.home_clicked.connect(self.show_report_buttons_llantas)
        self.navbar.aceites_clicked.connect(self.show_report_buttons_aceites)
        self.navbar.inventario_clicked.connect(self.mostrar_botones_inventario)
        self.navbar.services_clicked.connect(self.mostrar_prediccion_demanda_futura)  # ✅ Nuevo
        self.navbar.services_clicked.connect(self.mostrar_botones_prediccion_demanda)
        self.navbar.contact_clicked.connect(self.mostrar_botones_reporte_pedido)

    def mostrar_botones_reporte_pedido(self):
        self.ocultar_todos_los_botones()
        self.reporte_pedido_llantas_btn.show()
        self.reporte_pedido_aceites_btn.show()



    def ocultar_todos_los_botones(self):
        self.reporte_sin_filtros_llantas_btn.hide()
        self.reporte_con_filtros_llantas_btn.hide()
        self.reporte_sin_filtros_aceites_btn.hide()
        self.reporte_con_filtros_aceites_btn.hide()
        self.inventario_llantas_btn.hide()
        self.inventario_aceites_btn.hide()
        self.prediccion_llantas_btn.hide()
        self.prediccion_aceites_btn.hide()
        self.reporte_pedido_llantas_btn.hide()
        self.reporte_pedido_aceites_btn.hide()


    def mostrar_botones_inventario(self):
        self.ocultar_todos_los_botones()
        self.inventario_llantas_btn.show()
        self.inventario_aceites_btn.show()

    def show_report_buttons_llantas(self):
        self.ocultar_todos_los_botones()
        self.reporte_sin_filtros_llantas_btn.show()
        #self.reporte_con_filtros_llantas_btn.show()

    def show_report_buttons_aceites(self):
        self.ocultar_todos_los_botones()
        self.reporte_sin_filtros_aceites_btn.show()
        # self.reporte_con_filtros_aceites_btn.show()
    
    def mostrar_inventario_llantas(self):
        self.status_bar.showMessage("Cargando inventario de llantas...")
        QApplication.processEvents()
        QTimer.singleShot(0, self.async_cargar_inventario_llantas)
    def mostrar_inventario_aceites(self):
        self.status_bar.showMessage("Cargando inventario de aceites...")
        QApplication.processEvents()
        QTimer.singleShot(0, self.async_cargar_inventario_aceites)

    def LlenarLlantas(self):
        self.status_bar.showMessage("Cargando datos sin filtros de llantas...")
        QApplication.processEvents()
        if not self.conn:
            self.status_bar.showMessage("Error: No hay conexión a BD", 5000)
            return
        QTimer.singleShot(0, self.async_load_data_llantas)

    def LlenarLlantasConFiltros(self):
        marca, ok = QInputDialog.getText(self, "Filtro por Marca - Llantas", "Ingrese la marca:")
        if ok and marca:
            self.status_bar.showMessage(f"Cargando llantas para '{marca}'...")
            QApplication.processEvents()
            if not self.conn:
                self.status_bar.showMessage("Error: No hay conexión a BD", 5000)
                return
            QTimer.singleShot(0, lambda: self.async_load_filtered_data_llantas(marca))

    def LlenarAceitesSinFiltros(self):
        self.status_bar.showMessage("Cargando datos sin filtros de aceites...")
        QApplication.processEvents()
        if not self.conn:
            self.status_bar.showMessage("Error: No hay conexión a BD", 5000)
            return
        QTimer.singleShot(0, self.async_load_data_aceites)

    def LlenarAceitesConFiltros(self):
        marca, ok = QInputDialog.getText(self, "Filtro por Marca - Aceites", "Ingrese la marca:")
        if ok and marca:
            self.status_bar.showMessage(f"Cargando aceites para '{marca}'...")
            QApplication.processEvents()
            if not self.conn:
                self.status_bar.showMessage("Error: No hay conexión a BD", 5000)
                return
            QTimer.singleShot(0, lambda: self.async_load_filtered_data_aceites(marca))

    def clear_content(self):
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    
    def display_data(self, df):
        self.clear_content()

        botones_widget = QWidget()
        botones_layout = QVBoxLayout()
        botones_layout.setSpacing(10)
        botones_layout.setContentsMargins(10, 10, 10, 10)
        botones_widget.setLayout(botones_layout)

        btn_exportar = BotonReporte("Exportar a Excel", self.exportar_excel_actual)
        btn_filtrar = BotonReporte("Filtrar por Marca", self.filtrar_por_marca2)

        botones_layout.addWidget(btn_exportar)
        botones_layout.addWidget(btn_filtrar)

        self.content_layout.addWidget(botones_widget)

        # ✅ Reiniciar índice antes de mostrar
        df_reset = df.reset_index(drop=True)

        tabla = TablaDatos(df_reset)
        self.tabla_actual = tabla
        self.content_layout.addWidget(tabla)
        btn_exportar.setFixedHeight(40)
        btn_filtrar.setFixedHeight(40)

        self.data_original = df.copy()
        self.ultimo_dataframe = df_reset  # 🔁 usar también la versión sin índices raros

        self.status_bar.showMessage("Datos cargados correctamente", 3000)


#aca es lo de las predicciones
    @Slot()
    def mostrar_prediccion_demanda_futura(self):  # ✅ NUEVO
        try:
            ruta_csv = os.path.join("ConexionSql", "predicciones_llantas_final.csv")
            df = pd.read_csv(ruta_csv)
            self.display_data(df)
            print("📊 Predicción de demanda futura cargada con éxito.")
        except FileNotFoundError:
            self.status_bar.showMessage("Archivo predicciones_llantas_final.csv no encontrado.", 5000)
        except Exception as e:
            self.status_bar.showMessage(f"Error al cargar predicción: {e}", 5000)

    @Slot()
    def mostrar_prediccion_llantas(self):
        try:
            ruta = os.path.join("ConexionSql", "predicciones_llantas_final.csv")
            df = pd.read_csv(ruta)
            self.display_data(df)
            print("📊 Cargado: predicciones_llantas_final.csv")
        except Exception as e:
            self.status_bar.showMessage(f"Error cargando predicción de llantas: {e}", 5000)

    @Slot()
    def mostrar_prediccion_aceites(self):
        try:
            ruta = os.path.join("ConexionSql", "predicciones_aceites_final.csv")
            df = pd.read_csv(ruta)
            self.display_data(df)
            print("📊 Cargado: predicciones_aceites_final.csv")
        except Exception as e:
            self.status_bar.showMessage(f"Error cargando predicción de aceites: {e}", 5000)



    @Slot()
    def async_cargar_inventario_llantas(self):
        try:
            start = time.time()
            df = self.manager.AnalisisInventarioLlantas(self.conn)
            elapsed = time.time() - start
            print(f"⏱ Tiempo carga inventario llantas: {elapsed:.2f}s")
            self.display_data(df)
        except Exception as e:
            self.status_bar.showMessage("Error al cargar inventario de llantas", 5000)

    @Slot()
    def async_load_data_llantas(self):
        try:
            start = time.time()
            df = self.manager.VentasPorMesSinFiltroLlantas(self.conn)
            elapsed = time.time() - start
            print(f"⏱ Tiempo carga llantas sin filtro: {elapsed:.2f}s")
            self.display_data(df)
        except Exception as e:
            self.status_bar.showMessage("Error al cargar datos de llantas", 5000)

    @Slot()
    def async_load_filtered_data_llantas(self, marca):
        try:
            start = time.time()
            df = self.manager.VentasPorMesFiltroLlantasMarca(self.conn, marca)
            elapsed = time.time() - start
            print(f"⏱ Tiempo carga llantas con filtro '{marca}': {elapsed:.2f}s")
            self.display_data(df)
        except Exception as e:
            self.status_bar.showMessage(f"Error al cargar llantas para '{marca}'", 5000)

    @Slot()
    def async_load_data_aceites(self):
        try:
            start = time.time()
            df = self.manager.VentasPorMesSinFiltroAceites(self.conn)
            elapsed = time.time() - start
            print(f"⏱ Tiempo carga aceites sin filtro: {elapsed:.2f}s")
            self.display_data(df)
        except Exception as e:
            self.status_bar.showMessage("Error al cargar datos de aceites", 5000)

    @Slot()
    def async_load_filtered_data_aceites(self, marca):
        try:
            start = time.time()
            df = self.manager.VentasPorMesFiltroAceitesMarca(self.conn, marca)
            elapsed = time.time() - start
            print(f"⏱ Tiempo carga aceites con filtro '{marca}': {elapsed:.2f}s")
            self.display_data(df)
        except Exception as e:
            self.status_bar.showMessage(f"Error al cargar aceites para '{marca}'", 5000)

    @Slot()
    def async_cargar_inventario_aceites(self):
        try:
            start = time.time()
            df = self.manager.InventarioAceites(self.conn)
            elapsed = time.time() - start
            print(f"⏱ Tiempo carga inventario aceites: {elapsed:.2f}s")
            self.display_data(df)
        except Exception as e:
            self.status_bar.showMessage("Error al cargar inventario de aceites", 5000)

    #aca es lo de reportes
    @Slot()
    def mostrar_reporte_pedido_llantas(self):
        try:
            df = pd.read_csv("ConexionSql/llantas_con_demanda_y_pedido.csv")
            df = df.fillna(0)

            # 👉 Redondear y convertir a enteros
            float_cols = df.select_dtypes(include=['float']).columns
            df[float_cols] = df[float_cols].round(0).astype(int)

            self.display_data(df)
            print("📊 Cargado: llantas_con_demanda_y_pedido.csv")
        except Exception as e:
            self.status_bar.showMessage(f"Error al cargar reporte de pedido de llantas: {e}", 5000)

    @Slot()
    def mostrar_reporte_pedido_aceites(self):
        try:
            df = pd.read_csv("ConexionSql/aceites_con_demanda_y_pedido.csv")
            df = df.fillna(0)

            # 👉 Redondear y convertir a enteros
            float_cols = df.select_dtypes(include=['float']).columns
            df[float_cols] = df[float_cols].round(0).astype(int)

            self.display_data(df)
            print("📊 Cargado: aceites_con_demanda_y_pedido.csv")
        except Exception as e:
            self.status_bar.showMessage(f"Error al cargar reporte de pedido de aceites: {e}", 5000)

    @Slot()
    def exportar_excel_actual(self):
        if self.ultimo_dataframe is not None and not self.ultimo_dataframe.empty:
            os.makedirs("reportes", exist_ok=True)
            nombre_archivo = os.path.join("reportes", "reporte_exportado.xlsx")
            try:
                exportar_excel_bonito(self.ultimo_dataframe, nombre_archivo)
                self.status_bar.showMessage(f"📁 Exportado exitosamente a {nombre_archivo}", 5000)

                # Mostrar diálogo de éxito
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Exportación Exitosa")
                msg.setText(f"Archivo exportado correctamente a:\n{nombre_archivo}")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec()

            except Exception as e:
                self.status_bar.showMessage(f"Error al exportar: {str(e)}", 5000)
        else:
            self.status_bar.showMessage("No hay datos para exportar", 3000)



    @Slot()
    def filtrar_por_marca(self):
        marca, ok = QInputDialog.getText(self, "Filtrar por Marca", "Ingrese la marca:")
        if ok and marca:
            self.status_bar.showMessage(f"Filtrando por marca '{marca}'...")
            QApplication.processEvents()
            # Debes decidir qué función llamar aquí, esto es solo un ejemplo
            if "llanta" in self.windowTitle().lower():  # Puedes usar otra lógica si prefieres
                QTimer.singleShot(0, lambda: self.async_load_filtered_data_llantas(marca))
            else:
                QTimer.singleShot(0, lambda: self.async_load_filtered_data_aceites(marca))
    @Slot()
    def filtrar_por_marca2(self):
        if self.ultimo_dataframe is None or self.ultimo_dataframe.empty:
            self.status_bar.showMessage("No hay datos cargados para filtrar", 3000)
            return

        marca, ok = QInputDialog.getText(self, "Filtrar por Marca", "Ingrese la marca:")
        if not ok or not marca:
            return

        self.status_bar.showMessage(f"Filtrando por marca '{marca}'...")
        QApplication.processEvents()

        # Asegurate de trabajar con la última copia de filtrado
        df_base = self.ultimo_dataframe.copy()

        # Identificar columna que contiene la marca
        nombre_columna = df_base.columns[1]

        print("Primeros 10 valores columna descripción (antes del filtro):")
        print(df_base[nombre_columna].head(10))

        df_filtrado = df_base[
            df_base[nombre_columna].astype(str).str.contains(marca, case=False, na=False)
        ]

        print(f"Filtrado con marca '{marca}': {len(df_filtrado)} filas encontradas")
        print("Primeros 10 valores columna descripción (después del filtro):")
        print(df_filtrado[nombre_columna].head(10))

        if df_filtrado.empty:
            self.status_bar.showMessage(f"No se encontraron registros con '{marca}'", 5000)
        else:
            self.ultimo_dataframe = df_filtrado  # 🔁 esta es la nueva base para más filtros
            self.display_data(df_filtrado)
            self.status_bar.showMessage(f"Mostrando {len(df_filtrado)} registros filtrados", 5000)




