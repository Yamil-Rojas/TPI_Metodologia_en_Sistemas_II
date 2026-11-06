"""Pruebas de unidad y de diseno sobre el codigo refactorizado.

No usan archivos: el servicio se prueba con repositorios en memoria, que es
justamente lo que permite el principio de inversion de dependencias (DIP).
"""
import os
import re
import sys
import unittest
from dataclasses import asdict

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from errores import DatosInvalidos, NoEncontrado  # noqa: E402
from modelos import TIPOS, DatosSolicitud, Estado, Prioridad, Responsable, Solicitud, TipoSolicitud  # noqa: E402
from repositorio import RepositorioEstudiantes, RepositorioResponsables, RepositorioSolicitudes  # noqa: E402
from servicio import ServicioSolicitudes  # noqa: E402
from validaciones import mensaje_de_error  # noqa: E402


class RepositorioEnMemoria(RepositorioSolicitudes, RepositorioEstudiantes, RepositorioResponsables):
    def __init__(self):
        self.solicitudes = {}
        self.estudiantes = {}
        self.responsables = {1: Responsable(1, "Marta Gimenez", "Alumnado")}

    def listar_solicitudes(self):
        return [Solicitud(**asdict(solicitud)) for solicitud in self.solicitudes.values()]

    def obtener_solicitud(self, id_solicitud):
        solicitud = self.solicitudes.get(id_solicitud)
        return Solicitud(**asdict(solicitud)) if solicitud else None

    def guardar_solicitud(self, solicitud):
        self.solicitudes[solicitud.id] = Solicitud(**asdict(solicitud))

    def obtener_estudiante(self, legajo):
        return self.estudiantes.get(legajo)

    def guardar_estudiante(self, estudiante):
        self.estudiantes[estudiante.legajo] = estudiante

    def listar_responsables(self):
        return list(self.responsables.values())

    def obtener_responsable(self, id_responsable):
        return self.responsables.get(id_responsable)


def datos(**cambios):
    base = dict(nombre="Lucia", legajo="10001", email="l@e.com", tipo="cert", prioridad=2,
                descripcion="x", area="Alumnado", fecha="2026-11-01")
    base.update(cambios)
    return DatosSolicitud(**base)


def servicio_nuevo():
    repositorio = RepositorioEnMemoria()
    return ServicioSolicitudes(repositorio, repositorio, repositorio), repositorio


class TestServicioConRepositorioEnMemoria(unittest.TestCase):
    def test_registrar_asigna_id_plazo_y_estado_inicial(self):
        servicio, repositorio = servicio_nuevo()
        solicitud = servicio.registrar_solicitud(datos(tipo="equi", prioridad=1))
        self.assertEqual((solicitud.id, solicitud.plazo_dias, solicitud.estado), (1, 13, "pen"))
        self.assertIn("10001", repositorio.estudiantes)

    def test_ids_correlativos_y_estudiante_no_se_duplica(self):
        servicio, repositorio = servicio_nuevo()
        servicio.registrar_solicitud(datos())
        segunda = servicio.registrar_solicitud(datos())
        self.assertEqual(segunda.id, 2)
        self.assertEqual(len(repositorio.estudiantes), 1)

    def test_datos_invalidos_lanza_error_con_el_mensaje(self):
        servicio, _ = servicio_nuevo()
        with self.assertRaises(DatosInvalidos) as contexto:
            servicio.registrar_solicitud(datos(legajo="12"))
        self.assertEqual(str(contexto.exception), "Legajo invalido")

    def test_flujo_de_estados_y_cambio_no_permitido(self):
        servicio, _ = servicio_nuevo()
        servicio.registrar_solicitud(datos())
        with self.assertRaises(DatosInvalidos):
            servicio.cambiar_estado(1, "fin")
        servicio.cambiar_estado(1, "pro")
        servicio.cambiar_estado(1, "fin")
        self.assertEqual(servicio.resumen().finalizadas, 1)

    def test_errores_de_ids_inexistentes(self):
        servicio, _ = servicio_nuevo()
        servicio.registrar_solicitud(datos())
        with self.assertRaises(NoEncontrado):
            servicio.cambiar_estado(99, "pro")
        with self.assertRaises(NoEncontrado):
            servicio.asignar_responsable(1, 99)

    def test_asignar_responsable_actualiza_nombre_y_area(self):
        servicio, repositorio = servicio_nuevo()
        servicio.registrar_solicitud(datos(area="Otra"))
        servicio.asignar_responsable(1, 1)
        guardada = repositorio.solicitudes[1]
        self.assertEqual((guardada.responsable, guardada.area), ("Marta Gimenez", "Alumnado"))

    def test_busquedas_y_cantidad_por_legajo(self):
        servicio, _ = servicio_nuevo()
        servicio.registrar_solicitud(datos())
        servicio.registrar_solicitud(datos(legajo="10002", tipo="baja"))
        self.assertEqual(len(servicio.buscar_por_tipo("baja")), 1)
        self.assertEqual(servicio.cantidad_de_solicitudes("10001"), 1)
        with self.assertRaises(DatosInvalidos):
            servicio.buscar_por_legajo("abc")


