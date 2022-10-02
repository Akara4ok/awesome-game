from Labyrynth.Labyrynth import labyrynth
from Unit.NPC.Enemy.SmartEnemy import SmartEnemy
from Unit.NPC.Enemy.RandEnemy import RandEnemy
from Unit.Player.Player import Player
from random import randint

def genEnemies(number, type):
    correctNumber = 0
    while(correctNumber < number):
        x = randint(0, labyrynth.width - 1)
        y = randint(0, labyrynth.height - 1)
        if(labyrynth.full_map[y][x] == ' '):
            if(type == "Random"):
                rand = RandEnemy('r', y, x)
                labyrynth.addUnit(rand)
            elif(type == "Smart"):
                smart = SmartEnemy('e', y, x)
                labyrynth.addUnit(smart)
            correctNumber += 1



player = Player('p', 4, 19)
labyrynth.addUnit(player, "Player")

randNumber = 2
smartNumber = 1

genEnemies(randNumber, type="Random")
genEnemies(smartNumber, type="Smart")


labyrynth.init_screen("auto")
while(not labyrynth.isGameOver()):
    labyrynth.update("auto")

print("Winner: ", labyrynth.getWinner())