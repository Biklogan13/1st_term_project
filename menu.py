import pygame

import settings

buttons = []
screen = None


def menu_init():
    global buttons, screen
    screen = pygame.Surface(settings.SIZE)
    screen.fill((0, 0, 0))
    exit_button = settings.Button(settings.WIDTH - 60, 0, 60, 60, 'exit')
    shop_button = settings.Button(settings.WIDTH // 2, settings.HEIGHT // 2 - 100, 60, 60, 'switch_to_shop')
    levels_button = settings.Button(settings.WIDTH - 60, 0, 60, 60, 'switch_to_levels')
    buttons += [exit_button, shop_button, levels_button]


def menu_screen():
    global buttons, screen
    for b in buttons:
        b.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            for b in buttons:
                b.act(event)
    return screen

