#Juego en el que una vaca se mueve en un jardin regando plantas. Las plantas se marchitan después de cierto
#tiempo si no son regadas. De igual manera, algunas de ellas se convierten en carnivoras que se comen la 
#vaca. El juego acaba cuando esto pasa o alguna planta se marchita totalmente (se mide el tiempo)

from random import randint
import pgzrun
import time

#dimensiones y cordenadas centrales de la ventana del juego
WIDTH = 800
HEIGHT = 600
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2

#variables globales que actuan como suiches para cambiar estados
game_over = False
terminado = False
jardin_feliz = True
colision_carnivora = False

#variables que llevan el registro del tiempo
tiempo_pasado = 0
tiempo_incial = time.time()

#sprite o actor principal del juego y su posición
vaca = Actor("cow")
vaca.pos = 100, 500

#listas que van a contener los objetos del juego, inicialmente vacias por no saber el número exacto
plantas = []
plantas_marchitas = []
carnivoras = []
vel_carnivoras_vertical = []
vel_carnivoras_horizontal = []

#poner los objetos en pantalla
def draw():
    """Maneja todos los objetos que aparecerán en pantalla"""
    global game_over, tiempo_pasado, terminado

    #si el juego no ha acabado poner los objetos y textos necesarios 
    if not game_over:
        #limpiar la pantalla, poner el fondo "el jardín"
        screen.clear()
        screen.blit("garden", (0, 0))

        #dibujar los objetos
        vaca.draw()
        for planta in plantas:
            planta.draw()
        for carnivora in carnivoras:
            carnivora.draw()
        
        #escribir el tiempo transcurrido en pantalla en la parte superior derecha
        tiempo_pasado = int(time.time() - tiempo_incial)
        screen.draw.text("Jardin Feliz por: " + str(tiempo_pasado) + " segundos", topleft=(10, 10), color="black")
    else:
        if not terminado:
            vaca.draw()
            screen.draw.text("Jardin Feliz por: " + str(tiempo_pasado) + " segundos ", topleft=(10, 10), color="black")
            if (not jardin_feliz):
                screen.draw.text("JARDIN TRISTE - GAME OVER", color="black", topleft=(10, 50))
                terminado = True
            else:
                screen.draw.text("TE MORDIERON - GAME OVER", color="black", topleft=(10, 50))
                terminado = True
    return

def nueva_planta():
    """Crea y almacena sprite de las plantas, con su posición, en la lista plantas """
    global plantas, plantas_marchitas

    new_planta = Actor("flower")
    new_planta.pos = randint(50, WIDTH - 50), randint(150, HEIGHT - 100)
    plantas.append(new_planta)
    #esta planta no esta marchita
    plantas_marchitas.append("feliz")

    return

def agregar_planta():
    """Pone plantas en la lista cada determinado tiempo"""
    global game_over
    #si el juego no ha terminado agrega plantas al jardin cada 4 segundos
    if not game_over:
        nueva_planta()
        clock.schedule(agregar_planta, 5)
    return

def tiempo_marchito():
    """Maneja el tiempo de marchitación, si se cumple se acaba el juego"""
    global plantas_marchitas, game_over, jardin_feliz

    #si hay plantas marchitandose
    if plantas_marchitas:
        for marchitandose in plantas_marchitas:
            #si no se ha regado la planta
            if(not marchitandose == "feliz"):
            #cuanto tiempo se ha ido marchitnado, si van más de 10s se vacia el jardin y se acaba el juego
                tiempo_marchitado = int(time.time() - marchitandose)
                if (tiempo_marchitado) > 10.0:
                    jardin_feliz = False
                    game_over =True
                    break
    return

def planta_marchita():
    """Hace que plantas aleatorias se marchiten cada determinado tiempo"""
    global plantas, plantas_marchitas, game_over

    #si el juego esta avtivo
    if not game_over:
        #si hay plantas en en el jardín
        if plantas:
            #escoger la planta aleatoria
            planta_aleatoria = randint(0, len(plantas) - 1)
            #si la planta esta feliz y sana se empieza a marchitar
            if(plantas[planta_aleatoria].image == "flower"):
                plantas[planta_aleatoria].image = "flower-wilt"
                #reinicia el tiempo de marchitación
                plantas_marchitas[planta_aleatoria] = time.time()

        #se hace el llamdo recursivo cada 3 segundos
        clock.schedule(planta_marchita, 1)
    return
            
def colision_planta():
    """Maneja la cercania de la imagenes de vaca y las plantas, para dar el efecto de regar la planta"""
    global vaca, plantas, plantas_marchitas
    index = 0
    for planta in plantas:
        #si la vaca esta cerca a la planta y se riega se cambia la imagen de la planta a feliz
        if (planta.colliderect(vaca) and planta.image == "flower-wilt"):
            planta.image = "flower"
            #para el tiempo de la planta que se esta marchitando
            plantas_marchitas[index] = "feliz"
            #se para el ciclo para no revisar otras plantas
            break
        index += 1
    return

