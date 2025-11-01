#!/usr/bin/env python3
"""
Script para ejecutar el dashboard de predicciones DeepAR
"""

import subprocess
import sys
import os

def check_dependencies():
    """Verificar que las dependencias estén instaladas"""
    required_packages = ['streamlit', 'pandas', 'plotly', 'numpy', 'openpyxl']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Faltan las siguientes dependencias:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Instalando dependencias...")
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Dependencias instaladas correctamente")
        except subprocess.CalledProcessError:
            print("❌ Error al instalar dependencias")
            return False
    
    return True

def check_data_file():
    """Verificar que el archivo de datos existe"""
    data_file = "../ConexionSql/predicciones_deepAR.csv"
    
    if not os.path.exists(data_file):
        print(f"❌ No se encontró el archivo de datos: {data_file}")
        print("   Asegúrate de que el archivo existe en la ruta correcta")
        return False
    
    print(f"✅ Archivo de datos encontrado: {data_file}")
    return True

def main():
    """Función principal"""
    print("🚀 Iniciando Dashboard de Predicciones DeepAR")
    print("=" * 50)
    
    # Verificar dependencias
    if not check_dependencies():
        return
    
    # Verificar archivo de datos
    if not check_data_file():
        return
    
    print("\n🌐 Iniciando servidor Streamlit...")
    print("   El dashboard se abrirá automáticamente en tu navegador")
    print("   Para detener el servidor, presiona Ctrl+C")
    print("=" * 50)
    
    try:
        # Ejecutar Streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Dashboard cerrado")
    except Exception as e:
        print(f"❌ Error al ejecutar el dashboard: {e}")

if __name__ == "__main__":
    main() 