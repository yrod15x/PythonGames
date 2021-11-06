#Escaping Rectangle. Juego de scroll vertical in el cual un rectangulo trata de sortear misiles, ganando puntos
# Cada vez que lo hace. Los obstaculos aparecen de arriba a abajo de la pantalla y despararecen por debajo.
#Se reposicionan arriba una vez desparecen. Cada cierto numero de puntos aumenta la velocida de los mismos.

from random import randint

HEIGHT = 600
WIDTH = 800

rect_heroe = Rect((WIDTH / 2, HEIGHT - 30), (30, 30))
estado_juego = False
progreso = "nivel0"
pausa_nivel = True
score = 0

nivel = 1
pos_misil1 = (randint(15, WIDTH - 50), 0)
pos_misil2 = (randint(15, WIDTH - 50), 0)
pos_misil3 = (randint(15, WIDTH - 50), 0)
misil1 = Actor("misilazul" , pos = (pos_misil1))
misil2 = Actor("misilnaranja", pos = (pos_misil2))
misil3 = Actor("misilverde", pos = (pos_misil3))
pos_misil4 = (randint(15, WIDTH - 50), 0)
pos_misil5 = (randint(15, WIDTH - 50), 0)
pos_misil6 = (randint(15, WIDTH - 50), 0)
misil4 = Actor("misilazul" , pos = (pos_misil4))
misil5 = Actor("misilnaranja", pos = (pos_misil5))
misil6 = Actor("misilverde", pos = (pos_misil6))


def draw():
    global estado_juego, progreso, score, nivel
    screen.blit("fondo", (0,0))

    #Pantalla inicial del juego los switches estan apagados

    if not estado_juego:
        if score == 0:
            menu_texto(1)
        elif score == 10:
            menu_texto(2)
        elif score == 19:
            menu_texto(3)

    if estado_juego:
        if score <= 9:
            screen.draw.filled_rect(rect_heroe, "red")
            misil1.draw()
            misil2.draw()
            misil3.draw()
            screen.draw.text(str(score), (750, 20), fontsize = 45)
        if score >= 9 and score <= 18:
            screen.draw.filled_rect(rect_heroe, "red")
            misil1.draw()
            misil2.draw()
            misil3.draw()
            misil4.draw()
            misil5.draw()
            misil6.draw()
            screen.draw.text(str(score - 1), (750, 20), fontsize = 45)






def limpiar_posicion(posicion, new_x, new_y):
    #como la posicion es una tupla y estas son inmutables se debe limpiarlas a traves de una doble conversion
    #lista a tupla y luego tupla lista. Devuelve una lista con la nueva posicion que sera reconvertida a tupla

    limpia_tupla = list(posicion)
    limpia_tupla.clear()
    limpia_tupla = [new_x, new_y]

    return limpia_tupla


def update():
    global estado_juego, score, nivel, progreso

    #iniciar el juego presionando espacio. Se activan los switches
    if not estado_juego:
        if keyboard.space:
            estado_juego = True

    if estado_juego:
        if score < 9:
            #movimiento misiles  el misil en el nivel 1
            misil1.y += 2
            misil2.y += 2
            misil3.y += 2
            #si los misiles se salen de abajo de la pantalla. Se reinicia la posicion. Se asignan puntos
            if misil1.y > HEIGHT:
                score += 3
                misil1.pos = tuple(limpiar_posicion(misil1.pos, randint(15, WIDTH - 50), 0))
                misil2.pos = tuple(limpiar_posicion(misil1.pos, randint(15, WIDTH - 50), 0))
                misil3.pos = tuple(limpiar_posicion(misil1.pos, randint(15, WIDTH - 50), 0))
        if score >= 9 and score < 18:
            #movimiento misiles  el misil en el nivel 1
            misil1.y += 3
            misil2.y += 3
            misil3.y += 3
            misil4.y += 3
            misil5.y += 3
            misil6.y += 3
            #si los misiles se salen de abajo de la pantalla. Se reinicia la posicion. Se asignan puntos
            if misil1.y > HEIGHT:
                score += 3
                misil1.pos = tuple(limpiar_posicion(misil1.pos, randint(15, WIDTH - 50), 0))
                misil2.pos = tuple(limpiar_posicion(misil1.pos, randint(15, WIDTH - 50), 0))
                misil3.pos = tuple(limpiar_posicion(misil1.pos, randint(15, WIDTH - 50), 0))
                misil4.pos = tuple(limpiar_posicion(misil1.pos, randint(15, WIDTH - 50), 0))
                misil5.pos = tuple(limpiar_posicion(misil1.pos, randint(15, WIDTH - 50), 0))
                misil6.pos = tuple(limpiar_posicion(misil1.pos, randint(15, WIDTH - 50), 0))



        #Mover el actor en varias direcciones sin salirse
    if keyboard.right  and rect_heroe.x < WIDTH - 30:
        rect_heroe.x += 3
    if keyboard.left  and rect_heroe.x > 0:
        rect_heroe.x -= 3
    if keyboard.up  and rect_heroe.y > 0:
        rect_heroe.y -= 3
    if keyboard.down  and rect_heroe.y < HEIGHT - 30:
        rect_heroe.y += 3

    if score == 9 or score == 18:
        #llego a cierto score detengo el juego. Sumo 1 al score para:
        #que el juego no se apague ya que siempre quedaria en 9 0 18 --> if score == 9 or score == 18: estado_juego = False
        #imprimir mensaje en pantalla (draw) elif score == 10: --> menu_texto(2)
        #queda listo para presionar espacio otra vez e iniciar el ste nivel
        estado_juego = False
        score += 1
        print("juego parado")




def menu_texto(nivel):
    #funcion que controla los textos en pantalla para realizar una accioon con barra de espacio
    screen.draw.text(">>> Misile Rain <<<", (WIDTH/2 - 180, HEIGHT/2 - 70), fontsize = 55)
    screen.draw.text("Presione Espacio", (WIDTH/2 - 110, HEIGHT/2), fontsize = 35)
    screen.draw.text("Nivel " + str(nivel), (WIDTH/2 - 50, HEIGHT/2 - 30), fontsize = 45)

