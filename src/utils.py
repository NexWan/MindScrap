import json
import os
import itertools
import sys
import time

class Utils:
    def __init__(self) -> None:
        pass

    def printNotExistingMessage(self):
        print("\033c", end="")
        print("No existe el archivo cookies.json")
        print("A continuacion se creara el archivo cookies.json")

    def printFileEmptyMessage(self):
        print("\033c", end="")
        print("El archivo cookies.json esta vacio o no contiene las cookies necesarias")
        print("Por favor, ingresa las cookies de Mindbox en el archivo cookies.json")
        print("Si no estas seguro de como obtener las cookies, visita el siguiente enlace: \033]8;;https://github.com/NexWan/MindScrap\033\\https://github.com/NexWan/MindScrap\033]8;;\033\\")
        exit(0)

    def checkCookiesFile(self):
        # Check if the cookies file exists
        if not os.path.exists('cookies.json'):
            self.printNotExistingMessage()
            self.initConfig()
            return False
        # Check if the cookies file is empty
        if os.path.getsize('cookies.json') == 0:
            self.printFileEmptyMessage()
            return False
        try:
            with open('cookies.json', 'r') as f:
                cookies = json.load(f)
                token = cookies.get('INGRESSCOOKIE')
                xsrf = cookies.get('XSRF-TOKEN')
                session = cookies.get('mbid_11_session')
                if token and xsrf and session:
                    return True
                else:
                    self.printFileEmptyMessage()
                    exit(0)
                    return False
        except:
            return False

    def initConfig(self):
        # Initialize the configuration
        open('cookies.json', 'w').close()
        path = os.path.abspath('cookies.json')
        toWrite = {
            "INGRESSCOOKIE": "",
            "XSRF-TOKEN": "",
            "mbid_11_session": "",
            "_token": ""
        }
        with open('cookies.json', 'w') as f:
            json.dump(toWrite, f, indent=4)
        print(f"Archivo de cookies creado en {path}")
        print("Por favor, ingresa las cookies de Mindbox en el archivo cookies.json")
        print("Si no estas seguro de como obtener las cookies, visita el siguiente enlace: \033]8;;https://github.com/NexWan/MindScrap\033\\https://github.com/NexWan/MindScrap\033]8;;\033\\")
        exit(0)

    def mostrar_cargando(stop_event):
        for simbolo in itertools.cycle(['|', '/', '-', '\\']):
            if stop_event.is_set():
                break
            sys.stdout.write(f'\rCargando {simbolo}')
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\rListo!     \n')

    def generateSchedule(materias_seleccionadas):
        return None
    
    def preventOverlapse(self, time1, time2):
        start1, end1 = time1.split('-')
        start2, end2 = time2.split('-')
        return not (end1 <= start2 or end2 <= start1)

    def overlapseWithSome(self, schedule, schedules):
        for s in schedules:
            for day in schedule:
                if schedule[day] and s[day] and self.preventOverlapse(schedule[day], s[day]):
                    return True
        return False

    def genCombinations(self, materias, num_materias):
        def backtrack(actual, index, used):
            if len(actual) == num_materias:
                combinations.append(actual[:])
                return
            if index == len(materias):
                return
            for i in range(index, len(materias)):
                if materias[i]["Materia"] not in used and not self.overlapseWithSome(materias[i]["Horario"], [h["Horario"] for h in actual]):
                    actual.append(materias[i])
                    used.add(materias[i]["Materia"])
                    backtrack(actual, i + 1, used)
                    actual.pop()
                    used.remove(materias[i]["Materia"])

        combinations = []
        backtrack([], 0, set())
        return combinations
    
    def createJson(self, data):
        labeled_data = {}
        for i, schedule in enumerate(data, start=1):
            labeled_data[f"Horario {i}"] = schedule

        with open('horarios.json', 'w') as f:
            json.dump(labeled_data, f, indent=4, ensure_ascii=False)

        print("Archivo horarios.json creado")
