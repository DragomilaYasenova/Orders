import pygame
from sprites.player import Player

pygame.init()
screen_width = 1800
screen_height = 900

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Orders")
player = Player()

run = True
while run:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    key = pygame.key.get_pressed()
    player.movements(key)

    mouse_pos = pygame.mouse.get_pos()
    pygame.draw.circle(screen, (0, 0, 0), mouse_pos, 5)
    player.rotate_towards_mouse(mouse_pos)

    player.draw(screen)
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
