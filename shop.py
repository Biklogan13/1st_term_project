import pygame
import os
import settings

# Creating global variables (variables needed for more than 1 frame but only in shop module)
buttons, items_ships, items_upgrades, items_cosmetics = [], [], [], []
section_indicator = 'ships'
screen = None

# Loading images
background_path = os.path.join('.', 'backgrounds', 'shop_background.jpg')
background = pygame.image.load(background_path)

section_indicator_path = os.path.join('.', 'interface_elements', 'section_indicator.png')
section_indicator = pygame.image.load(section_indicator_path)

shop_plate_path = os.path.join('.', 'interface_elements', 'shop_plate.png')
shop_plate = pygame.image.load(shop_plate_path)
left_side_path = os.path.join('.', 'interface_elements', 'left_side.png')
left_side = pygame.image.load(left_side_path)
right_side_path = os.path.join('.', 'interface_elements', 'right_side.png')
right_side = pygame.image.load(right_side_path)

ships_button_image_path = os.path.join('.', 'interface_elements', 'ships_button.png')
upgrades_button_image_path = os.path.join('.', 'interface_elements', 'upgrades_button.png')
cosmetics_button_image_path = os.path.join('.', 'interface_elements', 'cosmetics_button.png')

ships_button_image_hover_path = os.path.join('.', 'interface_elements', 'ships_button_hover.png')
upgrades_button_image_hover_path = os.path.join('.', 'interface_elements', 'upgrades_button_hover.png')
cosmetics_button_image_hover_path = os.path.join('.', 'interface_elements', 'cosmetics_button_hover.png')

ships_button_image_pressed_path = os.path.join('.', 'interface_elements', 'ships_button_pressed.png')
upgrades_button_image_pressed_path = os.path.join('.', 'interface_elements', 'upgrades_button_pressed.png')
cosmetics_button_image_pressed_path = os.path.join('.', 'interface_elements', 'cosmetics_button_pressed.png')


