import pygame
import math


class Player:
    def __init__(self):
        player_width = 180
        player_height = 120
        self.rect = pygame.Rect(0, 0, player_width, player_height)
        self.original_images = [
            pygame.transform.smoothscale(pygame.image.load("images/player/player_left_foot.png").convert_alpha(),
                                         (player_width, player_height)),
            pygame.transform.smoothscale(pygame.image.load("images/player/player_right_foot.png").convert_alpha(),
                                         (player_width, player_height))]
        self.images = self.original_images
        self.current_image = 0
        self.rotation_angle = 0
        self.animation_timer = 0
        self.animation_speed = 10
        self.speed = 5

    def animate(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_image = (self.current_image + 1) % len(self.original_images)

    def draw(self, screen):
        screen.blit(self.images[self.current_image], self.rect)

    def movements(self, key):
        if key[pygame.K_a]:
            self.rect.x -= self.speed
            self.animate()
        elif key[pygame.K_d]:
            self.rect.x += self.speed
            self.animate()
        elif key[pygame.K_w]:
            self.rect.y -= self.speed
            self.animate()
        elif key[pygame.K_s]:
            self.rect.y += self.speed
            self.animate()

    def rotate_towards_mouse(self, mouse_pos):
        dx = mouse_pos[0] - (self.rect.x + self.rect.width / 2)
        dy = mouse_pos[1] - (self.rect.y + self.rect.height / 2)
        angle = math.degrees(math.atan2(dy, dx))
        self.images = [pygame.transform.rotate(image, -angle) for image in self.original_images]
