import requests as req
import json
import os
from bs4 import BeautifulSoup
from unidecode import unidecode
import re
import time

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

    def getSearchToken(self):
        with open('cookies.json', 'r') as f:
            cookies = json.load(f)
            token = cookies.get('_token')
            return token
        return None

    def getHorario(self, semestre):
        print(f"Extrayendo datos de {semestre} semestre...")
        _token = self.getSearchToken() #I'm not sure if this token is static or works by session
        form_data = {
            'semester': str(semestre),
            '_token': _token
        }
        print(form_data)
        cookies = self.getCookies();
        response = req.post(self.url, cookies=cookies, data=form_data)
        data = self.extractTableData(response.text)
        self.parseToJson(data)
    
    def parseToJson(self, data, createFile=True):
        print("Convirtiendo a JSON...")
        json_data = []
        for row in data:
            print(row)
            if len(row) >= 10:
                json_row = {
                    "Materia": row[0],
                    "Profesor": row[1],
                    "Grupo": row[2],
                    "Semestre": row[3],
                    "Horario": {
                        "Lunes": row[4],
                        "Martes": row[5],
                        "Miercoles": row[6],
                        "Jueves": row[7],
                        "Viernes": row[8],
                    }
                }
                json_data.append(json_row)
        # Print or process the JSON data
        json_output = json.dumps(json_data, indent=4, ensure_ascii=False)
        if(createFile):
            self.createJson(json_data)
        else:
            return json_data

    def createJson(self, data):
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)
        print("Archivo data.json creado")

    def createJsonBySemesters(self, data):
        try:
            os.makedirs('semesters', exist_ok=True)
            for i in range(0, len(data)):
                with open(f'semesters/semestre_{i+1}.json', 'w') as f:
                    json.dump(data[i], f, indent=4)
                print(f"Archivo semestre_{i}.json creado")
            print("Archivos creados")
        except Exception as e:
            print(f"Error: {e}")


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
                print(cell)
                childrenSize = (len(list(cell.children)))
                # Collect text parts separately
                for element in cell.children:
                    if childrenSize == 1 and element.strip() == '': # If there's only one child, it's a string
                        cell_text_parts.append(" ")
                    if element.name == 'br':
                        continue  # Skip <br> tags
                    elif element.name == 'small':
                        if '/' in element.get_text(strip=True): continue
                        cell_text_parts.append(self.normalizeData(element.get_text(strip=True)))
                    elif isinstance(element, str) and element.strip() != '':
                        print(f"String: {element}")
                        cell_text_parts.append(self.normalizeData(element.strip()))
                    else:
                        cell_text_parts.append(self.normalizeData(element.get_text(strip=True)))
                # Join the parts to form the complete cell text
                for part in filter(None, cell_text_parts):
                        row_data.append(part)
            if row_data:
                table_data.append(row_data)
        
        return table_data
    
    def fetchSubjects(self, semester):
        cookies = self.getCookies()
        form_data = {
            'semester': semester,
            '_token': self.getSearchToken()
        }
        response = req.post(self.url, cookies=cookies, data=form_data)
        html_content = self.extractTableData(response.text)
        json = self.parseToJson(html_content, False)
        return json

    def getSubjectsBySemesters(self, semesters):
        subjects = []
        for semestre in semesters:
            subjects.extend(self.fetchSubjects(semestre))  # Asegúrate de extender la lista
        return self.groupSubjects(subjects)
    
    def groupSubjects(self, subjects):
        # Crear un diccionario para agrupar las materias por nombre
        grouped_subjects = {}
        for subject in subjects:
            materia = subject['Materia']
            if materia not in grouped_subjects:
                grouped_subjects[materia] = []
            grouped_subjects[materia].append(subject)
        # Crear una lista para guardar los resultados con identificadores
        result = []
        for materia, subjects in grouped_subjects.items():
            for idx, subject in enumerate(subjects, start=1):
                subject_with_id = {
                    "ID": idx,
                    "Materia": subject['Materia'],
                    "Profesor": subject['Profesor'],
                    "Horario": subject['Horario'],
                    "Semestre": subject['Semestre']
                }
                result.append(subject_with_id)
        return result
    
    def groupGroups(self, groups):
        grouped_groups = {}
        for group in groups:
            materia = group['Materia']
            if materia not in grouped_groups:
                grouped_groups[materia] = []
            grouped_groups[materia].append(group)
        return grouped_groups
    
    def getAllSemesters(self):
        semesters = []
        for i in range(1, 9):
            print(f"Extrayendo datos de {i} semestre...")
            _token = self.getSearchToken()
            form_data = {
                'semester': str(i),
                '_token': _token
            }
            cookies = self.getCookies();
            response = req.post(self.url, cookies=cookies, data=form_data)
            data = self.extractTableData(response.text)
            jsonData = self.parseToJson(data, False)
            semesters.append(jsonData)

        self.createJsonBySemesters(semesters)
        return semesters