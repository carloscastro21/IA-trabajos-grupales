import numpy as np
from random import randint
import pygame
import sys
from pygame.locals import *
from algorithms import *

pygame.init()

#Colors
red= pygame.Color(255,0,0)
black= pygame.Color(0,0,0)
white= pygame.Color(255,255,255)
green= pygame.Color(0,255,0)
blue= pygame.Color(0,0,255)


#Vars: Values in pixels
del_percent= 0.3
edge_size= 2
graph_size= 50
edge_distance= 20
node_radius= edge_distance/5
pixels= (graph_size*edge_distance+ edge_distance,graph_size*edge_distance+ edge_distance)
window= pygame.display.set_mode(pixels, pygame.RESIZABLE)
clean_color= black
node_color= red
edge_color= white
title= "A STAR"
graph = Graph(graph_size)

graph.delete(del_percent)

pygame.display.set_caption(title)

def graphic_nodes():
    for i in range(graph_size):
        for j in range(graph_size):
            if graph.graph[i][j]:
                pygame.draw.circle(window, node_color, (i*edge_distance+edge_distance,j*edge_distance+edge_distance), node_radius)
    return 0

def graphic_edges():
    for i in range(graph_size):
        for j in range(graph_size):
            adjs= graph.get_adjs(i,j)
            for l in adjs:
                if graph.graph[i][j] and graph.graph[l[0]][l[1]]:
                    pygame.draw.line(window, edge_color, (i*edge_distance+edge_distance,j*edge_distance+edge_distance), (l[0]*edge_distance+edge_distance,l[1]*edge_distance+edge_distance), edge_size)




def graphic_escenary():
    window.fill(clean_color) #Clean the window
    graphic_edges()
    graphic_nodes()
        

def main():
    graphic_escenary()
    mouse_pos1= None
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mouse_pos2= None
                if not mouse_pos1:
                    mouse_pos1= pygame.mouse.get_pos()
                    mouse_pos1= (int(mouse_pos1[0]/edge_distance)-1, int(mouse_pos1[1]/edge_distance)-1)
                else:
                    mouse_pos2= pygame.mouse.get_pos()
                    mouse_pos2= (int(mouse_pos2[0]/edge_distance)-1, int(mouse_pos2[1]/edge_distance)-1)
                    if graph.validate_range(mouse_pos1[0], mouse_pos1[1]) and graph.validate_range(mouse_pos2[0], mouse_pos2[1]):
                        #CODE: GETTING INIT AND END, RUN THE SEARCH ALGORITHM. 
                        print(mouse_pos1, mouse_pos2)
                    mouse_pos1= None
        pygame.display.update()
        graphic_escenary()

if __name__=="__main__":
    main()