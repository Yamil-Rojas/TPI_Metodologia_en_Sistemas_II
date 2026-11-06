"""Escenarios de uso, descritos como las líneas que escribiría una persona.

COMPORTAMIENTO: lo que no debe cambiar nunca con un refactoring.
CORRECCIONES: las tres fallas conocidas; su comportamiento cambia a propósito
en el paso final (commits aparte).
"""
from arnes import SIN_ARCHIVO


def reg(nombre, legajo, email, tipo, prioridad, descripcion, area):
    return ["1", nombre, legajo, email, tipo, prioridad, descripcion, area]


def estado(id_solicitud, nuevo):
    return ["2", str(id_solicitud), nuevo]


def asignar(id_solicitud, id_responsable):
    return ["3", str(id_solicitud), str(id_responsable)]


def buscar(criterio, valor=None):
    return ["4", criterio] if valor is None else ["4", criterio, valor]


def reporte(legajo=""):
    return ["5", legajo]


SALIR = ["0"]

DATOS_VACIOS = '{"estudiantes": [], "responsables": [], "solicitudes": []}'

DATOS_CON_HUECOS = """{
  "estudiantes": [{"legajo": "10001", "nombre": "Lucia Fernandez", "email": "lucia@ejemplo.com"}],
  "responsables": [{"id": 1, "nombre": "Marta Gimenez", "area": "Alumnado"}],
  "solicitudes": [
    {"id": 1, "legajo": "10001", "tipo": "cert", "prioridad": 2, "descripcion": "a", "area": "Alumnado",
     "fecha": "2026-10-20", "estado": "fin", "responsable": "Marta Gimenez", "plazo_dias": 5},
    {"id": 7, "legajo": "10001", "tipo": "baja", "prioridad": 1, "descripcion": "b", "area": "Alumnado",
     "fecha": "2026-10-21", "estado": "pen", "responsable": null, "plazo_dias": 1}
  ]
}"""

