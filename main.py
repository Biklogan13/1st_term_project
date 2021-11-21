import math
from random import *
import pygame
from pygame.mixer import *

from menu.py import *
from shop.py import *
from levels.py import *
from shuttle.py import *
from ammunition.py import *
from enemies.py import *


# Variable which shows what gamescreen is now displayed
screen_flag = menu


pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
mainsurface = pygame.display.set_mode(SIZE)

clock = pygame.time.Clock()


while not finished:
    if screen_flag == menu:
        screen = menu_screen()
    elif screen_flag == levels:
        screen = menu_screen()
    elif screen_flag == shop:
        screen = shop_screen()

pygame.quit()