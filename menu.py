import pygame
import os

import settings

# Global variables of menu section
# Surface on which menu elements will be drown
screen = None
# An array which contains all Buttons objects
buttons = []
# Array which contains all images which will be displayed directly on screen
images = dict.fromkeys(['name', 'plate'])


class MenuButton(settings.Button):
    def __init__(self, x, y, size, action, image, image_hover):
        """
        Initializes button specified for menu.
        :param x: x coordinate of the button
        :param y: y coordinate of the button
        :param size: (width, height) tuple which defines size of the button
        :param action: 1 of 3 actions: 'switch_to_levels', 'switch_to_shop', 'exit'
        :param image: image of the button when mouse is not hovering over it
        :param image_hover:  image of the button when mouse is hovering over it
        """
        self.x = x
        self.y = y
        self.width = size[0]
        self.height = size[1]
        self.action = action
        self.hover = False
        self.image = image
        self.image_hover = image_hover

    def draw(self):
        if self.hover:
            screen.blit(self.image_hover, (self.x, self.y))
        else:
            screen.blit(self.image, (self.x, self.y))

    def act(self, event):
        if event.button == 1 and 0 <= event.pos[0] - self.x <= self.width and 0 <= event.pos[1] - self.y <= self.height:
            if self.action == 'exit':
                pygame.quit()
                settings.running = False
            elif self.action == 'switch_to_levels':
                settings.flag = 'levels'
            elif self.action == 'switch_to_shop':
                settings.flag = 'shop'


def load_images():
    """
    Loads all images which are going to be blit directly on screen.
    """
    menu_background_path = os.path.join('.', 'backgrounds', 'menu_background_1.png')
    menu_background = pygame.image.load(menu_background_path).convert_alpha()
    settings.menu_background = pygame.transform.scale(menu_background, settings.SIZE)

    name_path = os.path.join('.', 'interface_elements', 'name_white.png')
    name = pygame.image.load(name_path).convert_alpha()
    images['name'] = pygame.transform.scale(name, (settings.WIDTH, int(800 * settings.WIDTH / 3840)))

    plate_path = os.path.join('.', 'interface_elements', 'plate.png')
    plate = pygame.image.load(plate_path).convert_alpha()
    images['plate'] = pygame.transform.scale(plate, (500, 500))


def create_interface_elements():
    """
    Creates interface elements (button objects).
    """
    global buttons

    # Loading images for buttons
    play_image_path = os.path.join('.', 'interface_elements', 'play_button.png')
    shop_image_path = os.path.join('.', 'interface_elements', 'shop_button.png')
    exit_image_path = os.path.join('.', 'interface_elements', 'exit_button.png')
    play_image = pygame.image.load(play_image_path).convert_alpha()
    shop_image = pygame.image.load(shop_image_path).convert_alpha()
    exit_image = pygame.image.load(exit_image_path).convert_alpha()

    play_image_hover_path = os.path.join('.', 'interface_elements', 'play_button_hover.png')
    shop_image_hover_path = os.path.join('.', 'interface_elements', 'shop_button_hover.png')
    exit_image_hover_path = os.path.join('.', 'interface_elements', 'exit_button_hover.png')
    play_image_hover = pygame.image.load(play_image_hover_path).convert_alpha()
    shop_image_hover = pygame.image.load(shop_image_hover_path).convert_alpha()
    exit_image_hover = pygame.image.load(exit_image_hover_path).convert_alpha()

    # Resizing images
    button_size = (400, 100)
    [play_image, shop_image, exit_image, play_image_hover, shop_image_hover, exit_image_hover] =\
        [pygame.transform.scale(image, button_size) for image in
         [play_image, shop_image, exit_image, play_image_hover, shop_image_hover, exit_image_hover]]

    # Creating button objects
    play_button = MenuButton((settings.WIDTH - button_size[0]) // 2, settings.HEIGHT // 2 - button_size[1],
                             button_size, 'switch_to_levels', play_image, play_image_hover)
    shop_button = MenuButton((settings.WIDTH - button_size[0]) // 2, settings.HEIGHT // 2 + 50,
                             button_size, 'switch_to_shop', shop_image, shop_image_hover)
    exit_button = MenuButton((settings.WIDTH - button_size[0]) // 2, settings.HEIGHT // 2 + button_size[1] + 100,
                             button_size, 'exit', exit_image, exit_image_hover)
    buttons += [play_button, shop_button, exit_button]


def init():
    """
    Loads all data necessary to display menu.
    """
    global screen
    screen = pygame.Surface(settings.SIZE)

    load_images()
    create_interface_elements()


def create_screen():
    """
    Defines the appearance and event processing of the game when player is in the menu (settings.flag == 'menu').
    :return: pygame.surface with the size of screen
    """
    # Displaying images
    screen.blit(settings.menu_background, (0, 0))
    screen.blit(images['name'], (0, 0))
    screen.blit(images['plate'], (settings.WIDTH // 2 - 250, settings.HEIGHT // 2 - 150))

    # Drawing buttons
    for b in buttons:
        b.draw()

    # Processing events
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            for b in buttons:
                b.act(event)
        if event.type == pygame.MOUSEMOTION:
            for b in buttons:
                b.hover_test(event)

    # Returning the screen which will be displayed
    return screen

