import random
import pygame.time
from gamemode import Gamemode
from obstacle import Obstacle
from constants import *


class Gamemode1(Gamemode):
    OBSTACLE_WIDTH = 10
    OBSTACLE_SPEED = 3
    TIME_BEWTEEN_OBSTACLES = 1000
    GAMEMODE_LENGTH = 10000
    OBSTACLE_GAP_RATIO = 2.5

    def __init__(self, game):
        super().__init__(game)
        self.obstacle_gap = self.game.player.rect.w * self.OBSTACLE_GAP_RATIO
        self.obstacles = []
        self.obstacle_timer = 0

        # Quadrados pretos que cobrem os obstaculos que saíram do jogo
        self.sides = [
            pygame.Rect(0, 0, self.game.rect.left, SCREEN_HEIGHT),
            pygame.Rect(0, 0, SCREEN_WIDTH, self.game.rect.top),
            pygame.Rect(self.game.rect.right, 0, SCREEN_WIDTH - self.game.rect.right, SCREEN_HEIGHT),
            pygame.Rect(0, self.game.rect.bottom, SCREEN_WIDTH, SCREEN_HEIGHT - self.game.rect.bottom)
        ]

    def create_obstacles(self):
        # Escolhe uma altura para o spawn do obstaculo
        top_height = random.randint(int(self.game.rect.top * 1.2), int(self.game.rect.bottom * 0.8))
        bottom_height = top_height + self.obstacle_gap

        # Cria obstaculos dos dois lados
        top_left_rect = Obstacle(self.game.rect.left, self.game.rect.top, self.OBSTACLE_WIDTH, top_height - self.game.rect.top, self.OBSTACLE_SPEED, 0)
        bottom_left_rect = Obstacle(self.game.rect.left, bottom_height, self.OBSTACLE_WIDTH, self.game.rect.bottom - bottom_height, self.OBSTACLE_SPEED, 0)
        top_right_rect = Obstacle(self.game.rect.right + self.OBSTACLE_WIDTH, self.game.rect.top, self.OBSTACLE_WIDTH, top_height - self.game.rect.top, -self.OBSTACLE_SPEED, 0)
        bottom_right_rect = Obstacle(self.game.rect.right + self.OBSTACLE_WIDTH, bottom_height, self.OBSTACLE_WIDTH, self.game.rect.bottom - bottom_height, -self.OBSTACLE_SPEED, 0)

        # Appenda o novo obstaculo a lista do gamemode
        self.obstacles.append(top_left_rect)
        self.obstacles.append(bottom_left_rect)
        self.obstacles.append(top_right_rect)
        self.obstacles.append(bottom_right_rect)

    def check_collisions(self):
        for obstacle in self.obstacles:
            if not self.game.player.invicible and self.game.player.rect.colliderect(obstacle.rect):
                self.game.player.set_invicible()
                self.game.lives -= 1

    def update(self):
        # Começa o relógio
        if not self.gamemode_start_timer:
            self.gamemode_start_timer = pygame.time.get_ticks()

        # Checa se o gamemode acabou
        if pygame.time.get_ticks() - self.gamemode_start_timer >= self.GAMEMODE_LENGTH:
            if not self.obstacles:
                self.over = True

        # Spawna um obstaculo novo em um tempo x
        elif pygame.time.get_ticks() - self.obstacle_timer >= self.TIME_BEWTEEN_OBSTACLES:
            self.obstacle_timer = pygame.time.get_ticks()
            self.create_obstacles()

        # Atualiza todos os obstaculos
        for obstacle in self.obstacles:
            obstacle.update()

            # Checa se o obstáculo saiu do jogo
            if obstacle.rect.left <= 0 or SCREEN_WIDTH <= obstacle.rect.right:
                self.obstacles.remove(obstacle)

        # Checa colisões entre o jogador e os obstáculos
        self.check_collisions()

    def draw(self, screen):
        # Desenha todos os obstáculos
        for obstacle in self.obstacles:
            obstacle.draw(screen)

        # Cobre os obstáculos que sairam do jogo
        for side in self.sides:
            pygame.draw.rect(screen, BLACK, side)