import json

class Utils:
    def __init__(self) -> None:
        pass

    def checkCookiesFile(self):
        # Check if the cookies file exists
        try:
            with open('cookies.json', 'r') as f:
                cookies = json.load(f)
                token = cookies.get('INGRESSCOOKIE')
                xsrf = cookies.get('XSRF-TOKEN')
                session = cookies.get('mbid_11_session')
                if token and xsrf and session:
                    return True
                else:
                    return False
        except:
            return False

    def initConfig(self):
        # Initialize the configuration
        open('cookies.json', 'w').close()
        print("Archivo de configuracion creado")
        print("Por favor, ingresa las cookies de Mindbox en el archivo cookies.json")
        exit(0)