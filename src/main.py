import pygame
from sprites.player import Player

pygame.init()
screen_width = 1800
screen_height = 900

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Orders")
player = Player()

crosshair = pygame.image.load("../images/crosshair/crosshair.png")
crosshair = pygame.transform.scale(crosshair, (50, 50))

pygame.mouse.set_visible(False)

run = True
while run:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    key = pygame.key.get_pressed()
    player.movements(key)

    mouse_pos = pygame.mouse.get_pos()
    screen.blit(crosshair, (mouse_pos[0] - crosshair.get_width() / 2, mouse_pos[1] - crosshair.get_height() / 2))

    previous_rotation_angle = player.rotation_angle
    player.rotate_towards_mouse(mouse_pos)

    if player.rotation_angle != previous_rotation_angle:
        player.animate()

    mouse_pressed = pygame.mouse.get_pressed()[0]
    player.shoot(mouse_pressed)

    for projectile in player.projectiles:
        projectile.update()

    player.draw(screen)

    for projectile in player.projectiles:
        projectile.draw(screen)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
