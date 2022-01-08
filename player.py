import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, x_coord, y_coord, width, height, walls_group):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill((0, 0, 255))

        self.rect = self.image.get_rect()
        self.rect.x = x_coord
        self.rect.y = y_coord

        self.move_x = 0
        self.move_y = 0

        self.walls_group = walls_group

    def update(self, *args):
        # изменяем координаты
        self.rect = self.rect.move(self.move_x, self.move_y)

        # проверка на столконовение со стенами
        hit_wall = pygame.sprite.spritecollide(self, self.walls_group, False)
        for wall in hit_wall:
            if self.move_x > 0:
                self.rect.right = wall.rect.left
            elif self.move_x < 0:
                self.rect.left = wall.rect.right
            if self.move_y > 0:
                self.rect.bottom = wall.rect.top
            elif self.move_y < 0:
                self.rect.top = wall.rect.bottom