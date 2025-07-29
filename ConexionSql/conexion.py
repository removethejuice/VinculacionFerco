import os
import configparser
import pyodbc
from tkinter import messagebox
from pathlib import Path
import sys

def conectorcito():
    # Detectar si se está ejecutando como ejecutable (.exe) o script
    if getattr(sys, 'frozen', False):
        # Ejecutable (.exe)
        raiz_proyecto = Path(sys.executable).parent
    else:
        # Script .py normal
        raiz_proyecto = Path(__file__).parent.parent.resolve()

    config_raiz = raiz_proyecto / "config.properties"

    config = configparser.ConfigParser()
    config.optionxform = str  # mantener mayúsculas/minúsculas en claves

    if not config_raiz.exists():
        config['DEFAULT'] = {
            'db.server': 'localhost',
            'db.port': '1433',
            'db.name': 'NombreDeTuBase',
            'db.user': 'sa',
            'db.password': '1234'
        }
        with open(config_raiz, 'w') as out:
            config.write(out)
        messagebox.showwarning(
            "Archivo de configuración",
            f"⚠️ Archivo '{config_raiz}' creado en la raíz del proyecto.\nPor favor edítalo y vuelve a ejecutar el programa."
        )
        return None

    try:
        config.read(config_raiz)

        servidor = config['DEFAULT']['db.server']
        puerto = config['DEFAULT']['db.port']
        nombre_base = config['DEFAULT']['db.name']
        USER = config['DEFAULT']['db.user']
        PASSWORD = config['DEFAULT']['db.password']

        URL = f"Driver={{SQL Server}};Server={servidor},{puerto};Database={nombre_base};UID={USER};PWD={PASSWORD};"
        conn = pyodbc.connect(URL)
        messagebox.showinfo("Éxito", "✅ Conexión exitosa a la base de datos")
        return conn

    except Exception as e:
        messagebox.showerror("Error", f"❌ Error al conectar a la base de datos:\n{str(e)}")
        return None



