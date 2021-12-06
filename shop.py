import pygame

import settings

buttons = []
screen, background = None, None

items_ships, items_upgrades, items_appearance = [], [], []
section, section_indicator = None, None


class Item:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.button = settings.Button(self.x + self.width // 2, self.y + self.height // 2, 400, 100, 'is_pressed')
        self.image = None
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
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))

    def hover_test(self, event):
        if 0 <= event.pos[0] - self.x <= self.width and 0 <= event.pos[1] - self.y <= self.height:
            self.hover = True
        else:
            self.hover = False


def init():
    global buttons, screen, background, section, section_indicator
    section = 'ships'
    screen = pygame.Surface(settings.SIZE)
    background = pygame.image.load('backgrounds/shop_background.jpg').convert()
    section_indicator = pygame.image.load('menu_images/section_indicator.png').convert_alpha()
    #plate = pygame.im
    background = pygame.transform.scale(background, settings.SIZE)
    section_indicator = pygame.transform.scale(section_indicator, (400, 1080))

    for i in range(20):
        items_ships.append(Item(200, i * 100, 300, 50))


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
                y = 15
            elif event.button == 5:
                y = -15

    # Drawing left-sided menu
    screen.blit(section_indicator, (0, int(settings.HEIGHT/2 - 540)))

    # Drawing and moving blocks
    move = (y > 0 and items_ships[0].y <= 0) or (y < 0 and items_ships[len(items_ships) - 1].y >= settings.HEIGHT -
                                                 items_ships[len(items_ships) - 1].height)
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

