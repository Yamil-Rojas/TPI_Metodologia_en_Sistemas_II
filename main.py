"""Unica capa que imprime y lee del teclado."""
import os
from datetime import date

from errores import ErrorDeSistema
from modelos import TIPOS, DatosSolicitud
from repositorio import RepositorioJSON
from servicio import ServicioSolicitudes

RUTA_DATOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos.json")
PEDIDO_TIPO = "Tipo (" + "/".join(TIPOS) + "): "


def mostrar_menu():
    print()
    print("=== Gestion de Solicitudes Academicas ===")
    print("1. Registrar solicitud")
    print("2. Cambiar estado")
    print("3. Asignar responsable")
    print("4. Buscar solicitudes")
    print("5. Reporte basico")
    print("6. Ver responsables")
    print("0. Salir")


def pedir_entero_o_cero(mensaje):
    try:
        return int(input(mensaje))
    except ValueError:
        return 0


def mostrar_solicitudes(solicitudes):
    for solicitud in solicitudes:
        print(
            "ID", solicitud.id,
            "| legajo", solicitud.legajo,
            "| tipo", solicitud.tipo,
            "| prioridad", solicitud.prioridad,
            "| estado", solicitud.estado,
            "| responsable", solicitud.responsable,
        )
    if len(solicitudes) == 0:
        print("Sin resultados")


def pedir_datos_de_solicitud():
    nombre = input("Nombre: ")
    legajo = input("Legajo (5 digitos): ")
    email = input("Email: ")
    tipo = input(PEDIDO_TIPO)
    prioridad = pedir_entero_o_cero("Prioridad (1=alta, 2=media, 3=baja): ")
    descripcion = input("Descripcion: ")
    area = input("Area: ")
    return DatosSolicitud(
        nombre=nombre,
        legajo=legajo,
        email=email,
        tipo=tipo,
        prioridad=prioridad,
        descripcion=descripcion,
        area=area,
        fecha=date.today().isoformat(),
    )


def registrar(servicio):
    solicitud = servicio.registrar_solicitud(pedir_datos_de_solicitud())
    print("Solicitud registrada con ID", solicitud.id, "- plazo:", solicitud.plazo_dias, "dias")


def cambiar_estado(servicio):
    id_solicitud = pedir_entero_o_cero("ID de la solicitud: ")
    nuevo_estado = input("Nuevo estado (pro/fin): ")
    servicio.cambiar_estado(id_solicitud, nuevo_estado)
    print("Estado actualizado")


def asignar_responsable(servicio):
    try:
        id_solicitud = int(input("ID de la solicitud: "))
        id_responsable = int(input("ID del responsable: "))
    except ValueError:
        id_solicitud = 0
        id_responsable = 0
    responsable = servicio.asignar_responsable(id_solicitud, id_responsable)
    print("Responsable asignado:", responsable.nombre)


def buscar(servicio):
    print("a. Por estado  b. Por tipo  c. Por legajo")
    criterio = input("Criterio: ")
    if criterio == "a":
        mostrar_solicitudes(servicio.buscar_por_estado(input("Estado (pen/pro/fin): ")))
    elif criterio == "b":
        mostrar_solicitudes(servicio.buscar_por_tipo(input(PEDIDO_TIPO)))
    elif criterio == "c":
        mostrar_solicitudes(servicio.buscar_por_legajo(input("Legajo: ")))
    else:
        print("Criterio invalido")


def reporte(servicio):
    resumen = servicio.resumen()
    print("--- REPORTE ---")
    print("Pendientes:", resumen.pendientes)
    print("En proceso:", resumen.en_proceso)
    print("Finalizadas:", resumen.finalizadas)
    print("Total:", resumen.total)
    legajo = input("Legajo para ver su cantidad de solicitudes (Enter para omitir): ")
    if legajo != "":
        print("Solicitudes del legajo", legajo + ":", servicio.cantidad_de_solicitudes(legajo))


def ver_responsables(servicio):
    for responsable in servicio.listar_responsables():
        print(responsable.id, "-", responsable.nombre, "(" + responsable.area + ")")


ACCIONES = {
    "1": registrar,
    "2": cambiar_estado,
    "3": asignar_responsable,
    "4": buscar,
    "5": reporte,
    "6": ver_responsables,
}


def main():
    repositorio = RepositorioJSON(RUTA_DATOS)
    servicio = ServicioSolicitudes(repositorio, repositorio, repositorio)
    while True:
        mostrar_menu()
        opcion = input("Opcion: ")
        if opcion == "0":
            print("Hasta luego")
            break
        accion = ACCIONES.get(opcion)
        if accion is None:
            print("Opcion invalida")
            continue
        try:
            accion(servicio)
        except ErrorDeSistema as error:
            print(error)


if __name__ == "__main__":
    main()
