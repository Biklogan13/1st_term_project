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

thickarrow_strings = (               #sized 24x24
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

cursor, mask = pygame.cursors.compile(thickarrow_strings, "X", ".")
cursor_sizer = ((24, 24), (7, 11), cursor, mask)
pygame.mouse.set_cursor(*cursor_sizer)

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
ammunition.init()


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

    if settings.spaceship.hp <= 0:
        # FIXME надо сделать геймовер, пока просто квит, для тестов вырубайте его
        print('GAME OVER, SACKBOY')
        pygame.quit()
        running = False
pygame.quit()
