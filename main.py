import pygame
import os

import menu
import shop
import levels
import shuttle
import ammunition
import enemies
import settings


# --------------------- Saving data functions ---------------------


def load_player_data():
    """
    Loads player progress from txt file.
    """
    check_file = os.path.exists('player_data.txt')
    if check_file:
        file = open('player_data.txt', 'r')
        data = file.readlines()
        # Settings variables
        for i in range(len(data)):
            words = data[i].split()
            if words[0] == '#' and words[1] == 'General_information':
                pass
            elif words[0] == '#' and words[1] == 'Purchases_and_selections':
                shop.load_player_data(data[i + 1:])
            elif words[0] == 'money':
                settings.money = int(words[1])
            elif words[0] == 'hp':
                settings.spaceship.hp = int(words[1])

        file.close()


def save_player_data():
    """
    Saves player progress into txt file.
    """
    file = open('player_data.txt', 'w')

    # General information
    file.write('# General_information' + '\n')
    file.write('money ' + str(settings.money) + '\n')
    file.write('hp ' + str(settings.spaceship.hp) + '\n')

    # Bought objects and upgrades
    file.write('# Purchases_and_selections' + '\n')
    shop.save_player_data(file)

    file.close()


# ------------------------- Initialization -------------------------


# Initializing libraries
pygame.init()
pygame.font.init()
pygame.mixer.init()

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

# Loading player data
load_player_data()


# --------------------------- Main core ---------------------------


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


# ---------------------------- Quiting ----------------------------


save_player_data()
pygame.quit()
