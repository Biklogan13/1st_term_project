import pygame

import settings

buttons = []
screen, background = None, None

items_ships, items_upgrades, items_appearance = [], [], []
section, section_indicator = None, None
shop_plate, left_side, right_side, block = None, None, None, None

class Item:
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.button = settings.Button(self.x + self.width // 2, self.y + self.height // 2, 400, 100, 'is_pressed')
        self.image = image
        self.icon = None
        self.image_hover = None
        self.hover = False

    def move(self, y, move):
        global section, items_ships, items_upgrades, items_appearance
        if move:
            if section == 'ships':
                self.y += y
                self.button.y += y
            elif section == 'upgrades':
                self.y += y
                self.button.y += y
            elif section == 'appearance':
                self.y += y
                self.button.y += y

    def act(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def hover_test(self, event):
        if 0 <= event.pos[0] - self.x <= self.width and 0 <= event.pos[1] - self.y <= self.height:
            self.hover = True
        else:
            self.hover = False


def init():
    global buttons, screen, background, section, section_indicator, shop_plate, left_side, right_side, block
    section = 'ships'
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

    block = pygame.Surface((settings.WIDTH - 480, 300))
    block.set_colorkey((0, 0, 0))
    block.blit(left_side, (0, 0))
    block.blit(shop_plate, (50, 0))
    block.blit(right_side, (settings.WIDTH - 530, 0))

    for i in range(20):
        items_ships.append(Item(440, i * 340 + 40, settings.WIDTH - 480, 300, block))


def create_screen():
    global buttons, screen, items_ships, items_upgrades, items_appearance, section, section_indicator
    screen.blit(background, (0, 0))

    # Events
    y = 0

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if section == 'ships':
                for i in items_ships:
                    i.act()
            elif section == 'upgrades':
                for i in items_upgrades:
                    i.act()
            elif section == 'appearance':
                for i in items_appearance:
                    i.act()
            if event.button == 4:
                y = 20
            elif event.button == 5:
                y = -20

    # Drawing left-sided menu
    screen.blit(section_indicator, (0, int(settings.HEIGHT/2 - 540)))

    # Drawing and moving blocks
    if (y > 0 and items_ships[0].y < 40) or (y < 0 and items_ships[len(items_ships) - 1].y > settings.HEIGHT - items_ships[len(items_ships) - 1].height + 40):
        move = True
    else:
        move = False
    if section == 'ships':
        for i in items_ships:
            i.move(y, move)
            i.draw(screen)
    elif section == 'upgrades':
        for i in items_upgrades:
            i.move(y, move)
            i.draw(screen)
    elif section == 'appearance':
        for i in items_appearance:
            i.move(y, move)
            i.draw(screen)

    # Exiting to menu
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        settings.flag = 'menu'

    return screen