class Item:
    def __init__(self, x, y, width, height, image, cost, purchase):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.button = settings.Button(self.x + self.width // 2, self.y + self.height // 2, 400, 100, 'is_pressed')
        self.image = image
        self.cost = cost
        self.purchase = purchase

    def move(self, y, move):
        if move:
            self.y += y
            self.button.y += y

    def draw(self):
        screen.blit(left_side, (self.x, self.y))
        screen.blit(shop_plate, (self.x + 50, self.y))
        screen.blit(right_side, (self.x + settings.WIDTH - 530, self.y))
        self.button.draw(screen)


class ShopButton(settings.Button):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bought = False
        self.hover = False
        self.selected = False
        self.enough_money = False
        self.image_buy_enough_money = None
        self.image_buy_enough_money_hover = None
        self.image_buy_not_enough_money = None
        self.image_select = None
        self.image_select_hover = None
        self.image_selected = None

    def act(self, event):
        if event.button == 1 and 0 <= event.pos[0] - self.x <= self.width and 0 <= event.pos[1] - self.y <= self.height:
            if self.button.bought:
                self.button.selected = True
            elif self.cost <= settings.money:
                self.button.bought = True
                settings.money -= self.cost

    def draw(self):
        if self.selected:
            #screen.blit(self.image_selected, (self.x, self.y))
        elif self.bought:
            if self.hover:
                #screen.blit(self.image_select_hover, (self.x, self.y))
            else:
                #screen.blit(self.image_select, (self.x, self.y))
        else:
            if self.enough_money:
                if self.hover:
                    #screen.blit(self.image_buy_enough_money_hover, (self.x, self.y))
                else:
                    #screen.blit(self.image_buy_enough_money, (self.x, self.y))
            else:
                #screen.blit(self.image_buy_not_enough_money, (self.x, self.y))


def init():
    global buttons, screen, background, section_indicator, shop_plate, left_side, right_side
    settings.shop_section = 'ships'

    # Creating screen and transforming images
    screen = pygame.Surface(settings.SIZE)
    background = pygame.transform.scale(background, settings.SIZE)
    left_side = pygame.transform.scale(left_side, (50, 300))
    shop_plate = pygame.transform.scale(shop_plate, (settings.WIDTH - 580, 300))
    right_side = pygame.transform.scale(right_side, (50, 300))
    section_indicator = pygame.transform.scale(section_indicator, (400, 1080))

    # Creating Items
    items_ships.append(Item(440, 40, settings.WIDTH - 480, 300, settings.skins[0].image, 0, settings.skins[0]))

    # Creating Buttons
    ships_button = settings.Button(50, settings.HEIGHT // 2 - 145, 300, 75, 'switch_to_ships')
    upgrades_button = settings.Button(50, settings.HEIGHT // 2 - 270, 300, 75, 'switch_to_upgrades')
    cosmetics_button = settings.Button(50, settings.HEIGHT // 2 - 395, 300, 75, 'switch_to_cosmetics')

    button_size = (300, 75)

    ships_button.image = pygame.image.load(ships_button_image_path).convert_alpha()
    upgrades_button.image = pygame.image.load(upgrades_button_image_path).convert_alpha()
    cosmetics_button.image = pygame.image.load(cosmetics_button_image_path).convert_alpha()

    ships_button.image_hover = pygame.image.load(ships_button_image_hover_path).convert_alpha()
    upgrades_button.image_hover = pygame.image.load(upgrades_button_image_hover_path).convert_alpha()
    cosmetics_button.image_hover = pygame.image.load(cosmetics_button_image_hover_path).convert_alpha()

    ships_button.image_pressed = pygame.image.load(ships_button_image_pressed_path).convert_alpha()
    upgrades_button.image_pressed = pygame.image.load(upgrades_button_image_pressed_path).convert_alpha()
    cosmetics_button.image_pressed = pygame.image.load(cosmetics_button_image_pressed_path).convert_alpha()

    ships_button.image, upgrades_button.image, cosmetics_button.image,\
    ships_button.image_hover, upgrades_button.image_hover, cosmetics_button.image_hover,\
    ships_button.image_pressed, upgrades_button.image_pressed, cosmetics_button.image_pressed = [
        pygame.transform.scale(image, button_size) for image in
        (ships_button.image, upgrades_button.image, cosmetics_button.image,
         ships_button.image_hover, upgrades_button.image_hover, cosmetics_button.image_hover,
         ships_button.image_pressed, upgrades_button.image_pressed, cosmetics_button.image_pressed)]

    ships_button.pressed = True
    buttons += [cosmetics_button, upgrades_button, ships_button]


def create_screen():
    global buttons, screen, items_ships, items_upgrades, items_cosmetics, section_indicator
    screen.blit(background, (0, 0))

    # Selection of section
    if settings.shop_section == 'ships':
        current_items = items_ships
    elif settings.shop_section == 'upgrades':
        current_items = items_upgrades
    elif settings.shop_section == 'cosmetics':
        current_items = items_cosmetics

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
        if b.action == 'switch_to_'+settings.shop_section:
            b.pressed = True
        else:
            b.pressed = False

    for b in buttons:
        b.draw(screen)

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in current_items:
                i.button.act(event)
            if event.button == 4:
                dy = 40
            elif event.button == 5:
                dy = -40
        if event.type == pygame.MOUSEMOTION:
            for i in current_items:
                i.button.hover_test(event)

    # Drawing and moving blocks
    if (dy > 0 and items_ships[0].y < 40) or (dy < 0 and items_ships[len(items_ships) - 1].y > settings.HEIGHT - items_ships[len(items_ships) - 1].height + 40):
        move = True
    else:
        move = False

    for i in current_items:
        i.move(dy, move)
        i.draw()

    # Exiting to menu
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        settings.flag = 'menu'

    return screen

