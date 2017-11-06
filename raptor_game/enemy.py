import pygame
from raptor_game.functions import load_image
from raptor_game.functions import Direction
from raptor_game.bullet import Bullet

from random import randrange, random


class Enemy(pygame.sprite.Sprite):

    enemies_count = 0

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('images/enemy' + str(randrange(1, 6)) + '.gif', -1)
        self.pos = pos
        self.damage = 10
        self.rect.center = self.pos
        self.health = randrange(50, 100)
        self.score_for_kill = 10
        self.speed = random() * 2.5

    def update(self):
        pos_x, pos_y = self.pos
        pos_y += self.speed
        self.pos = (pos_x, pos_y,)
        self.rect.center = (round(pos_x), round(pos_y))

        if pos_y > 600:
            self.kill()
            Enemy.enemies_count -= 1

    def create_bullet(self):
        bullet = Bullet(self.rect.center, Direction.DOWN)
        return bullet
