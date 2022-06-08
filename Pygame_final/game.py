import random
from constants import *
from player import Player
from gamemode1 import Gamemode1
from gamemode2 import Gamemode2
from gamemode3 import Gamemode3


class Game:
    def __init__(self):
        # Dimensões
        self.rect = pygame.Rect(0, 0, SCREEN_WIDTH * 0.3, SCREEN_WIDTH * 0.3)
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.6)

        # Variaveis do jogador
        self.lives = PLAYER_LIVES
        self.player = Player(self)

        # Variaveis do nível atual
        self.current_level = 1
        self.level_timer = 0
        self.current_gamemode = None
        self.level_start_timer = 0
        self.level_started = False
        self.game_over = False

    def start_level(self):
        # Espera um tempo x para começar o nível
        if pygame.time.get_ticks() - self.level_start_timer >= TIME_BEWTEEN_LEVELS:
            self.level_timer = pygame.time.get_ticks()
            self.level_started = True

    def choose_gamemode(self):
        # Escolhe modo de jogo
        gamemode_class = random.choice([Gamemode1, Gamemode2, Gamemode3])
        self.current_gamemode = gamemode_class(self)

    def update(self, keys):
        # Atualiza os elementos do jogo
        self.player.update(keys)

        # Escolhe um modo de jogo e o atualiza 
        if self.current_gamemode and not self.current_gamemode.over:
            if self.level_started:
                self.current_gamemode.update()
        else:
            self.choose_gamemode()

        # Checa se o jogador colidiu com a parede
        if self.player.rect.left <= self.rect.left:
            self.player.rect.left = self.rect.left
        if self.player.rect.right >= self.rect.right:
            self.player.rect.right = self.rect.right
        if self.player.rect.top <= self.rect.top:
            self.player.rect.top = self.rect.top
        if self.player.rect.bottom >= self.rect.bottom:
            self.player.rect.bottom = self.rect.bottom

        # Checa se o nível começou
        if self.level_started is False:
            self.start_level()

        # Checa se o nível acabou
        if pygame.time.get_ticks() - self.level_timer >= LEVELS[self.current_level]["length"]:
            # Checa se o nível era o último
            if self.level_started:
                if (self.current_level + 1) in LEVELS.keys():
                    self.current_gamemode = None
                    self.level_started = False
                    self.level_start_timer = pygame.time.get_ticks()
                    self.current_level += 1
                else:
                    self.game_over = True

    def draw(self, screen):
        # Desenha o jogador
        self.player.draw(screen)

        # Se o nível está começando, mostra o nível em que o jogador está
        if self.level_started is False:
            text = FONT_100.render(f"LEVEL {self.current_level}", True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
            screen.blit(text, text_rect)
        else:
            # Desenha os obstaculos do gamemode 
            if self.current_gamemode:
                self.current_gamemode.draw(screen)

            # Desenha a imagem do boss
            img_rect = BOSS_IMG.get_rect(center=(self.rect.centerx, self.rect.top // 2))
            screen.blit(BOSS_IMG, img_rect)

            # Desenha o relógio
            time_left = str(((LEVELS[self.current_level]["length"] - (pygame.time.get_ticks() - self.level_timer)) // 1000) + 1)
            timer_text = FONT_50.render(time_left, True, WHITE)
            timer_rect = timer_text.get_rect(center=(SCREEN_WIDTH // 2, ((SCREEN_HEIGHT - self.rect.bottom) // 2) + self.rect.bottom))
            screen.blit(timer_text, timer_rect)

        # Desenha o retângulo
        pygame.draw.rect(screen, WHITE, self.rect.inflate(16, 16), 8)
