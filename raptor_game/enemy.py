import pygame
from raptor_game.functions import load_image


class Enemy(pygame.sprite.Sprite):

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('images/enemy1.gif', -1)
        self.pos = pos
        self.rect.center = self.pos
        self.health = 100
        self.score_for_kill = 10

    def update(self):
        pos_x, pos_y = self.pos
        pos_y += 0.3
        self.pos = (pos_x, pos_y,)
        self.rect.center = (round(pos_x), round(pos_y))
