import pygame

import settings

global SIZE, flag

def menu_init():
    global menu_buttons, menu_screen,
    menu_buttons = []
    menu_screen = pygame.Surface(SIZE)
    menu_screen.fill((0, 0, 0))
    exit_button = Button(SIZE[0] - 100, 0, 100, 100, 'exit')
    menu_buttons.append(exit_button)

def menu_screen():
    for b in settings.menu_buttons:
        b.draw(settings.menu_screen)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            for b in settings.buttons:
                b.action(event)
    return settings.screen

