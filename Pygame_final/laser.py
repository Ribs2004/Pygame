import math
from constants import *


class Laser:
    SPEED = 3

    def __init__(self, game):
        self.game = game
        self.started_rotating = False
        self.speed = self.SPEED

        # Cria os circulos 
        self.edge_radius = 20
        self.edge_distance = int(self.game.rect.w * 0.8)

        # Informações do laser
        self.laser_rect = pygame.Rect(0, 0, 1, int(self.edge_radius * 0.7))
        self.laser_rect.midleft = (self.game.rect.centerx - self.edge_distance, self.game.rect.centery)
        self.laser_surface = pygame.Surface((self.laser_rect.w, self.laser_rect.w))
        self.laser_image = self.laser_surface.copy()
        self.laser_mask = None
        self.laser_x = 0
        self.laser_y = 0

        # Ângulo
        self.angle = 0

    def rotate_laser(self):
        self.laser_surface = pygame.Surface((self.laser_rect.w, self.laser_rect.h), pygame.SRCALPHA)
        self.laser_surface.fill(WHITE)
        self.laser_image = pygame.transform.rotate(self.laser_surface, math.degrees(-self.angle))
        self.laser_x = self.game.rect.centerx - int(self.laser_image.get_width() / 2)
        self.laser_y = self.game.rect.centery - int(self.laser_image.get_height() / 2)

    def check_collision(self):
        self.laser_mask = pygame.mask.from_surface(self.laser_image)
        player_mask = pygame.mask.from_surface(self.game.player.img)
        offset = (self.game.player.rect.left - self.laser_x, self.game.player.rect.top - self.laser_y)

        if self.laser_mask.overlap(player_mask, offset):
            return True
        return False

    def update(self):
        # Espera o laser se expandir para começar a girar
        if self.started_rotating:
            self.angle += self.speed / 100
        else:
            self.laser_rect.w += 7
            if self.laser_rect.right >= self.game.rect.centerx + self.edge_distance:
                self.started_rotating = True

        # Rotaciona o laser
        self.rotate_laser()

    def draw(self, screen):
        # Desenha os círculos
        pygame.draw.circle(screen, WHITE, ((self.edge_distance * math.cos(self.angle)) + self.game.rect.centerx, (self.edge_distance * math.sin(self.angle)) + self.game.rect.centery),
                           self.edge_radius)
        pygame.draw.circle(screen, WHITE,
                           ((self.edge_distance * math.cos(self.angle + math.pi)) + self.game.rect.centerx, (self.edge_distance * math.sin(self.angle + math.pi)) + self.game.rect.centery),
                           self.edge_radius)

        # Desenha o Laser
        if self.started_rotating:
            screen.blit(self.laser_image, (self.laser_x, self.laser_y))
            # pygame.draw.rect(screen, RED, pygame.Rect(self.laser_x, self.laser_y, self.laser_image.get_width(), self.laser_image.get_height()), 5)
        else:
            pygame.draw.rect(screen, WHITE, self.laser_rect)