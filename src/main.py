import pygame
import pytmx
from sprites.player import Player
from core.map import draw_map, parse_collision_objects
from support_files.camera import Camera
from sprites.light import Light, parse_light_objects
from sprites.enemy import parse_enemy_objects

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Orders")
clock = pygame.time.Clock()
FPS = 60

zoom_factor = 2
tmx_data = pytmx.util_pygame.load_pygame('./core/Map.tmx')
collision_rects = parse_collision_objects(tmx_data, zoom_factor)

player = Player()
camera = Camera(tmx_data.width * tmx_data.tilewidth, tmx_data.height * tmx_data.tileheight, screen, zoom_factor)

crosshair = pygame.image.load("../images/crosshair/crosshair.png").convert_alpha()
crosshair = pygame.transform.smoothscale(crosshair, (50, 50))

pygame.mouse.set_visible(False)

player_light = Light((player.rect.centerx, player.rect.centery), radius=200)
lights = parse_light_objects(tmx_data)
enemies = parse_enemy_objects(tmx_data, zoom_factor)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            run = False

    key = pygame.key.get_pressed()
    player.movements(key, collision_rects)

    mouse_pos = pygame.mouse.get_pos()

    screen.fill((0, 0, 0))

    camera.update(player)

    draw_map(screen, tmx_data, camera, zoom_factor)

    for projectile in player.projectiles:
        projectile.update()
        projectile.draw(screen, camera)

    player.draw(screen, camera)

    previous_rotation_angle = player.rotation_angle
    player.rotate_towards_mouse(mouse_pos, camera)
    if player.rotation_angle != previous_rotation_angle:
        player.animate()

    mouse_pressed = pygame.mouse.get_pressed()[0]
    player.shoot(mouse_pressed)

    dark_overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    dark_overlay.fill((0, 0, 0, 220))

    player_light.position = (player.rect.centerx, player.rect.centery)

    player_light.draw(dark_overlay, camera)
    for light in lights:
        light.draw(dark_overlay, camera, zoom_factor)

    for enemy in enemies:
        enemy.update(player.rect, collision_rects)
        enemy.draw(screen, camera)

    screen.blit(dark_overlay, (0, 0))

    screen.blit(crosshair, (mouse_pos[0] - crosshair.get_width() / 2, mouse_pos[1] - crosshair.get_height() / 2))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
