# MINDSCRAP

Esta herramienta esta hecha para poder scrappear la informacion respecto a los horarios en la pagina mindbox https://itsaltillo.mindbox.app

## INDEX  

- [Como usarla](#como-usarla)
    - [Linux o MacOs](#linux-o-macos)
    - [Windows](#windows)
- [Configuracion](#configuracion)
- [Ejemplo](#ejemplo)

## COMO USARLA

Para empezar tendras que tener instalado Python, despues tendras que crear un entorno virtual (venv)
```sh
python -m venv env
```
### LINUX o Macos
Para activar el entorno virtual en linux usa el siguiente comando:
```sh
source env/bin/activate
```

### WINDOWS
En windows utiliza el siguiente comando
```sh
source env/bin/activate
```

Una vez activado tu entorno virtual utiliza el siguiente comando para instalar las librerias utilizadas:
```sh
pip install -r requirements.txt
```

Una vez hecho eso solo basta con correr el siguiente comando para ejecutar el script:
```sh
python src/main.py
```

## CONFIGURACION
Esta herramienta requiere de las cookies de tu sesion de mindbox.  
Esto debido a que para iniciar sesion tiene que existir una "sesion" activa (o sea tus cookies), el como obtenerlas es relativamente facil, solo sigue los siguientes pasos:  

1. <b> Entra a la pagina de mindbox y loggeate </b>  
Solamente inicia sesion en [mindbox](https://itsaltillo.mindbox.app\alumnos) como de costumbre.  
2. <b> Abre herramientas de desarrollador </b>  
Si utilizas un navegador normal (o sea no safari) solamente basta con que hagas click derecho a la pagina y selecciones "inspeccionar elemento o inspect element" para abrir las herramientas de desarrollador o presionando F12 en tu teclado, una vez abierto es hora de buscar las cookies  
<img src='gitImgs/inspeccion.png'>   

3. <b> Conseguir tus cookies de sesion </b>  
En las herramientas de desarrollador tendras que irte a el apartado de storage (o almacenamiento en spanish), de ahi tendras que irte a el apartado de Cookies, seleccionas la de la opcion "https://itsaltillo.mindbox.app" y tendras que copiar el valor de las siguientes cookies:
![alt text](gitImgs/cookies1.png)  
(solo dale doble click en donde dice value/valor y copialo cada uno).

4. <b>Ponerlas en config.json</b>

Si es la primera vez que ejecutas el script, deberia generarte un archivo en la carpeta raiz del programa, se llamara 'cookies.json', ahi pondras las cookies de la siguiente forma:
![alt text](gitImgs/cookies2.png)

5. <b> Ejecutar el programa </b>

Ahora solo bastaria correr el script con el comando 
```sh
python src/main.py
```

## EJEMPLO

Si quieres ver un ejemplo de como almacena la informacion ve a el siguiente [enlace](example/example.json)
