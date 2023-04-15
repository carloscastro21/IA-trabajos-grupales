import pygame as pg
import numpy as np
from pygame.locals import *
import sys
from tkn_fnc import *

pg.init()

#colors
red= pg.Color(255,0,0)
black= pg.Color(0,0,0)
white= pg.Color(255,255,255)
lemon= pg.Color(155, 245, 130)
brown= pg.Color(185, 145, 50)


#vars
cln_color= white
brd_color= brown

size= 20
pixels= (10*size, 10*size)
window= pg.display.set_mode(pixels, pg.RESIZABLE)

class board:
    def __init__(self, rd_tkns= [[0,0],[0,2],[0,4],[0,6],[1,1],[1,3],[1,5],[1,7],[2,0],[2,2],[2,4],[2,6]], blck_tkns= [[5,1],[5,3],[5,5],[5,7],[6,0],[6,2],[6,4],[6,6],[7,1],[7,3],[7,5],[7,7]]):
        self.gm_brd= np.chararray((8,8))
        self.gm_brd[:]= '0'
        for i in rd_tkns:
            self.gm_brd[i[0]][i[1]]= 'r'
        for i in blck_tkns:
            self.gm_brd[i[0]][i[1]]= 'b'
        self.widht= len(rd_tkns)-len(blck_tkns)

    def draw_brd(self):
        for i in range(8):
            for j in range(8):
                if (i+j)%2==0:
                    pg.draw.rect(window, brd_color, pg.Rect(i*size+size, j*size+size, i*size+2*size, j*size+2*size))
class checker:
    def __init__(self, diff_: int, turn_: int):
        """
        diff_: difficult of game [1:3]
        """
        self.now_brd= board()
        self.diff= diff_
        
    #black bottom, red up
    
    def minimax(self):
        pass #Necesita retornar la posición de la siguiente ficha

    def run(self):
        pg.display.set_caption("Checkers")
        while True:
            window.fill(cln_color)
            for event in pg.event.get():
                if event.type==QUIT:
                    pg.quit()
                    sys.exit()

            self.now_brd.draw_brd()
            pg.display.update()