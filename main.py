import datetime
import pygame, sys
from wall import Wall
from player import Player
from enemy import Enemy
from monet import Monet


pygame.font.init()
menu_font = pygame.font.Font(None, 48)
lives_monets_font = pygame.font.Font(None, 28)
seconds, minute, count, flag, flag2, count2 = 0, 0, 0, False, False, 0


def quit():
    pygame.quit()


def pause():
    pause_game = True
    global running
    while pause_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c: # if u press C the game will continue
                    pause_game = False
                elif event.key == pygame.K_q: # if u do Q the game will over
                    quit()
        screen.fill((15, 82, 186))
        message1 = menu_font.render('PAUSED', True, (0, 0, 0))
        message2 = menu_font.render('нажмите C, чтобы', True, (0, 0, 0))
        message3 = menu_font.render('продолжить', True, (0, 0, 0))
        message4 = menu_font.render('или Q, чтобы выйти', True, (0, 0, 0))
        screen.blit(message1, (150, 120))
        screen.blit(message2, (80, 220))
        screen.blit(message3, (110, 270))
        screen.blit(message4, (55, 320))

        pygame.display.update()
        clock.tick(10)


def the_end():
    global running
    global num_of_try
    while running:
        screen.fill((15, 82, 186))
        message_1 = menu_font.render('РЕЗУЛЬТАТЫ:', True, (0, 0, 0))
        message_2 = menu_font.render('всего:', True, (0, 0, 0))
        message_3 = menu_font.render(f'потраченных жизней - {player.used_lives}', True, (0, 0, 0))
        message_4 = menu_font.render('потраченного времени - ', True, (0, 0, 0))
        message_5 = menu_font.render('чтобы выйти из игры', True, (0, 0, 0))
        message_6 = menu_font.render('нажмите Q', True, (0, 0, 0))
        message_7 = menu_font.render('вернуться на старт - B', True, (0, 0, 0))
        screen.blit(message_1, (100, 120))
        screen.blit(message_2, (1250, 160))
        screen.blit(message_3, (10, 200))
        screen.blit(message_4, (10, 240))
        screen.blit(message_5, (10, 280))
        screen.blit(message_6, (700, 320))
        screen.blit(message_7, (10, 360))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b: # if u press B u will back to the start menu
                    num_of_try = 1
                    player.used_lives = 0
                    start_menu()
                elif event.key == pygame.K_q: # if u press Q u will get out of the game
                    quit()

        pygame.display.update()


