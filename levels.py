import pygame

import enemies
import shuttle
import settings
import ammunition

buttons = []
screen = None
ammo_type = 1
level_background = None

def init():
    global buttons, screen, level_background
    screen = pygame.Surface(settings.SIZE)
    level_background = pygame.image.load('backgrounds/menu_background.png').convert_alpha()
    level_background = pygame.transform.scale(level_background, settings.SIZE)
    ammunition.processing(screen)


def create_screen():
    global buttons, screen, ammo_type, level_background
    screen.blit(level_background, (0, 0))
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
    ammunition.processing(screen)
    enemies.processing(screen)
    shuttle.processing(screen)
    return screen


