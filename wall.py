import pygame


class Wall(pygame.sprite.Sprite):

    def __init__(self, x_coord, y_coord, width, height, wall_color, group):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(wall_color)
        self.rect = self.image.get_rect()

        self.rect.x = x_coord
        self.rect.y = y_coord
        self.add(group)