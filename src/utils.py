import json
import os

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