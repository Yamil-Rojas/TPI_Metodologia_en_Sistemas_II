from modelos import Prioridad


def legajo_valido(legajo):
    return len(legajo) == 5 and legajo.isdigit()


def mensaje_de_error(nombre, legajo, email, tipo, prioridad, descripcion):
    """Devuelve el mensaje del primer dato invalido, o None si todos son validos."""
    if not legajo_valido(legajo):
        return "Legajo invalido"
    if nombre.strip() == "":
        return "El nombre no puede estar vacio"
    if "@" not in email:
        return "Email invalido"
    if tipo != "cert" and tipo != "equi" and tipo != "baja":
        return "Tipo invalido"
    if prioridad not in [valor.value for valor in Prioridad]:
        return "Prioridad invalida"
    if descripcion.strip() == "":
        return "La descripcion no puede estar vacia"
    return None
