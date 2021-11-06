#Juego que simula un quiz de preguntas sobre cultura general. Se desplega una ventana con una pregunta
#y cuatro respuestas, cada una de estas son textos que se encuentran dentro de rectangulos, además de un #tablero de tiempo que va caminando hacia atrás. Si el tiempo se acaba
#el juego termina, si el usuario hace click en la respuesta correcta, se pasa a otra pregunta, 
#se suma 1 punto, y el reloj se reinicia. Si se hace click en la respuesta incorrecta, se acaba el juego

import pgzrun

WIDTH = 1000
HEIGHT = 600

#rectangulo que contiene la pregunta. Rect(izquierda, arriba, derecha abajo (ancho - alto))
caja_pregunta = Rect(0, 0, 620, 140)

#rectangulo para el timpo
caja_tiempo = Rect(0, 0, 140, 140)

#Rectangulos de respuestas
caja_respuesta1 = Rect(0, 0, 295, 85)
caja_respuesta2 = Rect(0, 0, 295, 85)
caja_respuesta3 = Rect(0, 0, 295, 85)
caja_respuesta4 = Rect(0, 0, 295, 85)

#mover las cajas a sus posiciones en pantalla. Al principio todas aparecerian una encima de las otras
#con la función move_ip() puedo desplazarlas por la pantalla mediante coordenadas
caja_pregunta.move_ip(180, 60)
caja_tiempo.move_ip(425, 335)
caja_respuesta1.move_ip(50, 280)
caja_respuesta2.move_ip(650, 280)
caja_respuesta3.move_ip(50, 448)
caja_respuesta4.move_ip(650, 448)

#se genera una lista con las respuestas para mejor manejo en su aparición en pantalla
respuestas = [caja_respuesta1, caja_respuesta2, caja_respuesta3, caja_respuesta4]

puntaje = 0
tiempo_disponible = 10

#crear los textos de preguntas y respuestas --> lista con 6 elementos: 1 = preguntas,
#2 - 5= respuestas, 6 = número correposdiente al indice de la respuesta correcta
q1 = ["Los 1 y 0 en binarios son como: ", "suiches", "gatos", "combiaciones", "numeros", 1]
q2 = ["rojo + amarillo produce: ", "verde", "rosado", "narajado", "marron", 3]
q3 = ["La vaca es un  ", "reptil", "mamifero", "ave", "insecto", 2]
q4 = ["Python es lenguaje de: ", "humanos", "programación", "serpientes", "musicos", 2]
q5 = ["El agua se puede escribir como: ", "H02", "NaO2", "PhH20", "H20", 4]

#organizar los textos en forma de lista para manejo más eficiente
trivias = [q1, q2, q3, q4, q5]
#tomar la primera pregunta de la lista y almacenarla para su uso (pop --> elimina elementos de lista)
trivia = trivias.pop(0)

def draw():
    """Función que dibuja los elementos en pantalla"""
    #poner color de fondo
    screen.fill("black")

    #dibujar los rectangulo de pregunta y el tiempo con cierto color
    screen.draw.filled_rect(caja_pregunta, "dark blue")
    screen.draw.filled_rect(caja_tiempo, "black")

    #poner los rectangulos de las respuestas sacandolas de la lista
    for caja_respuesta in respuestas:
        screen.draw.filled_rect(caja_respuesta, "spring green")

    #poner los textos en los rectangulos
    screen.draw.textbox(str(tiempo_disponible), caja_tiempo, color=("red"))
    screen.draw.textbox(trivia[0], caja_pregunta, color=("spring green"))

    #index 1 porque ya el primer elemento(pregunta) se uso para llenar el rectangulo pregunta
    index = 1
    for caja in respuestas:
        screen.draw.textbox(trivia[index], caja, color=("dark blue"))
        index += 1

def game_over():
    """Función que termina el juego desplegando mensaje con los puntos obtenidos"""
    #variables que van a ser modificadas desde esta función
    global trivia, tiempo_disponible

    mensaje = f"Game Over. Usted obtuvo {puntaje} respuestas correctas"

    #muestra en vez de una pregunta el mensaje. Cajas respuestas vacias. 5 por no igualar a correcta
    trivia = [mensaje, "", "", "", "", 5]
    tiempo_disponible = 0

def correcta():
    """Función que verifica si la respuesta correcta fue clickeada"""
    global trivia, puntaje, tiempo_disponible

    puntaje += 1

    #si hay preguntas en la lista
    if trivias:
        #saca de la lista de preguntas y respuesta la siguiente. pop amontona cuando saca elementos
        trivia = trivias.pop(0)
        tiempo_disponible = 10
    else:
        game_over()

def on_mouse_down(pos):
    """Función que verifica si hace click y este en las coordenadas adecuadas"""
    #index 1 representa la caja en respuestas 
    index = 1
    for caja in respuestas:
        #si se hace click en la caja
        if caja.collidepoint(pos):
        #si se hace click en la caja correcta (indice) y es = al ultimo elemento de trivias(index correcto)
            if index == trivia[5]:
                correcta()
            else:
                game_over()
        index += 1

def actualizar_tiempo():
    """Función que maneja el tiempo restante en pantalla"""
    global tiempo_disponible
    
    #si tiempo disponible no ha llegado a 0, sigue descontanto
    if tiempo_disponible:
        tiempo_disponible -= 1
    else:
        game_over()

#activar la funcion actualizar_tiempo mediante la función clock
clock.schedule_interval(actualizar_tiempo, 1.0)

pgzrun.go()