def revisa_planta_carnivora():
    """Maneja si la carnivora encuentra a la vaca"""
    global vaca, carnivoras, colision_carnivora
    global game_over

    for carnivora in carnivoras:
        if carnivora.colliderect(vaca):
            vaca.image = "zap"
            game_over = True
            break
    return

def velocidad():
    """Maneja el movimiento de las plantas carnivoras, dirección y velocidad"""
    direccion_aleatoria = randint(0, 1)
    vel_aleatoria = randint(2, 3)
    
    #si la dirección es 0, moverse a la izquieda, si es 1 a la derecha
    if direccion_aleatoria == 0:
        return -vel_aleatoria
    else:
        return vel_aleatoria

def mutar():
    """Cambia las plantas aleatorias a carnivoras cada cierto tiempo"""
    global plantas, carnivoras, vel_carnivoras_horizontal
    global vel_carnivoras_vertical, game_over

    if not game_over and plantas:
        #tomar una planta al azar para transformarla
        planta_aleatoria = randint(0, len(plantas) - 1)
        pos_x_carnivora = plantas[planta_aleatoria].x
        pos_y_carnivora = plantas[planta_aleatoria].y

        #borrar la planta de las normales
        del plantas[planta_aleatoria]

        #poner la imagen de la planta carnivora y su posición
        planta_carnivora = Actor("fangflower")
        planta_carnivora.pos = pos_x_carnivora, pos_y_carnivora

        #mover la planta carnivora por el jardín con velocidad y dirección para más dificultad
        planta_carnivora_vel_x = velocidad()
        planta_carnivora_vel_y = velocidad()

        #agregar la planta carnivora  a la lista general de carnivoras
        planta_carnivora = carnivoras.append(planta_carnivora)

        #agregar las velocidades de las carnivoras en la lista de  coordenadas
        vel_carnivoras_horizontal.append(planta_carnivora_vel_x)
        vel_carnivoras_vertical.append(planta_carnivora_vel_y)

        #hacer la llamada recursiva a la función cada 20 segundos
        clock.schedule(mutar, 20)

    return

def actualizar_carnivoras():
    """maneja la posición de las carnivoras, esten siempre en el jardín"""
    global carnivoras, game_over

    if not game_over:
        index = 0
        for carnivora in carnivoras:
            #tomar las velociades de las carnivoras
            planta_carnivora_vel_x = vel_carnivoras_horizontal[index]
            planta_carnivora_vel_y = vel_carnivoras_vertical[index]

            #tomar la posición de las carnivoras
            carnivora.x += planta_carnivora_vel_x
            carnivora.y += planta_carnivora_vel_y

            #si la planta llegase a salir de pantalla, hacerla devolver
            if carnivora.left < 0:
                vel_carnivoras_horizontal[index] = -planta_carnivora_vel_x
            if carnivora.right > WIDTH:
                vel_carnivoras_horizontal[index] = -planta_carnivora_vel_x
            if carnivora.top < 150:
                vel_carnivoras_vertical[index] = -planta_carnivora_vel_y
            if carnivora.bottom > HEIGHT:
                vel_carnivoras_horizontal[index] = -planta_carnivora_vel_y
            index += 1
    return

def reinciar_vaca():
    global game_over
    if not game_over:
        vaca.image = "cow"
    return

#se llama la función al menos una vez para comenzar el proceso de agregar cada tiempo
agregar_planta()
planta_marchita()

def update():
    """Maneja los cambios lógicos del juego; estados, imagenes, movimientos ..."""
    global puntaje, game_over, colision_carnivora
    global plantas, carnivoras, tiempo_pasado

    colision_carnivora = revisa_planta_carnivora()

    #cuanto tiempo ha transcurrido para marchitarse
    tiempo_marchito()

    #si el juego no acaba mirar los eventos registrados por el teclado
    if not game_over:
        #si el usuario presiona la barra espaciadora la vaca riega plantas (se cambia la imagen)
        if keyboard.space:
            vaca.image = "cow-water"
            clock.schedule(reinciar_vaca, 0.5)
            colision_planta()
        #si se presiona la flechas de dirección la vaca se mueve sin salirse de los bordes
        if keyboard.left and vaca.x > 0:
            vaca.x -= 5
        elif keyboard.right and vaca.x < WIDTH:
            vaca.x += 5
        elif keyboard.up and vaca.y > 150: #se descuenta el alto de la imagen de la vaca
            vaca.y -= 5
        elif keyboard.down and vaca.y < HEIGHT:
            vaca.y += 5
        
        #si pasaron 15 segundos mutar a carnivoras
        if tiempo_pasado > 15 and not carnivoras:
            mutar()
        actualizar_carnivoras()

        
        
pgzrun.go()