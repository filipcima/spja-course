
import pygame
from raptor_game.functions import load_image

DIR_UP = 1
DIR_DOWN = -1


class Bullet(pygame.sprite.Sprite):

    def __init__(self, pos, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('images/bullet.gif', -1)
        self.direction = direction
        self.rect.center = pos
        self.damage = 10

    def update(self):
        if self.direction == DIR_DOWN:
            move_y = 1
        elif self.direction == DIR_UP:
            move_y = -1

        self.rect.move_ip(0, move_y)

        b_x, b_y = self.rect.center
        if b_y <= 0:
            self.kill()
