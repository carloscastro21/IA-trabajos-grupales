import pygame
import numpy as np
from pygame.locals import *
import sys
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

pygame.init()

#Colors
red= pygame.Color(255,0,0)
black= pygame.Color(0,0,0)
white= pygame.Color(255,255,255)
brown= pygame.Color(184,134,11)
l_green= pygame.Color(144,238,144)

#Vars
#lvls= int(input("Ingrese el nivel del árbol:\n"))
#start= int(input("Seleccione quién empieza:\n1. Jugador\n2. Máquina\n"))
size= 60
w_size= (size*10, size*10)
gm_brd= np.chararray((8,8))
gm_brd[:]= '0'
window= pygame.display.set_mode(w_size, pygame.RESIZABLE)
title= "CHECKERS"
cln_color= white
brd_color= brown
tkn_rad= int(size/3)

pygame.display.set_caption(title)

def init_brd():
    for i in range(3):
        for j in range(8):
            if not (i+j)%2:
                gm_brd[i][j]= b'r'
    for i in range(5, 8):
        for j in range(8):
            if not (i+j)%2:
                gm_brd[i][j]= b'b'

init_brd()

def draw_brd(board: np.chararray):
    pygame.draw.rect(window, brown, (size, size, size*8, size*8), 2)
    for i in range(8):
        for j in range(8):
            if not (i+j)%2:
                pygame.draw.rect(window, brown, ((j+1)*size, (i+1)*size, size, size))
            if board[i][j]==b'r':
                pygame.draw.circle(window, red, ((j+1)*size+ size/2,(i+1)*size+ size/2), tkn_rad)
            elif board[i][j]==b'b':
                pygame.draw.circle(window, black, ((j+1)*size+ size/2,(i+1)*size+ size/2), tkn_rad)

def draw():
    window.fill(cln_color) #clear window
    draw_brd(gm_brd)

def weight(board: np.chararray):
    """
    Devuelve el número de fichas rojas menos las negras
    """
    return (board.count(b'r')- board.count(b'b')).sum()


def run():
    while True:
        draw()
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

if __name__=="__main__":
    run()
>>>>>>> dd03b0b7e0798a339b154921dd6354b63a59e414
