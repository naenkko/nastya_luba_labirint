import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, x_coord, y_coord, width, height, walls_group, enemy_group, finish_group, monets):
        super().__init__()

        # left, right = False, False
        # right_walk = ['player1.png', 'player2.png', 'player3.png', 'player4.png']
        # left_walk = ['player5.png', 'player6.png', 'player7.png', 'player8.png']
        # straight_walk = 'player9.png'
        # if left is True and right is False:
        #     count = 5
        #     self.last_update = pygame.time.get_ticks()
        #     if count == 5 and pygame.time.get_ticks() - self.last_update > 5:
        #         self.image = pygame.image.load(left_walk[0])
        #         count += 1
        #         self.last_update = pygame.time.get_ticks()
        #     elif count == 6 and pygame.time.get_ticks() - self.last_update > 5:
        #         self.image = pygame.image.load(left_walk[1])
        #         count += 1
        #         self.last_update = pygame.time.get_ticks()
        #     elif count == 7 and pygame.time.get_ticks() - self.last_update > 5:
        #         self.image = pygame.image.load(left_walk[2])
        #         count += 1
        #         self.last_update = pygame.time.get_ticks()
        #     elif count == 8 and pygame.time.get_ticks() - self.last_update > 5:
        #         self.image = pygame.image.load(left_walk[1])
        #         count -= 3
        #         self.last_update = pygame.time.get_ticks()
        # if left is False and right is True:
        #     count = 1
        #     self.last_update = pygame.time.get_ticks()
        #     if count == 1 and pygame.time.get_ticks() - self.last_update > 5:
        #         self.image = pygame.image.load(right_walk[0])
        #         count += 1
        #         self.last_update = pygame.time.get_ticks()
        #     elif count == 2 and pygame.time.get_ticks() - self.last_update > 5:
        #         self.image = pygame.image.load(right_walk[1])
        #         count += 1
        #         self.last_update = pygame.time.get_ticks()
        #     elif count == 3 and pygame.time.get_ticks() - self.last_update > 5:
        #         self.image = pygame.image.load(right_walk[2])
        #         count += 1
        #         self.last_update = pygame.time.get_ticks()
        #     elif count == 4 and pygame.time.get_ticks() - self.last_update > 5:
        #         self.image = pygame.image.load(right_walk[1])
        #         count -= 3
        #         self.last_update = pygame.time.get_ticks()
        # if left is False and right is False:
        #     self.image = pygame.image.load(straight_walk)

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
        self.used_lives = 0
        self.selected_monets = 0

        self.next_level = False
        self.open_door = False

        self.walls_group = walls_group
        self.enemy_group = enemy_group
        self.finish_group = finish_group
        self.monet_group = monets

    def update(self, *args):
        # проверка, пора ли открывать стену выхода, если да, то мегяем ее цвет
        if not self.monet_group:
            self.open_door = True

        # изменяем координаты по горизонтали
        self.rect.x += self.move_x

        # проверка на столконовение со стенами
        hit_wall = pygame.sprite.spritecollide(self, self.walls_group, False)
        for wall in hit_wall:
            if self.move_x > 0:
                self.rect.right = wall.rect.left
            elif self.move_x < 0:
                self.rect.left = wall.rect.right

        # проверка на столкновение с финишем
        if pygame.sprite.spritecollideany(self, self.finish_group):
            if not self.monet_group:
                self.next_level = True
            else:
                hit_finish = pygame.sprite.spritecollide(self, self.finish_group, False)
                for finish in hit_finish:
                    if self.move_x > 0:
                        self.rect.right = finish.rect.left
                    elif self.move_x < 0:
                        self.rect.left = finish.rect.right

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
            if not self.monet_group:
                self.next_level = True
            else:
                hit_finish = pygame.sprite.spritecollide(self, self.finish_group, False)
                for finish in hit_finish:
                    if self.move_y > 0:
                        self.rect.bottom = finish.rect.top
                    elif self.move_y < 0:
                        self.rect.top = finish.rect.bottom

        # проверка на столкновение с монетами
        selected_monet = pygame.sprite.spritecollide(self, self.monet_group, False)
        for monet in selected_monet:
            self.selected_monets += 1
            monet.kill()

        # проверка на столкновение с монстрами
        if pygame.sprite.spritecollideany(self, self.enemy_group):
            self.rect.x = self.start_coord_x
            self.rect.y = self.start_coord_y

        # здесь будет проверка жизней, если их 0, то игрок возвращается на 1 уровень