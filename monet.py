import pygame


class Monet(pygame.sprite.Sprite):

    def __init__(self, x_coord, y_coord, group):
        super().__init__()

        self.image = pygame.image.load('images/монета1.png')
        self.rect = self.image.get_rect()
        self.rect.x = x_coord
        self.rect.y = y_coord

        self.add(group)
