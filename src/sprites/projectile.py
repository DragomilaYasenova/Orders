import math
import pygame


class Projectile:
    def __init__(self, x, y, angle):
        self.radius = 3
        self.color = (255, 0, 0)
        self.speed = 10
        self.angle = math.radians(-angle)

        self.x = x + math.cos(self.angle) * self.radius
        self.y = y - math.sin(self.angle) * self.radius

    def update(self):
        self.x += self.speed * math.cos(self.angle)
        self.y -= self.speed * math.sin(self.angle)

    def draw(self, screen, camera):
        pygame.draw.circle(screen, self.color,
                           camera.apply((int(self.x), int(self.y))), self.radius)

    def check_collision_with_walls(self, collision_rects):
        projectile_rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        for rect in collision_rects:
            if projectile_rect.colliderect(rect):
                return True
        return False
