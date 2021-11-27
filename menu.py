import pygame

import settings

buttons = []
screen = None
background = None


def init():
    global buttons, screen, background
    screen = pygame.Surface(settings.SIZE)

    name = pygame.image.load('menu_images/name_white.png')
    name = pygame.transform.scale(name, (settings.WIDTH, int(800 * settings.WIDTH / 3840)))
    moon_part = pygame.image.load('menu_images/moon_part.png')
    background = pygame.Surface(settings.SIZE)
    for i in range(settings.WIDTH // 600 + 1):
        for j in range(settings.HEIGHT // 600 + 1):
            background.blit(moon_part, (600 * i, 600 * j))
    background.blit(name, (0, 0))

    play_image = pygame.image.load('menu_images/play_button.png').convert_alpha()
    shop_image = pygame.image.load('menu_images/shop_button.png').convert_alpha()
    exit_image = pygame.image.load('menu_images/exit_button.png').convert_alpha()
    play_image = pygame.transform.scale(play_image, (400, 100))
    shop_image = pygame.transform.scale(shop_image, (400, 100))
    exit_image = pygame.transform.scale(exit_image, (400, 100))

    play_button = settings.Button(settings.WIDTH // 2 - 200, settings.HEIGHT // 2 - 200, 400, 100, 'switch_to_levels')
    play_button.image = play_image
    shop_button = settings.Button(settings.WIDTH // 2 - 200, settings.HEIGHT // 2 - 50, 400, 100, 'switch_to_shop')
    shop_button.image = shop_image
    exit_button = settings.Button(settings.WIDTH // 2 - 200, settings.HEIGHT // 2 + 100, 400, 100, 'exit')
    exit_button.image = exit_image
    buttons += [exit_button, shop_button, play_button]


def create_screen():
    global buttons, screen, background
    screen.blit(background, (0, 0))
    for b in buttons:
        b.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            for b in buttons:
                b.act(event)
    return screen

