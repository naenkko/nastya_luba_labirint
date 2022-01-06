import pygame

screen_color = (0, 0, 0)
wall_color = (255, 255, 255)
# цвета можно так сделать: pygame.Color('#008000')

screen_size = width, height = 600, 650


pygame.init()
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('The maze infested with monsters')

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        # при закрытии окна
        if event.type == pygame.QUIT:
            running = False

    # отрисовка и изменение свойств объектов
    screen.fill(screen_color)

    # обновление экрана

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
