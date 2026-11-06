"""Errores propios del sistema: el servicio los lanza, main decide que mostrar."""


class ErrorDeSistema(Exception):
    """Base de todos los errores esperables del sistema."""


class DatosInvalidos(ErrorDeSistema):
    """Un dato ingresado no cumple las reglas. El mensaje dice cual."""


class SolicitudNoEncontrada(ErrorDeSistema):
    pass


class CambioDeEstadoNoPermitido(ErrorDeSistema):
    def __init__(self):
        super().__init__("Cambio de estado no permitido")
