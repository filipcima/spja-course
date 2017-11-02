import sys
import pygame
from pygame.locals import *

from random import randrange, choice

from raptor_game.raptor import Raptor
from raptor_game.enemy import Enemy

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')


class RaptorMain:
    
    def __init__(self, width=800,height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.score = 0

    def init_background(self):
        MAX_STARS = 250

        self.stars = []
        for i in range(MAX_STARS):
            star = [randrange(0, self.screen.get_width() - 1),
                    randrange(0, self.screen.get_width() - 1),
                    choice([1, 1.5, 2])
                    ]
            self.stars.append(star)

    def move_stars(self):
        for star in self.stars:
            star[1] += star[2] #pohyb hvezdy smerem dolu
            if star[1] >= self.screen.get_height():
                star[1] = 0
                star[0] = randrange(0, self.screen.get_width() - 1)

            if star[2] == 1:
                color = (100, 100, 100)
            elif star[2] == 1.5:
                color = (190, 190, 190)
            elif star[2] == 2:
                color = (255, 255, 255)

            self.screen.fill(color, (star[0], star[1], star[2], star[2]))


    def draw(self):
        self.screen.blit(self.background, (0, 0))

        self.move_stars()

        self.raptor_sprites.draw(self.screen)
        self.enemy_sprites.draw(self.screen)
        if self.bullet_sprites is not None:
            self.bullet_sprites.draw(self.screen)

        if pygame.font:
            font = pygame.font.Font(None, 36)
            text = font.render('Score: {}'.format(self.score), 1, (255, 0, 0))
            textpos = text.get_rect(centerx=self.width/2)
            self.screen.blit(text, textpos)

        pygame.display.flip()

    def update_scene(self):
        self.enemy_sprites.update()
        self.bullet_sprites.update()

        for bullet in self.bullet_sprites:
            lst_cols = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False)

            for col_obj in lst_cols:
                col_obj.health -= bullet.damage
                if col_obj.health <= 0:
                    col_obj.kill()
                    self.score += col_obj.score_for_kill

            if lst_cols:
                bullet.kill()

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == KEYDOWN or event.type == KEYUP:
                self.raptor.update(event)

                if event.key == K_SPACE:
                    self.bullet_sprites.add(self.raptor.create_bullet())

    def main_loop(self):
        pygame.key.set_repeat(500, 30)
        
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()

        self.init_background()
        self.load_sprites()

        while 1:
            self.handle_keys()
            self.update_scene()
            self.draw()


    def load_sprites(self):
        self.raptor = Raptor((self.width/2, self.height - 20,))
        self.raptor_sprites = pygame.sprite.RenderPlain((self.raptor))
        self.enemy = Enemy((20.0, 10.0,))
        self.enemies = []
        x = 5
        for enemy in range(5):

            enemy = Enemy((x, 20.0))
            self.enemies.append(enemy)
            x += 50

        self.enemy_sprites = pygame.sprite.RenderPlain(self.enemies, enemy)
        self.bullet_sprites = pygame.sprite.RenderPlain()


if __name__ == '__main__':
    main_window = RaptorMain()
    main_window.main_loop()
