#Juego cuyo objetivo es replicar los movimientos secuenciales (flechas) presentados por la computadora, #pulsando las teclas de dirección simulando los pasos de un baile y un figurín en el centro de la pantalla.
#El jugador adquiere puntos si emula correctamente las pulsaciones de las flechas en pantalla. El juego
#termina cuando no se hace la se secuencia correctamente. 

import pgzrun
from random import randint

#ancho, largo y centro de la pantalla
WIDTH = 800
HEIGHT = 600
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2

#suiches que manejan los estados del juego
a_bailar = False
tiempo_contra = True
pases_completados = False
game_over = False

#listas con los pasos de baile a ejecutar y ejecutados
lista_pases = []
lista_pases_mostrados = []

#contadores
puntaje = 0
pase_actual = 0
cont = 0
duracion_baile = 4

#actores del juego. Imagen y posicionamiento
bailador = Actor("dancer-start")
bailador.pos = CENTER_X + 5, CENTER_Y + 135
arriba = Actor("up")
arriba.pos = CENTER_X + 5, CENTER_Y - 165
derecha = Actor("right")
derecha.pos = CENTER_X + 90, CENTER_Y - 90
abajo = Actor("down")
abajo.pos = CENTER_X + 5, CENTER_Y - 15
izquierda = Actor("left")
izquierda.pos = CENTER_X - 80, CENTER_Y - 90

def draw():
    """Maneja la presentación de los objetos(actores - texto - fondo) en la pantalla"""
    global game_over, puntaje, a_bailar
    global cont, tiempo_contra
    if not game_over:
        screen.clear()
        screen.blit("scenario", (0, 0))
        bailador.draw()
        derecha.draw()
        arriba.draw()
        abajo.draw()
        izquierda.draw()
        screen.draw.text("Puntos: " + str(puntaje), color="black", topleft=(20, 30))
        #si ya se mostró la secuencia (empieza a bailar)
        if a_bailar:
            screen.draw.text("A Bailar!", color="black", topleft=(CENTER_X - 80, 40), fontsize=60)
        #mostrar cuenta regresiva
        if tiempo_contra:
            screen.draw.text(str(cont), color="black", topleft=(CENTER_X - 8, 195), fontsize=60)
    #si el usuario pedió se desplegar mensajes y puntación
    else:
        screen.clear()
        screen.blit("scenario", (0, 0))
        screen.draw.text(str(puntaje), color="black", topleft=(10, 10))
        screen.draw.text("GAME OVER!!!", color="black", topleft=(CENTER_X - 130, 220), fontsize=60)
    return

def reiniciar_bailador():
    """Pone los actores en su posición inicial"""
    global game_over

    #si el juego esta activo
    if not game_over:
        bailador.image = "dancer-start"
        arriba.image = "up"
        derecha.image = "right"
        abajo.image = "down"
        izquierda.image = "left"
    return

def actualizar_bailador(pase):
    """actualiza los actores para mostar un paso de baile"""
    
    global game_over

    #si el juego esta activo y se presionan las teclas de dirección cambiar imagen por 0.5 segundos
    if not game_over:
        #si el pase es 0 movimiento hacia arriba se activa
        if pase == 0:
            arriba.image = "up-lit"
            bailador.image = "dancer-up"
            clock.schedule(reiniciar_bailador, 0.5)
        #si el pase es 1 movimiento hacia derecha se activa
        elif pase == 1:
            derecha.image = "right-lit"
            bailador.image = "dancer-right"
            clock.schedule(reiniciar_bailador, 0.5)
        #si el pase es 2 movimiento hacia abajo se activa
        elif pase == 2:
            abajo.image = "down-lit"
            bailador.image = "dancer-down"
            clock.schedule(reiniciar_bailador, 0.5)
        #si el pase es 3 movimiento hacia izquierda se activa
        else:
            izquierda.image = "left-lit"
            bailador.image = "dancer-left"
            clock.schedule(reiniciar_bailador, 0.5)
    return
        
