import math
import pygame
import pygame.mixer

from menu import *
from shop import *
from levels import *
#from shuttle import *
from ammunition import *
from enemies import *
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

menu_init()

while settings.running:
    if settings.flag == 'menu':
        screen = menu_screen()
    elif settings.flag == 'levels':
        screen = menu_screen()
    elif settings.flag == 'shop':
        screen = shop_screen()
    if settings.running:
        main_surface.blit(screen, (0, 0))
        pygame.display.update()

pygame.quit()
