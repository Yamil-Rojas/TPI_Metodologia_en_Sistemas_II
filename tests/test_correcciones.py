"""Las tres fallas conocidas del sistema original, ya corregidas.

Cada prueba fija el comportamiento NUEVO (mensaje explicito, el programa no se
corta, los datos no se pisan). El comportamiento viejo esta grabado en
tests/golden/antes_correcciones.
"""
import unittest

from arnes import ejecutar
from escenarios import CORRECCIONES, SALIR


def datos_sin_tocar():
    return ejecutar(SALIR)["datos"]


class TestCorrecciones(unittest.TestCase):
    def verificar(self, nombre, mensaje, datos_esperados):
        escenario = CORRECCIONES[nombre]
        resultado = ejecutar(escenario["entradas"], escenario.get("datos"))
        self.assertIn(mensaje, resultado["salida"])
        self.assertEqual(resultado["codigo"], 0, resultado["error"])
        self.assertEqual(resultado["datos"], datos_esperados)

    def test_c01_cambiar_estado_de_solicitud_inexistente_avisa(self):
        self.verificar("c01_estado_id_inexistente", "No existe la solicitud con ID 99", datos_sin_tocar())

    def test_c03_asignar_a_solicitud_inexistente_avisa(self):
        self.verificar("c03_asignar_solicitud_inexistente", "No existe la solicitud con ID 99", datos_sin_tocar())


if __name__ == "__main__":
    unittest.main()
