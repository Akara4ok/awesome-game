import abc
from Unit.NPC.NPC import NPC

class Enemy(NPC):
    def __init__(self, skin, y, x):
        super().__init__(skin, y, x)
    
    @abc.abstractmethod
    def update(self):
        pass