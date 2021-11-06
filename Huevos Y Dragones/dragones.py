#Juego en el que el usuario mueve al protagonista para que robe huevos que guardan 3 dragones que
#duermen y se despiertan. Estos dragones se encuentra cada uno en un carril (cueva). Si el protagonista esta cerca de un dragón despierto se le quitan una de 
#sus vidas.

import pgzrun
import math
from random import choice

#Constantes que manejan los valores de las dimensiones y colores de la pantalla
WIDTH = 800
HEIGHT = 600
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2
CENTER = (CENTER_X, CENTER_Y)
FONT_COLOR = (0, 0, 0)

#Constantes que manejan valores de los elementos(huevis, protagonista) del juego
EGG_TARGET = 20
HERO_START = (200, 200)
ATTACK_DISTANCE = 200
DRAGON_WAKE_TIME = 2
EGG_HIDE_TIME = 2
MOVE_DISTANCE = 5

#variables globales que serán modificadas por las funciones del programa
hero = Actor("hero", pos=HERO_START)
lives = 3
eggs_collected = 0
game_over = False
game_completed = False
#cuando se pierde una vida el usuario debe volver a una posición inicial
reset_required = False

#se crean 3 cuevas (diccionarios) para los dragones, cada una con mismas caracteristicas pero valores en
#diferentes niveles para darle más dificultad al juego
easy_lair = {
    "dragon": Actor("dragon-asleep", pos=(600, 130)),
    "eggs": Actor("one-egg", pos=(430, 130)),
    "egg_count": 1,
    "egg_hidden": False,
    "egg_hide_counter": 0,
    "sleep_length": 10,
    "sleep_counter": 0,
    "wake_counter": 0
}

medium_lair = {
    "dragon": Actor("dragon-asleep", pos=(600, 300)),
    "eggs": Actor("one-egg", pos=(430, 300)),
    "egg_count": 2,
    "egg_hidden": False,
    "egg_hide_counter": 0,
    "sleep_length": 7,
    "sleep_counter": 0,
    "wake_counter": 0
}

hard_lair = {
    "dragon": Actor("dragon-asleep", pos=(600, 500)),
    "eggs": Actor("one-egg", pos=(430, 500)),
    "egg_count": 3,
    "egg_hidden": False,
    "egg_hide_counter": 0,
    "sleep_length": 4,
    "sleep_counter": 0,
    "wake_counter": 0
}

#las cuevas se guardan en una lista para facilitar su manejo dentro del programa
lairs = [easy_lair, medium_lair, hard_lair]

#función que pone todos los elementos en pantalla
def draw():
    global lairs, eggs_collected, lives, game_completed

    #refrescar e imagen de fondo en pantalla
    screen.clear()
    screen.blit("dungeon", (0, 0))

    #Mostrar mensajes y actores dependiendo del estado del juego
    if game_over:
        screen.draw.text("GAME OVER!!!", fontsize=60, center = CENTER, color=FONT_COLOR)
    elif game_completed:
        screen.draw.text("YOU WON!!!", fontsize=60, center = CENTER, color=FONT_COLOR)
    else:
        hero.draw()
        draw_lairs(lairs)
        draw_counters(eggs_collected, lives) 

def draw_lairs(cuevas):
    """Ayuda a poner en pantalla a los tres dragones, guardados en las cuevas"""
    
    #recorrer la lista y tomar cada uno de los dragones. Poner los huevos si no estan escondidos
    for cueva in cuevas:
        cueva["dragon"].draw()
        if cueva["egg_hidden"] is False:
            cueva["eggs"].draw()

def draw_counters(huevos_recolectados, vidas):
    """Ayuda a poner en pantalla todos los valores e íconos de los contadores del juego"""

    screen.blit("egg-count", (0, HEIGHT - 30))
    screen.draw.text(str(huevos_recolectados), fontsize=40, pos=(30, HEIGHT - 30), color=FONT_COLOR)

    screen.blit("life-count", (60, HEIGHT - 30))
    screen.draw.text(str(vidas), fontsize=40, pos=(90, HEIGHT - 30), color=FONT_COLOR)

