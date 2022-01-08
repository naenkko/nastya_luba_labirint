import pygame
from wall import Wall


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

running = True
while running:
    for event in pygame.event.get():
        # при закрытии окна
        if event.type == pygame.QUIT:
            running = False

    # отрисовка и изменение свойств объектов
    screen.fill(screen_color)

    # Отображаем стены
    walls.draw(screen)

    # обновление экрана
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
