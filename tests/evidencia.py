"""Genera la evidencia de pruebas antes/despues en Markdown.

Uso: python tests/evidencia.py <carpeta_del_codigo_original> <archivo_salida.md>

Corre los mismos escenarios sobre el codigo original (la carpeta indicada) y
sobre el codigo actual de este repositorio, y compara lo que ve el usuario y lo
que queda guardado en datos.json.
"""
import re
import sys

from arnes import RAIZ, ejecutar
from escenarios import COMPORTAMIENTO, CORRECCIONES, SALIR

DESCRIPCION = {
    "s01_salir": "Abrir el programa y salir",
    "s02_responsables": "Ver la lista de responsables",
    "s03_registrar_valido": "Registrar una solicitud valida y buscarla",
    "s04_plazos": "Plazo calculado para cada tipo y prioridad",
    "s05_validaciones": "Datos invalidos: legajo, nombre, email, tipo, prioridad, descripcion",
    "s06_estados_validos": "Cambios de estado permitidos",
    "s07_estados_no_permitidos": "Cambios de estado no permitidos",
    "s08_asignar": "Asignar responsables",
    "s09_busquedas": "Busquedas por estado, tipo y legajo (validas e invalidas)",
    "s10_reportes": "Reporte basico con y sin legajo",
    "s11_opciones_invalidas": "Opciones de menu invalidas",
    "s12_flujo_completo": "Flujo completo: registrar, procesar, asignar, finalizar, reportar",
    "s13_estudiante_existente": "Registrar con un legajo de estudiante ya existente",
    "s14_sin_archivo": "Primer uso: datos.json no existe",
    "s15_datos_vacios": "datos.json con listas vacias",
    "s16_ids_con_huecos": "IDs con huecos (el nuevo ID sigue al mayor)",
    "c01_estado_id_inexistente": "Cambiar el estado de una solicitud que no existe (ID 99)",
    "c02_asignar_responsable_inexistente": "Asignar un responsable que no existe (ID 99)",
    "c03_asignar_solicitud_inexistente": "Asignar a una solicitud que no existe (ID 99)",
    "c04_json_danado_reporte": "Pedir el reporte con datos.json danado",
    "c05_json_danado_registro": "Registrar una solicitud con datos.json danado",
    "c06_estado_id_no_numerico": "Cambiar estado escribiendo letras en vez de un ID",
    "c07_asignar_id_no_numerico": "Asignar responsable escribiendo letras en vez de un ID",
}


def correr(carpeta, escenario):
    return ejecutar(escenario["entradas"], escenario.get("datos"), raiz=carpeta)


MENSAJE_NUEVO = re.compile(r"(No existe [^\n]+? con ID \d+|No se pudo leer [^\n]*|ID invalido)")


def mensaje_nuevo(resultado):
    """El mensaje de error que muestra el programa, si hay alguno."""
    encontrado = MENSAJE_NUEVO.search(resultado["salida"])
    return encontrado.group(1) if encontrado else None


def celda(texto):
    return texto.replace("|", "/").replace("\n", " ")


def marca(coincide):
    return "igual" if coincide else "DISTINTO"


def comportamiento(original):
    filas = [
        "| Escenario | Qué se prueba | Salida | Código de salida | datos.json guardado | Resultado |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    iguales = 0
    for nombre, escenario in COMPORTAMIENTO.items():
        antes, despues = correr(original, escenario), correr(RAIZ, escenario)
        misma_salida = antes["salida"] == despues["salida"]
        mismo_codigo = antes["codigo"] == despues["codigo"]
        mismos_datos = antes["datos"] == despues["datos"]
        igual = misma_salida and mismo_codigo and mismos_datos
        iguales += igual
        resultado = "sin cambios" if igual else "CAMBIÓ"
        filas.append(
            f"| {nombre} | {DESCRIPCION[nombre]} | {marca(misma_salida)} | {marca(mismo_codigo)} "
            f"| {marca(mismos_datos)} | {resultado} |"
        )
    return filas, iguales, len(COMPORTAMIENTO)


def antes_de_corregir(resultado, base):
    """Que pasaba en el codigo original, dicho con hechos observables."""
    hechos = []
    if resultado["codigo"] != 0:
        hechos.append(f"el programa se corta con `{resultado['error']}`")
    if resultado["datos"] != base:
        solicitudes = len(resultado["datos"].get("solicitudes", []))
        hechos.append(f"pisa datos.json (queda con {solicitudes} solicitud)")
    total = re.search(r"Total: (\d+)", resultado["salida"])
    if isinstance(base, dict) and "texto" in base and total:
        hechos.append(f"muestra el reporte como si no hubiera datos (Total: {total.group(1)})")
    if mensaje_nuevo(resultado) is None and not hechos:
        hechos.append("no muestra ningún mensaje")
    return "; ".join(hechos)


def despues_de_corregir(resultado, base):
    hechos = []
    mensaje = mensaje_nuevo(resultado)
    hechos.append(f"muestra `{mensaje}`" if mensaje else "no muestra mensaje")
    if resultado["codigo"] == 0:
        hechos.append("el programa sigue funcionando")
    else:
        hechos.append(f"el programa se corta con `{resultado['error']}`")
    hechos.append("datos.json queda igual" if resultado["datos"] == base else "datos.json cambió")
    return "; ".join(hechos)


def correcciones(original):
    filas = [
        "| Caso | Qué se prueba | Antes (código original) | Después (código refactorizado) |",
        "| --- | --- | --- | --- |",
    ]
    for nombre, escenario in CORRECCIONES.items():
        antes, despues = correr(original, escenario), correr(RAIZ, escenario)
        base = correr(RAIZ, {"entradas": SALIR, "datos": escenario.get("datos")})["datos"]
        filas.append(
            f"| {nombre[:3]} | {DESCRIPCION[nombre]} | {celda(antes_de_corregir(antes, base))} "
            f"| {celda(despues_de_corregir(despues, base))} |"
        )
    return filas


def main(original, salida):
    filas_comp, iguales, total = comportamiento(original)
    filas_corr = correcciones(original)
    texto = [
        "# Evidencia de pruebas antes/después",
        "",
        "Generado por `tests/evidencia.py`: corre los mismos escenarios sobre el código original "
        "(tag `estado-inicial`) y sobre el código refactorizado, con los mismos datos de partida "
        "(`tests/datos_base.json`).",
        "",
        f"## Comportamiento que no debe cambiar: {iguales} de {total} escenarios idénticos",
        "",
        *filas_comp,
        "",
        "## Fallas conocidas que se corrigieron a propósito",
        "",
        *filas_corr,
        "",
    ]
    with open(salida, "w", encoding="utf-8") as archivo:
        archivo.write("\n".join(texto))
    print(f"{iguales}/{total} escenarios de comportamiento idénticos; evidencia en {salida}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
