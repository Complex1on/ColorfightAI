 # You need to import colorfight for all the APIs
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

def surrounding_cells(mycells):
    #takes mycells and finds the surrounding
    direct = [[0,1], [0,-1], [1, 0], [-1,0]]
    adjacentcells = []
    for cell in mycells:
        for d in range(4):
            x = cell.x+direct[d][0]
            y = cell.y+direct[d][1]
            cc = g.GetCell(x,y)
            if cc != None and cc.owner != g.uid and (cc not in adjacentcells):
                adjacentcells.append(cc)
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

def GetAdjacent( cell ):
        up = g.GetCell( cell.x, cell.y - 1 )
        right = g.GetCell( cell.x + 1, cell.y )
        down = g.GetCell( cell.x, cell.y + 1 )
        left = g.GetCell( cell.x - 1, cell.y )
        return ( up, right, down, left )

def distance_to(start,end):
    return (abs(end.x-start.x) + abs(end.y-start.y))

def path_to(cell, target):
    return distance_to(cell,target) + cell.takeTime

def gold_expand():
    surcell = surrounding_cells(my_cells())
    goldcells = find_gold_cells()
    data = []
    
    for cell in surcell:
        for gold in goldcells:
            score = path_to(cell,gold)
            data.append((score,cell))
    data.sort(key = lambda tup: tup[0])
    print(g.AttackCell(data[0][1].x,data[0][1].y))

    

     
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
    if g.cellNum < 200:
        gold_expand()
    if g.cellNum < 400 and g.cellNum > 200:
        enval = 10
        goldval = 5
        empty = 7
        smart_expand(enval, goldval, empty, boostval)  
    else: 
        enval = 3
        goldval = 15
        empty = 12
        smart_expand(enval, goldval, empty, boostval)
    

if __name__ == '__main__':
    # Instantiate a Game object.
    g = colorfight.Game()
    if g.JoinGame('Dumb'):
        print('hello')
        while True:
            g.Refresh()
            #rand_expand() 
            behaviour()     
    else:
        print("Failed to join the game!")

