import pygame

import enemies
import shuttle
import settings
import ammunition

buttons = []
screen = None
ammo_type = 1


def init():
    global buttons, screen
    screen = pygame.Surface(settings.SIZE)
    screen.fill((0, 100, 0))
    ammunition.processing(screen)


def create_screen():
    global buttons, screen, ammo_type
    screen.fill((0, 100, 0))
    for b in buttons:
        b.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            for b in buttons:
                b.act(event)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
            ammo_type += 1
            ammo_type = ammo_type % 3
        # Exiting to menu if esc is pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        settings.flag = 'menu'
    shuttle.processing(screen)
    ammunition.processing(screen)
    enemies.processing(screen)
    return screen


