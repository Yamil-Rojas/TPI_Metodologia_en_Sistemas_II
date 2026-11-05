"""El comportamiento externo con datos válidos no cambia con los refactorings.

Compara, escenario por escenario, lo que ve el usuario y lo que queda guardado
contra las referencias grabadas sobre el estado-inicial.
"""
import json
import os
import unittest

from arnes import ejecutar
from escenarios import COMPORTAMIENTO

CARPETA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "golden", "comportamiento")


def cargar_referencia(nombre):
    with open(os.path.join(CARPETA, nombre + ".json"), encoding="utf-8") as archivo:
        return json.load(archivo)


class TestComportamiento(unittest.TestCase):
    def test_escenarios_identicos_al_estado_inicial(self):
        for nombre, escenario in COMPORTAMIENTO.items():
            with self.subTest(escenario=nombre):
                real = ejecutar(escenario["entradas"], escenario.get("datos"))
                self.assertEqual(real, cargar_referencia(nombre))


if __name__ == "__main__":
    unittest.main()
