import pygame
from wall import Wall
from player import Player
from enemy import Enemy


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

        # отображаем врагов
        enemies.draw(screen)

        # отображаем игрока
        screen.blit(player.image, player.rect)

        # обновление экрана
        pygame.display.flip()
        clock.tick(60)

        player.update()
        enemies.update()

pygame.quit()
