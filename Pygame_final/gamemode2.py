from gamemode import Gamemode
from constants import *
from laser import Laser
import pygame
import math


class Gamemode2(Gamemode):
    LASERS_TIME = 18000
    STOP_LASERS_TIME = 2000
    END_TIME_OFFSET = 2000

    def __init__(self, game):
        super().__init__(game)
        self.lasers = [Laser(game)]
        self.first_part_over = False
        self.second_part_over = False

        # Cria um retângulo para segunda parte do jogo
        self.horizontal_rect = pygame.Rect(self.game.rect.left, self.game.rect.centery, self.game.rect.w, 1)
        self.vertical_rect = pygame.Rect(self.game.rect.centerx, self.game.rect.top, 1, self.game.rect.h)

    def check_collision(self):
        if not self.game.player.invicible and (self.game.player.rect.colliderect(self.horizontal_rect) or self.game.player.rect.colliderect(self.vertical_rect)):
            self.game.player.set_invicible()
            self.game.lives -= 1

    def update_part_1(self):
        # Spawna o segundo laser depois do primero dar duas voltas e meia
        if self.lasers:
            if self.lasers[0].angle >= math.pi * 3.5 and len(self.lasers) <= 1:
                self.lasers.append(Laser(self.game))

        # Atualiza os elementos do gammemode
        lasers_deploying = any([not laser.started_rotating for laser in self.lasers])
        for laser in self.lasers:
            if lasers_deploying and not laser.started_rotating:
                laser.update()
            elif not lasers_deploying:
                laser.update()

        # Checa colisões entre o jogador e o laser
        for laser in self.lasers:
            if laser.started_rotating:
                if not self.game.player.invicible and laser.check_collision():
                    self.game.player.set_invicible()
                    self.game.lives -= 1
            elif not self.game.player.invicible and laser.laser_rect.colliderect(self.game.player.rect):
                self.game.player.set_invicible()
                self.game.lives -= 1

        # Checa se a primeira parte acabou
        if pygame.time.get_ticks() - self.gamemode_start_timer >= self.LASERS_TIME:
            for laser in self.lasers:
                laser.speed = 0
            if pygame.time.get_ticks() - self.gamemode_start_timer >= self.LASERS_TIME + self.STOP_LASERS_TIME:
                self.gamemode_start_timer = pygame.time.get_ticks()
                self.lasers.clear()
                self.first_part_over = True

    def update_part_2(self):
        # Aumenta a largura dos retângulos
        if self.horizontal_rect.h <= self.game.rect.h * 0.7:
            self.horizontal_rect.h += 4
            self.vertical_rect.w += 4
        else:
            if pygame.time.get_ticks() - self.gamemode_start_timer >= self.END_TIME_OFFSET * 2:
                self.gamemode_start_timer = pygame.time.get_ticks()
                self.second_part_over = True
                self.horizontal_rect.h = 0
                self.vertical_rect.w = 0

        # Atualiza a posição doo retangulo para o centro da tela
        self.horizontal_rect.midleft = self.game.rect.midleft
        self.vertical_rect.midtop = self.game.rect.midtop

        # Checa colisões com o jogador
        self.check_collision()

    def update(self):
        # Começa o cronômetro do gamemode
        if not self.gamemode_start_timer:
            self.gamemode_start_timer = pygame.time.get_ticks()

        # Checa se a segunda parte acabou
        if self.second_part_over and pygame.time.get_ticks() - self.gamemode_start_timer >= self.END_TIME_OFFSET:
            self.over = True

        # Atualiza a primeira parte do gamemode
        if not self.first_part_over:
            self.update_part_1()
        elif pygame.time.get_ticks() - self.gamemode_start_timer >= 1000:
            self.update_part_2()

    def draw(self, screen):
        # Desenha os elementos para a primeira parte do gamemode
        if not self.first_part_over:
            # Desenha os lasers
            for laser in self.lasers:
                laser.draw(screen)

        # Desenha os elementos para a segunda parte do gamemode
        elif self.first_part_over and not self.second_part_over:
            # Desenha as linhas centrais
            pygame.draw.line(screen, RED, self.game.rect.midtop, self.game.rect.midbottom)
            pygame.draw.line(screen, RED, self.game.rect.midleft, self.game.rect.midright)

            # Desenha os retângulos
            pygame.draw.rect(screen, WHITE, self.horizontal_rect)
            pygame.draw.rect(screen, WHITE, self.vertical_rect)
