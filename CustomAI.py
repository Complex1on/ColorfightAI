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
            if c.cellType == 'gold':
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
    
def evaluate( c, enval, goldval, empty, disten, distgold ):
    goldencells = find_gold_cells()
    energycells = find_energy_cells()
    shortgold = 999
    shortenergy = 999
    bonus = 0
    for en in energycells:
        dist = distance_to(c,en)
        if dist < shortenergy:
            shortenergy = dist
    for gold in goldencells:
        dist = distance_to(c,gold)
        if dist < shortgold:
            shortgold = dist
    if shortenergy < 7:
        bonus += disten
    if shortgold < 7:
        bonus += distgold
    if c.owner == 0:
        bonus += empty
    if c.cellType == 'gold':
        bonus += goldval
    if c.cellType == 'energy':
        bonus += enval
    return bonus/c.takeTime
    

def smart_expand(enval, goldval, empty, disten, distgold):
    g.Refresh()
    surcells = surrounding_cells(my_cells())
    attacktarget = random.choice(surcells)
    bestval = evaluate(attacktarget,enval, goldval, empty, disten, distgold)
    for cell in surcells:
        value = evaluate(cell,enval, goldval, empty, disten, distgold)
        if value > bestval:
            attacktarget = cell
    print(g.AttackCell(attacktarget.x,attacktarget.y))
    return "working"

def rand_expand():
    #picks one of my cells and a random cell next to it to attack
    #picks random surrounding cell and attacks it
    randcell = random.choice(surrounding_cells(my_cells()))
    cinfo = g.GetCell(randcell.x,randcell.y)
    if cinfo.takeTime < 5:
        print(g.AttackCell(randcell.x,randcell.y))
    #picks a random surrounding cell and attacks it 

def behaviour():
    if g.baseNum < 3 and g.gold > 30:
        randcell = random.choice(my_cells())
        g.BuildBase(randcell.x,randcell.y)
    if g.cellNum < 50:
        enval = 5
        goldval = 3
        empty = 5
        disten = 10
        distgold = 10
        smart_expand(enval, goldval, empty, disten, distgold)
    

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

