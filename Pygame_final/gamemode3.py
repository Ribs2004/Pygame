import random
import pygame.time
from gamemode import Gamemode
from movingobstacle import MovingObstacle
from glidingobstacle import GlidingObstacle
from constants import *


class Gamemode3(Gamemode):
    NUMBER_OF_WAVES = 8
    TIME_BETWEEN_WAVES = 3000
    TIME_BETWEEN_CENTER_OBSTACLES = 1500
    OBSTACLES_PER_WAVE = 80
    OBSTACLE_SPEED = 5
    SPAWNING_MARK_TIME = 1000
    OBSTACLE_BOUNDARIES_DISPAWN_OFFSET = 500

    def __init__(self, game):
        super().__init__(game)
        self.wave_obstacles = []
        self.center_obstacles = []
        self.wave_counter = 0
        self.current_wave_side = None

        # Marca do Spawn
        self.wave_spawning_mark = False
        self.spawning_mark_img = pygame.transform.scale(DANGER_IMG, (int(self.game.rect.w * 0.2), int(self.game.rect.h * 0.5)))
        self.spawning_mark_rect_left = pygame.Rect(0, 0, self.spawning_mark_img.get_width(), self.spawning_mark_img.get_height())
        self.spawning_mark_rect_left.center = (self.game.rect.left + int(self.game.rect.w * 0.15), self.game.rect.centery)
        self.spawning_mark_rect_right = pygame.Rect(0, 0, self.spawning_mark_img.get_width(), self.spawning_mark_img.get_height())
        self.spawning_mark_rect_right.center = (self.game.rect.left + int(self.game.rect.w * 0.85), self.game.rect.centery)

        # Relógios
        self.wave_spawn_timer = 0
        self.wave_spawning_mark_timer = 0
        self.center_obstacle_timer = 0

        # Quadrados pretos para cobrir os obstáculos que saíram do jogo
        self.sides = [
            pygame.Rect(0, 0, self.game.rect.left, SCREEN_HEIGHT),
            pygame.Rect(0, 0, SCREEN_WIDTH, self.game.rect.top),
            pygame.Rect(self.game.rect.right, 0, SCREEN_WIDTH - self.game.rect.right, SCREEN_HEIGHT),
            pygame.Rect(0, self.game.rect.bottom, SCREEN_WIDTH, SCREEN_HEIGHT - self.game.rect.bottom)
        ]

    def spawn_wave(self):
        # Escolhe o lado da onda
        self.current_wave_side = "LEFT" if random.choice([0, 1]) == 0 else "RIGHT"
        side_range = (self.game.rect.left, self.game.rect.left + (self.game.rect.w // 3)) if self.current_wave_side == "LEFT" else (
            self.game.rect.right - (self.game.rect.w // 3), self.game.rect.right)

        # Gera obstáculos randomicamente do lado esquerdo ou direito
        for i in range(self.OBSTACLES_PER_WAVE):
            # Metade dos obstáculos vão para cima e metade para baixo
            side = "TOP" if i % 2 == 0 else "BOTTOM"

            # Escolhe uma posição y aleatória em cima o embaixo do quadrado
            random_y = random.randint(0, self.game.rect.h // 2)
            y = self.game.rect.bottom + random_y + 300 if side == "BOTTOM" else self.game.rect.top - random_y - 300

            # Escolhe os valores dos obstáculos
            speed_value = random.choice([4, 5, 6])
            speed = speed_value if side == "TOP" else -speed_value

            # Escolhe uma posição x randômica
            x = random.randint(side_range[0], side_range[1])

            # Cria novos obstáculos e os adiciona na lista
            new_obstacle = MovingObstacle(x, y, speed)
            self.wave_obstacles.append(new_obstacle)

        self.wave_counter += 1

    def check_boundaries(self):
        # Remove os obstáculos que saíram da tela
        for i, obstacle in enumerate(self.wave_obstacles):
            if obstacle.rect.y <= -self.OBSTACLE_BOUNDARIES_DISPAWN_OFFSET or obstacle.rect.y >= SCREEN_HEIGHT + self.OBSTACLE_BOUNDARIES_DISPAWN_OFFSET:
                self.wave_obstacles.pop(i)

        for i, obstacle in enumerate(self.center_obstacles):
            if obstacle.rect.y <= -self.OBSTACLE_BOUNDARIES_DISPAWN_OFFSET or obstacle.rect.y >= SCREEN_HEIGHT + self.OBSTACLE_BOUNDARIES_DISPAWN_OFFSET:
                self.center_obstacles.pop(i)

    def spawn_center_obstacle(self):
        y = int(self.game.rect.top * 0.8)
        x = random.randint(self.game.rect.left + (self.game.rect.w // 4), self.game.rect.right - (self.game.rect.w // 4))
        obstacle_range = (self.game.rect.left + (self.game.rect.w // 4), self.game.rect.right - (self.game.rect.w // 4))

        obstacle = GlidingObstacle(x, y, obstacle_range)
        self.center_obstacles.append(obstacle)

    def check_collision(self):
        # Colisões com os objetos da onda
        for obstacle in self.wave_obstacles:
            if not self.game.player.invicible and self.game.player.rect.colliderect(obstacle.rect):
                self.game.player.set_invicible()
                self.game.lives -= 1

        # Colisões com os obstáaculos do centro
        for obstacle in self.center_obstacles:
            if not self.game.player.invicible and self.game.player.rect.colliderect(obstacle.rect):
                self.game.player.set_invicible()
                self.game.lives -= 1

    def update(self):
        # Spawna uma nova onda em x segundos
        if pygame.time.get_ticks() - self.wave_spawn_timer >= self.TIME_BETWEEN_WAVES and self.wave_counter < self.NUMBER_OF_WAVES:
            # Ativa a marca de spawn temporariamente
            self.wave_spawning_mark = True
            self.wave_spawning_mark_timer = pygame.time.get_ticks()

            # Spawna a wave e reinicia o cronômetro
            self.wave_spawn_timer = pygame.time.get_ticks()
            self.spawn_wave()

        if pygame.time.get_ticks() - self.wave_spawning_mark_timer >= self.SPAWNING_MARK_TIME:
            self.wave_spawning_mark = False

        # Spawna um novo obstáculo de centro a cada x segundos
        if pygame.time.get_ticks() - self.center_obstacle_timer >= self.TIME_BETWEEN_CENTER_OBSTACLES and self.wave_counter < self.NUMBER_OF_WAVES:
            self.center_obstacle_timer = pygame.time.get_ticks()
            self.spawn_center_obstacle()

        # Se não existem mais obstáculos, o gamemode se encerra
        if self.wave_counter >= self.NUMBER_OF_WAVES and not self.wave_obstacles and not self.center_obstacles:
            self.over = True

        # Atualiza cada obsáculo
        for obstacle in self.wave_obstacles:
            obstacle.update()

        for obstacle in self.center_obstacles:
            obstacle.update()

        # Checa se os obstáculos saíram da tela
        self.check_boundaries()

        # Checa colisões com o jogador
        self.check_collision()

    def draw(self, screen):
        # Desnha a marca quando a onda for começar 
        if self.wave_spawning_mark and not pygame.time.get_ticks() % 5 == 0:
            if self.current_wave_side == "LEFT":
                screen.blit(self.spawning_mark_img, self.spawning_mark_rect_left)
            elif self.current_wave_side == "RIGHT":
                screen.blit(self.spawning_mark_img, self.spawning_mark_rect_right)

        # Desenha os obstáculos da onda
        for obstacle in self.wave_obstacles:
            obstacle.draw(screen)

        # Desenha os obstáculos do centro
        for obstacle in self.center_obstacles:
            obstacle.draw(screen)

        # Cobre os elementos que saíram do jogo
        for side in self.sides:
            pygame.draw.rect(screen, BLACK, side)
