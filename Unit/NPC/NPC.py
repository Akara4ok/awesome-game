import abc
from Unit.Unit import Unit
from Labyrynth.Labyrynth import labyrynth

class NPC(Unit):
    def __init__(self, skin, y, x):
        super().__init__(skin, y, x)
    
    @abc.abstractmethod
    def update(self):
        pass