def update():
    """Maneja todos los cambios de los elementos que facilitan los movimientos en pantalla"""
    
    #mover el usuario por pantalla sin salirse de ella
    if keyboard.right:
        hero.x += MOVE_DISTANCE
        if hero.x > WIDTH:
            hero.x = WIDTH
    elif keyboard.left:
        hero.x -= MOVE_DISTANCE
        if hero.x < 0:
            hero.x = 0
    elif keyboard.down:
        hero.y += MOVE_DISTANCE
        if hero.y > HEIGHT:
            hero.y = HEIGHT
    elif keyboard.up:
        hero.y -= MOVE_DISTANCE
        if hero.y < 0:
            hero.y = 0
    check_for_collisions()

def update_lairs():
    """Hace que los dragones cambien de estado: despiertos-dormidos. Animar las cuevas"""
    global lairs, hero, lives

    #recorrer todas las cuevas para despertar o dormir a los dragones
    for lair in lairs:
        if lair["dragon"].image == "dragon-asleep":
            update_sleeping_dragon(lair)
        elif lair["dragon"].image == "dragon-awake":
            update_waking_dragon(lair)
        update_egg(lair)

#animar a los dragones cada 1 segundo
clock.schedule_interval(update_lairs, 1)

def update_sleeping_dragon(cueva):
    """Revisa el tiempo dormido del dragón para cambiar la imagen a despierto"""
    
    if cueva["sleep_counter"] >= cueva["sleep_length"]:
        #para decidir aleatoriamente que dragones se levantan
        if choice([True, False]):
            cueva["dragon"].image = "dragon-awake"
            cueva["sleep_counter"] = 0
    else:
        cueva["sleep_counter"] += 1

def update_waking_dragon(cueva):
    """Revisa el tiempo despierto del dragón para cambiar la imagen a dormido"""

    if cueva["wake_counter"] >= DRAGON_WAKE_TIME:
        cueva["dragon"].image = "dragon-asleep"
        cueva["wake_counter"] = 0
    else:
        cueva["wake_counter"] += 1

def update_egg(cueva):
    """Cambiar el estado de los huevos si han estado sin mostrarse por un tiempo determinado"""

    if cueva["egg_hidden"] is True:
        if cueva["egg_hide_counter"] >= EGG_HIDE_TIME:
            cueva["egg_hidden"] = False
            cueva["egg_hide_counter"] = 0
        else:
            cueva["egg_hide_counter"] += 1

def check_for_collisions():
    """Maneja las colisones entre objetos. Heroe para coger huevos. Heroes cerca de los dragones"""
    global lairs, eggs_collected, lives, reset_required, game_completed

    #recorrer las cuevas para revisar cada una de las colisiones
    for lair in lairs:
        #si los huevos no estan escondidos mira si el heroe los recogió
        if lair["egg_hidden"] is False:
            check_for_egg_collision(lair)
        #si el heroe esta cerca de los dragones que estan despiertes
        if lair["dragon"].image == "dragon-awake" and reset_required is False:
            check_for_dragon_collision(lair)

def check_for_dragon_collision(cueva):
    """Revisas las distancia entre el protagonista y los dragones"""

    x_distance = hero.x - cueva["dragon"].x
    y_distance = hero.y - cueva["dragon"].y

    #ecuentra la distance entre dos actores que se encuentran en una linea
    distance = math.hypot(x_distance, y_distance)

    if distance < ATTACK_DISTANCE:
        handle_dragon_collision()

def handle_dragon_collision():
    """Reinicia la posicion del heroe(animate) si pierde la vida y quitarle una del contador"""
    global reset_required
    reset_required = True

    animate(hero, pos=HERO_START, on_finished=subtract_life)

def check_for_egg_collision(cueva):
    """Revisas las distancia entre el protagonista y los huevos (colliderect)"""
    global eggs_collected, game_completed

    #si el heroe recoge los huevos, se agregan al contador y si estan los suficientes se gana
    if hero.colliderect(cueva["eggs"]):
        cueva["egg_hidden"] = True
        eggs_collected += cueva["egg_count"]
        if eggs_collected >= EGG_TARGET:
            game_completed = True
    
def subtract_life():
    """Resta vidas del usuario si es quemado por algún dragón. Termina el juego si se pierden todas"""
    global lives, reset_required, game_over

    lives -= 1
    if lives == 0:
        game_over = True
    #el heroe ya esta en la posición inicial
    reset_required = False


pgzrun.go()