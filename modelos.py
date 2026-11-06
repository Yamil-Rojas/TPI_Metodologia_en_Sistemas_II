from abc import ABC
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

    @property
    def ajuste_de_plazo(self):
        """Dias que suma o resta esta prioridad al plazo base del tipo."""
        return {Prioridad.ALTA: -2, Prioridad.MEDIA: 0, Prioridad.BAJA: 2}[self]


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


PLAZO_MINIMO_DIAS = 1


class TipoSolicitud(ABC):
    """Contrato: cada tipo tiene un codigo y un plazo base; el plazo final nunca baja del minimo."""

    codigo: str
    plazo_base_dias: int

    def calcular_plazo(self, prioridad):
        return max(PLAZO_MINIMO_DIAS, self.plazo_base_dias + prioridad.ajuste_de_plazo)


class Certificado(TipoSolicitud):
    codigo = "cert"
    plazo_base_dias = 5


class Equivalencia(TipoSolicitud):
    codigo = "equi"
    plazo_base_dias = 15


class BajaMateria(TipoSolicitud):
    codigo = "baja"
    plazo_base_dias = 3


# Para agregar un tipo nuevo: crear su clase y sumarla a esta lista.
TIPOS = {tipo.codigo: tipo for tipo in (Certificado(), Equivalencia(), BajaMateria())}


@dataclass
class ResumenReporte:
    pendientes: int
    en_proceso: int
    finalizadas: int

    @property
    def total(self):
        return self.pendientes + self.en_proceso + self.finalizadas
