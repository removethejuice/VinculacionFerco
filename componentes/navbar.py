from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PySide6.QtCore import Signal

class NavBar(QWidget):
    # Definir señales personalizadas
    home_clicked = Signal()
    inventario_clicked = Signal()
    services_clicked = Signal()
    contact_clicked = Signal()
    aceites_clicked = Signal()  # Nueva señal para el botón de Aceites

    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.setStyleSheet("""
            background-color: white;
            padding: 10px;
        """)

        # Crear botones y conectar a señales
        self.create_button(" Análisis de Ventas por Mes Llantas", self.home_clicked)
        self.create_button(" Análisis de Ventas por Mes Aceites", self.aceites_clicked)  # Aquí se usa la nueva señal
        self.create_button(" Análisis de Inventario por Mes", self.inventario_clicked)
        self.create_button("Predicción de Demanda Futura", self.services_clicked)
        self.create_button("Cálculo del Pedido Sugerido", self.contact_clicked)

    def create_button(self, text, signal):
        """Crea un botón estilizado para el navbar"""
        btn = QPushButton(text)
        btn.setStyleSheet("""
            QPushButton {
                color: black;
                background-color: #F8EDEB;
                border: none;
                padding: 8px 16px;
                font-size: 14px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #FCD5CE;
                border-bottom: 2px solid #FFB5A7;
            }
        """)
        btn.clicked.connect(signal.emit)
        self.layout().addWidget(btn)
