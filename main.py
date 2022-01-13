import pygame, sys
from wall import Wall
from player import Player
from enemy import Enemy
from monet import Monet


pygame.font.init()
menu_font = pygame.font.Font(None, 48)

screen_color = (0, 0, 0)
wall_color = (255, 255, 255)
# цвета можно так сделать: pygame.Color('#008000')
screen_size = width, height = 455, 600

start_dort = {1: (10, 155),
              2: (415, 155),
              3: (10, 560),
              4: (235, 155),
              5: (10, 335)}

enemy_info = {1: {'coords': [(190, 155), (235, 200), (10, 380), (415, 155)], 'move': [(0, 1), (1, 0), (0, 1), (0, 1)]},
              2: {'coords': [(190, 155), (280, 425), (10, 335), (100, 515)], 'move': [(0, 1), (0, 1), (1, 0), (1, 0)]},
              3: {'coords': [(145, 200), (415, 155), (100, 335)], 'move': [(1, 0), (0, 1), (1, 0)]},
              4: {'coords': [(145, 155), (235, 515), (10, 155), (190, 335), (370, 380)],
                  'move': [(0, 1), (1, 0), (0, 1), (1, 0), (0, 1)]},
              5: {'coords': [(10, 560), (280, 155), (190, 245), (415, 155), (235, 425)],
                  'move': [(1, 0), (0, 1), (0, 1), (0, 1), (1, 0)]}
              }

monet_coords = {1: [(375, 250), (60, 385), (15, 565)],
                2: [(375, 205), (60, 205), (375, 430), (150, 565), (375, 565)],
                3: [(285, 250), (375, 565), (60, 475), (15, 295), (375, 430), (240, 565)],
                4: [(375, 160), (105, 340), (195, 475), (420, 160), (420, 475), (330, 565)],
                5: [(105, 385), (195, 520), (285, 475), (105, 250), (375, 160), (15, 250)]
                }


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


def progress():
    global running
    global level
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move_x = 0 - speed_player
                elif event.key == pygame.K_RIGHT:
                    player.move_x = speed_player
                if event.key == pygame.K_UP:
                    player.move_y = 0 - speed_player
                elif event.key == pygame.K_DOWN:
                    player.move_y = speed_player
                if event.key == pygame.K_p:
                    pause()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.move_x = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player.move_y = 0

        if player.next_level and level <= 5: # проверка, дошел ли игрок до финиша
            level += 1
            player.next_level = False
            walls.empty() # очищаем все группы спрайтов
            finish.empty()
            enemies.empty()
            create_level(level) # создаем новый уровень

        elif player.next_level and level > 5: # !что будет происходить, когда игрок пройдет 5 уровень!
            pass

        else: # если не дошел до финиша
            screen.fill(screen_color)

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
                if event.key == pygame.K_s:# if u press S the game will start
                    progress()
                elif event.key == pygame.K_q: # if u press Q u will get out of the game
                    quit()

        pygame.display.update()


def draw_wall(wall_color, finish_color, x_coord, y_coord, level, group_wall, group_finish):
    f_name = [f'lab_map/level_{level}_down.txt', f'lab_map/level_{level}_left.txt']
    with open(f_name[0]) as file:
        data = file.read()
        for row in data.split('\n'):
            for symb in row:
                if symb == '0':
                    Wall(x_coord, y_coord, 50, 5, wall_color, group_wall)
                elif symb == '!':
                    Wall(x_coord, y_coord, 50, 5, finish_color, group_finish)
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
                    Wall(x_coord, y_coord, 5, 50, finish_color, group_finish)
                x_coord += 45
            x_coord = 0
            y_coord += 45


def create_level(level):
    # создание стен лабиринта
    wall_x = 0
    wall_y = 145
    draw_wall(wall_color, screen_color, wall_x, wall_y, level, walls, finish)

    # создание врагов на поле
    for i in range(len(enemy_info[level]['coords'])):
        Enemy(enemy_info[level]['coords'][i][0], enemy_info[level]['coords'][i][1],
              30, 30,
              enemy_info[level]['move'][i][0], enemy_info[level]['move'][i][1], walls, enemies)

    # создание монет на поле
    for i in range(len(monet_coords[level])):
        Monet(monet_coords[level][i][0], monet_coords[level][i][1], 20, 20, monets)

    # изменение координат игрока
    player.rect.x = start_dort[level][0]
    player.rect.y = start_dort[level][1]

    player.start_coord_x = start_dort[level][0]
    player.start_coord_y = start_dort[level][1]

    # изменение координат начальной точки
    start.rect.x = start_dort[level][0]
    start.rect.y = start_dort[level][1]


pygame.init()
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('The maze infested with monsters')

clock = pygame.time.Clock()

level = 1

walls = pygame.sprite.Group()
finish = pygame.sprite.Group()
enemies = pygame.sprite.Group()
monets = pygame.sprite.Group()

# создание игрока
player = Player(start_dort[level][0], start_dort[level][1], 20, 20, walls, enemies, finish)
speed_player = 2

# создание точки, с которой игрок начинает движение
start = pygame.sprite.Sprite()
start.image = pygame.Surface([30, 30])
start.image.fill((255, 0, 0))
start.rect = start.image.get_rect()

create_level(level)

running = True

start_menu()
