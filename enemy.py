import pygame


class Enemy(pygame.sprite.Sprite):

    def __init__(self, x_coord, y_coord, width, height, move_x, move_y, walls_group, enemy_group):
        super().__init__()

        self.image = pygame.image.load('images/newmonster1.png')

        self.rect = self.image.get_rect()
        self.rect.x = x_coord
        self.rect.y = y_coord

        self.move_x = move_x
        self.move_y = move_y

        if self.move_x > 0:
            self.type_of_move = 'horizontal'
        else:
            self.type_of_move = 'vertical'

        self.add(enemy_group)

        self.walls_group = walls_group

    def update(self):
        self.rect = self.rect.move(self.move_x, self.move_y)

        # проверка на столконовение со стенами
        if self.type_of_move == 'horizontal':
            hit_wall = pygame.sprite.spritecollide(self, self.walls_group, False)
            for wall in hit_wall:
                if self.move_x > 0:
                    self.rect.right = wall.rect.left
                elif self.move_x < 0:
                    self.rect.left = wall.rect.right
                self.move_x *= -1

        else:
            hit_wall = pygame.sprite.spritecollide(self, self.walls_group, False)
            for wall in hit_wall:
                if self.move_y > 0:
                    self.rect.bottom = wall.rect.top
                elif self.move_y < 0:
                    self.rect.top = wall.rect.bottom
                self.move_y *= -1
