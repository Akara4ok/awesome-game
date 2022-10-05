import os
import copy
from time import sleep
from termcolor import colored

class Labyrynth:
    def __init__(self, path):
        (self.clear_map, self.y_end, self.x_end) = self.read_map(path)
        self.full_map = copy.deepcopy(self.clear_map)
        self.height = len(self.clear_map)
        self.width = len(self.clear_map[0])
        self.units = []
        self.players = []
        self.enemies = []
        self.blocks = {'X'}
        self.playerSkin = ''
        self.enemySkins = {''}
        self.gameOver = False
        self.winner = ''


    def read_map(self, path):
        map = []
        with open(path, 'r') as f:
            for line in f.readlines():
                map.append(list(line.rstrip()))

        x_end = -1
        y_end = -1
        for y, row in enumerate(map):
            for x, element in enumerate(row):
                if(element == 'f'):
                    x_end = x
                    y_end = y
        return (map, y_end, x_end)


    def printMap(self, map):
        #os.system('cls' if os.name == 'nt' else 'clear')
        for row in map:
            for element in row:
                if(element in self.enemySkins):
                    print(colored(element, 'red'), end='')
                elif(element == self.playerSkin):
                    print(colored(element, 'green'), end='')
                elif(element == 'f'):
                    print(colored(element, 'yellow'), end='')
                else:
                    print(element, end='')
            print('')



    
    def getNeighbours(self, y, x):
        result = []
        if(y - 1 > 0 and self.full_map[y - 1][x] not in self.blocks):
            result.append((y - 1, x))
        if(x - 1 > 0 and self.full_map[y][x - 1] not in self.blocks):
            result.append((y, x - 1))
        if(y + 1 < self.height and self.full_map[y + 1][x] not in self.blocks):
            result.append((y + 1, x))
        if(x + 1 < self.width and self.full_map[y][x + 1] not in self.blocks):
            result.append((y, x + 1))

        if(y - 1 > 0 and x - 1 > 0 and self.full_map[y - 1][x - 1] not in self.blocks and (self.full_map[y - 1][x] not in self.blocks or self.full_map[y][x - 1] not in self.blocks)):
            result.append((y - 1, x - 1))
        if(y + 1 < self.height and x - 1 > 0 and self.full_map[y + 1][x - 1] not in self.blocks and (self.full_map[y + 1][x] not in self.blocks or self.full_map[y][x - 1] not in self.blocks)):
            result.append((y + 1, x - 1))
        if(y + 1 < self.height and x + 1 < self.width and self.full_map[y + 1][x + 1] not in self.blocks and (self.full_map[y + 1][x] not in self.blocks or self.full_map[y][x + 1] not in self.blocks)):
            result.append((y + 1, x + 1))
        if(y - 1 > 0 and x + 1 < self.width and self.full_map[y - 1][x + 1] not in self.blocks and (self.full_map[y - 1][x] not in self.blocks or self.full_map[y][x + 1] not in self.blocks)):
            result.append((y - 1, x + 1))

        return result

    def heuristic(self, y_start, x_start, y_end, x_end):
        return (abs(y_start - y_end) + abs(x_start - x_end))

    
    def addUnit(self, unit, cellType = "Enemy"):
        self.units.append(unit)
        if (cellType == "Enemy"):
            self.enemySkins.add(unit.skin)
            self.blocks.add(unit.skin)
            self.enemies.append(unit)
        elif (cellType == "Player"):
            self.playerSkin = unit.skin
            self.players.append(unit)



    def init_screen(self, type):
        self.full_map = copy.deepcopy(self.clear_map)
        for unit in self.units:
            self.full_map[unit.y][unit.x] = unit.skin
        
        self.printMap(self.full_map)
        if(type == 'auto'):
            sleep(0.3)
        elif(type == 'key'):
            input("")



    def update(self, type = "auto"):
        for unit in self.units:
            unit.update()
        
        for unit in self.units:
            if(unit.skin == self.playerSkin and self.full_map[unit.y][unit.x] == 'f'):
                self.full_map[unit.y_prev][unit.x_prev] = ' '
                self.gameOver = True
                self.winner = 'p'
                break

            if(unit.skin in self.enemySkins and self.full_map[unit.y][unit.x] == self.playerSkin):
                self.full_map[unit.y_prev][unit.x_prev] = ' '
                self.full_map[unit.y][unit.x] = unit.skin
                self.gameOver = True
                self.winner = unit.skin
                break

            if(self.full_map[unit.y][unit.x] in self.blocks):
                unit.returnUpdate()
            self.full_map[unit.y_prev][unit.x_prev] = ' '
            self.full_map[unit.y][unit.x] = unit.skin
        
        if(self.full_map[self.y_end][self.x_end] == ' '):
                self.full_map[self.y_end][self.x_end] = 'f'
        
        self.printMap(self.full_map)

        if(type == 'auto'):
            sleep(0.3)
        elif(type == 'key'):
            input("")

    def isGameOver(self):
        return self.gameOver
    
    def getWinner(self):
        if(self.winner == 'p'):
            return "Player"
        elif(self.winner == 'e'):
            return "Smart Enemy"
        elif(self.winner == 'r'):
            return "Random Enemy"
        

labyrynth = Labyrynth("Labyrynth/map.txt")