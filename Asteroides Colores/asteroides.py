#Juego que permite hacer click en una imagen (asteroide) adecuada y no en otras (se pierde) que se van 
#moviendo hacia abajo o arriba, si llegan a tocar el borde de la pantalla se pierde. Al escoger la correcta
#Se sube de nivel donde aparecen más asteroides, y se repite hasta llegar al nivel final. Cambian de posicion. 

import pgzrun
import random


#Color de la fuente al desplegar mensajes en pantalla
FONT_COLOR = (255, 255, 255)

#Ancho, altura  de la ventana central del juego
WIDTH = 1000
HEIGHT = 600

#Coordenadas para desplegar el mensaje de texto final 
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2
CENTER = (CENTER_X, CENTER_Y) 

#Muestra cuantos niveles va a tomar el juego. Da juego completado si se llegó al final
FINAL_LEVEL = 7

#velocidad inicial que se van a mover las asteroides nivel 1
asteroidT_SPEED = 10

#Colores de asteroides que no deben ser cliqueados
COLORS = ["green", "blue", "yellow", "purple"]

#variable que activa cuando el juego acabó en perdidad
game_over = False
#variable que se activa al culminar todos los niveles
game_complete = False
#variable que determina en que nivel esta el jugador
current_level = 1
#Lista con las asteroides de cada nivel
asteroids = []
#Registra los moviemientos de las asteroides. Si llegan al final de la pantalla
animations = []


def draw():
    """Maneja todos los eventos que se hacen pantalla: dibujar, esctribir, borrar"""
    #se declaran las variables globales para que puedan ser usadas dentro de la función
    global asteroids, current_level, game_complete, game_over
    screen.clear()
    #permite poner images de fondo (space.png), coordenadas iniciales
    screen.blit("space", (0, 0))
    
    if game_over:
        display_message("GAME OVER!", "Try again - Press SPACE to continue")
    elif game_complete:
        display_message("YOU WON!", "Congrats - Press SPACE to continue")
    else:
        #dibuja las asteroides que se encuentran en la lista (un grupo)
        for asteroid in asteroids:
            asteroid.draw()

#activa los cambios de nivel al iniciar la funcion de poner elementos en la pantalla
def update():
    """Maneja acciones lógicas del juego: movimientos, posiciones, tamaños de los objetos"""
    global asteroids, game_complete, game_over, current_level
    #cada vez que se aumente el nivel (no asteroides), se crean con otra funcion
    if len(asteroids) == 0:
        asteroids = make_asteroids(current_level)
    
    #si el juego esta acabado preguntar al usuario si desea jugar otro. Presionar la tecla espacio
    if(game_complete or game_over) and keyboard.space:
        asteroids = []
        current_level = 1
        game_complete = False
        game_over = False


def make_asteroids(extra_asteroids):
    #función con una lista de colores para las asteroides
    colores_extra = get_colors(extra_asteroids)

    #funcion que crea los Actores(asteroides) con la lista de colores
    new_asteroids = create_asteroids(colores_extra)

    #Pone las en posición las asteroides creadas
    layout_asteroids(new_asteroids)

    #da el movimiento vertical a las asteroides
    animate_asteroids(new_asteroids)

    #se devuelven los Actores con sus colores, posición y movimineto
    return new_asteroids

def get_colors(extra_asteroids):
    """Crea una lista de nombres de colores aleatorios para las asteroides (imagenes)"""
    #siempre debe haber una asteroide (imagen) de color rojo
    colores_to_create = ["red"]

    #el número de asteroides necesarias por nivel
    for i in range(0, extra_asteroids):
        #escoge aleatoriamente nombre de colores de la lista COLORS
        random_color = random.choice(COLORS)
        colores_to_create.append(random_color)

    return colores_to_create

def create_asteroids(colores_extra):
    """Crea las asteroides (Actores) que se van a visualizar en pantalla"""
    new_asteroids = []

    #Escoge de la lista de que se crean en get_colors 
    for color in colores_extra:
        #crea un actor compuesto con el nombre real de la imagen y el color de lista: color-asteroid --> blue-asteroid, red-asteroid ..
        asteroid = Actor(color + "-asteroid")
        new_asteroids.append(asteroid)
    
    return new_asteroids

