import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, x_coord, y_coord, width, height, walls_group, enemy_group, finish_group, monets,
                 heart_group):
        super().__init__()

        self.players = [pygame.image.load('images/the_newest_player_up.png'), pygame.image.load(
            'images/the_newest_player_down.png'),
                        pygame.image.load('images/the_newest_player_left.png'), pygame.image.load(
                'images/the_newest_player_right.png'),
                        pygame.image.load('images/the_newest_player_straight.png')]
        self.image = self.players[4]

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

        self.take_monet = False
        self.kill_by_monster = False

        self.walls_group = walls_group
        self.enemy_group = enemy_group
        self.finish_group = finish_group
        self.monet_group = monets
        self.heart_group = heart_group

    def left(self):
        self.image = self.players[2]

    def right(self):
        self.image = self.players[3]

    def straight(self):
        self.image = self.players[4]

    def up(self):
        self.image = self.players[0]

    def down(self):
        self.image = self.players[1]

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
            self.take_monet = True
            monet.kill()

        # проверка на столкновение с сердцами
        selected_hearts = pygame.sprite.spritecollide(self, self.heart_group, False)
        for heart in selected_hearts:
            self.take_monet = True
            self.lives += 1
            heart.kill()

        # проверка на столкновение с монстрами
        if pygame.sprite.spritecollideany(self, self.enemy_group):
            self.kill_by_monster = True
            self.rect.x = self.start_coord_x
            self.rect.y = self.start_coord_y
