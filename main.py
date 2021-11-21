import math
import pygame
import pygame.mixer

from menu import *
from shop import *
from levels import *
#from shuttle import *
from ammunition import *
from enemies import *

FPS = 60

pygame.init()
pygame.font.init()
pygame.mixer.init()
info = pygame.display.Info()
SIZE = WIDTH, HEIGHT = info.current_w, info.current_h
main_surface = pygame.display.set_mode(SIZE, pygame.FULLSCREEN | pygame.NOFRAME)
pygame.display.toggle_fullscreen()


# Variable which shows which gamescreen is now displayed
flag = 'menu'

flag = Screen_flag()

clock = pygame.time.Clock()


menu_init()

while True:
    if flag == 'menu':
        screen = menu_screen()
    elif flag == 'levels':
        screen = menu_screen()
    elif flag == 'shop':
        screen = shop_screen()
    main_surface.blit(screen, (0, 0))
    pygame.display.update()

pygame.quit()
