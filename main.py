import pygame.mixer
import math
import pygame


import menu
import shop
import levels
import shuttle
import ammunition
import enemies
import settings

FPS = 60

pygame.init()
pygame.font.init()
pygame.mixer.init()

info = pygame.display.Info()
settings.SIZE = settings.WIDTH, settings.HEIGHT = info.current_w, info.current_h
main_surface = pygame.display.set_mode(settings.SIZE, pygame.FULLSCREEN | pygame.NOFRAME)
pygame.display.toggle_fullscreen()

clock = pygame.time.Clock()

menu.init()
shuttle.init()
levels.init()
shop.init()
enemies.init()

while settings.running:
    if settings.flag == 'menu':
        screen = menu.create_screen()
    elif settings.flag == 'levels':
        screen = levels.create_screen()

    elif settings.flag == 'shop':
        screen = shop.create_screen()
    else:
        print('ERROR, no screen!')

    if settings.running:
        main_surface.blit(screen, (0, 0))
        pygame.display.update()
        settings.tick_counter += 1

pygame.quit()
