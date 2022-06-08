from constants import *


class GlidingObstacle:
    SIZE = 10
    Y_SPEED = 2

    def __init__(self, x, y, x_range):
        self.x_range = x_range
        self.x_speed = 4
        self.x = x
        self.y = y
        self.rect = pygame.Rect(0, 0, self.SIZE, self.SIZE)
        self.rect.center = (x, y)

    def update(self):
        self.y += self.Y_SPEED
        self.x += self.x_speed

        if self.x >= self.x_range[1] or self.x <= self.x_range[0]:
            self.x_speed = -self.x_speed

        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        # Desenha o obstáculo
        pygame.draw.rect(screen, WHITE, self.rect)