class TestSolicitud(unittest.TestCase):
    def test_tabla_completa_de_transiciones(self):
        permitidas = {("pen", "pro"), ("pro", "fin")}
        for origen in [estado.value for estado in Estado]:
            for destino in [estado.value for estado in Estado] + ["xx"]:
                with self.subTest(origen=origen, destino=destino):
                    solicitud = Solicitud(1, "10001", "cert", 2, "d", "a", "f", estado=origen)
                    self.assertEqual(solicitud.avanzar_a(destino), (origen, destino) in permitidas)


class TestTiposDeSolicitud(unittest.TestCase):
    def test_contrato_de_todos_los_tipos(self):
        """LSP: cualquier TipoSolicitud se puede usar donde se espera un TipoSolicitud."""
        for codigo, tipo in TIPOS.items():
            self.assertIsInstance(tipo, TipoSolicitud)
            self.assertEqual(tipo.codigo, codigo)
            plazos = [tipo.calcular_plazo(prioridad) for prioridad in (Prioridad.ALTA, Prioridad.MEDIA, Prioridad.BAJA)]
            with self.subTest(tipo=codigo):
                self.assertTrue(all(isinstance(plazo, int) and plazo >= 1 for plazo in plazos))
                self.assertLessEqual(plazos[0], plazos[1])
                self.assertLessEqual(plazos[1], plazos[2])

    def test_plazos_originales(self):
        esperado = {"cert": (3, 5, 7), "equi": (13, 15, 17), "baja": (1, 3, 5)}
        for codigo, plazos in esperado.items():
            prioridades = (Prioridad.ALTA, Prioridad.MEDIA, Prioridad.BAJA)
            real = tuple(TIPOS[codigo].calcular_plazo(prioridad) for prioridad in prioridades)
            self.assertEqual(real, plazos, codigo)

    def test_agregar_un_tipo_nuevo_no_toca_servicio_validaciones_ni_main(self):
        """OCP: alcanza con definir la clase y registrarla en TIPOS (ambos en modelos.py)."""

        class Constancia(TipoSolicitud):
            codigo = "cons"
            plazo_base_dias = 2

        TIPOS["cons"] = Constancia()
        try:
            self.assertIsNone(mensaje_de_error(datos(tipo="cons")))
            servicio, _ = servicio_nuevo()
            self.assertEqual(servicio.registrar_solicitud(datos(tipo="cons", prioridad=3)).plazo_dias, 4)
        finally:
            del TIPOS["cons"]


class TestReglasDeDiseno(unittest.TestCase):
    def leer(self, nombre):
        with open(os.path.join(RAIZ, nombre), encoding="utf-8") as archivo:
            return archivo.read()

    def test_servicio_y_modelos_no_conocen_persistencia_ni_pantalla(self):
        for nombre in ("servicio.py", "modelos.py", "validaciones.py"):
            codigo = self.leer(nombre)
            with self.subTest(modulo=nombre):
                self.assertNotRegex(codigo, r"^\s*(import|from)\s+(json|os)\b")
                self.assertNotRegex(codigo, r"\b(print|input|open)\(")

    def test_solo_el_repositorio_conoce_el_archivo(self):
        for nombre in ("servicio.py", "main.py", "validaciones.py", "modelos.py"):
            self.assertNotIn("import json", self.leer(nombre), nombre)

    def test_los_codigos_de_tipo_viven_solo_en_modelos(self):
        for nombre in ("servicio.py", "main.py", "validaciones.py", "repositorio.py"):
            self.assertIsNone(re.search(r"[\"'](cert|equi|baja)[\"']", self.leer(nombre)), nombre)

    def test_no_hay_except_vacios(self):
        for nombre in ("servicio.py", "main.py", "validaciones.py", "repositorio.py", "modelos.py"):
            self.assertIsNone(re.search(r"^\s*except\s*:", self.leer(nombre), re.M), nombre)


if __name__ == "__main__":
    unittest.main()
