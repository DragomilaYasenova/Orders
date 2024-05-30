import pygame
import math


class Enemy:
    def __init__(self, position):
        enemy_width = 45
        enemy_height = 30
        self.rect = pygame.Rect(position[0], position[1], enemy_width, enemy_height)
        self.original_position = position
        enemy_left_image = pygame.image.load("../images/npc/enemy_left_foot.png").convert_alpha()
        enemy_right_image = pygame.image.load("../images/npc/enemy_right_foot.png").convert_alpha()

        self.original_images = [
            pygame.transform.smoothscale(enemy_left_image, (enemy_width, enemy_height)),
            pygame.transform.smoothscale(enemy_right_image, (enemy_width, enemy_height))
        ]
        self.images = self.original_images
        self.rotation_angle = 0
        self.animation_timer = 0
        self.animation_speed = 20
        self.current_image = 0
        self.shooting_timer = 0
        self.shooting_delay = 30
        self.speed = 5
        self.projectiles = []

    def animate(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_image = (self.current_image + 1) % len(self.original_images)

    def draw(self, screen, camera):
        rotated_image = pygame.transform.rotate(self.images[self.current_image], -self.rotation_angle)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, camera.apply(rotated_rect))

    def _calculate_deltas(self, other_rect):
        dx = other_rect.centerx - self.rect.centerx
        dy = other_rect.centery - self.rect.centery
        return dx, dy

    def distance_to(self, other_rect):
        dx, dy = self._calculate_deltas(other_rect)
        return math.sqrt(dx ** 2 + dy ** 2)

    def rotate_towards_player(self, player_rect):
        distance = self.distance_to(player_rect)

        if distance < 300:
            dx, dy = self._calculate_deltas(player_rect)
            new_rotation_angle = math.degrees(math.atan2(dy, dx))
            if self.rotation_angle != new_rotation_angle:
                self.rotation_angle = new_rotation_angle
                self.animate()
        else:
            self.rotation_angle = 0

    def rotate_towards_original_position(self):
        dx, dy = self._calculate_deltas(pygame.Rect(self.original_position[0], self.original_position[1], 1, 1))
        new_rotation_angle = math.degrees(math.atan2(dy, dx))
        if self.rotation_angle != new_rotation_angle:
            self.rotation_angle = new_rotation_angle
            self.animate()

    def update(self, player_rect, collision_rects):
        if self.distance_to(player_rect) > 300:
            self.rotate_towards_original_position()
        else:
            self.rotate_towards_player(player_rect)

        self.movement(player_rect, collision_rects)

    def movement(self, player_rect, collision_rects):
        old_rect = self.rect.copy()
        distance_to_player = self.distance_to(player_rect)
        distance_to_original_position = self.distance_to(
            pygame.Rect(self.original_position[0], self.original_position[1], 1, 1))

        if 200 <= distance_to_player <= 300:
            dx, dy = self._calculate_deltas(player_rect)

            direction_length = math.sqrt(dx ** 2 + dy ** 2)
            if direction_length != 0:
                dx /= direction_length
                dy /= direction_length

            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

            new_distance = self.distance_to(player_rect)
            if new_distance < 200:
                scale_factor = (distance_to_player - 200) / direction_length
                self.rect.x -= dx * scale_factor
                self.rect.y -= dy * scale_factor
        elif distance_to_player > 300 and distance_to_original_position > 10:
            dx = self.original_position[0] - self.rect.x
            dy = self.original_position[1] - self.rect.y

            direction_length = math.sqrt(dx ** 2 + dy ** 2)
            if direction_length != 0:
                dx /= direction_length
                dy /= direction_length

            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

            if direction_length < self.speed:
                self.rect.x, self.rect.y = self.original_position

        for rect in collision_rects:
            if self.rect.colliderect(rect):
                self.rect = old_rect
                break


def parse_enemy_objects(tmx_data, zoom_factor):
    enemies = []
    for obj in tmx_data.get_layer_by_name("Enemy"):
        x = obj.x * zoom_factor
        y = obj.y * zoom_factor
        enemies.append(Enemy((x, y)))
    return enemies
