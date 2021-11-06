#Juego que muestra el rostro de homero buscando donas. El usuarario mueve la cara con las teclas
#de movimiento, al encontrar una dona la come y busca otra. LLevando un tiempo determinado para hacerlo
#de lo contrario el juego termina. Se muestra el puntaje en la pantalla

import pgzrun
from random import randint

#tamaño e de la pantalla
WIDTH = 800
HEIGHT = 600

#variables que manejan el flujo del juego
puntaje = 0
game_over = False

#las dos imagenes que funcionan como objetos (actores)
homero = Actor("homero")
dona = Actor("dona")

#cordenadas x - y dentro del plano de la pantalla para cada objeto
homero.pos = 100, 100
dona.pos = 200, 200

def poner_dona():
    """Poner la dona aleatoreamente a 20px de cada lado de la pantalla"""
    dona.x = randint(20, (WIDTH - 20))
    dona.y = randint(20, (HEIGHT - 20))

def tiempo_fuera():
    """Cuando el tiempo acaba vuelve la variable True. Terminar el juego"""
    global game_over
    game_over = True

#función propia de Pygame Zero permite frescar la pantalla al ejecutar un evento (presionar teclas)
def update():
    global puntaje

    if keyboard.left:
        homero.x -= 4
    elif keyboard.right:
        homero.x += 4
    elif keyboard.up:
        homero.y -= 4
    elif keyboard.down:
        homero.y += 4
    
    #Si homero llega a la dona(colliderect = True). Toma puntos
    donas_comidas = homero.colliderect(dona)
    if donas_comidas:
        puntaje += 10
        poner_dona()

#activa la función tiempo_fuera() luego de 7 segundos(cambiables)
clock.schedule(tiempo_fuera, 10.0)
poner_dona()

#dibujar objetos en pantalla, añandiendo un color.  
def draw():
    screen.fill("green")
    homero.draw()
    dona.draw()
    #Escribir puntaje en patanlla con color y cordenadas
    screen.draw.text("Puntaje: " + str(puntaje), color="black", topleft=(10,10))

    if game_over:
        screen.fill("red")
        screen.draw.text("Puntaje Final: " + str(puntaje), midleft=(250, 300), fontsize=60)

pgzrun.go()