def layout_asteroids(new_asteroids):
    """Poner todas las asteroides en las coordendas adecuadas"""
    #asteroides deben ser distanciadas por espacios. 1+ que el numero de asteroides en el nivel
    numbers_gaps = len(new_asteroids) + 1

    #el tamaño del espacio debe ser igual al ancho de pantalla entre los que puedan caber
    gag_size = WIDTH / numbers_gaps

    #reordena las asteroides en la lista, para que cada nivel esten en lugares diferentes
    random.shuffle(new_asteroids)

    #Enumerate permite trabajar con el index y los elementos de la lista. Haciendo operaciones
    #pone cada asteroide a una distancia de --> espacio-asteroide-espacio-asteroide-espacio...
    for index, asteroid in enumerate(new_asteroids):
        #posicion horizontal = num_asteroides_hechas * tamaño_especio_pixeles
        new_x_pos = (index + 1) * gag_size
        asteroid.x = new_x_pos
        #cambia la posicion incial vertical. pares abajo impares hacia arriba
        if index % 2 == 0:
            asteroid.y = 0
        else:
            asteroid.y = HEIGHT

def animate_asteroids(new_asteroids):
    """Mueve las asteroides arriba y abajo"""
    for asteroid in new_asteroids:
        #Algunos asteroides viajan a más velocidad. Nivel alto más velocidad
        random_speed = random.randint(0, 2)
        duration = asteroidT_SPEED - (current_level + 1.5) + random_speed
        #anchor es un punto que determina la posición en pantalla. Las coordenadas inciales del rectangulo
        if asteroid.y == 0:
            asteroid.anchor = ("center", "bottom")
        #animate mueve el Actor, duration=segundos, on_finished= si termina, a donde va(abajo)
            animation = animate(asteroid, duration=duration, on_finished=activate_game_over, y=HEIGHT)
        else:
            asteroid.anchor = ("center", "top")
            animation = animate(asteroid, duration=duration, on_finished=activate_game_over, y=0)
        #animate mueve el Actor, duration=segundos, on_finished= si termina, a donde va(arriba)
        animations.append(animation)

def activate_game_over():
    global game_over
    game_over = True

def on_mouse_down(pos):
    """Maneja el evento de hacer click sobre las asteroides"""
    global asteroids, current_level
    for asteroid in asteroids:
        #mira si se ha hecho click en una asteroide
        if asteroid.collidepoint(pos):
            #si se hizo click en la roja se activa red_asteroid_click()
            if "red" in asteroid.image:
                red_asteroid_click()
            else:
                activate_game_over()

def red_asteroid_click():
    """Maneja los acciones al presionar la asteroide correcta. Subir nivel, juego completado"""
    global current_level, asteroids, animations, game_complete
    
    #se detienen las asteroides que van bajando
    stop_animations(animations)

    #si es el final del juego se activa juego_completo
    if current_level == FINAL_LEVEL:
        game_complete = True
    else:
        current_level += 1
        asteroids = []
        animations = []

def  stop_animations(animations):
    """Detiene la asteroides en su moviento"""
    for animation in animations:
        if animation.running:
            animation.stop()

def display_message(heading_text, sub_heading):
    screen.draw.text(heading_text, fontsize=60, center=CENTER, color=FONT_COLOR)
    screen.draw.text(sub_heading, fontsize=30, center=(CENTER_X, CENTER_Y + 30), color=FONT_COLOR)

def shuffle():
    """Permite intercambiar la posicion horizontal de los asteroides mientras se mueven"""
    global asteroids
    #si la lista de asteroides esta no esta vacia
    if asteroids:
    #se hace una lista de compresión. Toma las posciones x de cada asteroide y las guarda
        x_values = [asteroid.x for asteroid in asteroids]
        #reorganiza las posiciones en desorden
        random.shuffle(x_values)
        for index, asteroid in enumerate(asteroids):
            new_x = x_values[index]
            #mueve los asteroides a sus nuevas posiciones con medio de segundo de intervalo
            animation = animate(asteroid, duration=0.5, x=new_x)
            animations.append(animation)

#se usa la función clock para programar el cambio de posicion cada segundo
clock.schedule_interval(shuffle, 1)

pgzrun.go()