"""
Quiero hacer un proyecto pequeño de programacion Lenguaje Python, Workbench Visual Studio Code, para el proyecto usare Django y Venv. Hagamos un simple chat P2P de principio basico 

Una interfaz sencilla, Ventana de fondo negro liso 1020x800
Dos botones, Unirse y Hostear 
La opcion de Hostear debe utilizar UPNP para abrir el puerto de red, y luego devolver un codigo unico para que otro pueda unirse
Y la opcion de Unirse debe pedir el codigo para conectarse con el Host.
"""

"""

Usar Developer Command prompt for VS

"""

"""
#Creacion del entorno con python 3.11 de Windows
(El 3.10 es de Linux-like)

"E:\Programacion\Python-3.11.11\python.exe" -m venv venv

call venv\Scripts\activate.bat

"""

"""

# --- Bugs a resolver ---

La limpieza de botones entre Unirse y Conectar
Al continuamente cambiar entre ellos se buggea y no muestra ningun label
(SOLUCIONADO)

Al "hostear" se abre la ventana de chat incluso apretando el boton de "volver"
(SOLUCIONADO)

No deja de incrementar los puertos y no los cierra cada vez que se "Hostea"
(SOLUCIONADO)

La app se relanza constantemente incluso cerrando desde administrador
...Al menos ya lo puedo cerrar desde el administrador
...Mentira, no se puede cerrar ni desde ahi
...YA CIERRA
(SOLUCIONADO)

La limpieza de puertos nos e ejecuta correctamente al cerrar el .exe
Se llama pero no se ejecuta
[ No solucionado ]


[[[--------------]]]
# ----- Notas -----

Voy a arreglar la estructura de las carpetas y archivos para mejorar un poco la legibilidad
Y asi evitarme mas problemas a futuro


[[[--------------]]]
"""