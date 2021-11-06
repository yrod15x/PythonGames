#Juego que permite "disparar" (hacer click) a un objeto en pantalla, si se acierta un mensaje
#Se acaba al errar un disparo

import pgzrun
from random import randint
import sys

#La clase Actor permite obtener la imagen que funciona como un objeto() parametro nombred eimagen png
gremlin = Actor("gremlin")

#función para dibujar en pantalla. Limipia y pone el Actor
def draw():
    screen.clear()
    gremlin.draw()

#establece las coordenadas del Actor
def posicion_gremlin():
    gremlin.x = randint(10, 800)
    gremlin.y = randint(10, 600)

#Función que registra al hacer click sobre un objeto. Parámetro (pos) tupla interna de cordenadas
#collidepoint evalua si el click se hace sobre el objeto
def on_mouse_down(pos):
    if gremlin.collidepoint(pos):
        print("Disparo Acertado!")
        posicion_gremlin()
    else:
        print("Disparo Errado!")
        print("Game Over!!")
        sys.exit()

posicion_gremlin()
pgzrun.go()