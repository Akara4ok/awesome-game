from unittest import result
from Unit.NPC.Enemy.Enemy import Enemy
from Labyrynth.Labyrynth import labyrynth

class SmartEnemy(Enemy):
    def __init__(self, skin, y, x):
        super().__init__(skin, y, x)

    def update(self):
        player = labyrynth.players[0]
        result = self.astar(player.y, player.x)
        if(not result):
            (_, path) = self.greedy_path(player.y, player.x)
            if path:
                (self.y_prev, self.x_prev) = (self.y, self.x)
                (self.y, self.x) = path
            return
        
        (_, path) = result
        if path and len(path) > 1:
            (self.y_prev, self.x_prev) = (self.y, self.x)
            (self.y, self.x) = path[1]