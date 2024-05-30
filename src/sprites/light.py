import pygame


class Light:
    def __init__(self, position, radius=100):
        self.position = position
        self.radius = radius

        self.fog = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        self.light_mask = pygame.image.load("../images/light/light.png").convert_alpha()
        self.light_mask = pygame.transform.smoothscale(self.light_mask, (radius * 2, radius * 2))

    def draw(self, surface, camera=None, zoom_factor=1):
        if camera:
            light_pos = camera.apply((self.position[0] * zoom_factor - self.radius,
                                      self.position[1] * zoom_factor - self.radius))
        else:
            light_pos = (self.position[0] - self.radius, self.position[1] - self.radius)

        self.fog.fill((0, 0, 0, 0))
        self.fog.blit(self.light_mask, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        scaled_fog = pygame.transform.scale(self.fog, (int(self.fog.get_width()),
                                                       int(self.fog.get_height())))

        surface.blit(scaled_fog, light_pos, special_flags=pygame.BLEND_RGBA_SUB)


def parse_light_objects(tmx_data):
    lights = []
    for obj in tmx_data.get_layer_by_name("Lights"):
        x = obj.x
        y = obj.y
        radius = 200
        lights.append(Light((x, y), radius))
    return lights
