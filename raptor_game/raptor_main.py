import sys
import pygame
from pygame.locals import *
from raptor_game.raptor import Raptor
from raptor_game.enemy import Enemy
from raptor_game.star import Star
from random import randrange, choice, random

if not pygame.font:
    print('Warning, fonts disabled')
if not pygame.mixer:
    print('Warning, sound disabled')


class RaptorMain:

    def __init__(self, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.score = 0

    def init_background(self):
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()

        max_stars = 250
        self.stars = []

        for i in range(max_stars):
            rand_x = randrange(0, self.screen.get_width())
            rand_y = randrange(0, self.screen.get_height())
            speed = choice([1, 1.5, 2])
            star = Star(rand_x, rand_y, speed)

            self.stars.append(star)

    def move_stars(self):
        for star in self.stars:
            star.pos_y += star.speed

            if star.pos_y >= self.screen.get_height():
                star.pos_y = 0
                star.pos_x = randrange(0, self.screen.get_width())

            if star.speed == 1:
                color = (100, 100, 100)
            elif star.speed == 1.5:
                color = (190, 190, 190)
            elif star.speed == 2:
                color = (255, 255, 255)

            self.screen.fill(color, (star.pos_x, star.pos_y, star.speed, star.speed))

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.move_stars()
        self.raptor_sprites.draw(self.screen)
        self.enemy_sprites.draw(self.screen)

        if self.enemy_bullet_sprites is not None:
            self.enemy_bullet_sprites.draw(self.screen)
        if self.player_bullet_sprites is not None:
            self.player_bullet_sprites.draw(self.screen)

        if pygame.font:
            font = pygame.font.Font(None, 36)

            score = font.render('Score: {}'.format(self.score), 1, (255, 0, 0))
            textpos = score.get_rect(centerx=self.width/2)

            health = font.render('HP: {}/100'.format(self.raptor.health), 1, (255, 0, 0))
            textpos2 = health.get_rect(centery=self.height - 10)

            if self.raptor.health <= 0:
                font = pygame.font.Font(None, 56)
                game_over = font.render('Game Over', 1, (255, 255, 255))
                textpos3 = game_over.get_rect(centerx=self.width/2, centery=self.height/2)
                self.screen.blit(game_over, textpos3)

            self.screen.blit(score, textpos)
            self.screen.blit(health, textpos2)

        pygame.display.flip()

    def update_scene(self):
        self.enemy_sprites.update()
        self.player_bullet_sprites.update()
        self.enemy_bullet_sprites.update()

        if random() < 0.02: # priblizne 1 z 50
            if Enemy.enemies_count < 10:
                self.enemy_sprites.add(Enemy((random() * self.width, random() * self.height / -2)))
                Enemy.enemies_count += 1

        for enemy in self.enemy_sprites:
            if random() < 0.01: # priblizne 1 ze 100
                self.enemy_bullet_sprites.add(enemy.create_bullet())

        for bullet in self.player_bullet_sprites:
            lst_cols = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False)

            for col_obj in lst_cols:
                col_obj.health -= bullet.damage
                if col_obj.health <= 0:
                    col_obj.kill()
                    Enemy.enemies_count -= 1
                    self.score += col_obj.score_for_kill

            if lst_cols:
                bullet.kill()

        for bullet in self.enemy_bullet_sprites:
            lst_cols = pygame.sprite.spritecollide(bullet, self.raptor_sprites, False)

            for col_obj in lst_cols:
                col_obj.health -= bullet.damage
                if col_obj.health <= 0:
                    col_obj.kill()

            if lst_cols:
                bullet.kill()

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == KEYDOWN or event.type == KEYUP:
                self.raptor.update(event)

                if event.key == K_SPACE:
                    self.player_bullet_sprites.add(self.raptor.create_bullet())

    def main_loop(self):
        pygame.key.set_repeat(500, 10)

        self.init_background()
        self.load_sprites()

        while 1:
            self.handle_keys()
            self.update_scene()
            self.draw()

    def load_sprites(self):
        self.raptor = Raptor((self.width / 2, self.height - 80,))
        self.raptor_sprites = pygame.sprite.RenderPlain(self.raptor)
        self.enemy_sprites = pygame.sprite.RenderPlain()
        self.player_bullet_sprites = pygame.sprite.RenderPlain()
        self.enemy_bullet_sprites = pygame.sprite.RenderPlain()


if __name__ == '__main__':
    main_window = RaptorMain()
    main_window.main_loop()
