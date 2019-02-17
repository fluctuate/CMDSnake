#
#   CMDSnake.py for CMDSnake
#
#   http://fluctuate.codes/
#   2/16/2019 (~2 hours to code)

import msvcrt #REQUIRES WINDOWS
import math
import time
from threading import Timer
import sys
import os
import random


#Printing System for better formatting for start/end screen
def infoPrint(text, centered):
    #How long the menus are horizontally
    infoWindowSize = 48
    if centered:
        spacesNeeded = math.floor(infoWindowSize/2)-math.floor(len(text)/2)-2
        spaces = ""
        for x in range(spacesNeeded):
            spaces += " "
        if len(("# " + spaces + text + spaces + " #")) < infoWindowSize:
            spaces2 += " "
            print("# " + spaces + text + spaces2 + " #")
        elif len(("# " + spaces + text + spaces + " #")) > infoWindowSize:
            spaces2 = spaces[1:]
            print("# " + spaces + text + spaces2 + " #")
        else:
            print("# " + spaces + text + spaces + " #")
    else:
        spacesNeeded = infoWindowSize-len(text)-4
        spaces = ""
        for x in range(spacesNeeded):
            spaces += " "
        print("# " + text + spaces + " #")
#Creates the empty board
def drawBoard(horizontal, vertical):
    boardMap = dict()
    for x in range(vertical):
        line = "#"
        for y in range(horizontal-2):
            line += " "
        line += "#"
        boardMap[x] = list(line)
    return boardMap
#Partially Edited Version of:
#https://stackoverflow.com/questions/2933399/how-to-set-time-limit-on-raw-input/2933423#2933423
#Allows the user to send input while game is running without pausing
def input_with_timeout(prompt, timeout, timer=time.monotonic):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    endtime = timer() + timeout
    result = []
    returnval = ''
    while timer() < endtime:
        if msvcrt.kbhit():
            returnval = msvcrt.getwche()
        time.sleep(0.01)
    return returnval
#Adds all objects to the board
def addObjects(boardMap, coords, fruit, trail):
    #Head
    boardMap[coords['y']][coords['x']] = 'O'
    for fruitnumber in fruit:
        #Fruit
        boardMap[fruit[fruitnumber]['y']][fruit[fruitnumber]['x']] = '$'
    for trailnumber in trail:
        #Trail
        boardMap[trail[trailnumber]['y']][trail[trailnumber]['x']] = 'o'
    return boardMap
#Puts the board into the console
def displayBoard(boardMap):
    os.system('cls')
    for y in boardMap:
        line = ''
        for x in boardMap[y]:
            line += x
        print(line)
def addRandomFruit(horizontal, vertical, fruit, maxfruit):
    fruitDict = dict()
    fruitDict['x'] = random.randint(1,horizontal-2)
    fruitDict['y'] = random.randint(0,vertical-1)
    for x in range(maxfruit):
        if x not in fruit.keys():
            fruit[x] = fruitDict
            break
    return fruit
#Shows game end screen
def endGame():
    os.system('cls')
    infoPrint("", False)
    infoPrint("You died!", True)
    infoPrint("Do you want to start again? (y/n)!", True)
    infoPrint("", False)
    if list(input())[0].lower() == 'y':
        startGame()
    else:
        sys.exit()
#Determines if the player collides into fruit or themself
def doCollide(coords, fruit, eaten, trail):
    returndict = dict()
    newfruit = fruit.copy()
    collide = False
    for trailnumber in trail:
        if trail[trailnumber] == coords:
            collide = True
    for fruitnumber in fruit:
        if fruit[fruitnumber] == coords:
            eaten += 1
            newfruit.pop(fruitnumber)
    returndict['eaten'] = eaten
    returndict['fruit'] = newfruit.copy()
    returndict['collide'] = collide
    return returndict
#Handles all game functions
def playGame(horizontal, vertical, speed):
    #Default Tick Speed (in seconds)
    speedDefault = 0.15
    speed = (speedDefault/speed)
    coords = dict()
    coords['y'] = math.floor(vertical/2)
    coords['x'] = math.floor(horizontal/2)-1
    facing = 0
    trail = set()
    fruit = dict()
    eaten = 0
    maxfruit = math.ceil((vertical*horizontal)/100)
    collide = False
    while collide == False:
        boardMap = drawBoard(horizontal, vertical)
        #Update Trail Behind Player Head
        if eaten > 0:
            newtrail = dict()
            for x in range(len(trail)):
                if x+1 < eaten:
                    newtrail[x+1] = trail[x]
            newtrail[0] = coords.copy()
            trail = newtrail.copy()
        #Move Player by Direction
        if facing == 0:
            coords['y'] -= 1
        elif facing == 2:
            coords['y'] += 1
        elif facing == 1:
            coords['x'] += 1
        elif facing == 3:
            coords['x'] -= 1
        #Loop Player to Other Side of Board
        if coords['x'] < 1:
            coords['x'] = horizontal-2
        elif coords['x'] > horizontal-2:
            coords['x'] = 1
        if coords['y'] < 0:
            coords['y'] = vertical-1
        elif coords['y'] > vertical-1:
            coords['y'] = 0
        #Adds new fruit
        while len(fruit) < maxfruit:
            fruit = addRandomFruit(horizontal, vertical, fruit, maxfruit)
        returndict = doCollide(coords, fruit, eaten, trail)
        #Ups the game speed
        if eaten != returndict['eaten']:
            difference = returndict['eaten'] - eaten
            for x in range(difference):
                speed *= 0.95
                if speed < 0.02:
                    speed = 0.02
        #Window Title Status
        os.system("title "+'[CMDSnake.py] [Game Speed: '+str(speed)+'sec] [Eaten: '+str(eaten)+'] [Fruit: '+str(len(fruit))+'/'+str(maxfruit)+']')       
        collide = returndict['collide']    
        eaten = returndict['eaten']
        fruit = returndict['fruit']   
        #Display Update
        addObjects(boardMap, coords, fruit, trail)
        displayBoard(boardMap)
        move = input_with_timeout('', speed)
        if move == 'w':
            facing = 0
        if move == 'a':
            facing = 3
        if move == 's':
            facing = 2
        if move == 'd':
            facing = 1
    endGame()
#Gets all needed details for the game display/speed
def buildGame():
    horizontal = int(input("Horizontal Height: "))
    vertical = int(input("Vertical Height: "))
    test = "#"
    for x in range(horizontal-2):
        test += "."
    test += "#"
    for x in range(vertical):
        print(test)
    speed = int(input("Game Speed: "))
    input("Press Enter to Begin Playing!")
    playGame(horizontal, vertical, speed)
#Start menu
def startGame():
    os.system('cls')
    infoPrint("", False)
    infoPrint("Welcome to CMD Snake!", True)
    infoPrint("Let's set up the board!", True)
    infoPrint("", False)
    buildGame()
    
startGame()