def progress():
    global running
    global level
    global num_of_try
    global seconds
    global minute
    global count, count2
    global flag, flag2
    global left, right

    seconds = datetime.datetime.now().second
    minute = datetime.datetime.now().minute

    while running:
        timer = 30
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # player.left, player.right = True, False
                    player.move_x = 0 - speed_player
                elif event.key == pygame.K_RIGHT:
                    # player.left, player.right = False, True
                    player.move_x = speed_player
                if event.key == pygame.K_UP:
                    # player.left, player.right = False, False
                    player.move_y = 0 - speed_player
                elif event.key == pygame.K_DOWN:
                    # player.left, player.right = False, False
                    player.move_y = speed_player
                if event.key == pygame.K_p:
                    pause()
                    flag = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.move_x = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player.move_y = 0

        if player.open_door: # если все монеты собраны, стенка выхода меняет цвет
            for f in finish:
                f.image.fill(screen_color)

        if player.next_level and level <= 5: # проверка, дошел ли игрок до финиша
            seconds = datetime.datetime.now().second
            minute = datetime.datetime.now().minute
            count = 0
            count2 = 0
            level += 1
            if level == 1:
                player.lives = 5
                player.selected_monets = 0
            player.next_level = False
            player.open_door = False
            player.selected_monets = 0
            walls.empty()  # очищаем все группы спрайтов
            finish.empty()
            enemies.empty()
            monets.empty()
            if level == 6:
                level = 1
                the_end()
            else:
                create_level(level)  # создаем новый уровень

        else: # если не дошел до финиша
            screen.fill(screen_color)
            timer_text = menu_font.render(f"{timer - count}", True, (255, 255, 255))
            screen.blit(timer_text, (10, 100))
            if flag:
                seconds = datetime.datetime.now().second
                minute = datetime.datetime.now().minute
                flag = False
            if flag is False and (seconds + 30 == datetime.datetime.now().second) or \
                    (minute + 1 == datetime.datetime.now().minute and
                     datetime.datetime.now().second == 30 - (60 - seconds)):
                seconds = datetime.datetime.now().second
                minute = datetime.datetime.now().minute
                count = 0
                timer = 30
                flag2 = True

            if flag is False and (seconds + count == datetime.datetime.now().second) or \
                    (minute + 1 == datetime.datetime.now().minute and
                     datetime.datetime.now().second + 60 == seconds + count):
                count += 1
                timer_text = menu_font.render(f"{timer - count}", True, (255, 255, 255))
                screen.blit(timer_text, (10, 100))

            # отображаем информацию о количестве жизней
            if flag2:
                player.lives -= 1
                player.used_lives += 1
                player.rect.x = start_dort[level][0]
                player.rect.y = start_dort[level][1]
                flag2 = False

            if player.lives == 0: # если жизни закончились
                level = 1
                num_of_try += 1
                player.lives = 5
                player.selected_monets = 0
                player.next_level = False
                player.open_door = False
                walls.empty()  # очищаем все группы спрайтов
                finish.empty()
                enemies.empty()
                create_level(level)

            about_lives_mess = lives_monets_font.render(f'Количество жизней: {player.lives}', True, (255, 162, 0))
            screen.blit(about_lives_mess, (235, 95))

            # отображаем информацию о количестве собранных монет
            about_monets_mess = lives_monets_font.render(f'Собранные монеты: '
                                                         f'{player.selected_monets}/{len(monet_coords[level])}',
                                                         True, (255, 255, 0))
            screen.blit(about_monets_mess, (225, 120))

            # отобрвжвем номер уровня
            level_mess = lives_monets_font.render(f'УРОВЕНЬ {level}', True, (255, 255, 255))
            screen.blit(level_mess, (336, 10))

            # отображаем № попытки
            level_mess = lives_monets_font.render(f'Попытка {num_of_try}', True, (255, 0, 0))
            screen.blit(level_mess, (10, 10))

            # Отображаем стены
            walls.draw(screen)

            # отображаем финиш
            finish.draw(screen)

            # отображаем точку начала
            screen.blit(start.image, start.rect)

            # отображаем монеты
            monets.draw(screen)

            # отображаем врагов
            enemies.draw(screen)

            # отображаем игрока
            screen.blit(player.image, player.rect)

            # обновление экрана
            pygame.display.flip()
            clock.tick(60)

            player.update()
            enemies.update()


def start_menu():
    global running
    global level
    while running:
        screen.fill((15, 82, 186))
        name1 = menu_font.render('THE MAZE INFESTED', True, (0, 0, 0))
        name2 = menu_font.render('WITH MONSTERS.', True, (0, 0, 0))
        start = menu_font.render('START GAME', True, (0, 0, 0))
        roots1 = menu_font.render('цель игрока:', True, (0, 0, 0))
        roots2 = menu_font.render('пройти все 5 лабиринтов', True, (0, 0, 0))
        roots3 = menu_font.render('и собрать монеты', True, (0, 0, 0))
        root4 = menu_font.render('нажмите S, чтобы', True, (0, 0, 0))
        root5 = menu_font.render('начать', True, (0, 0, 0))
        root6 = menu_font.render('или Q, чтобы выйти', True, (0, 0, 0))
        root7 = menu_font.render('пауза - P', True, (0, 0, 0))
        screen.blit(start, (120, 350))
        screen.blit(name1, (55, 100))
        screen.blit(name2, (70, 130))
        screen.blit(roots1, (115, 190))
        screen.blit(roots2, (35, 230))
        screen.blit(roots3, (80, 270))
        screen.blit(root4, (80, 395))
        screen.blit(root5, (170, 435))
        screen.blit(root6, (55, 475))
        screen.blit(root7, (160, 515))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s: # if u press S the game will start
                    create_level(level)
                    progress()
                elif event.key == pygame.K_q: # if u press Q u will get out of the game
                    quit()

        pygame.display.update()


