import pygame
import os
import settings

# Colors
WHITE = (255, 255, 255)
DARK_GREEN = (9, 44, 50)

# Fonts
font_path = os.path.join('.', 'interface_elements', 'Montserrat-Bold.ttf')

# Creating global variables (variables needed for more than 1 frame but only in shop module)
buttons, items_ships, items_upgrades, items_cosmetics = [], [], [], []
buy_button_selected, buy_button_select, buy_button_select_hover, \
    buy_button_buy_enough_money, buy_button_buy_enough_money_hover,\
    buy_button_buy_not_enough_money = None, None, None, None, None, None
section_indicator = 'ships'
current_items = None
screen = None
font = None

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

buy_button_selected_path = os.path.join('.', 'interface_elements', 'buy_button_selected.png')
buy_button_select_path = os.path.join('.', 'interface_elements', 'buy_button_select.png')
buy_button_select_hover_path = os.path.join('.', 'interface_elements', 'buy_button_select_hover.png')
buy_button_buy_enough_money_path = os.path.join('.', 'interface_elements', 'buy_button_buy_enough_money.png')
buy_button_buy_enough_money_hover_path = os.path.join('.', 'interface_elements', 'buy_button_buy_enough_money_hover.png')
buy_button_buy_not_enough_money_path = os.path.join('.', 'interface_elements', 'buy_button_buy_not_enough_money.png')


class Item:
    def __init__(self, x, y, width, height, image, cost, purchase):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.button = ShopButton(self.x + self.width // 2, self.y + self.height // 2, 400, 100, purchase)
        self.image = image
        self.cost = cost

    def move(self, y, move):
        if move:
            self.y += y
            self.button.y += y

    def draw(self):
        # Plate
        screen.blit(left_side, (self.x, self.y))
        screen.blit(shop_plate, (self.x + 50, self.y))
        screen.blit(right_side, (self.x + settings.WIDTH - 530, self.y))
        # Button
        self.button.draw()
        # Cost
        screen.blit(font.render(str(self.cost), True, WHITE), (self.x + 300, self.y))
        # Picture
        # Description


class ShopButton(settings.Button):
    def __init__(self, x, y, width, height, purchase):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.cost = 100
        self.bought = False
        self.hover = False
        self.selected = False
        self.enough_money = False
        self.purchase = purchase

    def act(self, event):
        if event.button == 1 and 0 <= event.pos[0] - self.x <= self.width and 0 <= event.pos[1] - self.y <= self.height:
            if self.bought:
                for i in current_items:
                    i.button.selected = False
                self.selected = True
                if settings.shop_section == 'ships':
                    settings.current_skin = self.purchase
            elif self.cost <= settings.money:
                self.bought = True
                settings.money -= self.cost

    def draw(self):
        if self.selected:
            screen.blit(buy_button_selected, (self.x, self.y))
        elif self.bought:
            if self.hover:
                screen.blit(buy_button_select_hover, (self.x, self.y))
            else:
                screen.blit(buy_button_select, (self.x, self.y))
        else:
            if self.enough_money:
                if self.hover:
                    screen.blit(buy_button_buy_enough_money_hover, (self.x, self.y))
                else:
                    screen.blit(buy_button_buy_enough_money, (self.x, self.y))
            else:
                screen.blit(buy_button_buy_not_enough_money, (self.x, self.y))


def init():
    global buttons, screen, background, section_indicator, shop_plate, left_side, right_side, buy_button_selected,\
        buy_button_select, buy_button_select_hover, buy_button_buy_enough_money, buy_button_buy_enough_money_hover,\
        buy_button_buy_not_enough_money, font
    settings.shop_section = 'ships'

    # Font
    font = pygame.font.Font(font_path, 55)

    # Creating screen and transforming images
    screen = pygame.Surface(settings.SIZE)
    background = pygame.transform.scale(background, settings.SIZE)
    left_side = pygame.transform.scale(left_side, (50, 300))
    shop_plate = pygame.transform.scale(shop_plate, (settings.WIDTH - 580, 300))
    right_side = pygame.transform.scale(right_side, (50, 300))
    section_indicator = pygame.transform.scale(section_indicator, (400, 1080))

    # Creating Items
    items_ships.append(Item(440, 40, settings.WIDTH - 480, 300, settings.skins[0].image, 0, settings.skins[0]))
    items_ships.append(Item(440, 380, settings.WIDTH - 480, 300, settings.skins[1].image, 0, settings.skins[1]))

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

    buy_button_selected = pygame.image.load(buy_button_selected_path).convert_alpha()
    buy_button_select = pygame.image.load(buy_button_select_path).convert_alpha()
    buy_button_select_hover = pygame.image.load(buy_button_select_hover_path).convert_alpha()
    buy_button_buy_enough_money = pygame.image.load(buy_button_buy_enough_money_path).convert_alpha()
    buy_button_buy_enough_money_hover = pygame.image.load(buy_button_buy_enough_money_hover_path).convert_alpha()
    buy_button_buy_not_enough_money = pygame.image.load(buy_button_buy_not_enough_money_path).convert_alpha()

    button_size = (400, 100)

    buy_button_selected, buy_button_select, buy_button_select_hover, \
    buy_button_buy_enough_money, buy_button_buy_enough_money_hover, buy_button_buy_not_enough_money = [
        pygame.transform.scale(image, button_size) for image in
        (buy_button_selected, buy_button_select, buy_button_select_hover, \
         buy_button_buy_enough_money, buy_button_buy_enough_money_hover, buy_button_buy_not_enough_money)]


def create_screen():
    global buttons, screen, items_ships, items_upgrades, items_cosmetics, section_indicator, current_items
    screen.blit(background, (0, 0))

    # Selection of section
    if settings.shop_section == 'ships':
        current_items = items_ships
    elif settings.shop_section == 'upgrades':
        current_items = items_upgrades
    elif settings.shop_section == 'cosmetics':
        current_items = items_cosmetics

    # Money analysis
    for i in current_items:
        if i.button.cost <= settings.money:
            i.button.enough_money = True
        else:
            i.button.enough_money = False

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

