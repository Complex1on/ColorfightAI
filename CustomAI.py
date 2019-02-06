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
                mycells.append([x,y])
    #returns a list of users cells in list form of [0] = x , [1] = y
    #print(mycells)
    return mycells

def surrounding_cells(mycells):
    direct = [[0,1], [0,-1], [1, 0], [-1,0]]
    adjacentcells = []
    for i in range(len(mycells)):
        for d in range(4):
            x = mycells[i][0]+direct[d][0]
            y = mycells[i][1]+direct[d][1]
            cc = g.GetCell(x,y)
            if cc != None and cc.owner != g.uid:
                adjacentcells.append([x,y])
    #print(adjacentcells)            
    return adjacentcells
            
def lowest_atktime(adjcells):
    xi = adjcells[0][0]
    yi = adjcells[0][1]
    lowesttime = [xi,yi]
    for i in range(len(adjcells)):
        x = adjcells[i][0]
        y = adjcells[i][1]
        c = g.GetCell(x ,y )
        c2 = g.GetCell(lowesttime[0],lowesttime[1]) 
        if (c.takeTime < c2.takeTime):
            lowesttime = []
            lowesttime.append([x,y])
            
    print(lowesttime)
    return lowesttime

def attack_random():
    #picks one of my cells and a random cell next to it to attack
    #picks random surrounding cell and attacks it
    cell = random.choice(surrounding_cells(my_cells()))
    cinfo = g.GetCell(cell[0],cell[1])
    if cinfo.takeTime < 5:
        print(g.AttackCell(cell[0],cell[1]))

def attack_lowest():
    target = lowest_atktime(surrounding_cells(my_cells()))
    print(g.AttackCell(target[0],target[1]))

def defend_base():
    #Need to implement defending a base
    return 0



if __name__ == '__main__':
    # Instantiate a Game object.
    g = colorfight.Game()
    # You need to join the game using JoinGame(). 'MyAI' is the name of your
    # AI, you can change that to anything you want. This function will generate
    # a token file in the folder which preserves your identity so that you can
    # stop your AI and continue from the last time you quit. 
    # If there's a token and the token is valid, JoinGame() will continue. If
    # not, you will join as a new player.
    if g.JoinGame('test'):
        print('hello')
        while True:
            g.Refresh()
            attack_random()
            
        
    else:
        print("Failed to join the game!")

