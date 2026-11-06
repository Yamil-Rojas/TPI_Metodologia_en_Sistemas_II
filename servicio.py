"""Reglas de negocio. No imprime ni lee de teclado: devuelve datos o lanza errores."""
from errores import DatosInvalidos, NoEncontrado
from modelos import TIPOS, Estado, Estudiante, Prioridad, ResumenReporte, Solicitud
from validaciones import legajo_valido, mensaje_de_error

MENSAJE_LEGAJO_INVALIDO = "Legajo invalido"


class ServicioSolicitudes:
    def __init__(self, solicitudes, estudiantes, responsables):
        self.solicitudes = solicitudes
        self.estudiantes = estudiantes
        self.responsables = responsables

    def _asegurar_estudiante(self, datos_solicitud):
        if self.estudiantes.obtener_estudiante(datos_solicitud.legajo) is None:
            self.estudiantes.guardar_estudiante(
                Estudiante(datos_solicitud.legajo, datos_solicitud.nombre, datos_solicitud.email)
            )

    def _proximo_id(self):
        nuevo_id = 1
        for solicitud in self.solicitudes.listar_solicitudes():
            if solicitud.id >= nuevo_id:
                nuevo_id = solicitud.id + 1
        return nuevo_id

    def _crear_solicitud(self, nuevo_id, datos_solicitud, plazo):
        return Solicitud(
            id=nuevo_id,
            legajo=datos_solicitud.legajo,
            tipo=datos_solicitud.tipo,
            prioridad=datos_solicitud.prioridad,
            descripcion=datos_solicitud.descripcion,
            area=datos_solicitud.area,
            fecha=datos_solicitud.fecha,
            plazo_dias=plazo,
        )

    def _validar_legajo(self, legajo):
        if not legajo_valido(legajo):
            raise DatosInvalidos(MENSAJE_LEGAJO_INVALIDO)

    def _solicitudes_del_legajo(self, legajo):
        self._validar_legajo(legajo)
        return [solicitud for solicitud in self.solicitudes.listar_solicitudes() if solicitud.legajo == legajo]

    def registrar_solicitud(self, datos_solicitud):
        error = mensaje_de_error(datos_solicitud)
        if error is not None:
            raise DatosInvalidos(error)
        self._asegurar_estudiante(datos_solicitud)
        plazo = TIPOS[datos_solicitud.tipo].calcular_plazo(Prioridad(datos_solicitud.prioridad))
        solicitud = self._crear_solicitud(self._proximo_id(), datos_solicitud, plazo)
        self.solicitudes.guardar_solicitud(solicitud)
        return solicitud

    def cambiar_estado(self, id_solicitud, nuevo_estado):
        solicitud = self.solicitudes.obtener_solicitud(id_solicitud)
        if solicitud is None:
            raise NoEncontrado("la solicitud", id_solicitud)
        if not solicitud.avanzar_a(nuevo_estado):
            raise DatosInvalidos("Cambio de estado no permitido")
        self.solicitudes.guardar_solicitud(solicitud)

    def asignar_responsable(self, id_solicitud, id_responsable):
        solicitud = self.solicitudes.obtener_solicitud(id_solicitud)
        if solicitud is None:
            raise NoEncontrado("la solicitud", id_solicitud)
        responsable = self.responsables.obtener_responsable(id_responsable)
        if responsable is None:
            raise NoEncontrado("el responsable", id_responsable)
        solicitud.asignar_a(responsable)
        self.solicitudes.guardar_solicitud(solicitud)
        return responsable

    def listar_responsables(self):
        return self.responsables.listar_responsables()

    def buscar_por_estado(self, estado):
        return [solicitud for solicitud in self.solicitudes.listar_solicitudes() if solicitud.estado == estado]

    def buscar_por_tipo(self, tipo):
        return [solicitud for solicitud in self.solicitudes.listar_solicitudes() if solicitud.tipo == tipo]

    def buscar_por_legajo(self, legajo):
        return self._solicitudes_del_legajo(legajo)

    def resumen(self):
        solicitudes = self.solicitudes.listar_solicitudes()
        return ResumenReporte(
            pendientes=len([solicitud for solicitud in solicitudes if solicitud.estado == Estado.PENDIENTE.value]),
            en_proceso=len([solicitud for solicitud in solicitudes if solicitud.estado == Estado.EN_PROCESO.value]),
            finalizadas=len([solicitud for solicitud in solicitudes if solicitud.estado == Estado.FINALIZADA.value]),
        )

    def cantidad_de_solicitudes(self, legajo):
        return len(self._solicitudes_del_legajo(legajo))
