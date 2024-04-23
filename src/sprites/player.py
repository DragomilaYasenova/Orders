import pygame
import math

from src.sprites.projectile import Projectile


class Player:
    def __init__(self):
        player_width = 180
        player_height = 120
        self.rect = pygame.Rect(0, 0, player_width, player_height)
        self.original_images = [
            pygame.transform.smoothscale(pygame.image.load("../images/player/player_left_foot.png").convert_alpha(),
                                         (player_width, player_height)),
            pygame.transform.smoothscale(pygame.image.load("../images/player/player_right_foot.png").convert_alpha(),
                                         (player_width, player_height))]
        self.images = self.original_images
        self.current_image = 0
        self.rotation_angle = 0
        self.animation_timer = 0
        self.animation_speed = 10
        self.speed = 5
        self.projectiles = []
        self.shoot_delay = 10
        self.shoot_timer = 0

    def animate(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_image = (self.current_image + 1) % len(self.original_images)

    def draw(self, screen):
        for projectile in self.projectiles:
            projectile.draw(screen)
        rotated_image = pygame.transform.rotate(self.images[self.current_image], -self.rotation_angle)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, rotated_rect)

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
        dx = mouse_pos[0] - self.rect.centerx
        dy = mouse_pos[1] - self.rect.centery
        self.rotation_angle = math.degrees(math.atan2(dy, dx))

    def shoot(self, mouse_pressed):
        if mouse_pressed and self.shoot_timer <= 0:
            projectile = Projectile(self.rect.centerx, self.rect.centery, self.rotation_angle)
            self.projectiles.append(projectile)
            self.shoot_timer = self.shoot_delay
        elif self.shoot_timer > 0:
            self.shoot_timer -= 1
