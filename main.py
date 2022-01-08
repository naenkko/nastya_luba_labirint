import pygame
from wall import Wall
from player import Player


def draw_wall(wall_color, x_coord, y_coord, level, group):
    f_name = [f'lab_map/level_{level}_down.txt', f'lab_map/level_{level}_left.txt']
    with open(f_name[0]) as file:
        data = file.read()
        for row in data.split('\n'):
            for symb in row:
                if symb == '0':
                    Wall(x_coord, y_coord, 50, 5, wall_color, group)
                x_coord += 45
            x_coord = 0
            y_coord += 45

    x_coord, y_coord = 0, 145
    with open(f_name[1]) as file:
        data = file.read()
        for row in data.split('\n'):
            for symb in row:
                if symb == '|':
                    Wall(x_coord, y_coord, 5, 50, wall_color, group)
                x_coord += 45
            x_coord = 0
            y_coord += 45


screen_color = (0, 0, 0)
wall_color = (255, 255, 255)
# цвета можно так сделать: pygame.Color('#008000')

screen_size = width, height = 455, 600

start_dort = {1: (10, 155),
              2: (),
              3: (),
              4: (),
              5: ()}


pygame.init()
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('The maze infested with monsters')

clock = pygame.time.Clock()

level = 1

# создание стен лабиринта
walls = pygame.sprite.Group()
wall_x = 0
wall_y = 145
draw_wall(wall_color, wall_x, wall_y, level, walls)

player = Player(start_dort[1][0], start_dort[1][1], 20, 20, walls)
speed_player = 2

running = True
while running:
    for event in pygame.event.get():
        # при закрытии окна
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move_x = 0 - speed_player
            elif event.key == pygame.K_RIGHT:
                player.move_x = speed_player
            elif event.key == pygame.K_UP:
                player.move_y = 0 - speed_player
            elif event.key == pygame.K_DOWN:
                player.move_y = speed_player
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.move_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player.move_y = 0

    # отрисовка и изменение свойств объектов
    screen.fill(screen_color)

    # Отображаем стены
    walls.draw(screen)

    # отображаем игрока
    screen.blit(player.image, player.rect)

    # обновление экрана
    pygame.display.flip()
    clock.tick(60)

    player.update()

pygame.quit()
