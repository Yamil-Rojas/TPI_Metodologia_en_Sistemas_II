import json
import os

from modelos import Estado, Prioridad
from validaciones import legajo_valido, mensaje_de_error

ARCHIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos.json")


class Sistema:
    def __init__(self, archivo=ARCHIVO):
        self.archivo = archivo

    def _cargar_datos(self):
        try:
            entrada = open(self.archivo, "r", encoding="utf-8")
            datos = json.load(entrada)
            entrada.close()
        except:
            datos = {"estudiantes": [], "responsables": [], "solicitudes": []}
        return datos

    def _guardar_datos(self, datos):
        salida = open(self.archivo, "w", encoding="utf-8")
        json.dump(datos, salida, indent=2, ensure_ascii=False)
        salida.close()

    def _mostrar_solicitudes(self, solicitudes):
        for solicitud in solicitudes:
            print("ID", solicitud["id"], "| legajo", solicitud["legajo"], "| tipo", solicitud["tipo"], "| prioridad", solicitud["prioridad"], "| estado", solicitud["estado"], "| responsable", solicitud["responsable"])
        if len(solicitudes) == 0:
            print("Sin resultados")

    def _asegurar_estudiante(self, datos, datos_solicitud):
        for estudiante in datos["estudiantes"]:
            if estudiante["legajo"] == datos_solicitud.legajo:
                return
        datos["estudiantes"].append({
            "legajo": datos_solicitud.legajo,
            "nombre": datos_solicitud.nombre,
            "email": datos_solicitud.email,
        })

    def _proximo_id(self, datos):
        nuevo_id = 1
        for solicitud in datos["solicitudes"]:
            if solicitud["id"] >= nuevo_id:
                nuevo_id = solicitud["id"] + 1
        return nuevo_id

    def _crear_solicitud(self, nuevo_id, datos_solicitud, plazo):
        return {
            "id": nuevo_id,
            "legajo": datos_solicitud.legajo,
            "tipo": datos_solicitud.tipo,
            "prioridad": datos_solicitud.prioridad,
            "descripcion": datos_solicitud.descripcion,
            "area": datos_solicitud.area,
            "fecha": datos_solicitud.fecha,
            "estado": Estado.PENDIENTE.value,
            "responsable": None,
            "plazo_dias": plazo,
        }

    def registrar_solicitud(self, datos_solicitud):
        error = mensaje_de_error(datos_solicitud)
        if error is not None:
            print(error)
            return None
        datos = self._cargar_datos()
        self._asegurar_estudiante(datos, datos_solicitud)
        nuevo_id = self._proximo_id(datos)
        plazo = self.calcular_plazo(datos_solicitud.tipo, datos_solicitud.prioridad)
        datos["solicitudes"].append(self._crear_solicitud(nuevo_id, datos_solicitud, plazo))
        self._guardar_datos(datos)
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
        datos = self._cargar_datos()
        for solicitud in datos["solicitudes"]:
            if solicitud["id"] == id_solicitud:
                if solicitud["estado"] == Estado.PENDIENTE.value and nuevo_estado == Estado.EN_PROCESO.value:
                    solicitud["estado"] = Estado.EN_PROCESO.value
                elif solicitud["estado"] == Estado.EN_PROCESO.value and nuevo_estado == Estado.FINALIZADA.value:
                    solicitud["estado"] = Estado.FINALIZADA.value
                else:
                    print("Cambio de estado no permitido")
                    return
                self._guardar_datos(datos)
                print("Estado actualizado")

    def asignar_responsable(self, id_solicitud, id_responsable):
        datos = self._cargar_datos()
        responsable = None
        for candidato in datos["responsables"]:
            if candidato["id"] == id_responsable:
                responsable = candidato
        for solicitud in datos["solicitudes"]:
            if solicitud["id"] == id_solicitud:
                solicitud["responsable"] = responsable["nombre"]
                solicitud["area"] = responsable["area"]
                self._guardar_datos(datos)
                print("Responsable asignado:", responsable["nombre"])

    def listar_responsables(self):
        datos = self._cargar_datos()
        for responsable in datos["responsables"]:
            print(responsable["id"], "-", responsable["nombre"], "(" + responsable["area"] + ")")

    def buscar_por_estado(self, estado):
        datos = self._cargar_datos()
        resultados = []
        for solicitud in datos["solicitudes"]:
            if solicitud["estado"] == estado:
                resultados.append(solicitud)
        self._mostrar_solicitudes(resultados)

    def buscar_por_tipo(self, tipo):
        datos = self._cargar_datos()
        resultados = []
        for solicitud in datos["solicitudes"]:
            if solicitud["tipo"] == tipo:
                resultados.append(solicitud)
        self._mostrar_solicitudes(resultados)

    def buscar_por_legajo(self, legajo):
        if not legajo_valido(legajo):
            print("Legajo invalido")
            return
        datos = self._cargar_datos()
        resultados = []
        for solicitud in datos["solicitudes"]:
            if solicitud["legajo"] == legajo:
                resultados.append(solicitud)
        self._mostrar_solicitudes(resultados)

    def reporte(self):
        datos = self._cargar_datos()
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
            if not legajo_valido(legajo):
                print("Legajo invalido")
                return
            cantidad = 0
            for solicitud in datos["solicitudes"]:
                if solicitud["legajo"] == legajo:
                    cantidad = cantidad + 1
            print("Solicitudes del legajo", legajo + ":", cantidad)
