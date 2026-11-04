import json
import os

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
        if prioridad != 1 and prioridad != 2 and prioridad != 3:
            print("Prioridad invalida")
            return None
        if descripcion.strip() == "":
            print("La descripcion no puede estar vacia")
            return None
        try:
            f = open(self.archivo, "r", encoding="utf-8")
            d = json.load(f)
            f.close()
        except:
            d = {"estudiantes": [], "responsables": [], "solicitudes": []}
        existe = False
        for x in d["estudiantes"]:
            if x["legajo"] == legajo:
                existe = True
        if not existe:
            d["estudiantes"].append({"legajo": legajo, "nombre": nombre, "email": email})
        n = 1
        for x in d["solicitudes"]:
            if x["id"] >= n:
                n = x["id"] + 1
        plazo = self.calcular_plazo(tipo, prioridad)
        nueva = {
            "id": n,
            "legajo": legajo,
            "tipo": tipo,
            "prioridad": prioridad,
            "descripcion": descripcion,
            "area": area,
            "fecha": fecha,
            "estado": "pen",
            "responsable": None,
            "plazo_dias": plazo,
        }
        d["solicitudes"].append(nueva)
        f = open(self.archivo, "w", encoding="utf-8")
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.close()
        print("Solicitud registrada con ID", n, "- plazo:", plazo, "dias")
        return n

    def calcular_plazo(self, tipo, prioridad):
        if tipo == "cert":
            p = 5
        elif tipo == "equi":
            p = 15
        elif tipo == "baja":
            p = 3
        else:
            p = 10
        if prioridad == 1:
            p = p - 2
        elif prioridad == 3:
            p = p + 2
        if p < 1:
            p = 1
        return p

    def proc(self, i, e):
        try:
            f = open(self.archivo, "r", encoding="utf-8")
            d = json.load(f)
            f.close()
        except:
            d = {"estudiantes": [], "responsables": [], "solicitudes": []}
        for x in d["solicitudes"]:
            if x["id"] == i:
                if x["estado"] == "pen" and e == "pro":
                    x["estado"] = "pro"
                elif x["estado"] == "pro" and e == "fin":
                    x["estado"] = "fin"
                else:
                    print("Cambio de estado no permitido")
                    return
                f = open(self.archivo, "w", encoding="utf-8")
                json.dump(d, f, indent=2, ensure_ascii=False)
                f.close()
                print("Estado actualizado")

    def asignar_responsable(self, id_solicitud, id_responsable):
        try:
            f = open(self.archivo, "r", encoding="utf-8")
            d = json.load(f)
            f.close()
        except:
            d = {"estudiantes": [], "responsables": [], "solicitudes": []}
        r = None
        for x in d["responsables"]:
            if x["id"] == id_responsable:
                r = x
        for x in d["solicitudes"]:
            if x["id"] == id_solicitud:
                x["responsable"] = r["nombre"]
                x["area"] = r["area"]
                f = open(self.archivo, "w", encoding="utf-8")
                json.dump(d, f, indent=2, ensure_ascii=False)
                f.close()
                print("Responsable asignado:", r["nombre"])

    def listar_responsables(self):
        try:
            f = open(self.archivo, "r", encoding="utf-8")
            d = json.load(f)
            f.close()
        except:
            d = {"estudiantes": [], "responsables": [], "solicitudes": []}
        for x in d["responsables"]:
            print(x["id"], "-", x["nombre"], "(" + x["area"] + ")")

    def buscar_por_estado(self, e):
        try:
            f = open(self.archivo, "r", encoding="utf-8")
            d = json.load(f)
            f.close()
        except:
            d = {"estudiantes": [], "responsables": [], "solicitudes": []}
        lst = []
        for x in d["solicitudes"]:
            if x["estado"] == e:
                lst.append(x)
        for x in lst:
            print("ID", x["id"], "| legajo", x["legajo"], "| tipo", x["tipo"], "| prioridad", x["prioridad"], "| estado", x["estado"], "| responsable", x["responsable"])
        if len(lst) == 0:
            print("Sin resultados")

    def buscar_por_tipo(self, t):
        try:
            f = open(self.archivo, "r", encoding="utf-8")
            d = json.load(f)
            f.close()
        except:
            d = {"estudiantes": [], "responsables": [], "solicitudes": []}
        lst = []
        for x in d["solicitudes"]:
            if x["tipo"] == t:
                lst.append(x)
        for x in lst:
            print("ID", x["id"], "| legajo", x["legajo"], "| tipo", x["tipo"], "| prioridad", x["prioridad"], "| estado", x["estado"], "| responsable", x["responsable"])
        if len(lst) == 0:
            print("Sin resultados")

    def buscar_por_legajo(self, l):
        if len(l) != 5 or not l.isdigit():
            print("Legajo invalido")
            return
        try:
            f = open(self.archivo, "r", encoding="utf-8")
            d = json.load(f)
            f.close()
        except:
            d = {"estudiantes": [], "responsables": [], "solicitudes": []}
        lst = []
        for x in d["solicitudes"]:
            if x["legajo"] == l:
                lst.append(x)
        for x in lst:
            print("ID", x["id"], "| legajo", x["legajo"], "| tipo", x["tipo"], "| prioridad", x["prioridad"], "| estado", x["estado"], "| responsable", x["responsable"])
        if len(lst) == 0:
            print("Sin resultados")

    def reporte(self):
        try:
            f = open(self.archivo, "r", encoding="utf-8")
            d = json.load(f)
            f.close()
        except:
            d = {"estudiantes": [], "responsables": [], "solicitudes": []}
        a = 0
        b = 0
        c = 0
        for x in d["solicitudes"]:
            if x["estado"] == "pen":
                a = a + 1
            elif x["estado"] == "pro":
                b = b + 1
            elif x["estado"] == "fin":
                c = c + 1
        print("--- REPORTE ---")
        print("Pendientes:", a)
        print("En proceso:", b)
        print("Finalizadas:", c)
        print("Total:", a + b + c)
        l = input("Legajo para ver su cantidad de solicitudes (Enter para omitir): ")
        if l != "":
            if len(l) != 5 or not l.isdigit():
                print("Legajo invalido")
                return
            k = 0
            for x in d["solicitudes"]:
                if x["legajo"] == l:
                    k = k + 1
            print("Solicitudes del legajo", l + ":", k)
