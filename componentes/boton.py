from PySide6.QtWidgets import QPushButton

class BotonReporte(QPushButton):
    def __init__(self, texto, callback):
        super().__init__(texto)
        self.clicked.connect(callback)
        self.setStyleSheet("""
            QPushButton {
                background-color: #F8EDEB;
                color: black;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 14px;
                min-width: 150px;
                margin-bottom: 5px;
            }
            QPushButton:hover {
                background-color: #FCD5CE;
                border-color: #FFB5A7;
            }
        """)
