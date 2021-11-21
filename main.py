import math
import pygame
import pygame.mixer

from menu import *
from shop import *
from levels import *
#from shuttle import *
from ammunition import *
from enemies import *
from settings import *

init_global()

FPS = 60

pygame.init()
pygame.font.init()
pygame.mixer.init()
info = pygame.display.Info()
settings.SIZE = settings.WIDTH, settings.HEIGHT = info.current_w, info.current_h
main_surface = pygame.display.set_mode(settings.SIZE, pygame.FULLSCREEN | pygame.NOFRAME)
pygame.display.toggle_fullscreen()


# Variable which shows which gamescreen is now displayed
clock = pygame.time.Clock()

menu_init()

while True:
    if settings.flag == 'menu':
        screen = menu_screen()
    elif settings.flag == 'levels':
        screen = menu_screen()
    elif settings.flag == 'shop':
        screen = shop_screen()
    main_surface.blit(screen, (0, 0))
    pygame.display.update()

pygame.quit()
