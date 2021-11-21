import pygame

import settings

buttons = []
screen = None


def init():
    global buttons, screen
    screen = pygame.Surface(settings.SIZE)
    screen.fill((100, 0, 0))
    back_button = settings.Button(0, 0, 60, 60, 'switch_to_menu')
    buttons += [back_button]


def create_screen():
    global buttons, screen
    for b in buttons:
        b.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            for b in buttons:
                b.act(event)
    return screen

