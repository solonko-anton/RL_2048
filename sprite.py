import pygame
from pygame import sprite

colors_rgb = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 197, 63),
    1024: (60, 58, 50),
    2048: (60, 65, 58)
}


class Sprite(sprite.Sprite):

    def __init__(self, height, width, number):
        super().__init__()
        self.number = number
        self.color = colors_rgb[number if number <= 2048 else 2048]

        self.image = pygame.Surface([width, height])
        self.image.fill(self.color)

        pygame.draw.rect(
            self.image,
            self.color,
            pygame.Rect(0, 0, width, height),
            border_radius=8
        )

        font_size = int(height * 0.45)
        font = pygame.font.Font(None, font_size)

        text_color = (119, 110, 101)
        text_surface = font.render(str(number), True, text_color)

        text_rect = text_surface.get_rect(center=(width / 2, height / 2))

        self.image.blit(text_surface, text_rect)

        self.rect = self.image.get_rect()

