import pygame
import pytmx


def draw_map(screen, tmx_data, camera, zoom_factor):
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    zoomed_tile_pos = camera.apply((x * tmx_data.tilewidth * zoom_factor,
                                                    y * tmx_data.tileheight * zoom_factor))
                    zoomed_tile = pygame.transform.scale(tile, (int(tmx_data.tilewidth * zoom_factor),
                                                                int(tmx_data.tileheight * zoom_factor)))
                    screen.blit(zoomed_tile, zoomed_tile_pos)
