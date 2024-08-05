import json
import os
import itertools
import sys
import time
import xlsxwriter

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
                    print("El archivo cookies.json no contiene las cookies necesarias")
                    print("Por favor, ingresa las cookies de Mindbox en el archivo cookies.json o mediante la consola")
                    return True
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

    def setCookies(self, cookies):
        with open('cookies.json', 'r') as f:
            data = json.load(f)
            data['INGRESSCOOKIE'] = cookies['INGRESSCOOKIE']
            data['XSRF-TOKEN'] = cookies['XSRF-TOKEN']
            data['mbid_11_session'] = cookies['mbid_11_session']
            data['_token'] = cookies['_token']
        with open('cookies.json', 'w') as f:
            json.dump(data, f, indent=4)
        print("Cookies guardadas correctamente")

    def cookiesPrompt(self):
        print("Por favor, ingresa las cookies de Mindbox")
        print("Si no estas seguro de como obtener las cookies, visita el siguiente enlace: \033]8;;https://github.com/NexWan/MindScrap\033\\https://github.com/NexWan/MindScrap\033]8;;\033\\")
        ingress = input("Ingresa la cookie INGRESSCOOKIE: ")
        xsrf = input("Ingresa la cookie XSRF-TOKEN: ")
        session = input("Ingresa la cookie mbid_11_session: ")
        token = input("Ingresa la cookie _token: ")
        cookies = {
            "INGRESSCOOKIE": ingress,
            "XSRF-TOKEN": xsrf,
            "mbid_11_session": session,
            "_token": token
        }
        self.setCookies(cookies)

    def createExcel(self, data):
        workbook = xlsxwriter.Workbook('horarios.xlsx')
        bold = workbook.add_format({'bold': True})
        for i, schedule in enumerate(data, start=1):
            worksheet = workbook.add_worksheet(f'Horario {i}')

             # Set column widths
            worksheet.set_column('A:A', 30)  # Materia
            worksheet.set_column('B:B', 30)  # Profesor
            worksheet.set_column('C:G', 15)  # Lunes to Viernes

            worksheet.write('A1', 'Materia', bold)
            worksheet.write('B1', 'Profesor', bold)
            worksheet.write('C1', 'Lunes', bold)
            worksheet.write('D1', 'Martes', bold)
            worksheet.write('E1', 'Miércoles', bold)
            worksheet.write('F1', 'Jueves', bold)
            worksheet.write('G1', 'Viernes', bold)

            row = 1
            for materia in schedule:
                worksheet.write(row, 0, materia['Materia'])
                worksheet.write(row, 1, materia['Profesor'])
                worksheet.write(row, 2, materia['Horario'].get('Lunes', ''))
                worksheet.write(row, 3, materia['Horario'].get('Martes', ''))
                worksheet.write(row, 4, materia['Horario'].get('Miercoles', ''))
                worksheet.write(row, 5, materia['Horario'].get('Jueves', ''))
                worksheet.write(row, 6, materia['Horario'].get('Viernes', ''))
                row += 1

        workbook.close()
        print("Archivo horarios.xlsx creado")
