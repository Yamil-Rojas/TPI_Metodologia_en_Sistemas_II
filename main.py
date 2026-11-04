from datetime import date

from sistema import Sistema


def main():
    s = Sistema()
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
        op = input("Opcion: ")

        if op == "1":
            nombre = input("Nombre: ")
            legajo = input("Legajo (5 digitos): ")
            email = input("Email: ")
            tipo = input("Tipo (cert/equi/baja): ")
            try:
                prioridad = int(input("Prioridad (1=alta, 2=media, 3=baja): "))
            except:
                prioridad = 0
            descripcion = input("Descripcion: ")
            area = input("Area: ")
            s.registrar_solicitud(nombre, legajo, email, tipo, prioridad, descripcion, area, date.today().isoformat())
        elif op == "2":
            try:
                i = int(input("ID de la solicitud: "))
            except:
                i = 0
            e = input("Nuevo estado (pro/fin): ")
            s.proc(i, e)
        elif op == "3":
            try:
                i = int(input("ID de la solicitud: "))
                r = int(input("ID del responsable: "))
            except:
                i = 0
                r = 0
            s.asignar_responsable(i, r)
        elif op == "4":
            print("a. Por estado  b. Por tipo  c. Por legajo")
            c = input("Criterio: ")
            if c == "a":
                s.buscar_por_estado(input("Estado (pen/pro/fin): "))
            elif c == "b":
                s.buscar_por_tipo(input("Tipo (cert/equi/baja): "))
            elif c == "c":
                s.buscar_por_legajo(input("Legajo: "))
            else:
                print("Criterio invalido")
        elif op == "5":
            s.reporte()
        elif op == "6":
            s.listar_responsables()
        elif op == "0":
            print("Hasta luego")
            break
        else:
            print("Opcion invalida")


if __name__ == "__main__":
    main()
