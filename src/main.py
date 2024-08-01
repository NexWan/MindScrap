import scrap as sc
from colors import *
from utils import *

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

def getInput():
    print("\n Menu:")
    print("1. Obtener horario")
    print("2. Instrucciones")
    print("3. Salir")
    return input("Selecciona una opcion: ")

def printInstructions():
    instrucciones = """
    Instrucciones:
1. Asegurate que el archivo cookies.json tenga las cookies de Mindbox
2. Ingresa el semestre que deseas obtener el horario
3. El programa generara un archivo data.json con el horario

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
            printInstructions()
        elif option == '3':
            # Secuencia de escape ANSI para limpiar la consola
            print("\033c", end="")
            print("Bye bye")
            break
        else:
            print("Opcion no valida")


if __name__ == '__main__':
    __main__()