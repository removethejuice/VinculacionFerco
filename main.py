import sys
from PySide6.QtWidgets import QApplication
from App.contenedor import MainWindow  # Cambiamos la importación
from actualizador import actualizar_si_es_necesario 

def main():
    # Configuración de la aplicación
    if not actualizar_si_es_necesario():
        print("❌ Error en la actualización. Cerrando la aplicación.")
        return  # No continuar si falló la actualización

    app = QApplication(sys.argv)
    
    # Configuración de estilo opcional (puedes personalizarlo)
    app.setStyle('Fusion')  # Un estilo moderno
    
    # Crear y mostrar la ventana principal
    ventana = MainWindow()  # Ahora usamos MainWindow en lugar de ContenedorPrincipal
    ventana.show()
    
    # Ejecutar el bucle principal
    sys.exit(app.exec())

if __name__ == "__main__":
    main()


