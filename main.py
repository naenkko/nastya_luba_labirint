import pygame


def draw_wall(screen, wall_color, wall_x, wall_y, level):
    f_name = [f'lab_map/level_{level}_down.txt', f'lab_map/level_{level}_left.txt']
    with open(f_name[0]) as file:
        data = file.read()
        for row in data.split('\n'):
            for symb in row:
                if symb == '0':
                    pygame.draw.rect(screen, wall_color, (wall_x, wall_y, 50, 5), 0)
                wall_x += 45
            wall_x = 0
            wall_y += 45

    wall_x, wall_y = 0, 145
    with open(f_name[1]) as file:
        data = file.read()
        for row in data.split('\n'):
            for symb in row:
                if symb == '|':
                    pygame.draw.rect(screen, wall_color, (wall_x, wall_y, 5, 50), 0)
                wall_x += 45
            wall_x = 0
            wall_y += 45


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

wall_x = 0
wall_y = 145

level = 1

running = True
while running:
    for event in pygame.event.get():
        # при закрытии окна
        if event.type == pygame.QUIT:
            running = False

    # отрисовка и изменение свойств объектов
    screen.fill(screen_color)

    # Отображаем стены
    draw_wall(screen, wall_color, wall_x, wall_y, level)




    # обновление экрана
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
