import pygame

import networkx as nx

import random

import time

import heapq

try:
    pygame.init()
except:
    print("Erro. Programa não inicializado")


WIDTH = 500
HEIGHT = 600
FPS = 30

tela = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption ("MazegenPRIM-DCShortestPath")


# Define colours
WHITE = (255, 255, 255)
GREEN = (0, 255, 0,)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
PURPLE = (255, 0, 255)
YELLOW = (255,255,0)

w=20

# build the grid
def build_grid(x, y, w):
    x = 0
    y = 0 
    for i in range(1,21):
        x = 20                                                            
        y = y + 20                                                        
        for j in range(1, 21):
            pygame.draw.line(tela, WHITE, [x, y], [x + w, y])           
            pygame.draw.line(tela, WHITE, [x + w, y], [x + w, y + w])   
            pygame.draw.line(tela, WHITE, [x + w, y + w], [x, y + w])   
            pygame.draw.line(tela, WHITE, [x, y + w], [x, y])           
            x = x + 20                                                    


def up(y, x):
    x=20*(x+1)
    y=20*(y+1)
    pygame.draw.rect(tela, GREEN, (x + 1, y - 20 + 1, 19, 39), 0)        
    pygame.display.update()                                              
    #time.sleep(2)

def down(y, x):   
    x=20*(x+1)
    y=20*(y+1)
    pygame.draw.rect(tela, GREEN, (x +  1, y + 1, 19, 39), 0)
    pygame.display.update()
    #time.sleep(2)


def left(y, x):
    x=20*(x+1)
    y=20*(y+1)
    pygame.draw.rect(tela, GREEN, (x - 20 +1, y +1, 39, 19), 0)
    pygame.display.update()
    #time.sleep(2)


def right(y, x):
    x=20*(x+1)
    y=20*(y+1)
    pygame.draw.rect(tela, GREEN, (x +1, y +1, 39, 19), 0)
    pygame.display.update()
    #time.sleep(2)


def colup(y, x, color):
    x=20*(x+1)
    y=20*(y+1)
    pygame.draw.rect(tela, color, (x + 1, y - 20 + 1, 19, 39), 0)        
    pygame.display.update()                                              
    #time.sleep(2)

def coldown(y, x, color):   
    x=20*(x+1)
    y=20*(y+1)
    pygame.draw.rect(tela, color, (x +  1, y + 1, 19, 39), 0)
    pygame.display.update()
    #time.sleep(2)


def colleft(y, x, color):
    x=20*(x+1)
    y=20*(y+1)
    pygame.draw.rect(tela, color, (x - 20 +1, y +1, 39, 19), 0)
    pygame.display.update()
    #time.sleep(2)


def colright(y, x, color):
    x=20*(x+1)
    y=20*(y+1)
    pygame.draw.rect(tela, color, (x +1, y +1, 39, 19), 0)
    pygame.display.update()
    #time.sleep(2)

#Random DFS

G = nx.grid_2d_graph(20,20)
#Graph of the mst(edge = 1 means it connects the two nodes)
GMAZE = nx.grid_2d_graph(20,20)

for (x, y) in GMAZE.edges():
    GMAZE.edges[x, y]['weight'] = 0

def randUnvisitedNeighbor(vertex):
    unvNeigh = []
    neigh = G[vertex]
    for (x, y) in neigh:
        if G.nodes[(x, y)] != {'visited': 1} :
            unvNeigh.append((x, y))

    if len(unvNeigh) >= 1:
        chosenVertex = random.choice(unvNeigh)

    else:
        chosenVertex = False

    return chosenVertex

def moveCell(vertex, nextVertex):
    (x, y) = vertex
    (x2, y2) = nextVertex

    if x == x2:
        if y < y2:
            time.sleep(.05)
            right(x, y)
        else:
            time.sleep(.05)
            left(x, y)
    else:
        if x < x2:
            time.sleep(.05)
            down(x, y)
        else:
            time.sleep(.05)
            up(x, y)

def moveCellColor(vertex, nextVertex, color):
    (x, y) = vertex
    (x2, y2) = nextVertex

    if x == x2:
        if y < y2:
            time.sleep(.05)
            colright(x, y, color)
        else:
            time.sleep(.05)
            colleft(x, y, color)
    else:
        if x < x2:
            time.sleep(.05)
            coldown(x, y, color)
        else:
            time.sleep(.05)
            colup(x, y, color)

#Instead of iterating through the neigbors it chooses one randomly
def randomDFS(vertex):
    G.nodes[vertex]['visited'] = 1
    nextVertex = randUnvisitedNeighbor(vertex)

    while nextVertex:
        moveCell(vertex, nextVertex)
        GMAZE.edges[vertex, nextVertex]['weight'] = 1
        randomDFS(nextVertex)
        nextVertex = randUnvisitedNeighbor(vertex)
    
#MST MAZE
def randomEdgesWeight():
    for (u, v) in G.edges():
        G.edges[u, v]['weight'] = random.randint(0,100)
