import pygame

import settings

buttons = []
screen = None


def menu_init():
    global buttons, screen
    screen = pygame.Surface(settings.SIZE)
    screen.fill((0, 0, 0))
    exit_button = settings.Button(settings.WIDTH - 50, 0, 50, 50, 'exit')
    buttons.append(exit_button)


def menu_screen():
    global buttons, screen
    for b in buttons:
        b.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            for b in buttons:
                b.act(event)
    return screen

