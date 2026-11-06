"""Graba la salida actual de los escenarios como referencia.

Uso: python tests/grabar.py comportamiento|antes_correcciones [carpeta_del_codigo_original]
Solo se ejecuta sobre el estado-inicial: las referencias son el comportamiento
de la versión original.
"""
import json
import os
import sys

from arnes import RAIZ, ejecutar
from escenarios import COMPORTAMIENTO, CORRECCIONES

CARPETA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "golden")


def grabar(grupo, escenarios, raiz=RAIZ):
    destino = os.path.join(CARPETA, grupo)
    os.makedirs(destino, exist_ok=True)
    for nombre, escenario in escenarios.items():
        resultado = ejecutar(escenario["entradas"], escenario.get("datos"), raiz=raiz)
        ruta = os.path.join(destino, nombre + ".json")
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(resultado, archivo, indent=2, ensure_ascii=False)
            archivo.write("\n")
        print("grabado", grupo, nombre, "codigo", resultado["codigo"])


if __name__ == "__main__":
    grupo = sys.argv[1] if len(sys.argv) > 1 else ""
    codigo = sys.argv[2] if len(sys.argv) > 2 else RAIZ  # carpeta con el codigo original
    if grupo == "comportamiento":
        grabar(grupo, COMPORTAMIENTO, codigo)
    elif grupo == "antes_correcciones":
        grabar(grupo, CORRECCIONES, codigo)
    else:
        print(__doc__)
        sys.exit(1)
