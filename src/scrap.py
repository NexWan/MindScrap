import requests as req
import json
from bs4 import BeautifulSoup
from unidecode import unidecode
import re

class Scrap:
    def __init__(self, url):
        self.url = url

    def to_camel_case(self,text):
        words = text.split()
        if not words:
            return ''
        return ' '.join(word.capitalize() for word in words)


    def normalizeData(self, data):
        # Normalize the data
        data = unidecode(data)
        data = data.strip()
        data = re.sub(r'\s+', ' ', data)
        data = self.to_camel_case(data)
        return data

    def getCookies(self):
        with open('cookies.json', 'r') as f:
            cookies = json.load(f)
            token = cookies.get('INGRESSCOOKIE')
            xsrf = cookies.get('XSRF-TOKEN')
            session = cookies.get('mbid_11_session')
            cookies = {
                'INGRESSCOOKIE': token,
                'XSRF-TOKEN': xsrf,
                'mbid_11_session': session
            }
            return cookies
        return None

    def testConnection(self):
        cookies = self.getCookies();
        response = req.get(self.url, cookies=cookies)
        print(response.text)

    def getHorario(self, semestre):
        print(f"Extrayendo datos de {semestre} semestre...")
        _token = 'MTLYLyxv3DDa9KLnPoFk00l19A5IhVENPcEcnnZf' #I'm not sure if this token is static or works by session
        form_data = {
            'semester': str(semestre),
            '_token': _token
        }
        print(form_data)
        cookies = self.getCookies();
        response = req.post(self.url, cookies=cookies, data=form_data)
        data = self.extractTableData(response.text)
        self.parseToJson(data)
    
    def parseToJson(self, data):
        print("Convirtiendo a JSON...")
        json_data = []
        for row in data:
            if len(row) >= 10:
                json_row = {
                    "Materia": f"{row[0]} {row[1]}",
                    "Profesor": row[2],
                    "Grupo": row[3],
                    "Semestre": row[4],
                    "Horario": {
                        "Lunes": row[5],
                        "Martes": row[7],
                        "Miercoles": row[9],
                        "Jueves": row[11],
                        "Viernes": row[13] if len(row) > 13 else None
                    }
                }
                json_data.append(json_row)
        # Print or process the JSON data
        json_output = json.dumps(json_data, indent=4, ensure_ascii=False)
        self.createJson(json_data)

    def createJson(self, data):
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)
        print("Archivo data.json creado")

    def notValidCookie(self):
        print("Las cookies dadas no son validas, favor de revisarlas")
        print("Si tienes dudas de como obtener las cookies, visita el siguiente enlace: \033]8;;https://github.com/NexWan/MindScrap\033\\https://github.com/NexWan/MindScrap\033]8;;\033\\")
        print("Saliendo...")
        exit(0)

    def extractTableData(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        # Find the table with the specified class
        table = soup.find('table', class_='table table-bordered table-striped default')
        if not table:
            self.notValidCookie()
            print("Table not found")
            return []
        table_data = []
        # Iterate through each row in the table
        for row in table.find_all('tr'):
            row_data = []
            # Iterate through each cell in the row
            for cell in row.find_all('td'):
                cell_text_parts = []
                # Collect text parts separately
                for element in cell.children:
                    if element.name == 'br':
                        continue  # Skip <br> tags
                    elif element.name == 'small':
                        cell_text_parts.append(self.normalizeData(element.get_text(strip=True)))
                    elif isinstance(element, str):
                        cell_text_parts.append(self.normalizeData(element.strip()))
                    else:
                        cell_text_parts.append(self.normalizeData(element.get_text(strip=True)))
                # Append each part as a separate value in the row_data list
                for part in filter(None, cell_text_parts):
                    row_data.append(part)
            if row_data:
                table_data.append(row_data)
        return table_data
