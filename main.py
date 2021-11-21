import math
import pygame
import pygame.mixer

from menu import *
from shop import *
from levels import *
from shuttle import *
from ammunition import *
from enemies import *


# Variable which shows what gamescreen is now displayed
class Screen_flag:
    def __init__(self):
        self.screen = 'menu'

flag = Screen_flag()


pygame.init()
info = pygame.display.Info()
SIZE = WIDTH, HEIGHT = info.current_w, info.current_h
main_surface = pygame.display.set_mode(SIZE)

clock = pygame.time.Clock()


while True:
    if flag.screen == 'menu':
        screen = menu_screen()
    elif screen_flag == 'levels':
        screen = menu_screen()
    elif screen_flag == 'shop':
        screen = shop_screen()
    main_surface.blit(screen, (0, 0))
pygame.quit()