#=====================================================================================
def Prim():
    h = []
    s = []
    a = []
    i =0
    rep=-1
    temp = []
    for (x, y) in G.nodes():
        a.append(101)
        heapq.heappush(h, (a[20*x + y], (x, y)))

    while(h != []):
        heapq.heapify(h)
        u = heapq.heappop(h)
        if rep == -1:
            u = (0, (0,0))
        if rep != -1:
            for (x, y) in G[u[1]]:
                if (x ,y) in s:
                    temp.append((x, y))

            lesser = -1
            lesserxy = 0
            for (x, y) in temp:
                if lesser < a[20*x + y]:
                    lesser = a[20*x + y]
                    lesserxy = (x, y)
            moveCell(u[1], lesserxy)
            GMAZE.edges[u[1], lesserxy]['weight'] = 1
            temp = []

        rep = 1
        s.append(u[1])
        neigh = G[u[1]]
        for (x, y) in neigh:
            if (x, y) not in s:
                if G.edges[u[1],(x, y)]['weight'] < a[20*x + y]:
                    a[20*x + y] = G.edges[u[1],(x, y)]['weight']
                    for i in range(len(h)):
                        if h[i][1] == (x, y):
                            h[i] = (a[20*x + y], (x, y))      
                            break          
#====================================================================================
#ShortestPath Divide and Conquer
def DCShortestPath(N, xo, yo, xd, yd, xf, yf, contr, distance=0, curCol = RED):
    if xd > xf or yd > yf:
        return 400
    
    if xd < 0 or yd < 0:
        return 400

    if xo > xf or yo > yf:
        return 400
    
    if xo < 0 or yo < 0:
        return 400
    
    if (xo != xd or yo != yd) and GMAZE.edges[(xo, yo),(xd, yd)]['weight'] == 0:
        return 400

    else:
        if xd == 19 and yd == 19:
            moveCellColor((xo, yo),(xd, yd), BLUE) 
            return distance

        if contr == -1:
            return min(DCShortestPath(N, xd, yd, xd+1, yd, xf, yf, 0, distance +1, RED), DCShortestPath(N, xd, yd, xd, yd+1, xf, yf, 1,distance +1, RED), DCShortestPath(N, xd, yd, xd-1, yd, xf, yf, 2,distance +1, RED), DCShortestPath(N, xd, yd, xd, yd-1, xf, yf, 3,distance +1, RED))    
        
        if contr == 0:
            moveCellColor( (xd, yd),(xo, yo), curCol)
            zmark=min(DCShortestPath(N, xd, yd, xd+1, yd, xf, yf, 0, distance +1, curCol), DCShortestPath(N, xd, yd, xd, yd+1, xf, yf, 1,distance +1, curCol), DCShortestPath(N, xd, yd, xd, yd-1, xf, yf, 3,distance +1, curCol))
            if zmark != None and zmark <400:
                moveCellColor((xd, yd),(xo, yo), BLUE)
            return zmark   

        if contr == 1:
            moveCellColor((xo, yo), (xd, yd), curCol)
            onemark =min(DCShortestPath(N, xd, yd, xd+1, yd, xf, yf, 0, distance +1, curCol), DCShortestPath(N, xd, yd, xd, yd+1, xf, yf, 1,distance +1, curCol), DCShortestPath(N, xd, yd, xd-1, yd, xf, yf, 2,distance +1, curCol))
            if onemark != None and onemark <400:
                moveCellColor((xd, yd),(xo, yo), BLUE)
            return onemark
        if contr == 2:

            moveCellColor((xo, yo), (xd, yd), curCol)
            twomark = min(DCShortestPath(N, xd, yd, xd, yd+1, xf, yf, 1,distance +1, curCol), DCShortestPath(N, xd, yd, xd-1, yd, xf, yf, 2,distance +1, curCol), DCShortestPath(N, xd, yd, xd, yd-1, xf, yf, 3,distance +1, curCol))
            if twomark != None and twomark <400:
                moveCellColor((xd, yd),(xo, yo), BLUE)
            return twomark
        if contr == 3:

            moveCellColor((xo, yo), (xd, yd), curCol)
            threemark = min(DCShortestPath(N, xd, yd, xd+1, yd, xf, yf, 0, distance +1, curCol), DCShortestPath(N, xd, yd, xd-1, yd, xf, yf, 2,distance +1, curCol), DCShortestPath(N, xd, yd, xd, yd-1, xf, yf, 3,distance +1, curCol))
            if threemark != None and threemark <400:
                moveCellColor((xd, yd),(xo, yo), BLUE)
            return threemark

#================================================================================================
#Shortest Path BellmanFord

def createMaze():
    startVertex = (0, 0)
    randomDFS(startVertex)

build_grid(40, 0, 20) 
#createMaze()
randomEdgesWeight()
Prim()

distance = 0
short = DCShortestPath(20, 0, 0, 0, 0, 19, 19, -1, distance)
print(short)

pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
myfont = pygame.font.SysFont('Comic Sans MS', 25)

textsurface = myfont.render('O menor caminho entre 0,0 e 19,19 passa por ' + str(short) + ' Nós', 1, (255, 0, 255))

tela.blit(textsurface,(2,500))


sair = True

while sair:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sair = False
    pygame.display.update()

pygame.quit()