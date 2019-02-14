 # You need to import colorfight for all the APIs
import colorfight
import random
lastattacked = None
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
        return ( up, right, down, left )

def surrounding_cells(mycells):
    #takes mycells and finds the surrounding
    adjacentcells = []
    for cell in mycells:
        up, right, down, left = GetAdjacent(cell)
        if up != None and up.owner != g.uid and (up not in adjacentcells): 
            adjacentcells.append(up)
        if right != None and right.owner != g.uid and (right not in adjacentcells): 
            adjacentcells.append(right)
        if down != None and down.owner != g.uid and (down not in adjacentcells): 
            adjacentcells.append(down)
        if left != None and left.owner != g.uid and (left not in adjacentcells): 
            adjacentcells.append(left)
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

def path_to(cell, target):
    return distance_to(cell,target) + cell.takeTime

def gold_expand():
    g.Refresh()
    surcell = surrounding_cells(my_cells())
    goldcells = find_gold_cells()
    data = []
    lastattacked = None
    for cell in surcell:
        for gold in goldcells:
            score = path_to(cell,gold)
            data.append((score,cell))
    data.sort(key = lambda tup: tup[0])
    #print(data[0])
    if data[0] != lastattacked:
        lastattacked = g.AttackCell(data[0][1].x,data[0][1].y)

def energy_expand():
    g.Refresh()
    surcell = surrounding_cells(my_cells())
    encells = find_energy_cells()
    data = []
    for cell in surcell:
        for en in encells:
            score = path_to(cell,en)
            data.append((score,cell))
    data.sort(key = lambda tup: tup[0])
    #print(data[0])
    global lastattacked
    target = data[0][1]
    if lastattacked == None:
        lastattacked = target
        print(g.AttackCell(target.x,target.y))
    if (target.x != lastattacked.x) and (target.y != lastattacked.y):
        lastattacked = target
        print(g.AttackCell(target.x,target.y))  

def evaluate( c, enval, goldval, empty):
    bonus = 0
    if c.takeTime < 5:
        bonus += 3
    if c.owner == 0:
        bonus += empty
    if c.cellType == 'gold':
        bonus += goldval
    if c.cellType == 'energy':
        bonus += enval
    return bonus/c.takeTime

def smart_expand(enval, goldval, empty, boostval):
    g.Refresh()
    surcells = surrounding_cells(my_cells())
    attacktarget = random.choice(surcells)
    bestval = evaluate(attacktarget,enval, goldval, empty)
    for cell in surcells:
        value = evaluate(cell,enval, goldval, empty)
        if value > bestval:
            attacktarget = cell
    print(g.AttackCell(attacktarget.x,attacktarget.y,boost=boostval))
    return "working"

def rand_expand():
    #picks one of my cells and a random cell next to it to attack
    #picks random surrounding cell and attacks it
    randcell = random.choice(surrounding_cells(my_cells()))
    cinfo = g.GetCell(randcell.x,randcell.y)
    if cinfo.takeTime < 3:
        print(g.AttackCell(randcell.x,randcell.y))
    #picks a random surrounding cell and attacks it 

def behaviour():
    boostval = False
    if g.baseNum < 3 and g.gold > 30:
        randcell = random.choice(my_cells())
        g.BuildBase(randcell.x,randcell.y)
    if g.energy >=45:
        boostval = True
    if g.cellNum < 100:
        energy_expand()
    if g.cellNum < 150 and g.cellNum > 100:
        enval = 10
        goldval = 5
        empty = 7
        smart_expand(enval, goldval, empty, boostval)  
    else: 
        enval = 3
        goldval = 25
        empty = 12
        smart_expand(enval, goldval, empty, boostval)
    
if __name__ == '__main__':
    # Instantiate a Game object.
    g = colorfight.Game()
    lastattacked = None 
    if g.JoinGame('C2'):
        print('hello')
        while True:
            g.Refresh() 
            behaviour()     
    else:
        print("Failed to join the game!")

