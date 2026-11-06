"""Acceso a los datos: interfaces chicas (ISP) y su implementacion en JSON.

Es el unico modulo que conoce el archivo datos.json. Trabaja con las
entidades de modelos.py: el resto del sistema nunca ve diccionarios.
"""
import json
from abc import ABC, abstractmethod
from dataclasses import asdict

from modelos import Estudiante, Responsable, Solicitud


class RepositorioSolicitudes(ABC):
    @abstractmethod
    def listar_solicitudes(self): ...

    @abstractmethod
    def obtener_solicitud(self, id_solicitud): ...

    @abstractmethod
    def guardar_solicitud(self, solicitud): ...


class RepositorioEstudiantes(ABC):
    @abstractmethod
    def obtener_estudiante(self, legajo): ...

    @abstractmethod
    def guardar_estudiante(self, estudiante): ...


class RepositorioResponsables(ABC):
    @abstractmethod
    def listar_responsables(self): ...

    @abstractmethod
    def obtener_responsable(self, id_responsable): ...


class RepositorioJSON(RepositorioSolicitudes, RepositorioEstudiantes, RepositorioResponsables):
    def __init__(self, ruta):
        self.ruta = ruta

    def _leer(self):
        try:
            with open(self.ruta, "r", encoding="utf-8") as entrada:
                return json.load(entrada)
        except:
            return {"estudiantes": [], "responsables": [], "solicitudes": []}

    def _escribir(self, datos):
        with open(self.ruta, "w", encoding="utf-8") as salida:
            json.dump(datos, salida, indent=2, ensure_ascii=False)

    def _guardar(self, seccion, clave, entidad):
        datos = self._leer()
        registro = asdict(entidad)
        for posicion, existente in enumerate(datos[seccion]):
            if existente[clave] == registro[clave]:
                datos[seccion][posicion] = registro
                break
        else:
            datos[seccion].append(registro)
        self._escribir(datos)

    def listar_solicitudes(self):
        return [Solicitud(**registro) for registro in self._leer()["solicitudes"]]

    def obtener_solicitud(self, id_solicitud):
        for solicitud in self.listar_solicitudes():
            if solicitud.id == id_solicitud:
                return solicitud
        return None

    def guardar_solicitud(self, solicitud):
        self._guardar("solicitudes", "id", solicitud)

    def obtener_estudiante(self, legajo):
        for registro in self._leer()["estudiantes"]:
            if registro["legajo"] == legajo:
                return Estudiante(**registro)
        return None

    def guardar_estudiante(self, estudiante):
        self._guardar("estudiantes", "legajo", estudiante)

    def listar_responsables(self):
        return [Responsable(**registro) for registro in self._leer()["responsables"]]

    def obtener_responsable(self, id_responsable):
        for responsable in self.listar_responsables():
            if responsable.id == id_responsable:
                return responsable
        return None
