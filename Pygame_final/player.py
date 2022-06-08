import pygame
from constants import *


class Player:
    INVICIBLE_TIME = 2000

    def __init__(self, game):
        # Variaveis da imagem
        self.alive_img = pygame.transform.scale(HEART_IMG, (game.rect.w // 15, game.rect.w // 15)).convert()
        self.invicible_img = pygame.transform.scale(HEART_INVICIBLE_IMG, (game.rect.w // 15, game.rect.w // 15)).convert_alpha()
        self.img = self.alive_img

        self.rect = self.img.get_rect(center=game.rect.center)
        self.game = game
        self.velocity = 5
        self.invicible = False
        self.inviciblity_timer = 0

    def set_invicible(self):
        HURT_SOUND.play()
        self.img = self.invicible_img
        self.invicible = True
        self.inviciblity_timer = pygame.time.get_ticks()

    def update(self, keys):
        # Checa se o jogador está no modo invisível
        if self.invicible and pygame.time.get_ticks() - self.inviciblity_timer >= self.INVICIBLE_TIME:
            self.img = self.alive_img
            self.invicible = False

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocity
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocity
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocity

    def draw(self, screen):
        # Mostra a imagem do jogador e o seu retângulo
        #pygame.draw.rect(screen, RED, self.rect, 1)
        screen.blit(self.img, self.rect)
