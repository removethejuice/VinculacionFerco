from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt, QTimer
import pandas as pd

class TablaDatos(QWidget):
    def __init__(self, df: pd.DataFrame, parent=None):  # ← corregido __init__
        super().__init__(parent)
        self.df = df
        self.table = QTableWidget()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.table)
        self.llenar_tabla(self.df)

    def llenar_tabla(self, df: pd.DataFrame):
        self.df = df

        self.table.setRowCount(0)
        self.table.setColumnCount(0)

        if df.empty:
            return

        self.table.setColumnCount(len(df.columns))
        self.table.setRowCount(len(df))
        self.table.setHorizontalHeaderLabels(df.columns.astype(str).tolist())

        for row_idx, row in enumerate(df.itertuples(index=False)):
            for col_idx, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.table.setItem(row_idx, col_idx, item)

        # Primero, ajustar al contenido mínimo necesario
        header = self.table.horizontalHeader()
        for i in range(len(df.columns)):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)

        # Esperamos un momento a que Qt calcule tamaños reales
        QTimer.singleShot(0, self.adjust_column_resize_behavior)

        self.table.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)
        self.table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)

    def adjust_column_resize_behavior(self):
        total_table_width = sum([self.table.columnWidth(i) for i in range(self.table.columnCount())])
        visible_width = self.table.viewport().width()

        if total_table_width < visible_width:
            # Si sobra espacio, repartirlo equitativamente
            header = self.table.horizontalHeader()
            for i in range(self.table.columnCount()):
                header.setSectionResizeMode(i, QHeaderView.Stretch)