COMPORTAMIENTO = {
    "s01_salir": {"entradas": SALIR},
    "s02_responsables": {"entradas": ["6"] + SALIR},
    "s03_registrar_valido": {
        "entradas": reg("Juan Perez", "10004", "juan.perez@ejemplo.com", "cert", "2",
                        "Certificado de prueba", "Alumnado")
        + buscar("a", "pen") + buscar("c", "10004") + SALIR
    },
    "s04_plazos": {
        "entradas": (
            reg("Ana A", "10005", "a@e.com", "equi", "1", "d", "Bedelia")
            + reg("Ana B", "10006", "b@e.com", "baja", "1", "d", "Alumnado")
            + reg("Ana C", "10007", "c@e.com", "baja", "3", "d", "Alumnado")
            + reg("Ana D", "10008", "d@e.com", "cert", "3", "d", "Alumnado")
            + reg("Ana E", "10009", "e@e.com", "equi", "3", "d", "Bedelia")
            + reg("Ana F", "10010", "f@e.com", "cert", "1", "d", "Alumnado")
            + reg("Ana G", "10011", "g@e.com", "equi", "2", "d", "Bedelia")
            + reg("Ana H", "10012", "h@e.com", "baja", "2", "d", "Alumnado")
            + SALIR
        )
    },
    "s05_validaciones": {
        "entradas": (
            reg("Ana", "12", "a@e.com", "cert", "2", "x", "Alumnado")
            + reg("Ana", "12a45", "a@e.com", "cert", "2", "x", "Alumnado")
            + reg("Ana", "1234567", "a@e.com", "cert", "2", "x", "Alumnado")
            + reg("   ", "10020", "a@e.com", "cert", "2", "x", "Alumnado")
            + reg("Ana", "10020", "anaejemplo.com", "cert", "2", "x", "Alumnado")
            + reg("Ana", "10020", "a@e.com", "otro", "2", "x", "Alumnado")
            + reg("Ana", "10020", "a@e.com", "CERT", "2", "x", "Alumnado")
            + reg("Ana", "10020", "a@e.com", "cert", "5", "x", "Alumnado")
            + reg("Ana", "10020", "a@e.com", "cert", "abc", "x", "Alumnado")
            + reg("Ana", "10020", "a@e.com", "cert", "2", "   ", "Alumnado")
            + reg("   ", "12", "mal", "zzz", "9", "  ", "Alumnado")
            + reg("   ", "10020", "mal", "zzz", "9", "  ", "Alumnado")
            + reporte() + SALIR
        )
    },
    "s06_estados_validos": {
        "entradas": estado(3, "pro") + estado(3, "fin") + estado(4, "pro") + reporte() + SALIR
    },
    "s07_estados_no_permitidos": {
        "entradas": (
            estado(1, "pro") + estado(1, "pen") + estado(1, "fin")
            + estado(2, "pen") + estado(2, "pro")
            + estado(3, "fin") + estado(3, "pen") + estado(3, "xyz")
            + estado(4, "") + estado(2, "fin") + reporte() + SALIR
        )
    },
    "s08_asignar": {
        "entradas": (
            asignar(4, 2) + asignar(3, 1) + asignar(3, 3)
            + buscar("c", "10001") + buscar("c", "10003") + SALIR
        )
    },
    "s09_busquedas": {
        "entradas": (
            buscar("a", "pen") + buscar("a", "pro") + buscar("a", "fin")
            + buscar("a", "xyz") + buscar("a", "PEN")
            + buscar("b", "cert") + buscar("b", "equi") + buscar("b", "baja") + buscar("b", "zzz")
            + buscar("c", "10001") + buscar("c", "10003") + buscar("c", "10099")
            + buscar("c", "12") + buscar("c", "abcde")
            + buscar("d") + buscar("") + SALIR
        )
    },
    "s10_reportes": {
        "entradas": (
            reporte("") + reporte("10001") + reporte("10003") + reporte("1")
            + reporte("abcde") + reporte("10099") + SALIR
        )
    },
    "s11_opciones_invalidas": {"entradas": ["9", "", "abc"] + SALIR},
    "s12_flujo_completo": {
        "entradas": (
            reg("Maria Lopez", "10030", "maria@ejemplo.com", "equi", "1",
                "Equivalencia de Ingles", "Bedelia")
            + estado(5, "pro") + asignar(5, 2) + estado(5, "fin")
            + buscar("c", "10030") + reporte("10030") + buscar("a", "fin") + SALIR
        )
    },
    "s13_estudiante_existente": {
        "entradas": (
            reg("Otro Nombre", "10001", "otro@ejemplo.com", "baja", "1",
                "Baja de materia", "Alumnado")
            + buscar("c", "10001") + SALIR
        )
    },
    "s14_sin_archivo": {
        "datos": SIN_ARCHIVO,
        "entradas": (
            reporte() + ["6"]
            + reg("Nuevo", "10040", "n@e.com", "cert", "2", "d", "Alumnado")
            + reporte() + SALIR
        ),
    },
    "s15_datos_vacios": {
        "datos": DATOS_VACIOS,
        "entradas": (
            buscar("a", "pen") + ["6"]
            + reg("Nuevo", "10040", "n@e.com", "baja", "3", "d", "Alumnado")
            + buscar("c", "10040") + SALIR
        ),
    },
    "s16_ids_con_huecos": {
        "datos": DATOS_CON_HUECOS,
        "entradas": (
            reg("Nuevo", "10050", "n@e.com", "cert", "2", "d", "Alumnado")
            + buscar("a", "pen") + reporte() + SALIR
        ),
    },
}

CORRECCIONES = {
    "c01_estado_id_inexistente": {"entradas": estado(99, "pro") + reporte() + SALIR},
    "c02_asignar_responsable_inexistente": {"entradas": asignar(4, 99) + reporte() + SALIR},
    "c03_asignar_solicitud_inexistente": {"entradas": asignar(99, 1) + SALIR},
    "c04_json_danado_reporte": {"datos": "{ roto", "entradas": reporte() + SALIR},
    "c05_json_danado_registro": {
        "datos": "{ roto",
        "entradas": reg("Nuevo", "10040", "n@e.com", "cert", "2", "d", "Alumnado") + SALIR,
    },
    "c06_estado_id_no_numerico": {"entradas": ["2", "abc", "pro"] + SALIR},
    "c07_asignar_id_no_numerico": {"entradas": ["3", "abc"] + SALIR},
}
