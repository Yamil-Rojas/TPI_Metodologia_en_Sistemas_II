"""Arnés de pruebas de caja negra.

Ejecuta main.py en una carpeta temporal con entradas simuladas y devuelve lo que
el usuario ve (salida, código de salida, último renglón del error) y lo que
queda guardado en datos.json. No depende de la estructura interna del código,
por eso sirve igual antes y después de refactorizar.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import date

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Datos de partida de todas las pruebas: una copia propia, para que usar el
# programa a mano (que modifica datos.json) no rompa las pruebas.
DATOS_BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos_base.json")
HOY = date.today().isoformat()
SIN_ARCHIVO = object()


def _copiar_codigo(raiz, destino):
    for nombre in os.listdir(raiz):
        if nombre.endswith(".py"):
            shutil.copy(os.path.join(raiz, nombre), destino)
    shutil.copy(DATOS_BASE, os.path.join(destino, "datos.json"))


def _leer_datos(ruta):
    if not os.path.exists(ruta):
        return "<no existe>"
    with open(ruta, encoding="utf-8") as archivo:
        texto = archivo.read()
    try:
        datos = json.loads(texto)
    except ValueError:
        return {"texto": texto}
    for solicitud in datos.get("solicitudes", []):
        if solicitud.get("fecha") == HOY:
            solicitud["fecha"] = "<HOY>"
    return datos


def _ultima_linea(texto):
    lineas = [linea for linea in texto.splitlines() if linea.strip()]
    return lineas[-1] if lineas else ""


def ejecutar(entradas, datos=None, raiz=RAIZ):
    """Corre main.py (el de la carpeta raiz) con las entradas dadas.

    datos: None usa tests/datos_base.json, un texto lo reemplaza y
    SIN_ARCHIVO lo borra antes de empezar.
    """
    with tempfile.TemporaryDirectory() as carpeta:
        _copiar_codigo(raiz, carpeta)
        ruta_datos = os.path.join(carpeta, "datos.json")
        if datos is SIN_ARCHIVO:
            os.remove(ruta_datos)
        elif datos is not None:
            with open(ruta_datos, "w", encoding="utf-8") as archivo:
                archivo.write(datos)
        proceso = subprocess.run(
            [sys.executable, "main.py"],
            cwd=carpeta,
            input="\n".join(entradas) + "\n",
            capture_output=True,
            encoding="utf-8",
            timeout=30,
        )
        return {
            "salida": proceso.stdout,
            "codigo": proceso.returncode,
            "error": _ultima_linea(proceso.stderr),
            "datos": _leer_datos(ruta_datos),
        }
