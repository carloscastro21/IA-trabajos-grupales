from checker import *


diff= int(input("Indique el nivel de árbol[3:5]:\n"))
turn= int(input("Indique quién empieza:\n1: Sistema\n2: Jugador\n"))
game= checker(diff, turn)

#Definir quien empieza
#Arbol minimax
#Comer una sola vez
#Ingresar nivel (del arbol)
#Función restar número de piezas
#Opcional: alpha-beta, c++

if __name__=="__main__":
    game.run()