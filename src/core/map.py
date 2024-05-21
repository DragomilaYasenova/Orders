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


def parse_collision_objects(tmx_data, zoom_factor):
    collision_rects = []
    for obj in tmx_data.get_layer_by_name("Obstacles"):
        rect = pygame.Rect(obj.x * zoom_factor, obj.y * zoom_factor, obj.width * zoom_factor, obj.height * zoom_factor)
        collision_rects.append(rect)
    for obj in tmx_data.get_layer_by_name("Objects"):
        rect = pygame.Rect(obj.x * zoom_factor, obj.y * zoom_factor, obj.width * zoom_factor, obj.height * zoom_factor)
        collision_rects.append(rect)

    return collision_rects
