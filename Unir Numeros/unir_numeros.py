#Juego que presenta pentagonos con números en espanol, a los cuales se debe hacer click en el orden
#correcto, si se hace en orden, se dibujan líneas que unen las figuras. Si el orden no es correcto, 
#las líneas se deshacen comenzando desde inicio. LLeva tiempo, intentos y niveles

import pgzrun
import sys
from random import randint
from time import time

#ancho y altura de la pantalla
WIDTH = 1200
HEIGHT = 700

limite_numeros = 3

def carga_numeros(limite_numeros):
    numeros = []
    """Función que pone las imagnes de los numeros en un lista"""
    for numero in range(0, limite_numeros):
        #cada que vez se pasa al ciclo, se carga las imagenes (nombres son 1, 2 .. 9)
        actor = Actor(str(numero + 1))
        #aseguarse que las cordenadas de la figura esten a 20px de los bordes de la ventana
        actor.pos = randint(40, WIDTH - 40), randint(40, HEIGHT - 40)
        numeros.append(actor)
    return numeros

numeros = carga_numeros(limite_numeros)
lineas = []
numero_siguiente = 0
cont = 0
game_over = False
tiempo = time()
tiempo_str = ""

def draw():
    screen.fill("black")
    for numero in numeros:
        numero.draw()
    
    #Solo cuando 2 números hayan sido cliqueados se dibuja la linea
    for linea in lineas:
        #screen.draw.line .. dibuja lineas(punto x --> y + color (rgb)). 
        screen.draw.line(linea[0], linea[1], (0, 255, 0))

    if game_over:
        screen.fill("white")
        screen.draw.text("Tiempo Transcurrido: " + tiempo_str[0:5], color="purple",center=(400, 300), fontsize=60)


def on_mouse_down(pos):
    global numeros
    global limite_numeros
    global cont
    global lineas
    global game_over
    global tiempo
    global tiempo_str
    
    #si se hizo click en la posición adecuada del número correcto siguiente. --> collidepoint(pos)
    if numeros[cont].collidepoint(pos):
        #ya se hizo click en el primer número? Se establecen las cordendas conectoras de la linea
        if cont:
            lineas.append((numeros[cont - 1].pos, numeros[cont].pos))
        cont += 1
    #si se comete un error se borra todo y se comienza de 0
    else:
        lineas = []
        cont = 0

    #si se acaban los primeros numeros, carga 1+. Borra las lineas
    if cont == limite_numeros:
        numeros = carga_numeros(limite_numeros + 1)
        limite_numeros += 1
        lineas = []
        cont = 0
    if limite_numeros == 10:
        tiempo = time() - tiempo
        tiempo_str = str(tiempo)
        game_over = True

    
    


pgzrun.go()