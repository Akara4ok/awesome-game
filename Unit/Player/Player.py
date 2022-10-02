from Unit.Unit import Unit
from Labyrynth.Labyrynth import labyrynth

class Player(Unit):
    def __init__(self, skin, y, x):
        super().__init__(skin, y, x)
        
    
    def update(self):
        result = self.astar(labyrynth.y_end, labyrynth.x_end)
        if(not result):
            (_, path) = self.greedy_path(labyrynth.y_end, labyrynth.x_end)
            if path:
                (self.y_prev, self.x_prev) = (self.y, self.x)
                (self.y, self.x) = path
            return
        
        (_, path) = result
        if path and len(path) > 1:
            (self.y_prev, self.x_prev) = (self.y, self.x)
            (self.y, self.x) = path[1]