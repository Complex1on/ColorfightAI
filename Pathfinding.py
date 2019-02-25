import colorfight
import random

lastattacked = None

def lastattackedcell(cell):
    global lastattacked
    if lastattacked == None:
        lastattacked = cell
        return False
    elif (cell.x != lastattacked.x) and (cell.y != lastattacked.y):
        lastattacked = cell
        return False
    else:
        return True

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
            if c.cellType == 'gold' and c.owner != g.uid and c.isTaking == False:
                gold_cells.append(c)
    return gold_cells
    
def find_energy_cells():
    #Find all the energy cells on the board
    energy_cells = []
    for x in range(g.width):
        for y in range(g.height):
            c = g.GetCell(x,y)
            if c.cellType == 'energy' and c.owner != g.uid:
                energy_cells.append(c)
    return energy_cells

def get_info():
    g.Refresh()
    mycells = my_cells()
    surcells = surrounding_cells(my_cells())
    goldcells = find_gold_cells()
    energy_cells = find_energy_cells()
    return (mycells, surcells, goldcells, energy_cells)

def attack_line(cell,end,mode):
    global lastattacked
    if mode == "horiz":
        if end > 0:
            x = 1
            stepx = 1
        else:
            x = -1
            stepx = -1
        while x != end:
            g.Refresh()
            check = g.GetCell(cell.x+x,cell.y)
            if g.cdTime < g.currTime and check.owner != g.uid:                
                print(g.AttackCell(cell.x + x, cell.y ))
                x += stepx
                

    if mode == "vert":
        if end > 0:
            x = 1
            stepx = 1
        else:
            x = -1
            stepx = -1
        while x != end:
            g.Refresh()
            check = g.GetCell(cell.x,cell.y + x)
            if g.cdTime < g.currTime and check.owner != g.uid:
                
                print(g.AttackCell(cell.x , cell.y + x))
                x += stepx
                

def path_to(start,end):
    deltax = end.x - start.x
    deltay = end.y - start.y
    if deltax==0:
        if deltay < 0:
            deltay-=1
        if deltay>0:
            deltay+=1
        attack_line(start,deltay,"vert")
    elif deltay==0:
        if deltax<0:
            deltax-=1
        if deltax>0:
            deltax+=1
        attack_line(start,deltax,"horiz")
    else:
        if deltax < 0:
            deltax-=1
        if deltax>0:
            deltax+=1
        if deltay<0:
            deltay-=1
        if deltay>0:
            deltay+=1
        attack_line(start,deltax,"horiz")
        finishedx=g.GetCell(end.x,start.y)
        attack_line(finishedx,deltay,"vert")
      

def distance_to(start,end):
    return (abs(end.x-start.x) + abs(end.y-start.y))


def Expand_energy():
    lowestdist = []
    for cell in info[0]:
        for energy in info[3]:
            start = g.GetCell(cell.x,cell.y)
            end = g.GetCell(energy.x,energy.y)
            dist = distance_to(start,end)
            if lowestdist == [] and end.isTaking==False:
                lowestdist.append((dist,start,end))
            elif lowestdist[0][0] > dist and end.isTaking==False:
                lowestdist.pop(0)
                lowestdist.append((dist,start,end))

    print(lowestdist)
    path_to(lowestdist[0][1], lowestdist[0][2])
    
    
        



if __name__== '__main__':
    g = colorfight.Game()
    if g.JoinGame('It gonna break'):
        print('hello')
        #info = get_info()
        #start = random.choice(info[0])
        #start = g.GetCell(29,0)
        #end = random.choice(info[2])
        #end = g.GetCell(0,0)
        #path_to(start,end)
        #attack_line(start, -5,"vert")
        
        while True:
            g.Refresh()
            info = get_info()
            Expand_energy()

        
        
    else:
        print("Failed to join game")