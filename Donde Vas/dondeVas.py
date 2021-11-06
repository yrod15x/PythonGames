#Enseñar los 4 puntos cardinales. El usuario debe moverse hacia donde se le dice

HEIGHT = 600
WIDTH = 800

plataforma = Actor("plataforma")
plataforma.pos = (WIDTH / 2, (HEIGHT / 2) + 10)
dinosario = Actor("dinowalk1")
dinosario.pos = (WIDTH / 2, (HEIGHT / 2) - 45)

def draw():
    screen.blit("fondo2",(0, 0))
    plataforma.draw()
    dinosario.draw()