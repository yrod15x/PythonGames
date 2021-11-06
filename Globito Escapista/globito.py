#Juego que muestra un globo en mitad de pantalla que va evitando obstaculos, subiendo y bajando. Esto se
#hace al presionar el mouse. Si se mantiene presionado eel globo sube y al soltar baja. Los obstáculos van
#saliendo en derecha a izquierda. Se van obteniendo puntos a medida que se va evitando los objetos. 
#los 3 puntajes más altos del juego en un arichivo de texto

import pgzrun
from random import randint

WIDTH = 1000
HEIGHT = 650

#Imagen del globpo y su posición en pantalla. Actor es la clase para representar objetos(imagenes)
globito = Actor("globito")
globito.pos = 500, 325

#Posición del dardo. Se coloca fuera de la pantalla (x) y arriba de la misma (y). Posiciones aleatorias
#Se coloca fuera de pantalla para que vaya entrando y dar la sensación de movimiento. Derecha a izquierda
#Sólo se usa un actor, una vez sale de pantalla por derecha, se vuelve y se pone a izquierda
dardo = Actor("dardo")
dardo.pos = randint(1000, 1600), randint(10, 200)

#Posición del t-rex, fuera de pantalla (x) y debajo de pantalla
trex = Actor("tirano")
trex.pos = randint(1100, 1400), 532

#Creación y posición de la planta. fuera de pantalla
planta = Actor("planta")
planta.pos = randint(1200, 2000), 490

#Suiche para cambiar imagen, haciendo efecto de movimiento
dardo_cambia = True

#Controla subir el globo mientras se presiona el mouse
globo_arriba = False

#Suiche terminar el juego
game_over = False

#puntaje del juego
puntaje = 0

#suiche que maneja cuantas veces se actualiza el juego, mediante la función update()
num_actualizaciones = 0

#lista para almacenar los 3 puntajes más altos del juego en un arichivo de texto
puntajes = []

def actualizar_puntajes():
    """Pone los 3 puntajes más altos en un archivo de texto"""
    global puntaje, puntajes
    archivo = r"/Users/Darling Sabino/Desktop/Pyhton/Juegos/Globito Escapista/globito.txt"
    puntajes = []
    with open(archivo, "r") as file:
        linea = file.readline()
        puntajes_max = linea.split()
    #comprobar si los puntajes en el archivo han sido superados
    for puntaje_max in puntajes_max:
        if(puntaje > int(puntaje_max)):
            puntajes.append(str(puntaje) + " ")
            puntaje = int(puntaje_max)
        else:
            puntajes.append(str(puntaje_max) + " ")

    with open(archivo, "w") as file:
        for puntaje_max in puntajes:
            file.write(puntaje_max)

def mostrar_puntajes():
    """Muestra los puntajes máximos del juego en pantalla"""
    screen.draw.text("PUNTAJES MAX", (350, 150), color = "white")
    y = 175
    posicion = 1
    for puntaje_max in puntajes:
        screen.draw.text(str(posicion) + ". " + puntaje_max, (350, y), color = "white")
        y += 25
        posicion += 1

def draw():
    """Dibujar los objetos en pantalla"""

    #poner el fondo
    screen.blit("fondo", (0, 0))

    #si el juego no se ha acabado, dibuja los actores y el texto del puntaje
    if not game_over:
        globito.draw()
        dardo.draw()
        trex.draw()
        planta.draw()
        screen.draw.text("Puntaje: " + str(puntaje), (800, 5), color="white")
    else:
        mostrar_puntajes()

def on_mouse_down():
    """Cuando se presiona el mouse el globo sube"""
    global globo_arriba
    globo_arriba = True
    globito.y -= 50

def on_mouse_up():
   """Cuando se deja de presionar el mouse el globo baja"""
   global globo_arriba
   globo_arriba = False

def ilusion_dardo():
    """Cambiar imagen del dardo para dar impresión de movimiento"""
    global dardo_cambia
    if dardo_cambia:
        dardo.image = "dardo_negro" 
        dardo_cambia = False
    else:
        dardo.image = "dardo"  
        dardo_cambia = True

def update():
    """Cambia cada 60 segundos, refrescando los actores. Crear ilusiones de cambio"""

    #variables que van a ser cambiadas por fuera de la función
    global game_over, puntaje, num_actualizaciones

    if not game_over:
        #si no se presiona el mouse el globo baja (gravedad)
        if not globo_arriba:
            globito.y += 1

        #mover el dardo en pantalla de derecha a izquierda
        if dardo.x > 0:
            dardo.x -= 4
            #llamar a la función cambia dardos controlando cuantos ciclos de actualización
            if num_actualizaciones == 9:
                #si hay 9 ciclos cambia el dardo y reinicia los ciclos para volver a cambiar
                ilusion_dardo()
                num_actualizaciones = 0
            else:
                num_actualizaciones += 1
        else:
            #si ya el dardo atraveso la pantalla, volver a ponerlo fuera de pantalla a derecha
            dardo.x = randint(1000, 1600)
            dardo.y = randint(10, 200)
            puntaje += 1
            num_actualizaciones = 0
        
        #mover el t-rex
        if trex.right > 0:
            trex.x -= 2
        else:
            #si ya atravesó la pantalla, volver a ponerlo fuera de pantalla a derecha
            trex.x = randint(1000, 1600)
            puntaje += 1

        #mover la planta
        if planta.right > 0:
            planta.x -= 2
        else:
            planta.x = randint(1000, 1600)
            puntaje += 1

        #acabar el juego si el globo toca el tope de la pantalla o el fondo
        if globito.top < 0 or globito.bottom > 560:
            game_over = True
            actualizar_puntajes()

        #si el globo toca el trex o la planta acaba el juego
        if globito.collidepoint(dardo.x, dardo.y) or globito.collidepoint(trex.x, trex.y) or globito.collidepoint(planta.x, planta.y):
            game_over = True
            actualizar_puntajes()

pgzrun.go()