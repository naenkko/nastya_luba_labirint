import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, x_coord, y_coord, width, height, walls_group, enemy_group, finish_group):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill((0, 0, 255))

        self.rect = self.image.get_rect()
        self.rect.x = x_coord
        self.rect.y = y_coord

        self.start_coord_x = x_coord
        self.start_coord_y = y_coord

        self.move_x = 0
        self.move_y = 0

        self.lives = 5

        self.next_level = False

        self.walls_group = walls_group
        self.enemy_group = enemy_group
        self.finish_group = finish_group

    def update(self, *args):
        # изменяем координаты по горизонтали
        self.rect.x += self.move_x

        # проверка на столконовение со стенами
        hit_wall = pygame.sprite.spritecollide(self, self.walls_group, False)
        for wall in hit_wall:
            if self.move_x > 0:
                self.rect.right = wall.rect.left
            elif self.move_x < 0:
                self.rect.left = wall.rect.right

        # изменяем координаты по вертикали
        self.rect.y += self.move_y

        # проверка на столконовение со стенами
        hit_wall = pygame.sprite.spritecollide(self, self.walls_group, False)
        for wall in hit_wall:
            if self.move_y > 0:
                self.rect.bottom = wall.rect.top
            elif self.move_y < 0:
                self.rect.top = wall.rect.bottom

        # проверка на столкновение с финишем
        if pygame.sprite.spritecollideany(self, self.finish_group):
            self.next_level = True

        # проверка на столкновение с монстрами
        if pygame.sprite.spritecollideany(self, self.enemy_group):
            self.rect.x = self.start_coord_x
            self.rect.y = self.start_coord_y

        # здесь будет проверка жизней, если их 0, то игрок возвращается на 1 уровень