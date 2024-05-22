import pygame
import pytmx
from sprites.player import Player
from core.map import draw_map, parse_collision_objects
from support_files.camera import Camera
from sprites.light import Light

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

player_light = Light((player.rect.centerx, player.rect.centery), radius=150)
mouse_light = Light((0, 0), radius=50)
lights = [
    Light((106.00, 1048.00), 200),
    Light((652.00, 1495.00), 200),
    Light((200.00, 1888.00), 200),
    Light((429.00, 1884.00), 200),
    Light((429.00, 2011.00), 200),
    Light((619.00, 2014.00), 200),
    Light((618.00, 891.00), 200),
    Light((1199.00, 1266.00), 80),
    Light((795.00, 700.00), 200),
    Light((1019.00, 700.00), 200)
]

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            run = False

    key = pygame.key.get_pressed()
    player.movements(key, collision_rects)

    mouse_pos = pygame.mouse.get_pos()
    mouse_light.position = mouse_pos

    screen.fill((0, 0, 0))

    camera.update(player)

    draw_map(screen, tmx_data, camera, zoom_factor)

    for projectile in player.projectiles:
        projectile.update()
        projectile.draw(screen, camera)

    player.draw(screen, camera)

    screen.blit(crosshair, (mouse_pos[0] - crosshair.get_width() / 2, mouse_pos[1] - crosshair.get_height() / 2))

    previous_rotation_angle = player.rotation_angle
    player.rotate_towards_mouse(mouse_pos, camera)
    if player.rotation_angle != previous_rotation_angle:
        player.animate()

    mouse_pressed = pygame.mouse.get_pressed()[0]
    player.shoot(mouse_pressed)

    dark_overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    dark_overlay.fill((0, 0, 0, 230))

    player_light.position = (player.rect.centerx, player.rect.centery)

    player_light.draw(dark_overlay, camera)
    mouse_light.draw(dark_overlay, None)
    for light in lights:
        light.draw(dark_overlay, camera, zoom_factor)

    screen.blit(dark_overlay, (0, 0))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
