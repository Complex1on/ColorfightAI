# You need to import colorfight for all the APIs
import colorfight
import random


def my_cells():
    #Goes through the board and finds user's cells
    mycells = []
    for x in range(g.width):
        for y in range(g.height):
            c = g.GetCell(x,y)
            if c.owner == g.uid:
                mycells.append([x,y])
    #returns a list of users cells in list form of [0] = x , [1] = y
    return mycells

def attack_random(cells):
    d = random.choice([[0,1], [0,-1], [1, 0], [-1,0]])
    foundcell = False
    while (foundcell == False):
        g2 = random.choice(cells)
        x = g2[0]+d[0] 
        y = g2[1]+d[1] 
        cc = g.GetCell(x,y)
        if (cc.owner != g.uid) and (cc.takeTime < 5):
            foundcell = True
    
    return [x, y]

def randomroutine():
    atk_target = attack_random(my_cells())
    print(g.AttackCell(atk_target[0], atk_target[1]))


 



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
            randomroutine()
        
    else:
        print("Failed to join the game!")
