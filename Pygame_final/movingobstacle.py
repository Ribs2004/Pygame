from constants import *


class MovingObstacle:
    SIZE = 10

    def __init__(self, x, y, speed):
        self.speed = speed
        self.x = x
        self.y = y
        self.rect = pygame.Rect(0, 0, self.SIZE, self.SIZE)
        self.rect.center = (x, y)

    def update(self):
        self.y += self.speed
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        # Desenha os obstáculos
        pygame.draw.rect(screen, WHITE, self.rect)
