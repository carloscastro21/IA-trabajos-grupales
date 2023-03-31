#ESTE ES EL CODIGO PRESENTADO EN CLASES
import pygame
import math 
import random
import json
from collections import deque
import random

WIDTH, HEIGHT = 1920, 1080
NODE_RADIUS = 5
N_NODES = int(input('Numero de nodos: '))
MIN_DIST_NODES = 3
ALGORITHM = input('Que algoritmo quiere usar: ')
pygame.init()
SCREEN = pygame.display.set_mode((0, 0))
pygame.display.set_caption("Graph")
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont("bahnschrift", 25)


def display_msg(msg):
    SCREEN.blit(msg, [200, 200])
    pygame.display.update()
    SCREEN.fill((0, 0, 0))

def generate_edges(nodes):
    graph = [[] for i in range(N_NODES)]
    edges = []
    for i, node in enumerate(nodes):
        x, y = node
        adjacent_nodes = [enum[0] for enum in enumerate(nodes) if ((enum[1][0]-x)**2 + (enum[1][1]-y)**2)**0.5 <= 29 and enum[0] != i]
        for adj_node in adjacent_nodes:
            if adj_node not in graph[i]:
                p = tuple(sorted((i, adj_node)))
                if p not in edges:
                    edges.append(p)
                graph[i].append(adj_node)
                graph[adj_node].append(i)
        msg = FONT.render("Nodes Processed to create edges: {}/{}".format(i, N_NODES), True, (255, 255, 255))
        display_msg(msg)
    return graph, edges



def delete_nodes(nodes, delete_percentage):
    n_to_delete = int(len(nodes) * (delete_percentage / 100.0))
    nodes_to_delete = random.sample(nodes, n_to_delete)
    new_nodes = [node for node in nodes if node not in nodes_to_delete]
    return new_nodes



def generate_nodes():
    nodes = []
    count = len(nodes) 
    numero = math.sqrt(N_NODES)
    it_x = 0
    y = NODE_RADIUS
    while count < N_NODES:
        if count % numero == 0 and count != 0:
            it_x = 0;
            x = NODE_RADIUS + 20*it_x
            y = y + 20
        else :
            x = NODE_RADIUS + 20*it_x

        flag = False
        for x1, y1 in nodes:
            distance = 30
            if distance < MIN_DIST_NODES:
                flag = True
        if flag:
            continue
        nodes.append((x, y))
        count += 1
        it_x += 1
        msg = FONT.render("Nodes Created:{}/{}".format(count, N_NODES), True, (255, 255, 255))
        display_msg(msg)
    nodes = delete_nodes(nodes,30)
    return nodes




def display(visited_nodes, visited_edges, nodes, edges):
    for i, edge in enumerate(edges):
        u, v = edge
        if visited_edges[i]:
            pygame.draw.line(SCREEN, (255, 0, 0), nodes[u], nodes[v])
        else:
            pygame.draw.line(SCREEN, (255, 255, 0), nodes[u], nodes[v])
    
    for i, node in enumerate(nodes):
        if visited_nodes[i]:
            pygame.draw.circle(SCREEN, (255, 0, 0), node, NODE_RADIUS)
        else:
            pygame.draw.circle(SCREEN, (255, 255, 255), node, NODE_RADIUS)
    pygame.display.update()


def dfs(start, target, n_nodes, graph, visited_nodes, visited_edges, nodes, edges):
    stack = deque([start])
    visited_nodes[start] = True
    while stack:
        u = stack.pop()
        display(visited_nodes, visited_edges, nodes, edges)
        #pygame.draw.circle(SCREEN, (0, 255, 0), (20*(start%20)+5,(start%20)*20), NODE_RADIUS) 
        #pygame.draw.circle(SCREEN, (0, 255, 0), (20*(target%20)+5,(target%20)*20), NODE_RADIUS)
        if u == target:
            break
        for v in graph[u]:
            if not visited_nodes[v]:
                stack.append(v)
                visited_nodes[v] = True
                edge = tuple(sorted([u, v]))
                edge_index = edges.index(edge)
                visited_edges[edge_index] = True

def bfs(start, target, n_nodes, graph, visited_nodes, visited_edges, nodes, edges):
    queue = deque([start])
    visited_nodes[start] = True
    while queue:
        u = queue.popleft()
        display(visited_nodes, visited_edges, nodes, edges)
        if u == target:
            break
        for v in graph[u]:
            if not visited_nodes[v]:
                queue.append(v)
                visited_nodes[v] = True
                edge = tuple(sorted([u, v]))
                edge_index = edges.index(edge)
                visited_edges[edge_index] = True







def run():
    nodes = generate_nodes()
    graph, edges = generate_edges(nodes)
    n_edges = len(edges)
    visited_nodes = [False]*N_NODES
    visited_edges = [False]*n_edges
    start_node = None
    target_node = None
    display(visited_nodes, visited_edges, nodes, edges)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, node in enumerate(nodes):
                    dist = math.sqrt((node[0]-mouse_pos[0])**2 + (node[1]-mouse_pos[1])**2)
                    if dist <= NODE_RADIUS:
                        if start_node is None:
                            start_node = i
                        elif target_node is None and i != start_node:
                            target_node = i
                        if i == target_node:
                            print("Target node clicked!")
                if start_node is not None and target_node is not None:
                    if ALGORITHM == "DFS":
                        dfs(start_node, target_node, N_NODES, graph, visited_nodes, visited_edges, nodes, edges)
                    else:
                        bfs(start_node, target_node, N_NODES, graph, visited_nodes, visited_edges, nodes, edges)
                        #return
        pygame.display.update()

run()

