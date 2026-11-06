from modelos import TIPOS, Prioridad


def legajo_valido(legajo):
    return len(legajo) == 5 and legajo.isdigit()


def mensaje_de_error(datos_solicitud):
    """Devuelve el mensaje del primer dato invalido, o None si todos son validos."""
    if not legajo_valido(datos_solicitud.legajo):
        return "Legajo invalido"
    if datos_solicitud.nombre.strip() == "":
        return "El nombre no puede estar vacio"
    if "@" not in datos_solicitud.email:
        return "Email invalido"
    if datos_solicitud.tipo not in TIPOS:
        return "Tipo invalido"
    if datos_solicitud.prioridad not in [valor.value for valor in Prioridad]:
        return "Prioridad invalida"
    if datos_solicitud.descripcion.strip() == "":
        return "La descripcion no puede estar vacia"
    return None
