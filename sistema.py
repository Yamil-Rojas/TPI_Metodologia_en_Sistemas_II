import json
import os

from modelos import Estado, Prioridad

ARCHIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos.json")


class Sistema:
    def __init__(self, archivo=ARCHIVO):
        self.archivo = archivo

    def registrar_solicitud(self, nombre, legajo, email, tipo, prioridad, descripcion, area, fecha):
        if len(legajo) != 5 or not legajo.isdigit():
            print("Legajo invalido")
            return None
        if nombre.strip() == "":
            print("El nombre no puede estar vacio")
            return None
        if "@" not in email:
            print("Email invalido")
            return None
        if tipo != "cert" and tipo != "equi" and tipo != "baja":
            print("Tipo invalido")
            return None
        if prioridad not in [valor.value for valor in Prioridad]:
            print("Prioridad invalida")
            return None
        if descripcion.strip() == "":
            print("La descripcion no puede estar vacia")
            return None
        try:
            entrada = open(self.archivo, "r", encoding="utf-8")
            datos = json.load(entrada)
            entrada.close()
        except:
            datos = {"estudiantes": [], "responsables": [], "solicitudes": []}
        existe = False
        for estudiante in datos["estudiantes"]:
            if estudiante["legajo"] == legajo:
                existe = True
        if not existe:
            datos["estudiantes"].append({"legajo": legajo, "nombre": nombre, "email": email})
        nuevo_id = 1
        for solicitud in datos["solicitudes"]:
            if solicitud["id"] >= nuevo_id:
                nuevo_id = solicitud["id"] + 1
        plazo = self.calcular_plazo(tipo, prioridad)
        nueva_solicitud = {
            "id": nuevo_id,
            "legajo": legajo,
            "tipo": tipo,
            "prioridad": prioridad,
            "descripcion": descripcion,
            "area": area,
            "fecha": fecha,
            "estado": Estado.PENDIENTE.value,
            "responsable": None,
            "plazo_dias": plazo,
        }
        datos["solicitudes"].append(nueva_solicitud)
        salida = open(self.archivo, "w", encoding="utf-8")
        json.dump(datos, salida, indent=2, ensure_ascii=False)
        salida.close()
        print("Solicitud registrada con ID", nuevo_id, "- plazo:", plazo, "dias")
        return nuevo_id

    def calcular_plazo(self, tipo, prioridad):
        if tipo == "cert":
            plazo = 5
        elif tipo == "equi":
            plazo = 15
        elif tipo == "baja":
            plazo = 3
        else:
            plazo = 10
        if prioridad == Prioridad.ALTA.value:
            plazo = plazo - 2
        elif prioridad == Prioridad.BAJA.value:
            plazo = plazo + 2
        if plazo < 1:
            plazo = 1
        return plazo

    def cambiar_estado(self, id_solicitud, nuevo_estado):
        try:
            entrada = open(self.archivo, "r", encoding="utf-8")
            datos = json.load(entrada)
            entrada.close()
        except:
            datos = {"estudiantes": [], "responsables": [], "solicitudes": []}
        for solicitud in datos["solicitudes"]:
            if solicitud["id"] == id_solicitud:
                if solicitud["estado"] == Estado.PENDIENTE.value and nuevo_estado == Estado.EN_PROCESO.value:
                    solicitud["estado"] = Estado.EN_PROCESO.value
                elif solicitud["estado"] == Estado.EN_PROCESO.value and nuevo_estado == Estado.FINALIZADA.value:
                    solicitud["estado"] = Estado.FINALIZADA.value
                else:
                    print("Cambio de estado no permitido")
                    return
                salida = open(self.archivo, "w", encoding="utf-8")
                json.dump(datos, salida, indent=2, ensure_ascii=False)
                salida.close()
                print("Estado actualizado")

    def asignar_responsable(self, id_solicitud, id_responsable):
        try:
            entrada = open(self.archivo, "r", encoding="utf-8")
            datos = json.load(entrada)
            entrada.close()
        except:
            datos = {"estudiantes": [], "responsables": [], "solicitudes": []}
        responsable = None
        for candidato in datos["responsables"]:
            if candidato["id"] == id_responsable:
                responsable = candidato
        for solicitud in datos["solicitudes"]:
            if solicitud["id"] == id_solicitud:
                solicitud["responsable"] = responsable["nombre"]
                solicitud["area"] = responsable["area"]
                salida = open(self.archivo, "w", encoding="utf-8")
                json.dump(datos, salida, indent=2, ensure_ascii=False)
                salida.close()
                print("Responsable asignado:", responsable["nombre"])

    def listar_responsables(self):
        try:
            entrada = open(self.archivo, "r", encoding="utf-8")
            datos = json.load(entrada)
            entrada.close()
        except:
            datos = {"estudiantes": [], "responsables": [], "solicitudes": []}
        for responsable in datos["responsables"]:
            print(responsable["id"], "-", responsable["nombre"], "(" + responsable["area"] + ")")

    def buscar_por_estado(self, estado):
        try:
            entrada = open(self.archivo, "r", encoding="utf-8")
            datos = json.load(entrada)
            entrada.close()
        except:
            datos = {"estudiantes": [], "responsables": [], "solicitudes": []}
        resultados = []
        for solicitud in datos["solicitudes"]:
            if solicitud["estado"] == estado:
                resultados.append(solicitud)
        for solicitud in resultados:
            print("ID", solicitud["id"], "| legajo", solicitud["legajo"], "| tipo", solicitud["tipo"], "| prioridad", solicitud["prioridad"], "| estado", solicitud["estado"], "| responsable", solicitud["responsable"])
        if len(resultados) == 0:
            print("Sin resultados")

    def buscar_por_tipo(self, tipo):
        try:
            entrada = open(self.archivo, "r", encoding="utf-8")
            datos = json.load(entrada)
            entrada.close()
        except:
            datos = {"estudiantes": [], "responsables": [], "solicitudes": []}
        resultados = []
        for solicitud in datos["solicitudes"]:
            if solicitud["tipo"] == tipo:
                resultados.append(solicitud)
        for solicitud in resultados:
            print("ID", solicitud["id"], "| legajo", solicitud["legajo"], "| tipo", solicitud["tipo"], "| prioridad", solicitud["prioridad"], "| estado", solicitud["estado"], "| responsable", solicitud["responsable"])
        if len(resultados) == 0:
            print("Sin resultados")

    def buscar_por_legajo(self, legajo):
        if len(legajo) != 5 or not legajo.isdigit():
            print("Legajo invalido")
            return
        try:
            entrada = open(self.archivo, "r", encoding="utf-8")
            datos = json.load(entrada)
            entrada.close()
        except:
            datos = {"estudiantes": [], "responsables": [], "solicitudes": []}
        resultados = []
        for solicitud in datos["solicitudes"]:
            if solicitud["legajo"] == legajo:
                resultados.append(solicitud)
        for solicitud in resultados:
            print("ID", solicitud["id"], "| legajo", solicitud["legajo"], "| tipo", solicitud["tipo"], "| prioridad", solicitud["prioridad"], "| estado", solicitud["estado"], "| responsable", solicitud["responsable"])
        if len(resultados) == 0:
            print("Sin resultados")

    def reporte(self):
        try:
            entrada = open(self.archivo, "r", encoding="utf-8")
            datos = json.load(entrada)
            entrada.close()
        except:
            datos = {"estudiantes": [], "responsables": [], "solicitudes": []}
        pendientes = 0
        en_proceso = 0
        finalizadas = 0
        for solicitud in datos["solicitudes"]:
            if solicitud["estado"] == Estado.PENDIENTE.value:
                pendientes = pendientes + 1
            elif solicitud["estado"] == Estado.EN_PROCESO.value:
                en_proceso = en_proceso + 1
            elif solicitud["estado"] == Estado.FINALIZADA.value:
                finalizadas = finalizadas + 1
        print("--- REPORTE ---")
        print("Pendientes:", pendientes)
        print("En proceso:", en_proceso)
        print("Finalizadas:", finalizadas)
        print("Total:", pendientes + en_proceso + finalizadas)
        legajo = input("Legajo para ver su cantidad de solicitudes (Enter para omitir): ")
        if legajo != "":
            if len(legajo) != 5 or not legajo.isdigit():
                print("Legajo invalido")
                return
            cantidad = 0
            for solicitud in datos["solicitudes"]:
                if solicitud["legajo"] == legajo:
                    cantidad = cantidad + 1
            print("Solicitudes del legajo", legajo + ":", cantidad)
