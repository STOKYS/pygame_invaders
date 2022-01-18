import random


class Bomb:
    def __init__(self, e_type, health, damage):
        self.type = e_type
        self.health = health
        self.damage = damage
        self.position = [random.randrange(900) + 50, -50]

    def fnc_bomb_update(self):
        self.fnc_bomb_move()

    def fnc_bomb_move(self):
        self.position = [self.position[0], self.position[1] + 3]