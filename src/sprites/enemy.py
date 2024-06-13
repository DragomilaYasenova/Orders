import random

import pygame
import math
from src.sprites.projectile import Projectile


class Enemy:
    def __init__(self, position, rotation):
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
        self.rotation_angle = rotation
        self.original_angle = rotation
        self.animation_timer = 0
        self.animation_speed = 20
        self.current_image = 0
        self.shooting_timer = 0
        self.shooting_delay = 50
        self.speed = 5
        self.projectiles = []
        self.health = 50
        self.max_health = 50
        self.shoot_range = 250
        self.start_shooting = False
        self.start_shooting_distance = 450
        self.spawn_distance = 250

        self.fov_angle = 60
        self.fov_range = 250
        self.is_moving = False

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

    def _calculate_deltas(self, other_rect):
        dx = other_rect.centerx - self.rect.centerx
        dy = other_rect.centery - self.rect.centery
        return dx, dy

    def distance_to(self, other_rect):
        dx, dy = self._calculate_deltas(other_rect)
        return math.sqrt(dx ** 2 + dy ** 2)

    def is_player_in_fov(self, player_rect):
        dx, dy = self._calculate_deltas(player_rect)
        distance_to_player = math.sqrt(dx ** 2 + dy ** 2)

        if distance_to_player > self.fov_range:
            return False

        angle_to_player = math.degrees(math.atan2(dy, dx))
        relative_angle = (angle_to_player - self.rotation_angle + 360) % 360

        if relative_angle > 180:
            relative_angle -= 360

        if abs(relative_angle) <= self.fov_angle / 2:
            return True
        return False

    def rotate_towards_player(self, player_rect):
        if self.is_player_in_fov(player_rect) or self.start_shooting:
            dx, dy = self._calculate_deltas(player_rect)
        elif self.is_moving:
            dx, dy = self._calculate_deltas(pygame.Rect(self.original_position[0], self.original_position[1], 1, 1))
        else:
            self.rotation_angle = self.original_angle
            return

        new_rotation_angle = math.degrees(math.atan2(dy, dx))
        if self.rotation_angle != new_rotation_angle:
            self.rotation_angle = new_rotation_angle
            self.animate()

    def spawn_enemies_if_low_health(self, enemies_list):
        if self.health < 5 and random.random() < 0.1:
            num_enemies = random.randint(1, 3)
            for _ in range(num_enemies):
                dx = random.randint(-self.spawn_distance, self.spawn_distance)
                dy = random.randint(-self.spawn_distance, self.spawn_distance)
                new_enemy_position = (self.rect.centerx + dx, self.rect.centery + dy)
                new_enemy_rotation = random.randint(0, 360)
                new_enemy = Enemy(new_enemy_position, new_enemy_rotation)
                enemies_list.append(new_enemy)

    def update(self, player, collision_rects, enemies_list):
        self.rotate_towards_player(player.rect)

        if self.health <= 30:
            self.spawn_enemies_if_low_health(enemies_list)

        if self.distance_to(player.rect) > self.start_shooting_distance:
            self.start_shooting = False
        elif player.shoot_timer > 0 and self.distance_to(player.rect) <= self.start_shooting_distance:
            self.start_shooting = True

        self.movement(player.rect, collision_rects)
        self.shoot(player.rect)
        self.update_projectiles(player, player.rect)

    def movement(self, player_rect, collision_rects):
        old_rect = self.rect.copy()
        distance_to_player = self.distance_to(player_rect)
        distance_to_original_position = self.distance_to(
            pygame.Rect(self.original_position[0], self.original_position[1], 1, 1))

        if self.start_shooting or self.is_player_in_fov(player_rect):
            if distance_to_player > 200:
                self._move_towards_target(player_rect, 200, old_rect)
            elif 200 <= distance_to_player <= self.shoot_range:
                self._move_towards_target(player_rect, distance_to_player, old_rect)

        elif distance_to_player > self.shoot_range and distance_to_original_position > 10:
            self._move_towards_target(pygame.Rect(self.original_position[0], self.original_position[1], 1, 1), 10,
                                      old_rect)

        elif distance_to_original_position > 10:
            self.is_moving = False

        self._handle_collision_movement(old_rect, collision_rects, player_rect, distance_to_player)

    def _move_towards_target(self, target_rect, distance, old_rect):
        dx, dy = self._calculate_deltas(target_rect)
        direction_length = math.sqrt(dx ** 2 + dy ** 2)
        if direction_length != 0:
            dx /= direction_length
            dy /= direction_length

        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        new_distance = self.distance_to(target_rect)
        if new_distance < distance:
            scale_factor = (distance - new_distance) / direction_length
            self.rect.x -= dx * scale_factor
            self.rect.y -= dy * scale_factor

    def _handle_collision_movement(self, old_rect, collision_rects, player_rect, distance_to_player):
        for rect in collision_rects:
            if self.rect.colliderect(rect):
                if distance_to_player <= self.shoot_range:
                    x = player_rect.centerx
                    y = player_rect.centery
                else:
                    x = self.original_position[0]
                    y = self.original_position[1]

                self.collision(x, y, old_rect)
                break

    def collision(self, x, y, old_rect):
        enemy_x = self.rect.centerx
        enemy_y = self.rect.centery

        if abs(x - enemy_x) > abs(y - enemy_y):
            self.rect.x, self.rect.y = old_rect.x, old_rect.y + math.copysign(self.speed, y - enemy_y)
        else:
            self.rect.x, self.rect.y = old_rect.x + math.copysign(self.speed, x - enemy_x), old_rect.y

    def shoot(self, player_rect):
        if self.is_player_in_fov(player_rect) and self.shooting_timer <= 0:
            dx = player_rect.centerx - self.rect.centerx
            dy = player_rect.centery - self.rect.centery
            angle = math.degrees(math.atan2(dy, dx))
            projectile = Projectile(self.rect.centerx, self.rect.centery, angle)
            self.projectiles.append(projectile)
            self.shooting_timer = self.shooting_delay
        elif self.shooting_timer > 0:
            self.shooting_timer -= 1

    def update_projectiles(self, player, player_rect):
        for projectile in self.projectiles:
            projectile.update()
            if player_rect.collidepoint(projectile.x, projectile.y):
                player.take_damage(10)
                self.projectiles.remove(projectile)

    def take_damage(self, amount):
        self.health -= amount
        self.start_shooting = True

        if self.health <= 0:
            self.die()

    def die(self):
        print("Enemy has died")

    def draw_projectiles(self, screen, camera):
        for projectile in self.projectiles:
            projectile.draw(screen, camera)


def parse_enemy_objects(tmx_data, zoom_factor):
    enemies = []
    for obj in tmx_data.get_layer_by_name("Enemy"):
        x = obj.x * zoom_factor
        y = obj.y * zoom_factor
        rotation = obj.rotation
        enemy = Enemy((x, y), rotation)
        enemies.append(enemy)
    return enemies
