
import pygame
from pygame.locals import *

from raptor_game.functions import load_image
from raptor_game.functions import Direction
from raptor_game.bullet import Bullet


class Raptor(pygame.sprite.Sprite):

    images = {'left': 'images/plane_turning_right_1.gif',
              'right': 'images/plane_turning_left_1.gif',
              'straight': 'images/plane.gif'}

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(self.images['straight'], -1)
        self.rect.center = pos
        self.x_dist, self.y_dist = 7, 7
        self.health = 100

    def update(self, event):
        move_x = 0
        move_y = 0

        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                move_x = self.x_dist
                center = self.rect.center
                self.image, self.rect = load_image(self.images['right'], -1)
                self.rect.center = center
            elif event.key == K_LEFT:
                move_x = -self.x_dist
                center = self.rect.center
                self.image, self.rect = load_image(self.images['left'], -1)
                self.rect.center = center
            elif event.key == K_UP:
                move_y = -self.y_dist
            elif event.key == K_DOWN:
                move_y = self.y_dist
        elif event.type == KEYUP:
            center = self.rect.center
            self.image, self.rect = load_image(self.images['straight'], -1)
            self.rect.center = center

        self.rect.move_ip(move_x, move_y)

    def create_bullet(self):
        bullet = Bullet(self.rect.center, Direction.UP)
        return bullet
