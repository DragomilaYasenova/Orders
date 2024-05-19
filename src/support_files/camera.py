import pygame


class Camera:
    def __init__(self, width, height, screen, zoom_factor):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.screen = screen
        self.zoom_factor = zoom_factor

    def apply(self, entity):
        return entity[0] + self.camera.topleft[0], entity[1] + self.camera.topleft[1]

    def update(self, target):
        x = -target.rect.centerx + int(self.screen.get_width() / 2)
        y = -target.rect.centery + int(self.screen.get_height() / 2)

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width * self.zoom_factor - self.screen.get_width()), x)
        y = max(-(self.height * self.zoom_factor - self.screen.get_height()), y)

        self.camera = pygame.Rect(x, y, self.width * self.zoom_factor, self.height * self.zoom_factor)
