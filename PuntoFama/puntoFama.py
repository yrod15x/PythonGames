import random

NUM_DIGITOS = 4
NUN_CHANCES = 10

def numero_secreto():
    #Devuelve el numero (cadena de texto) a adivinar. 
    numeros = list(range(10))
    random.shuffle(numeros)
    num_secreto = ''
    for i in range(NUM_DIGITOS):
        num_secreto += str(numeros[i])
    return num_secreto
    
def dar_pistas(jugada, num_secreto):
    #Devuelve Punto o Fama de acuerdo al numero ingresado por el usuario
    if jugada == num_secreto:
        print('Usted ha ganado !!! - Felicidades !!!')
        
    pistas = []
    for i in range(len(jugada)):
        if jugada[i] == num_secreto[i]:
            pistas.append('Fama')
        elif jugada in num_secreto:
            pistas.append('Punto')
    if len(pistas) == 0:
        return 'La Nada'
    
    #Para que el feedback de las pistas no salga en orden y sea más difícil el juego
    pistas.sort()
    return ' '.join(pistas)
    
def solo_digitos(numero):
    #Devuelve True si solo hay digitos en la entrada (num)
    digitos = '1234567890'
    if numero == '':
        return False
    for i in numero:
        if i not in digitos:
            return False
    return True

def mostar_menu():
    print(f'*** Bienvenido a Punto & Fama ***')
    print()
    print(f'Deseo que adivines un numero de {NUM_DIGITOS} cifras - Solo tienes {NUN_CHANCES} para adivinar')
    print(f'Te voy a dar 3 pistas pos cada intento - Estas son: ')
    print('Fama --> Un digito de tu numero es correcto y en la posicion adecuada')
    print('Punto --> Un digito de tu numero es correcto y pero no en la posicion adecuada')
    print('La Nada --> Ningun numero es correcto')
    print()
    
mostar_menu()

while True:
    num_secreto = numero_secreto()
    print('Ooopps!!! Solo tienes ', end='')
    
    num_jugados = 0 
    while num_jugados <= NUN_CHANCES:
        jugado = ''
        while len(jugado) != NUM_DIGITOS or not solo_digitos(jugado):
            print(f'{NUN_CHANCES - num_jugados} Oportunidades Restantes')
            print('Ingresa tu numero: ', end='')
            jugado = input()
        print(dar_pistas(jugado, num_secreto))
        num_jugados += 1
        
        if jugado == num_secreto:
            break
        if num_jugados > NUN_CHANCES:
            print(f'Ya no hay oprtunidades - Usted ha perdido!!! - El numero secreto era {num_secreto}')
    print('Deseas jugar otra vez? - Presione (si) para seguir - Cualquier otra tecla para salir ')
    if not input().lower().startswith('y'):
        break

    
