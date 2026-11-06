"""Acceso a los datos: interfaces chicas (ISP) y su implementacion en JSON.

Es el unico modulo que conoce el archivo datos.json.
"""
import json
from abc import ABC, abstractmethod


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

    def listar_solicitudes(self):
        return self._leer()["solicitudes"]

    def obtener_solicitud(self, id_solicitud):
        for solicitud in self._leer()["solicitudes"]:
            if solicitud["id"] == id_solicitud:
                return solicitud
        return None

    def guardar_solicitud(self, solicitud):
        datos = self._leer()
        for posicion, existente in enumerate(datos["solicitudes"]):
            if existente["id"] == solicitud["id"]:
                datos["solicitudes"][posicion] = solicitud
                break
        else:
            datos["solicitudes"].append(solicitud)
        self._escribir(datos)

    def obtener_estudiante(self, legajo):
        for estudiante in self._leer()["estudiantes"]:
            if estudiante["legajo"] == legajo:
                return estudiante
        return None

    def guardar_estudiante(self, estudiante):
        datos = self._leer()
        for posicion, existente in enumerate(datos["estudiantes"]):
            if existente["legajo"] == estudiante["legajo"]:
                datos["estudiantes"][posicion] = estudiante
                break
        else:
            datos["estudiantes"].append(estudiante)
        self._escribir(datos)

    def listar_responsables(self):
        return self._leer()["responsables"]

    def obtener_responsable(self, id_responsable):
        for responsable in self._leer()["responsables"]:
            if responsable["id"] == id_responsable:
                return responsable
        return None
