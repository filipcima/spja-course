import pygame
from raptor_game.functions import load_image
from raptor_game.functions import Direction


class Bullet(pygame.sprite.Sprite):

    def __init__(self, pos, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('images/bullet.gif', -1)
        self.direction = direction
        self.rect.center = pos
        self.damage = 10

    def update(self):
        move_y = 0

        if self.direction == Direction.DOWN:
            move_y = 3
        elif self.direction == Direction.UP:
            move_y = -3

        self.rect.move_ip(0, move_y)

        b_x, b_y = self.rect.center
        if b_y <= 0 or b_y > 600:
            self.kill()
