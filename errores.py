"""Errores propios del sistema: el servicio los lanza, main decide que mostrar."""


class ErrorDeSistema(Exception):
    """Base de todos los errores esperables del sistema."""


class DatosInvalidos(ErrorDeSistema):
    """Un dato ingresado no cumple las reglas. El mensaje dice cual."""


class SolicitudNoEncontrada(ErrorDeSistema):
    def __init__(self, id_solicitud):
        super().__init__(f"No existe la solicitud con ID {id_solicitud}")


class CambioDeEstadoNoPermitido(ErrorDeSistema):
    def __init__(self):
        super().__init__("Cambio de estado no permitido")


class ResponsableNoEncontrado(ErrorDeSistema):
    def __init__(self, id_responsable):
        super().__init__(f"No existe el responsable con ID {id_responsable}")


class ErrorDePersistencia(ErrorDeSistema):
    """No se pudo leer o escribir el archivo de datos."""
