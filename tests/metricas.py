"""Mide los smells del diagnóstico (etapa 3) sobre el código de la raíz del repo.

Uso: python tests/metricas.py [archivo_salida.json]
"""
import ast
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def modulos():
    return sorted(nombre for nombre in os.listdir(RAIZ) if nombre.endswith(".py"))


def lineas(nombre):
    with open(os.path.join(RAIZ, nombre), encoding="utf-8") as archivo:
        return archivo.read().splitlines()


def contar(patron, excluir=()):
    total = 0
    for nombre in modulos():
        if nombre in excluir:
            continue
        for linea in lineas(nombre):
            if not linea.strip().startswith("#") and re.search(patron, linea):
                total += 1
    return total


def funciones(excluir=()):
    for nombre in modulos():
        if nombre in excluir:
            continue
        arbol = ast.parse("\n".join(lineas(nombre)))
        for nodo in ast.walk(arbol):
            if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
                yield nombre, nodo


def parametros_registrar():
    for _, nodo in funciones():
        if nodo.name in ("registrar_solicitud", "registrar"):
            return len([a for a in nodo.args.args if a.arg != "self"])
    return None


def mas_larga(excluir=()):
    largos = [nodo.end_lineno - nodo.lineno + 1 for _, nodo in funciones(excluir)]
    return max(largos) if largos else 0


def medir():
    return {
        "modulos": len(modulos()),
        "open_fuera_de_repositorio": contar(r"\bopen\(", excluir=("repositorio.py",)),
        "except_vacios": contar(r"^\s*except\s*:"),
        "print_input_fuera_de_main": contar(r"\b(print|input)\(", excluir=("main.py",)),
        "copias_validacion_legajo": contar(r"isdigit"),
        "textos_estado_fuera_de_modelos": contar(r"[\"'](pen|pro|fin)[\"']", excluir=("modelos.py",)),
        "parametros_registrar": parametros_registrar(),
        "funcion_mas_larga_logica": mas_larga(excluir=("main.py",)),
        "funcion_mas_larga_total": mas_larga(),
    }


if __name__ == "__main__":
    resultado = medir()
    print(json.dumps(resultado, indent=2))
    if len(sys.argv) > 1:
        with open(sys.argv[1], "w", encoding="utf-8") as archivo:
            json.dump(resultado, archivo, indent=2)
            archivo.write("\n")
