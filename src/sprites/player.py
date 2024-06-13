import pygame
from src.sprites.projectile import Projectile
from src.support_files.cyrillic_keys import cyrillic_a, cyrillic_d, cyrillic_w, cyrillic_s


class Player:
    def __init__(self):
        player_width = 45
        player_height = 30
        self.rect = pygame.Rect(240, 2070, player_width, player_height)
        player_left_image = pygame.image.load("../images/player/player_left_foot.png").convert_alpha()
        player_right_image = pygame.image.load("../images/player/player_right_foot.png").convert_alpha()
        self.original_images = [
            pygame.transform.smoothscale(player_left_image, (player_width, player_height)),
            pygame.transform.smoothscale(player_right_image, (player_width, player_height))
        ]
        self.images = self.original_images
        self.current_image = 0
        self.rotation_angle = 0
        self.animation_timer = 0
        self.animation_speed = 0
        self.speed = 6
        self.projectiles = []
        self.shoot_delay = 10
        self.shoot_timer = 0
        self.health = 100

        self.max_health = 100

    def animate(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_image = (self.current_image + 1) % len(self.original_images)

    def draw(self, screen, camera):
        rotated_image = pygame.transform.rotate(self.images[self.current_image], -self.rotation_angle)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, camera.apply(rotated_rect))
        self.draw_health_bar(screen, camera)

    def draw_health_bar(self, screen, camera):
        bar_length = 50
        bar_height = 7
        fill = (self.health / self.max_health) * bar_length
        health_bar_rect = pygame.Rect(0, 0, bar_length, bar_height)
        health_fill_rect = pygame.Rect(0, 0, fill, bar_height)

        pygame.draw.rect(screen, (255, 0, 0), camera.apply((self.rect.x, self.rect.y - 10)) + health_bar_rect.size)
        pygame.draw.rect(screen, (0, 255, 0), camera.apply((self.rect.x, self.rect.y - 10)) + health_fill_rect.size)

    def movements(self, key, collision_rects):
        self.animation_speed = 15
        old_rect = self.rect.copy()

        if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT]:
            self.speed = 8
        else:
            self.speed = 6

        if key[pygame.K_a] or key[cyrillic_a]:
            self.rect.x -= self.speed
            self.animate()
        elif key[pygame.K_d] or key[cyrillic_d]:
            self.rect.x += self.speed
            self.animate()
        elif key[pygame.K_w] or key[cyrillic_w]:
            self.rect.y -= self.speed
            self.animate()
        elif key[pygame.K_s] or key[cyrillic_s]:
            self.rect.y += self.speed
            self.animate()

        for rect in collision_rects:
            if self.rect.colliderect(rect):
                self.rect = old_rect
                break

    def rotate_towards_mouse(self, mouse_pos, camera):
        dx = mouse_pos[0] - (self.rect.centerx + camera.camera.x)
        dy = mouse_pos[1] - (self.rect.centery + camera.camera.y)
        direction_vector = pygame.math.Vector2(dx, -dy)
        self.rotation_angle = direction_vector.angle_to(pygame.math.Vector2(1, 0))

    def shoot(self, mouse_pressed):
        if mouse_pressed and self.shoot_timer <= 0:
            projectile = Projectile(self.rect.centerx, self.rect.centery, self.rotation_angle)
            self.projectiles.append(projectile)
            self.shoot_timer = self.shoot_delay
        elif self.shoot_timer > 0:
            self.shoot_timer -= 1

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        print("Player has died")
        pygame.quit()
        exit()
