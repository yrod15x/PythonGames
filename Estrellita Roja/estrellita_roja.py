#Juego que permite hacer click en una imagen (estrella) adecuada y no en otras (se pierde) que se van 
#moviendo hacia abajo, si llegan a tocar el borde de la pantalla se pierde. Al escoger la correcta
#Se sube de nivel donde aparecen más estrellas, y se repite hasta llegar al nivel final. 

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
FINAL_LEVEL = 6

#velocidad inicial que se van a mover las estrellas nivel 1
START_SPEED = 10

#Colores de estrellas que no deben ser cliqueados
COLORS = ["green", "blue"]

#variable que activa cuando el juego acabó en perdidad
game_over = False
#variable que se activa al culminar todos los niveles
game_complete = False
#variable que determina en que nivel esta el jugador
current_level = 1
#Lista con las estrellas de cada nivel
stars = []
#Registra los moviemientos de las estrellas. Si llegan al final de la pantalla
animations = []


def draw():
    """Maneja todos los eventos que se hacen pantalla: dibujar, esctribir, borrar"""
    #se declaran las variables globales para que puedan ser usadas dentro de la función
    global stars, current_level, game_complete, game_over
    screen.clear()
    #permite poner images de fondo (space.png), coordenadas iniciales
    screen.blit("space", (0, 0))
    
    if game_over:
        display_message("GAME OVER!", "Try again")
    elif game_complete:
        display_message("YOU WON!", "Congrats")
    else:
        #dibuja las estrellas que se encuentran en la lista (un grupo)
        for star in stars:
            star.draw()

#activa los cambios de nivel al iniciar la funcion de poner elementos en la pantalla
def update():
    """Maneja acciones lógicas del juego: movimientos, posiciones, tamaños de los objetos"""
    global stars
    #cada vez que se aumente el nivel (no estrellas), se crean con otra funcion
    if len(stars) == 0:
        stars = make_stars(current_level)

def make_stars(extra_stars):
    #función con una lista de colores para las estrellas
    colores_extra = get_colors(extra_stars)

    #funcion que crea los Actores(estrellas) con la lista de colores
    new_stars = create_stars(colores_extra)

    #Pone las en posición las estrellas creadas
    layout_stars(new_stars)

    #da el movimiento vertical a las estrellas
    animate_stars(new_stars)

    #se devuelven los Actores con sus colores, posición y movimineto
    return new_stars

def get_colors(extra_stars):
    """Crea una lista de nombres de colores aleatorios para las estrellas (imagenes)"""
    #siempre debe haber una estrella (imagen) de color rojo
    colores_to_create = ["red"]

    #el número de estrellas necesarias por nivel
    for i in range(0, extra_stars):
        #escoge aleatoriamente nombre de colores de la lista COLORS
        random_color = random.choice(COLORS)
        colores_to_create.append(random_color)

    return colores_to_create

def create_stars(colores_extra):
    """Crea las estrellas (Actores) que se van a visualizar en pantalla"""
    new_stars = []

    #Escoge de la lista de que se crean en get_colors 
    for color in colores_extra:
        #crea un actor compuesto con el nombre real de la imagen y el color de lista: color-star --> blue-star, red-star ..
        star = Actor(color + "-star")
        new_stars.append(star)
    
    return new_stars

def layout_stars(new_stars):
    """Poner todas las estrellas en las coordendas adecuadas"""
    #estrellas deben ser distanciadas por espacios. 1+ que el numero de estrellas en el nivel
    numbers_gaps = len(new_stars) + 1

    #el tamaño del espacio debe ser igual al ancho de pantalla entre los que puedan caber
    gag_size = WIDTH / numbers_gaps

    #reordena las estrellas en la lista, para que cada nivel esten en lugares diferentes
    random.shuffle(new_stars)

    #Enumerate permite trabajar con el index y los elementos de la lista. Haciendo operaciones
    #pone cada estrella a una distancia de --> espacio-Estrella-espacio-Estrella-espacio...
    for index, star in enumerate(new_stars):
        #posicion = num_estrellas_hechas * tamaño_especio_pixeles
        new_x_pos = (index + 1) * gag_size
        star.x = new_x_pos

def animate_stars(new_stars):
    """Mueve las estrellas hacia abajo"""
    for star in new_stars:
        #Entre más alto el nivel más rapido bajaran las estrellas (más dificil)
        duration = START_SPEED - current_level
        #anchor es un punto que determina la posición en pantalla. Las coordenadas inciales del rectangulo
        star.anchor = ("center", "bottom")
        #animate mueve el Actor, duration=segundos, on_finished= si termina, a donde va(Vertical -Horizon)
        animation = animate(star, duration=duration, on_finished=activate_game_over, y=HEIGHT)
        animations.append(animation)

def activate_game_over():
    global game_over
    game_over = True

def on_mouse_down(pos):
    """Maneja el evento de hacer click sobre las estrellas"""
    global stars, current_level
    for star in stars:
        #mira si se ha hecho click en una estrella
        if star.collidepoint(pos):
            #si se hizo click en la roja se activa red_star_click()
            if "red" in star.image:
                red_star_click()
            else:
                activate_game_over()

def red_star_click():
    """Maneja los acciones al presionar la estrella correcta. Subir nivel, juego completado"""
    global current_level, stars, animations, game_complete
    
    #se detienen las estrellas que van bajando
    stop_animations(animations)

    #si es el final del juego se activa juego_completo
    if current_level == FINAL_LEVEL:
        game_complete = True
    else:
        current_level += 1
        stars = []
        animations = []

def  stop_animations(animations):
    """Detiene la estrellas en su moviento"""
    for animation in animations:
        if animation.running:
            animation.stop()

def display_message(heading_text, sub_heading):
    screen.draw.text(heading_text, fontsize=60, center=CENTER, color=FONT_COLOR)
    screen.draw.text(sub_heading, fontsize=30, center=(CENTER_X, CENTER_Y + 30), color=FONT_COLOR)



pgzrun.go()