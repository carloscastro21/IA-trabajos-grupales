import numpy as np
from random import *

def gen_graph(grp_size):
    gen = np.zeros((grp_size,grp_size),np.bool)
    for i in range(grp_size):
        for j in range(grp_size):
            tmp= not (i+j)%2
            gen[i][j]= tmp
    return gen

def delete(graph, percent):
    grp_size= len(graph) 
    total= ((grp_size**2)/2)*percent
    deleteds= 0
    while deleteds< total:
        x= randint(0, grp_size-1)
        y= randint(0, grp_size-1)
        if graph[x][y]:
            graph[x][y]= False
            deleteds+= 1
    return

