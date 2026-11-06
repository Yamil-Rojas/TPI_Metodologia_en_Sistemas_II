import os
from datetime import date

from modelos import TIPOS, DatosSolicitud
from repositorio import RepositorioJSON
from servicio import ServicioSolicitudes

RUTA_DATOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos.json")


def main():
    repositorio = RepositorioJSON(RUTA_DATOS)
    sistema = ServicioSolicitudes(repositorio, repositorio, repositorio)
    while True:
        print()
        print("=== Gestion de Solicitudes Academicas ===")
        print("1. Registrar solicitud")
        print("2. Cambiar estado")
        print("3. Asignar responsable")
        print("4. Buscar solicitudes")
        print("5. Reporte basico")
        print("6. Ver responsables")
        print("0. Salir")
        opcion = input("Opcion: ")

        if opcion == "1":
            nombre = input("Nombre: ")
            legajo = input("Legajo (5 digitos): ")
            email = input("Email: ")
            tipo = input("Tipo (" + "/".join(TIPOS) + "): ")
            try:
                prioridad = int(input("Prioridad (1=alta, 2=media, 3=baja): "))
            except:
                prioridad = 0
            descripcion = input("Descripcion: ")
            area = input("Area: ")
            datos_solicitud = DatosSolicitud(
                nombre=nombre,
                legajo=legajo,
                email=email,
                tipo=tipo,
                prioridad=prioridad,
                descripcion=descripcion,
                area=area,
                fecha=date.today().isoformat(),
            )
            sistema.registrar_solicitud(datos_solicitud)
        elif opcion == "2":
            try:
                id_solicitud = int(input("ID de la solicitud: "))
            except:
                id_solicitud = 0
            nuevo_estado = input("Nuevo estado (pro/fin): ")
            sistema.cambiar_estado(id_solicitud, nuevo_estado)
        elif opcion == "3":
            try:
                id_solicitud = int(input("ID de la solicitud: "))
                id_responsable = int(input("ID del responsable: "))
            except:
                id_solicitud = 0
                id_responsable = 0
            sistema.asignar_responsable(id_solicitud, id_responsable)
        elif opcion == "4":
            print("a. Por estado  b. Por tipo  c. Por legajo")
            criterio = input("Criterio: ")
            if criterio == "a":
                sistema.buscar_por_estado(input("Estado (pen/pro/fin): "))
            elif criterio == "b":
                sistema.buscar_por_tipo(input("Tipo (" + "/".join(TIPOS) + "): "))
            elif criterio == "c":
                sistema.buscar_por_legajo(input("Legajo: "))
            else:
                print("Criterio invalido")
        elif opcion == "5":
            sistema.reporte()
        elif opcion == "6":
            sistema.listar_responsables()
        elif opcion == "0":
            print("Hasta luego")
            break
        else:
            print("Opcion invalida")


if __name__ == "__main__":
    main()
