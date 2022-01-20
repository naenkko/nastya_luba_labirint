import pygame


class Heart(pygame.sprite.Sprite):

    def __init__(self, x_coord, y_coord, width, height, group):
        super().__init__()

        self.image = pygame.image.load('images/heart.png')

        # self.image = pygame.Surface([width, height])
        # self.image.fill((255, 0, 119))

        self.rect = self.image.get_rect()
        self.rect.x = x_coord
        self.rect.y = y_coord

        self.add(group)