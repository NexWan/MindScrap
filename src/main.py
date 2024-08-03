import scrap as sc
from colors import *
from utils import *
import time
import threading

def printWelcome2():
    # Secuencia de escape ANSI para limpiar la consola
    print("\033[H\033[J", end="")
    logo = """                              
                                          #@@@@#*++%@#"
                                     #@-................:%%
                                   +.........................-
                                 ................................
                               *...................................
             +      ................................................
           +.:.. -....................................................
          =.:.#+.......................................................
   ..:=+*@:.:%........#..................................................
-.       -:-+.........%:..................................................
        +:::@.........@.....=..............................................
        -.:.#%%@@@@%=.@...-%@@@@@@@*.........................................
        ++@..=@@@@@=..@.....@@@@@@.............................................#
        @....#@@@@@+..:.....@@@@@@...............................................@
      =#......:+*#.................................................................@%
      @...............................................................................%@
      @...................................................................................%#
       @...........................................................................................:
         *=................................................:=#%#=.+-.:+*#*%@@%@@##+:
              +%*=-:::::.....:=-:::::----=+#%@@@#%##%%+ """
    print(f"{colors.pink_color}{logo}{colors.reset_color}" + f"\n\n\n\n{colors.green_color}{('Herramienta creada por NexWan').center(100)}{colors.reset_color}")

def printWelcome():
    welcomeMessage = r"""
 __  __ _           _ ____                       
|  \/  (_)_ __   __| / ___|  ___ _ __ __ _ _ __  
| |\/| | | '_ \ / _` \___ \ / __| '__/ _` | '_ \ 
| |  | | | | | | (_| |___) | (__| | | (_| | |_) |
|_|  |_|_|_| |_|\__,_|____/ \___|_|  \__,_| .__/ 
                                          |_|    
"""
    print(welcomeMessage)
    print(f"Bienvenido a MindScrap, programa para convertir los horarios de la pagina Mindbox a JSON (ITS)")

def generarHorario(sc):
    print ("""
    Teclea los semestres de las materias que deseas obtener el horario.
    Asegurate de seleccionarlos separados por comas y sin espacios. (Ejemplo: 1,2,3,4)
           1. 1er Semestre 2. 2do Semestre 3. 3er Semestre 4. 4to Semestre
           5. 5to Semestre 6. 6to Semestre 7. 7mo Semestre 8. 8vo Semestre
    """)
    semestres = input("Semestres: ")
    if not validarSemestres(semestres):
        print("Por favor, ingresa los semestres correctamente")
        return
    semestres = semestres.split(",")
    print("Obteniendo las materias de los semestres seleccionados...")
    stop_event = threading.Event()
    hilo_cargando = threading.Thread(target=Utils.mostrar_cargando, args=(stop_event,))
    hilo_cargando.start()
    materias = sc.getSubjectsBySemesters(semestres)
    materiasGrupo = sc.groupGroups(materias)

    stop_event.set()
    hilo_cargando.join()
    
    materiasSeleccionadas = seleccionarMaterias(materiasGrupo)
    numMaterias = len(materiasSeleccionadas)
    print("A continuacion, se mostraran los grupos de las materias seleccionadas, se mostraran por materia")
    time.sleep(3)
    print("\033c", end="")
    materiasFinal = seleccionarMateriasConGrupos(materiasSeleccionadas, materiasGrupo)
    # Resetear la consola
    print("\033c", end="")
    print(f"{colors.pink_color}Estas son las materias seleccionadas{colors.reset_color}")
    for materia in materiasFinal:
        print(f"\n{colors.yellow_color}Materia: {materia['Materia']}{colors.reset_color}")
        print(f"Profesor: {materia['Profesor']}")
        print(f"Semestre: {materia['Semestre']}")
        print(f"Horario: {materia['Horario']}")
    print(f"{colors.pink_color}A continuacion se generaran las posibles combinaciones de horarios{colors.reset_color}")
    print("Esto puede tardar un poco, por favor espera...")
    stop_event = threading.Event()
    hilo_cargando = threading.Thread(target=Utils.mostrar_cargando, args=(stop_event,))
    hilo_cargando.start()
    combinaciones = Utils().genCombinations(materiasFinal, numMaterias)
    stop_event.set()
    hilo_cargando.join()
    print(f"{colors.pink_color}Se generaron {len(combinaciones)} combinaciones de horarios{colors.reset_color}")
    for i, combinacion in enumerate(combinaciones):
        print(f"\n{colors.pink_color}Combinacion {i+1}{colors.reset_color}")
        for materia in combinacion:
            print(f"\n{colors.yellow_color}Materia: {materia['Materia']}{colors.reset_color}")
            print(f"Profesor: {materia['Profesor']}")
            print(f"Semestre: {materia['Semestre']}")
            print(f"Horario: {materia['Horario']}")
    Utils().createJson(combinaciones)


