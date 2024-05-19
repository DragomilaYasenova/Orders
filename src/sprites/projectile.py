import math
import pygame


class Projectile:
    def __init__(self, x, y, angle):
        self.radius = 3
        self.color = (0, 0, 0)
        self.speed = 10
        self.angle = math.radians(-angle)

        self.x = x + math.cos(self.angle) * self.radius
        self.y = y - math.sin(self.angle) * self.radius

    def update(self):
        self.x += self.speed * math.cos(self.angle)
        self.y -= self.speed * math.sin(self.angle)

    def draw(self, screen, camera):
        pygame.draw.circle(screen, self.color,
                           camera.apply(pygame.Vector2(self.x, self.y)), self.radius)
