from enum import Enum


class Estado(Enum):
    PENDIENTE = "pen"
    EN_PROCESO = "pro"
    FINALIZADA = "fin"


class Prioridad(Enum):
    ALTA = 1
    MEDIA = 2
    BAJA = 3
