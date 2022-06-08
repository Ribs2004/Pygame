from constants import *


class Obstacle:
    def __init__(self, x, y, w, h, speedX, speedY):
        self.rect = pygame.Rect(x, y, w, h)
        self.speedX = speedX
        self.speedY = speedY

    def update(self):
        self.rect.x += self.speedX
        self.rect.y += self.speedY

    def draw(self, screen):
        # Desenha os obstáculos
        pygame.draw.rect(screen, WHITE, self.rect)
