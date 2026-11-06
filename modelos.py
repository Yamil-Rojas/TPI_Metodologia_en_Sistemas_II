from dataclasses import dataclass
from enum import Enum


class Estado(Enum):
    PENDIENTE = "pen"
    EN_PROCESO = "pro"
    FINALIZADA = "fin"


class Prioridad(Enum):
    ALTA = 1
    MEDIA = 2
    BAJA = 3


@dataclass
class DatosSolicitud:
    nombre: str
    legajo: str
    email: str
    tipo: str
    prioridad: int
    descripcion: str
    area: str
    fecha: str


@dataclass
class Solicitud:
    id: int
    legajo: str
    tipo: str
    prioridad: int
    descripcion: str
    area: str
    fecha: str
    estado: str = Estado.PENDIENTE.value
    responsable: str = None
    plazo_dias: int = None

    def avanzar_a(self, nuevo_estado):
        """Aplica el cambio de estado si esta permitido. Devuelve True o False."""
        pendiente_a_proceso = self.estado == Estado.PENDIENTE.value and nuevo_estado == Estado.EN_PROCESO.value
        proceso_a_final = self.estado == Estado.EN_PROCESO.value and nuevo_estado == Estado.FINALIZADA.value
        if not (pendiente_a_proceso or proceso_a_final):
            return False
        self.estado = nuevo_estado
        return True

    def asignar_a(self, responsable):
        self.responsable = responsable.nombre
        self.area = responsable.area


@dataclass
class Estudiante:
    legajo: str
    nombre: str
    email: str


@dataclass
class Responsable:
    id: int
    nombre: str
    area: str
