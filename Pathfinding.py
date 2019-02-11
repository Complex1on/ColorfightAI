
import colorfight
import random
def my_cells():
    #Goes through the board and finds user's cells
    g.Refresh()
    mycells = []
    for x in range(g.width):
        for y in range(g.height):
            c = g.GetCell(x,y)
            if c.owner == g.uid:
                mycells.append(c)
    #returns a list of users cells in list form of [0] = x , [1] = y
    #print(mycells)
    return mycells

def GetAdjacent( cell ):
        up = g.GetCell( cell.x, cell.y - 1 )
        right = g.GetCell( cell.x + 1, cell.y )
        down = g.GetCell( cell.x, cell.y + 1 )
        left = g.GetCell( cell.x - 1, cell.y )
        return  [up, right, down, left]

def surrounding_cells(mycells):
    #takes mycells and finds the surrounding
    adjacentcells = []
    for cell in mycells:
        testcells = GetAdjacent(cell)
        for t in range(len(testcells)):
            if testcells[t].owner != g.iud and testcells[t] != None and testcells[t] not in adjacentcells:
                adjacentcells.append(testcells[t])

    #print(len(adjacentcells)            
    return adjacentcells

def find_gold_cells():
    #Finds all golden cells on the board
    gold_cells = []
    for x in range(g.width):
        for y in range(g.height):
            c = g.GetCell(x,y)
            if c.cellType == 'gold' and c.owner != g.uid:
                gold_cells.append(c)
    return gold_cells
    
def find_energy_cells():
    #Find all the energy cells on the board
    energy_cells = []
    for x in range(g.width):
        for y in range(g.height):
            c = g.GetCell(x,y)
            if c.cellType == 'energy':
                energy_cells.append(c)
    return energy_cells

def distance_to(start,end):
    return (abs(end.x-start.x) + abs(end.y-start.y))

def value(cell, target):
    return distance_to(cell,target) + cell.takeTime

def pathfinding(cell,target):
    dist = distance_to(cell,target)
    nextcell = cell
    path = []
    sortc = []
    while dist > 0:
        adjcells = GetAdjacent(nextcell)
        for x in adjcells:
            if x != g.uid:
                sortc.append((value(x,target),x))
        sortc.sort(key = lambda tup: tup[0])
        path.append(sortc[0][1])
        nextcell = sortc[0][1]
    print(path)
    return path


def energy_expand():
    cell = my_cells()
    encells = find_energy_cells()
    start = random.choice(cell)
    end = random.choice(encells)
    path = pathfinding(start,end)
    print(start,end,path)
    for x in path:
        print(g.AttackCell(x.x,x.y))
        path.remove(x)

if __name__== '__main__':
    g = colorfight.Game()
    if g.JoinGame('test'):
        print('hello')
        while True:
            energy_expand()
    else:
        print("Failed to join game")