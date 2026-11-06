"""Errores propios del sistema: el servicio los lanza, main decide que mostrar."""


class ErrorDeSistema(Exception):
    """Base de todos los errores esperables del sistema."""


class DatosInvalidos(ErrorDeSistema):
    """Un dato o una accion no cumple las reglas. El mensaje dice cual."""


class NoEncontrado(ErrorDeSistema):
    """No existe lo que se busco por ID. Ejemplo: NoEncontrado("la solicitud", 99)."""

    def __init__(self, descripcion, identificador):
        super().__init__(f"No existe {descripcion} con ID {identificador}")


class ErrorDePersistencia(ErrorDeSistema):
    """No se pudo leer o escribir el archivo de datos."""
