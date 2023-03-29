import numpy as np
from random import randint


class Graph:
    def __init__(self, graph_size_: int):
        self.graph= np.full((graph_size_,graph_size_), True)
        self.graph_size= graph_size_

    def delete(self, del_percent: float):
        total= ((self.graph_size**2)/2)*del_percent
        deleteds= 0
        while deleteds< total:
            x= randint(0, self.graph_size-1)
            y= randint(0, self.graph_size-1)
            if self.graph[x][y]:
                self.graph[x][y]= False
                deleteds+= 1

    def validate_range(self, x: int, y: int):
        return (-1<x<self.graph_size and -1<y<self.graph_size)
    
    def get_adjs(self, x: int, y: int):
        adjs= None
        if not (x+y)%2:
            adjs= [[x-1,y-1],[x-1,y],[x-1,y+1],[x,y+1],[x+1,y+1],[x+1,y],[x+1,y-1],[x,y-1]]
        else:
            adjs= [[x-1,y],[x,y+1],[x+1,y],[x,y-1]]
        aux= adjs[:]
        for i in aux:
            if (self.validate_range(i[0], i[1])):
                continue
            adjs.remove(i)
        return adjs
    
    def by_a_star_h(self, start: list, end: list):
        adjs= self.get_adjacents(start[0], start[1])
        def heuristic(i: list):
            return self.distance(start, i) + self.distance(i, end)
        adjs.sort(key= heuristic)
        return adjs
    
    def by_h(self, start: list, end: list):
        adjs= self.get_adjacents(start[0], start[1])
        def heuristic(i: list):
            return self.distance(i, end)
        adjs.sort(key= heuristic())
        return adjs

    def distance(point_a: list, point_b: list):
        return np.linalg.norm(point_a - point_b)

def a_star(graph: Graph, start: list, end: list, road: list= None, visiteds: list= None):
    if not visiteds: 
        visiteds= np.full((graph.graph_size, graph.graph_size), False)
    for i in graph.by_a_star_h(start, end):
        road
    
    return road