def draw_wall(wall_color, x_coord, y_coord, level, group_wall, group_finish):
    f_name = [f'lab_map/level_{level}_down.txt', f'lab_map/level_{level}_left.txt']
    with open(f_name[0]) as file:
        data = file.read()
        for row in data.split('\n'):
            for symb in row:
                if symb == '0':
                    Wall(x_coord, y_coord, 50, 5, wall_color, group_wall)
                elif symb == '!':
                    Wall(x_coord, y_coord, 50, 5, (255, 0, 0), group_finish)
                x_coord += 45
            x_coord = 0
            y_coord += 45

    x_coord, y_coord = 0, 145
    with open(f_name[1]) as file:
        data = file.read()
        for row in data.split('\n'):
            for symb in row:
                if symb == '|':
                    Wall(x_coord, y_coord, 5, 50, wall_color, group_wall)
                elif symb == '!':
                    Wall(x_coord, y_coord, 5, 50, (255, 0, 0), group_finish)
                x_coord += 45
            x_coord = 0
            y_coord += 45


def create_level(level):
    # создание стен лабиринта
    wall_x = 0
    wall_y = 145
    draw_wall(wall_color, wall_x, wall_y, level, walls, finish)

    # создание врагов на поле
    for i in range(len(enemy_info[level]['coords'])):
        Enemy(enemy_info[level]['coords'][i][0], enemy_info[level]['coords'][i][1],
              30, 30,
              enemy_info[level]['move'][i][0], enemy_info[level]['move'][i][1], walls, enemies)

    # создание монет на поле
    for i in range(len(monet_coords[level])):
        Monet(monet_coords[level][i][0], monet_coords[level][i][1], 20, 20, monets)

    if level == 1:
        player.lives = 5

    # изменение координат игрока
    player.rect.x = start_dort[level][0]
    player.rect.y = start_dort[level][1]

    player.start_coord_x = start_dort[level][0]
    player.start_coord_y = start_dort[level][1]

    # изменение координат начальной точки
    start.rect.x = start_dort[level][0]
    start.rect.y = start_dort[level][1]


screen_color = (0, 0, 0)
wall_color = (255, 255, 255)
# цвета можно так сделать: pygame.Color('#008000')
screen_size = width, height = 455, 600

start_dort = {1: (10, 155),
              2: (415, 155),
              3: (10, 560),
              4: (235, 155),
              5: (10, 335)}

enemy_info = {1: {'coords': [(325, 245), (10, 425)], 'move': [(0, 1), (1, 0)]},
              2: {'coords': [(55, 380), (100, 515), (280, 425)], 'move': [(1, 0), (1, 0), (0, 1)]},
              3: {'coords': [(415, 155), (190, 470), (10, 155)], 'move': [(0, 1), (1, 0), (1, 0)]},
              4: {'coords': [(145, 155), (10, 515), (370, 380), (235, 515)],
                  'move': [(0, 1), (1, 0), (0, 1), (1, 0)]},
              5: {'coords': [(10, 560), (145, 155), (190, 245)],
                  'move': [(1, 0), (1, 0), (0, 1)]}
              }

monet_coords = {1: [(240, 250), (105, 520), (240, 475)],
                2: [(15, 250), (330, 160)],
                3: [(60, 160), (195, 430)],
                4: [(105, 205), (375, 385), (285, 565)],
                5: [(105, 250), (195, 385), (150, 520)]
                }


pygame.init()
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('The maze infested with monsters')

clock = pygame.time.Clock()

level = 1

num_of_try = 1

walls = pygame.sprite.Group()
finish = pygame.sprite.Group()
enemies = pygame.sprite.Group()
monets = pygame.sprite.Group()

# создание игрока
player = Player(start_dort[level][0], start_dort[level][1], 20, 20, walls, enemies, finish, monets)
speed_player = 3

# создание точки, с которой игрок начинает движение
start = pygame.sprite.Sprite()
start.image = pygame.Surface([30, 30])
start.image.fill((255, 0, 0))
start.rect = start.image.get_rect()

running = True

start_menu()
