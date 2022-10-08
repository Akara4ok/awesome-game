from itertools import combinations
from multiprocessing.sharedctypes import Value
from Unit.Unit import Unit
from Labyrynth.Labyrynth import labyrynth
import copy
import utils.utils as utils

class Node:
    def __init__(self, labyrynth):
        self.labyrynth = copy.deepcopy(labyrynth)


class Player(Unit):
    def __init__(self, skin, y, x):
        super().__init__(skin, y, x)
        self.allExpands = 0
        self.isDebug = False
        
    
    def update(self):
        (self.y_prev, self.x_prev) = (self.y, self.x)
        self.allExpands = 0
        (new_player, value) = self.minimax(Node(labyrynth), 2, "Min")
        #print((new_player.y, new_player.x), value, self.allExpands)
        (self.y, self.x) = (new_player.y, new_player.x)
        return

    
    def minimax(self, node, depth, type):
        self.allExpands += 1
        if depth == 0 or self.isTerminalNode(node):
            return (None, self.evaluateFunction(node))
        best_player = 0
        if (type == "Max"):
            value = -1
            for index, child in enumerate(self.expandChild(node, "Player")):
                minimax_heurastic = self.minimax(child, depth - 1, 'Min')[1]
                if (value < minimax_heurastic):
                    value = minimax_heurastic
                    best_player = child.labyrynth.players[0]
            return (best_player, value)

        elif (type == "Min"):
            value = 10000
            for child in self.expandChild(node, "Enemy"):
                minimax_heurastic = self.minimax(child, depth - 1, 'Max')[1]
                # self.evaluateFunction(child, True)
                # print(minimax_heurastic)
                if (value > minimax_heurastic):
                    value = minimax_heurastic
                    best_player = child.labyrynth.players[0]
            return (best_player, value)

    
    def minimax(self, node, depth, type):
        self.allExpands += 1
        if depth == 0 or self.isTerminalNode(node):
            return (None, self.evaluateFunction(node))
        best_player = 0
        if (type == "Max"):
            value = -1
            for index, child in enumerate(self.expandChild(node, "Player")):
                minimax_heurastic = self.minimax(child, depth - 1, 'Min')[1]
                if (value < minimax_heurastic):
                    value = minimax_heurastic
                    best_player = child.labyrynth.players[0]
            return (best_player, value)

        elif (type == "Min"):
            value = 10000
            for child in self.expandChild(node, "Enemy"):
                minimax_heurastic = self.minimax(child, depth - 1, 'Max')[1]
                if(self.isDebug):
                    self.evaluateFunction(child, True)
                    print(minimax_heurastic)
                if (value > minimax_heurastic):
                    value = minimax_heurastic
                    best_player = child.labyrynth.players[0]
            return (best_player, value)

    def alphabeta(self, node, depth, type):
        self.allExpands += 1
        if depth == 0 or self.isTerminalNode(node):
            return (None, self.evaluateFunction(node))
        best_player = 0
        if (type == "Max"):
            value = -1
            for index, child in enumerate(self.expandChild(node, "Player")):
                minimax_heurastic = self.minimax(child, depth - 1, 'Min')[1]
                if (value < minimax_heurastic):
                    value = minimax_heurastic
                    best_player = child.labyrynth.players[0]
            return (best_player, value)

        elif (type == "Min"):
            value = 10000
            for child in self.expandChild(node, "Enemy"):
                minimax_heurastic = self.minimax(child, depth - 1, 'Max')[1]
                self.evaluateFunction(child, True)
                print(minimax_heurastic)
                if (value > minimax_heurastic):
                    value = minimax_heurastic
                    best_player = child.labyrynth.players[0]
            return (best_player, value)


    def isTerminalNode(self, node):
        isExit = (node.labyrynth.players[0].y, node.labyrynth.players[0].x) == (node.labyrynth.y_end, node.labyrynth.x_end)
        isDead = False
        for enemy in node.labyrynth.enemies:
            if (enemy.y, enemy.x) == (node.labyrynth.players[0].y, node.labyrynth.players[0].x):
                isDead = True
        return isDead or isExit

    def expandChild(self, node, type):
        nodes = []
        if(type == "Enemy"):
            player = node.labyrynth.players[0]
            neighbours = node.labyrynth.getNeighbours(player.y, player.x)
            if(self.isDebug):   
                print((player.y, player.x))
                print(neighbours)
            for neighbour in neighbours:
                player.y = neighbour[0]
                player.x = neighbour[1]
                nodes.append(Node(node.labyrynth))

        elif(type == "Player"):
            possible_moves = []
            for enemy in node.labyrynth.enemies:
                possible_moves.append(node.labyrynth.getNeighbours(enemy.y, enemy.x))
            
            combinations = utils.getAllSingleArrayCombinations(possible_moves)
            for combination in combinations:
                new_labyrynth = copy.deepcopy(node.labyrynth)
                for index, enemy_coord in enumerate(combination):
                    node.labyrynth.enemies[index].y = enemy_coord[0]
                    node.labyrynth.enemies[index].x = enemy_coord[1]
                nodes.append(Node(new_labyrynth))
        return nodes
    
    def evaluateFunction(self, node, isDebug = False):
        meele_kef = 10000
        medium_kef = 100
        far_kef = 10

        finish_kef = 5

        result = 0

        enemies = node.labyrynth.enemies
        player = node.labyrynth.players[0]

        for enemy in enemies:
            (distance, _) = player.astar(enemy.y, enemy.x)
            if (not distance):
                continue
            if distance <= 1:
                if (distance != 0):
                    result += (1 / distance) * meele_kef
                else:
                    result += 10000
                if(isDebug):
                    print("melee", distance, enemy.y, enemy.x, end=' ')
            elif distance > 1 and distance <= 4:
                result += (1 / distance) * medium_kef
                if(isDebug):
                    print("medium", distance, enemy.y, enemy.x, end=' ')
            else:
                result += (1 / distance) * far_kef 
                if(isDebug):
                    print("far", distance, enemy.y, enemy.x, end=' ')
        
        (distance, _) = player.astar(labyrynth.y_end, labyrynth.x_end)
        if(distance):
            result += distance * finish_kef
            if(isDebug):
                print("lab", distance, end=' ')
        if(isDebug):
            print("")

        return result