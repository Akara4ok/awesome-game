import abc
import queue
import sys
import abc
from Labyrynth.Labyrynth import labyrynth
import random

class Unit(metaclass=abc.ABCMeta):
    def __init__(self, skin, y, x):
        self.skin = skin
        self.y = y
        self.x = x
        self.x_prev = x
        self.y_prev = y

    def returnUpdate(self):
        (self.y, self.x) = (self.y_prev, self.x_prev)

    @abc.abstractmethod
    def update(self):
        pass

    
    
    def getRandomDirection(self):
        return random.choice(labyrynth.getNeighbours(self.y, self.x))

    def astar(self, y_end, x_end):
        lin_kef = 1
        diag_kef = 1

        x_start = self.x
        y_start = self.y

        cost = [[sys.maxsize for i in range(labyrynth.width)] for i in range(labyrynth.height)]
        from_path = [[None for i in range(labyrynth.width)] for i in range(labyrynth.height)]
        vertex = queue.PriorityQueue()

        cost[y_start][x_start] = 0
        from_path[y_start][x_start] = -1
        vertex.put((labyrynth.heuristic(y_start, x_start, y_end, x_end), (y_start, x_start)))

        while(not vertex.empty()):
            _, (y, x) = vertex.get()

            if(y, x) == (y_end, x_end):
                return (cost[y][x], self.get_path(y_end, x_end, y_start, x_start, from_path))

            neighbours = labyrynth.getNeighbours(y, x)

            for new_y, new_x in neighbours:
                kef = diag_kef
                if (x == new_x or y == new_y):
                    kef = lin_kef
                if(cost[new_y][new_x] > cost[y][x] + kef):
                    cost[new_y][new_x] = cost[y][x] + kef
                    from_path[new_y][new_x] = (y, x)
                    vertex.put((cost[new_y][new_x] + labyrynth.heuristic(y, x, y_end, x_end), (new_y, new_x)))
        
        return (None, None)
    
    def greedy_path(self, y_end, x_end):
        (y, x) = (self.y, self.x)
        neighbours = labyrynth.getNeighbours(y, x)
        min_heuristic = labyrynth.heuristic(y, x, y_end, x_end)
        next_coord = (y, x)
        for y_next, x_next in neighbours:
            heuristic = labyrynth.heuristic(y_next, x_next, y_end, x_end)
            if(heuristic < min_heuristic):
                min_heuristic = heuristic
                next_coord = (y_next, x_next)
        
        return (min_heuristic, next_coord)

        
    
    def get_path(self, y, x, y_start, x_start, from_path):
        if(x == x_start and y == y_start):
            return [(y, x)]
        
        (y_next, x_next) = from_path[y][x]

        current_path = self.get_path(y_next, x_next, y_start, x_start, from_path)
        current_path.append((y, x))
        return current_path