def seleccionarMateriasConGrupos(materiasSeleccionadas, materiasGrupo):
    materiasFinal = []
    for nombre, materias in materiasGrupo.items():
        if nombre in [materia['Materia'] for materia in materiasSeleccionadas]:
            print(f"\n{colors.pink_color}Grupos disponibles de la materia {nombre}{colors.reset_color}")
            for i, materia in enumerate(materias, start=1):
                print(f"\n\n{colors.yellow_color}Materia: {nombre}{colors.reset_color}")
                print(f"ID: {materia['ID']}")
                print(f"Profesor: {materia['Profesor']}")
                print(f"Semestre: {materia['Semestre']}")
                print(f"Horario: {materia['Horario']}")
                print(f"Índice: {i}")
            
            selected_indices = input("\nIngresa los índices de las materias que deseas seleccionar, separados por comas, o presiona Enter para continuar: ")
            if selected_indices:
                selected_indices = selected_indices.split(',')
                for selected_index in selected_indices:
                    if selected_index.isdigit():
                        selected_index = int(selected_index)
                        if 1 <= selected_index <= len(materias):
                            print(f"Seleccionaste la opción {selected_index}")
                            materiasFinal.append(materias[selected_index-1])
                        else:
                            print(f"Índice {selected_index} no válido. Por favor, intenta de nuevo.")
                    else:
                        print(f"Entrada no válida: {selected_index}. Por favor, ingresa números separados por comas.")
            input("Presiona enter para continuar")
            print("\033c", end="")
    return materiasFinal


def seleccionarMaterias(grupoMaterias):
    print("\033c", end="")
    materias_unicas = {}
    for nombre, materias in grupoMaterias.items():
        for materia in materias:
            if materia['Materia'] not in materias_unicas:
                materias_unicas[materia['Materia']] = materia['Semestre']
    
    print("A continuacion, se mostraran las materias de los semestres seleccionados")
    for i, (materia, semestre) in enumerate(materias_unicas.items()):
        print(f"{i}. {materia} - Semestre: {semestre}")
    print(f"{colors.pink_color}Selecciona las materias que te gustaria cursar (Maximo 7) separadas por comas{colors.reset_color}")
    materias_seleccionadas = input("Materias: ")
    materias_seleccionadas = materias_seleccionadas.split(",")
    if len(materias_seleccionadas) > 7:
        print("Solo puedes seleccionar 7 materias")
        return
    materias_finales = {}
    for index in materias_seleccionadas:
        if index.isdigit():
            index = int(index)
            if 0 <= index < len(materias_unicas):
                materia = list(materias_unicas.keys())[index]
                semestre = materias_unicas[materia]
                materias_finales[materia] = {'Materia': materia, 'Semestre': semestre}
            else:
                print(f"Índice {index} fuera de rango. Por favor, intenta de nuevo.")
                return
        else:
            print(f"Entrada no válida: {index}. Por favor, ingresa números separados por comas.")
            return
    print("Materias seleccionadas:")
    for materia, detalles in materias_finales.items():
        print(f"{detalles['Materia']} - Semestre: {detalles['Semestre']}")
        print("\n")
    print(f"{colors.pink_color}Materias seleccionadas correctamente{colors.reset_color}")
    #Resetear la consola
    print("\033c", end="")
    return list(materias_finales.values())
    

def validarSemestres(semestres):
    semestres = semestres.split(",")
    for semestre in semestres:
        if not semestre.isdigit():
            print(f"El semestre {semestre} no es valido")
            return False
    return True

def getInput():
    print("\n Menu:")
    print("1. Obtener horario")
    print("2. Generar horario")
    print("3. Instrucciones")
    print("4. Salir")
    return input("Selecciona una opcion: ")

def printInstructions():
    instrucciones = """
    Instrucciones:
OPCION 1: Esta opcion lo unico que hace es generar un JSON con las materias del semestre que ingreses
1. Asegurate que el archivo cookies.json tenga las cookies de Mindbox
2. Ingresa el semestre que deseas obtener el horario
3. El programa generara un archivo data.json con el horario

OPCION 2: Esta opcion genera todas las combinaciones posibles de horarios con las materias que selecciones
1. Asegurate que el archivo cookies.json tenga las cookies de Mindbox
2. Ingresa los semestres de las materias que deseas obtener el horario
3. Selecciona las materias que deseas cursar
4. Selecciona los grupos de las materias seleccionadas
5. El programa generara todas las combinaciones posibles de horarios

Si no estas seguro de como obtener las cookies, visita el siguiente enlace: \033]8;;https://github.com/NexWan/MindScrap\033\\https://github.com/NexWan/MindScrap\033]8;;\033\\
    """
    print(instrucciones)

def __main__():
    printWelcome2()
    printWelcome()
    utils = Utils()
    if not utils.checkCookiesFile(): exit(0)
    scrapper = sc.Scrap("https://itsaltillo.mindbox.app/alumnos/reinscripcion/grupos-disponibles")
    while(True):
        option = getInput()
        if option == '1':
            semestre = input("Ingresa el semestre: ")
            scrapper.getHorario(semestre)
        elif option == '2':
            print("\033c", end="")
            generarHorario(scrapper)
        elif option == '3':
            print("\033c", end="")
            printInstructions()
        elif option == '4':
            # Secuencia de escape ANSI para limpiar la consola
            print("\033c", end="")
            print("Bye bye")
            break
        else:
            print("Opcion no valida")


if __name__ == '__main__':
    __main__()