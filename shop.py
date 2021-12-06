import pygame

import settings

buttons = []
screen, background = None, None

items_ships, items_upgrades, items_cosmetics = [], [], []
section_indicator = None
shop_plate, left_side, right_side, block = None, None, None, None


class Item:
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.button = settings.Button(self.x + self.width // 2, self.y + self.height // 2, 400, 100, 'is_pressed')
        self.image = image
        self.image_hover = None
        self.hover = False

    def move(self, y, move):
        if move:
            self.y += y
            self.button.y += y

    def act(self, event):
        pass

    def draw(self, screen):
        screen.blit(left_side, (self.x, self.y))
        screen.blit(shop_plate, (self.x + 50, self.y))
        screen.blit(right_side, (self.x + settings.WIDTH - 530, self.y))
        #screen.blit(self.image, (self.x, self.y))

    def hover_test(self, event):
        if 0 <= event.pos[0] - self.x <= self.width and 0 <= event.pos[1] - self.y <= self.height:
            self.hover = True
        else:
            self.hover = False


def init():
    global buttons, screen, background, section_indicator, shop_plate, left_side, right_side, block
    settings.shop_section = 'ships'

    # Menus
    screen = pygame.Surface(settings.SIZE)
    background = pygame.image.load('backgrounds/shop_background.jpg').convert()
    section_indicator = pygame.image.load('menu_images/section_indicator.png').convert_alpha()
    shop_plate = pygame.image.load('menu_images/shop_plate.png').convert_alpha()
    left_side = pygame.image.load('menu_images/left_side.png').convert_alpha()
    right_side = pygame.image.load('menu_images/right_side.png').convert_alpha()
    background = pygame.transform.scale(background, settings.SIZE)
    shop_plate = pygame.transform.scale(shop_plate, (settings.WIDTH - 580, 300))
    left_side = pygame.transform.scale(left_side, (50, 300))
    right_side = pygame.transform.scale(right_side, (50, 300))
    section_indicator = pygame.transform.scale(section_indicator, (400, 1080))

    # Blocks
    for i in range(20):
        items_ships.append(Item(440, i * 340 + 40, settings.WIDTH - 480, 300, None))

    # Buttons
    cosmetics_button = settings.Button(50, settings.HEIGHT // 2 - 145, 300, 75, 'switch_to_ships')
    upgrades_button = settings.Button(50, settings.HEIGHT // 2 - 270, 300, 75, 'switch_to_upgrades')
    ships_button = settings.Button(50, settings.HEIGHT // 2 - 395, 300, 75, 'switch_to_cosmetics')

    ships_button.image = pygame.image.load('menu_images/ships_button.png').convert_alpha()
    upgrades_button.image = pygame.image.load('menu_images/upgrades_button.png').convert_alpha()
    cosmetics_button.image = pygame.image.load('menu_images/cosmetics_button.png').convert_alpha()

    ships_button.image = pygame.transform.scale((300, 100))
    upgrades_button.image = pygame.transform.scale((300, 100))
    cosmetics_button.image = pygame.transform.scale((300, 100))

    ships_button.image_hover = pygame.image.load('menu_images/ships_button_hover.png').convert_alpha()
    upgrades_button.image_hover = pygame.image.load('menu_images/upgrades_button_hover.png').convert_alpha()
    cosmetics_button.image_hover = pygame.image.load('menu_images/cosmetics_button_hover.png').convert_alpha()

    ships_button.image_hover = pygame.transform.scale((300, 100))
    upgrades_button.image_hover = pygame.transform.scale((300, 100))
    cosmetics_button.image_hover = pygame.transform.scale((300, 100))

    ships_button.image_pressed = pygame.image.load('menu_images/ships_button_pressed.png').convert_alpha()
    upgrades_button.image_pressed = pygame.image.load('menu_images/upgrades_button_pressed.png').convert_alpha()
    cosmetics_button.image_pressed = pygame.image.load('menu_images/cosmetics_button_pressed.png').convert_alpha()

    ships_button.image_pressed = pygame.transform.scale((300, 100))
    upgrades_button.image_pressed = pygame.transform.scale((300, 100))
    cosmetics_button.image_pressed = pygame.transform.scale((300, 100))

    ships_button.pressed = True

    buttons += [cosmetics_button, upgrades_button, ships_button]


def create_screen():
    global buttons, screen, items_ships, items_upgrades, items_cosmetics, section_indicator
    screen.blit(background, (0, 0))

    # Events
    dy = 0
    events = pygame.event.get()

    # Drawing left-sided menu
    screen.blit(section_indicator, (0, int(settings.HEIGHT/2 - 540)))
    screen.blit(settings.current_skin.image, (50, int(settings.HEIGHT/2 + 225)))

    # Buttons in left-sided menu and blocks
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            for b in buttons:
                b.act(event)
        elif event.type == pygame.MOUSEMOTION:
            for b in buttons:
                b.hover_test(event)

    for b in buttons:
        b.draw(screen)

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if settings.shop_section == 'ships':
                for i in items_ships:
                    i.act(event)
            elif settings.shop_section == 'upgrades':
                for i in items_upgrades:
                    i.act(event)
            elif settings.shop_section == 'appearance':
                for i in items_cosmetics:
                    i.act(event)
            if event.button == 4:
                dy = 20
            elif event.button == 5:
                dy = -20

    # Drawing and moving blocks
    if (dy > 0 and items_ships[0].y < 40) or (dy < 0 and items_ships[len(items_ships) - 1].y > settings.HEIGHT - items_ships[len(items_ships) - 1].height + 40):
        move = True
    else:
        move = False

    if settings.shop_section == 'ships':
        for i in items_ships:
            i.move(dy, move)
            i.draw(screen)
    elif settings.shop_section == 'upgrades':
        for i in items_upgrades:
            i.move(dy, move)
            i.draw(screen)
    elif settings.shop_section == 'appearance':
        for i in items_cosmetics:
            i.move(dy, move)
            i.draw(screen)

    # Exiting to menu
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        settings.flag = 'menu'

    return screen

