import pygame
import os

import settings

# Global variables of menu section
# Surface on which menu elements will be drown
screen = None
# An array which contains all Buttons objects
buttons = []
# Array which contains all images which will be displayed directly on screen
images = dict.fromkeys(['background', 'name', 'plate'])


def load_images():
    """
    Function which loads all images which are going to be blit directly on screen
    """
    global images

    menu_background_path = os.path.join('.', 'backgrounds', 'menu_background_1.png')
    menu_background = pygame.image.load(menu_background_path).convert_alpha()
    images['background'] = pygame.transform.scale(menu_background, settings.SIZE)

    name_path = os.path.join('.', 'interface_elements', 'name_white.png')
    name = pygame.image.load(name_path).convert_alpha()
    images['name'] = pygame.transform.scale(name, (settings.WIDTH, int(800 * settings.WIDTH / 3840)))

    plate_path = os.path.join('.', 'interface_elements', 'plate.png')
    plate = pygame.image.load(plate_path).convert_alpha()
    images['plate'] = pygame.transform.scale(plate, (plate, (500, 500)))


def create_interface_elements():
    global buttons

    button_size = (400, 100)

    play_image_path = os.path.join('.', 'interface_elements', 'play_button.png')
    shop_image_path = os.path.join('.', 'interface_elements', 'shop_button.png')
    exit_image_path = os.path.join('.', 'interface_elements', 'exit_button.png')
    play_image = pygame.image.load(play_image_path).convert_alpha()
    shop_image = pygame.image.load(shop_image_path).convert_alpha()
    exit_image = pygame.image.load(exit_image_path).convert_alpha()
    play_image = pygame.transform.scale(play_image, button_size)
    shop_image = pygame.transform.scale(shop_image, button_size)
    exit_image = pygame.transform.scale(exit_image, button_size)

    play_image_hover_path = os.path.join('.', 'interface_elements', 'play_button_hover.png')
    shop_image_hover_path = os.path.join('.', 'interface_elements', 'shop_button_hover.png')
    exit_image_hover_path = os.path.join('.', 'interface_elements', 'exit_button_hover.png')
    play_image_hover = pygame.image.load(play_image_hover_path).convert_alpha()
    shop_image_hover = pygame.image.load(shop_image_hover_path).convert_alpha()
    exit_image_hover = pygame.image.load(exit_image_hover_path).convert_alpha()
    play_image_hover = pygame.transform.scale(play_image_hover, (400, 100))
    shop_image_hover = pygame.transform.scale(shop_image_hover, (400, 100))
    exit_image_hover = pygame.transform.scale(exit_image_hover, (400, 100))

    play_button = settings.Button(settings.WIDTH // 2 - 200, settings.HEIGHT // 2 - 100, 400, 100, 'switch_to_levels')
    play_button.image, play_button.image_hover = play_image, play_image_hover
    shop_button = settings.Button(settings.WIDTH // 2 - 200, settings.HEIGHT // 2 + 50, 400, 100, 'switch_to_shop')
    shop_button.image, shop_button.image_hover = shop_image, shop_image_hover
    exit_button = settings.Button(settings.WIDTH // 2 - 200, settings.HEIGHT // 2 + 200, 400, 100, 'exit')
    exit_button.image, exit_button.image_hover = exit_image, exit_image_hover
    buttons += [exit_button, shop_button, play_button]


def init():
    global screen
    screen = pygame.Surface(settings.SIZE)

    load_images()
    create_interface_elements()


def create_screen():
    global screen, buttons, images

    # Displaying images
    screen.blit(settings.menu_background, (0, 0))
    screen.blit(name, (0, 0))
    screen.blit(plate, (settings.WIDTH // 2 - 250, settings.HEIGHT // 2 - 150))

    # Drawing buttons
    for b in buttons:
        b.draw(screen)

    #
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            for b in buttons:
                b.act(event)
        if event.type == pygame.MOUSEMOTION:
            for b in buttons:
                b.hover_test(event)

    # Returning the screen which will be displayed
    return screen

