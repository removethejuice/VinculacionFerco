import os
import subprocess
from datetime import datetime, timedelta

ARCHIVO_FECHA = "ultima_ejecucion.txt"
ARCHIVO_LOG = "logs.txt"
CARPETA_SCRIPTS = os.path.join(os.path.dirname(__file__), "ConexionSql")
SCRIPTS_EN_ORDEN = [
    "dataset_creator_ventas.py",
    "dataset_creator_aceites.py",
    "preprocesamiento.py",
    "preprocesamiento_2.py",
    "train_prophet.py","Forecasting_dataset_creator.py",
    "generador_reporte.py"
]

def log(mensaje):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(ARCHIVO_LOG, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {mensaje}\n")
    print(mensaje)

def leer_fecha_ultima_ejecucion():
    if not os.path.exists(ARCHIVO_FECHA):
        return None
    try:
        with open(ARCHIVO_FECHA, "r") as f:
            return datetime.strptime(f.read().strip(), "%Y-%m-%d")
    except Exception as e:
        log(f" Error leyendo fecha: {e}")
        return None

def guardar_fecha_actual():
    with open(ARCHIVO_FECHA, "w") as f:
        f.write(datetime.today().strftime("%Y-%m-%d"))

def han_pasado_30_dias(fecha_anterior):
    return datetime.today() - fecha_anterior >= timedelta(days=30)

def ejecutar_scripts_en_orden():
    for script in SCRIPTS_EN_ORDEN:
        log(f" Ejecutando: {script} desde {CARPETA_SCRIPTS}")
        resultado = subprocess.run(["python", script], cwd=CARPETA_SCRIPTS)
        if resultado.returncode != 0:
            log(f" Error ejecutando {script}. Código de salida: {resultado.returncode}")
            return False
    guardar_fecha_actual()
    log(" Todos los scripts fueron ejecutados exitosamente.")
    return True

def actualizar_si_es_necesario():
    fecha_ultima = leer_fecha_ultima_ejecucion()
    if fecha_ultima is None or han_pasado_30_dias(fecha_ultima):
        log(" Ejecutando scripts porque ha pasado un mes o nunca se ejecutaron.")
        return ejecutar_scripts_en_orden()
    else:
        log(" Aún no ha pasado un mes desde la última ejecución. No se actualiza.")
        return True