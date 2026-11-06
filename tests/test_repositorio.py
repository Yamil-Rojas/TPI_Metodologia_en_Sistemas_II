"""El repositorio JSON: lectura, escritura y errores de persistencia (con archivos temporales)."""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from errores import ErrorDePersistencia  # noqa: E402
from modelos import Estudiante, Responsable, Solicitud  # noqa: E402
from repositorio import RepositorioJSON  # noqa: E402


def solicitud(id_solicitud=1):
    return Solicitud(id_solicitud, "10001", "cert", 2, "d", "Alumnado", "2026-11-01", plazo_dias=5)


class TestRepositorioJSON(unittest.TestCase):
    def setUp(self):
        self.carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(self.carpeta.cleanup)
        self.ruta = os.path.join(self.carpeta.name, "datos.json")
        self.repositorio = RepositorioJSON(self.ruta)

    def escribir(self, texto):
        with open(self.ruta, "w", encoding="utf-8") as archivo:
            archivo.write(texto)

    def test_sin_archivo_se_parte_de_datos_vacios(self):
        self.assertEqual(self.repositorio.listar_solicitudes(), [])
        self.assertEqual(self.repositorio.listar_responsables(), [])
        self.assertIsNone(self.repositorio.obtener_estudiante("10001"))

    def test_guardar_y_leer_conserva_todos_los_campos(self):
        self.repositorio.guardar_solicitud(solicitud())
        self.repositorio.guardar_estudiante(Estudiante("10001", "Lucia", "l@e.com"))
        self.assertEqual(self.repositorio.obtener_solicitud(1), solicitud())
        self.assertEqual(self.repositorio.obtener_estudiante("10001"), Estudiante("10001", "Lucia", "l@e.com"))

    def test_guardar_una_solicitud_existente_la_reemplaza_sin_duplicar(self):
        self.repositorio.guardar_solicitud(solicitud())
        cambiada = solicitud()
        cambiada.estado = "pro"
        self.repositorio.guardar_solicitud(cambiada)
        self.assertEqual(len(self.repositorio.listar_solicitudes()), 1)
        self.assertEqual(self.repositorio.obtener_solicitud(1).estado, "pro")

    def test_obtener_un_id_inexistente_devuelve_none(self):
        self.assertIsNone(self.repositorio.obtener_solicitud(99))
        self.assertIsNone(self.repositorio.obtener_responsable(99))

    def test_responsables_se_leen_como_entidades(self):
        self.escribir('{"estudiantes": [], "solicitudes": [],'
                      ' "responsables": [{"id": 1, "nombre": "Marta", "area": "Alumnado"}]}')
        self.assertEqual(self.repositorio.obtener_responsable(1), Responsable(1, "Marta", "Alumnado"))

    def test_json_danado_lanza_error_y_no_pisa_el_archivo(self):
        self.escribir("{ roto")
        with self.assertRaises(ErrorDePersistencia):
            self.repositorio.guardar_solicitud(solicitud())
        with open(self.ruta, encoding="utf-8") as archivo:
            self.assertEqual(archivo.read(), "{ roto")

    def test_json_valido_con_estructura_incorrecta_lanza_error(self):
        for texto in ('[]', '{"solicitudes": []}', '{"estudiantes": 1, "responsables": [], "solicitudes": []}'):
            with self.subTest(contenido=texto):
                self.escribir(texto)
                with self.assertRaises(ErrorDePersistencia):
                    self.repositorio.listar_solicitudes()

    def test_error_de_escritura_no_afirma_que_no_se_modifico_nada(self):
        repositorio = RepositorioJSON(self.carpeta.name)  # una carpeta no se puede abrir para escribir
        with self.assertRaises(ErrorDePersistencia) as contexto:
            repositorio._escribir({"estudiantes": [], "responsables": [], "solicitudes": []})
        self.assertIn("No se pudo guardar", str(contexto.exception))
        self.assertNotIn("No se modifico nada", str(contexto.exception))


if __name__ == "__main__":
    unittest.main()