def mostar_pases():
    """Muestra la serie de pases generados por el programa"""
    global lista_pases, lista_pases_mostrados, duracion_baile
    global a_bailar, tiempo_contra, pase_actual
    este_pase = 0

    #si hay pases que mostrar
    if lista_pases_mostrados:
        #poner el primer movimiento en la variable para que se pueda mirar que pase ocurrió
        este_pase = lista_pases_mostrados[0]
        #quitar el moviento que se uso en la variable y rearmar la lista. Cada ciclo va eliminado el 1ero
        lista_pases_mostrados = lista_pases_mostrados[1:]
        if este_pase == 0:
            #si no se hace la llamada recursiva por 1 segundo el cambio sería tan rápido que no se vería
            #si 1er valor de la lista es 0, el bailaó muestra el moviento hacia arriba
            actualizar_bailador(0)
            #hace una llamada recursiva a la función para que por un segundo sostenga el cambio de baile
            clock.schedule(mostar_pases, 1)
        elif este_pase == 1:
            #si 1er valor de la lista es 1, el bailaó muestra el moviento hacia derecha
            actualizar_bailador(1)
            #hace una llamada recursiva a la función para que por un segundo sostenga el cambio de baile
            clock.schedule(mostar_pases, 1)
        elif este_pase == 2:
            #si 1er valor de la lista es 2, el bailaó muestra el moviento hacia abajo
            actualizar_bailador(2)
            #hace una llamada recursiva a la función para que por un segundo sostenga el cambio de baile
            clock.schedule(mostar_pases, 1)
        else:
            #movimeinto hacia la izquierda
            actualizar_bailador(3)
            clock.schedule(mostar_pases, 1)
    else:
        #si ya se ejecutó la secuencia, se depliega un mensaje de bailar en pantalla
        #el tiempo para aprenderse los pasos se reinicia
        a_bailar = True
        tiempo_contra = False
    return
      
def generar_pasos():
    """Genera una lista con los pases de baile que se muestran en pantalla"""
    global lista_pases, duracion_baile, cont
    global tiempo_contra, a_bailar

    cont = 4
    lista_pases = []
    a_bailar = False

    #ciclo con de 4 movimientos para generar la secuencia y alamcenarlos en las listas
    for paso in range(0, duracion_baile):
        pase_aleatorio = randint(0, 3)
        lista_pases.append(pase_aleatorio)
        lista_pases_mostrados.append(pase_aleatorio)
    tiempo_contra = True
    cuenta_regresiva()
    return

def cuenta_regresiva():
    """Muestra un contador regresivo en pantalla para jugador memorice la secuencia"""
    global cont, game_over, tiempo_contra
    
    #si hay tiempo en el reloj, se va descontando de un segundo. 
    if cont > 1:
        cont -= 1
        #Llamada recursiva para que se logre ver el descuento
        clock.schedule(cuenta_regresiva, 1)
    else:
        tiempo_contra = False   
        mostar_pases()

def siguiente_pase():
    """Va al siguiente pase que exista en la lista de pasos"""
    global duracion_baile, pase_actual, pases_completados

    #si quedan pasos en la lista de generados pasa al siguiente
    if pase_actual < duracion_baile - 1:
        pase_actual = pase_actual + 1
    else:
        pases_completados = True
    return

def on_key_up(key):
    """Produce un evento al presionar una tecla"""
    
    global puntaje, game_over, lista_pases, pase_actual

    #si se presiona la tecla de arriba, el bailao se mueve hacia arriba
    if key == keys.UP:
        actualizar_bailador(0)
        #si arriba el es paso correcto en la secuencia otorga puntos
        if lista_pases[pase_actual] == 0:
            puntaje += 1
            siguiente_pase()
        #sino termina el juego
        else:
            game_over = True
    #si se presiona la tecla de derecha, el bailao se mueve hacia derecha
    elif key == keys.RIGHT:
        actualizar_bailador(1)
         #si derecha el es paso correcto en la secuencia otorga puntos
        if lista_pases[pase_actual] == 1:
            puntaje += 1
            siguiente_pase()
        #sino termina el juego
        else:
            game_over = True
    #si se presiona la tecla de abajo, el bailao se mueve hacia abajo
    elif key == keys.DOWN:
        actualizar_bailador(2)
         #si abajo el es paso correcto en la secuencia otorga puntos
        if lista_pases[pase_actual] == 2:
            puntaje += 1
            siguiente_pase()
        #sino termina el juego
        else:
            game_over = True
    #si se presiona la tecla de izquierda, el bailao se mueve hacia izquierda
    elif key == keys.LEFT:
        actualizar_bailador(3)
         #si izquierda el es paso correcto en la secuencia otorga puntos
        if lista_pases[pase_actual] == 3:
            puntaje += 1
            siguiente_pase()
        #sino termina el juego
        else:
            game_over = True
    return

generar_pasos()
music.play("vanishing-horizon")

def update():
    """Maneja todos los cambios lógicos del juego, cambio de pases"""
    global game_over, pase_actual, pases_completados

    #si el juego no ha acabado
    if not game_over:
        if pases_completados:
            generar_pasos()
            pases_completados = False
            pase_actual = 0
    else:
        music.stop()

pgzrun.go()