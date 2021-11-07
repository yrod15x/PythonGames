# Write your code here :-)

import pgzrun
from random import randint

WIDTH = 800
HEIGHT = 600
num_veces = 0
img_walker = []
back_img_walker = []
pos_x = randint(50, 750)
pos_y = randint(50, 550)
index = 0
direccion = "der"

def agregar_imagenes(nom_archivo):
    """Función que crea una lista con las imagenes de los movimientos del actor principal. Las he nombrado walker seguidas
    de un numero empezando por el 1: walker1, walker2 .. etc. """
    imagenes = []
    for i in range(1, 25):
        imagenes.append(nom_archivo+str(i))
    return imagenes

#creo la lista con las imagenes
img_walker = agregar_imagenes("walker")
back_img_walker = agregar_imagenes("backwalker")

#asigno la primera en pantalla con una posicion aleatoria
walker = Actor(img_walker[0])
walker.pos = (pos_x, pos_y)

def draw():
    screen.fill((23, 100, 23))
    walker.draw()

def update():
    global num_veces, walker, img_walker, direccion

    if keyboard.right and walker.x < WIDTH - 20:
        walker.x += 3
        direccion = "der"
        if num_veces == 2:
            walker.image = img_walker[1]
        if num_veces == 4:
            walker.image = img_walker[2]
        if num_veces == 6:
            walker.image = img_walker[3]
        if num_veces == 8:
            walker.image = img_walker[4]
        if num_veces == 10:
            walker.image = img_walker[5]
        if num_veces == 12:
            walker.image = img_walker[6]
        if num_veces == 14:
            walker.image = img_walker[7]
        if num_veces == 16:
            walker.image = img_walker[8]
        if num_veces == 18:
            walker.image = img_walker[9]
        else:
            num_veces += 1
            walker.image = img_walker[0]

    elif keyboard.left and walker.x < WIDTH - 20:
            walker.x -= 3
            direccion = "izq"
            if num_veces == 2:
                walker.image = back_img_walker[1]
            if num_veces == 4:
                walker.image = back_img_walker[2]
            if num_veces == 6:
                walker.image = back_img_walker[3]
            if num_veces == 8:
                walker.image = back_img_walker[4]
            if num_veces == 10:
                walker.image = back_img_walker[5]
            if num_veces == 12:
                walker.image = back_img_walker[6]
            if num_veces == 14:
                walker.image = back_img_walker[7]
            if num_veces == 16:
                walker.image = back_img_walker[8]
            if num_veces == 18:
                walker.image = back_img_walker[8]
            else:
                num_veces += 1
                walker.image = back_img_walker[0]
    else:
        if direccion == "der":
            walker.image = img_walker[0]
        elif direccion == "izq":
            walker.image = back_img_walker[0]
    
        
    
        
        

pgzrun.go()