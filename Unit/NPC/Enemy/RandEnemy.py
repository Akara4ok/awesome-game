from Unit.NPC.Enemy.Enemy import Enemy

class RandEnemy(Enemy):
    def __init__(self, skin, y, x):
        super().__init__(skin, y, x)

    def update(self):
        path = self.getRandomDirection()
        if path:
            (self.y_prev, self.x_prev) = (self.y, self.x)
            (self.y, self.x) = path