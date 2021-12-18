import pygame

import menu
import shop
import levels
import shuttle
import ammunition
import enemies
import settings

# Initializing libraries
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Setting a cursor
arrow_strings = (  # sized 24x24
  "XX                      ",
  "XXX                     ",
  "XXXX                    ",
  "XX.XX                   ",
  "XX..XX                  ",
  "XX...XX                 ",
  "XX....XX                ",
  "XX.....XX               ",
  "XX......XX              ",
  "XX.......XX             ",
  "XX........XX            ",
  "XX........XXX           ",
  "XX......XXXXX           ",
  "XX.XXX..XX              ",
  "XXXX XX..XX             ",
  "XX   XX..XX             ",
  "     XX..XX             ",
  "      XX..XX            ",
  "      XX..XX            ",
  "       XXXX             ",
  "       XX               ",
  "                        ",
  "                        ",
  "                        ")

cursor, mask = pygame.cursors.compile(arrow_strings, "X", ".")
cursor_sizer = ((24, 24), (7, 11), cursor, mask)
pygame.mouse.set_cursor(*cursor_sizer)

# Setting a display
info = pygame.display.Info()
settings.SIZE = settings.WIDTH, settings.HEIGHT = info.current_w, info.current_h
main_surface = pygame.display.set_mode(settings.SIZE, pygame.FULLSCREEN | pygame.NOFRAME)
pygame.display.toggle_fullscreen()

FPS = 60
clock = pygame.time.Clock()

# Initializing modules
menu.init()
shuttle.init()
levels.init()
shop.init()
enemies.init()
ammunition.init()

# Circle which crates output every frame
while settings.running:
    clock.tick(FPS)
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
