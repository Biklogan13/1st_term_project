import pygame
import os
import math

import settings


# ---------------- Global variables of shop section ----------------


# Surface on which shop elements will be drown
screen = None

# Shop background
background = None

# Colors
WHITE = (255, 255, 255)
DARK_GREEN = (1, 31, 38)

# Fonts
font, font_small = None, None

# Indicator os shop section
shop_section = 'ships'

# Array which contains shop menu buttons
buttons = []

# Items for purchasing
items_ships, items_upgrades, items_cosmetics = [], [], []

# Buttons elements
buy_button_elements = dict.fromkeys(['select', 'selected', 'select_hover', 'buy_enough_money',
                                     'buy_enough_money_hover', 'buy_not_enough_money'])
upgrade_button_elements = dict.fromkeys(['enough_money', 'not_enough_money', 'hover'])

# Arrays which contains all images which will be displayed directly on screen
left_block = dict.fromkeys(['menu_plate', 'plate'])
weapon_icons = dict.fromkeys(['gun', 'plasma', 'laser'])
item_plate = dict.fromkeys(['left_side', 'right_side', 'plate', 'price_tag'])


# ---------------------- Secondary functions ----------------------


def var_text(arr, plus):
    """
    Transforms array into string with integers responding to variables replaced with variables value.
    When variable is placed in array 2-nd time, replaces int with variables value + plus variable
    :param arr: array which contains integers and strings
    :param plus: value which added to variable if is=t shows up second time
    :return:
    """
    ret = ''
    multiplier = 0
    for i in range(len(arr)):
        if type(arr[i]) is int:
            if plus > 0:
                ret += str(int(delegate(arr[i], 'return')) + multiplier * plus)
            else:
                ret += str(round((60 / (int(delegate(arr[i], 'return')) + multiplier * plus)), 2))
            multiplier = 1
        else:
            ret += arr[i]
    return ret


def delegate(marker, value):
    """
    Function which allows shop objects to interact with settings variables.
    :param marker: value which shows which variable to modify
    :param value: value which is added to variable from settings
    :return: str of a variable from settings
    """
    if value == 'return':
        if marker == 0:
            return str(settings.bullet_damage)
        elif marker == 1:
            return str(settings.bullets_firerate)
        elif marker == 2:
            return str(settings.plasma_ball_damage)
        elif marker == 3:
            return str(settings.plasma_balls_firerate)
        elif marker == 4:
            return str(settings.laser_damage)
        else:
            print('ERROR, invalid marker')
    else:
        if marker == 0:
            settings.bullet_damage += value
        elif marker == 1:
            settings.bullets_firerate += value
        elif marker == 2:
            settings.plasma_ball_damage += value
        elif marker == 3:
            settings.plasma_balls_firerate += value
        elif marker == 4:
            settings.laser_damage += value


# ---------------------------- Classes ----------------------------


class ShopMenuButton(settings.Button):
    def __init__(self, x, y, size, action, image, image_hover, image_pressed):
        """
        Initializes button specified for left block of shop.
        :param x: x coordinate of the button
        :param y: y coordinate of the button
        :param size: (width, height) tuple which defines size of the button
        :param action: 1 of 3 actions: 'switch_to_ships', 'switch_to_upgrades', 'switch_to_cosmetics'
        :param image: image of the button when mouse is not hovering over it and it's not selected
        :param image_hover: image of the button when mouse is hovering over it and it's not selected
        :param image_pressed: image of the button when it's selected
        """
        self.x = x
        self.y = y
        self.width = size[0]
        self.height = size[1]
        self.action = action
        self.hover = False
        self.pressed = False
        self.image = image
        self.image_hover = image_hover
        self.image_pressed = image_pressed

    def draw(self):
        """
        Draws button on a current section screen, taking into account current button state.
        """
        if self.image is None:
            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
        elif self.pressed:
            screen.blit(self.image_pressed, (self.x, self.y))
        elif self.hover:
            screen.blit(self.image_hover, (self.x, self.y))
        else:
            screen.blit(self.image, (self.x, self.y))

    def act(self, event):
        """
        Detects if player pressed the button and acts based on its act parameter.
        :param event: pygame.MOUSEBUTTONDOWN event
        """
        global shop_section
        if event.button == 1 and 0 <= event.pos[0] - self.x <= self.width and 0 <= event.pos[1] - self.y <= self.height:
            if self.action == 'switch_to_ships':
                shop_section = 'ships'
            elif self.action == 'switch_to_upgrades':
                shop_section = 'upgrades'
            elif self.action == 'switch_to_cosmetics':
                shop_section = 'cosmetics'


class ShopBuyButton(settings.Button):
    def __init__(self, x, y, purchase, cost, section):
        """
        Initializes button specified for buying items in shop.
        :param x: x coordinate of the button
        :param y: y coordinate of the button
        :param purchase: object to buy with this button
        :param cost: cost of the item
        :param section: section in which item is placed
        """
        self.x = x
        self.y = y
        self.width = 400
        self.height = 100
        self.section = section
        self.cost = cost
        self.purchase = purchase
        self.bought = False
        self.hover = False
        self.selected = False
        self.enough_money = False

    def act(self, event):
        """
        Detects if player pressed the button and acts based on its act parameter.
        :param event: pygame.MOUSEBUTTONDOWN event
        """
        if self.check_mouse(event):
            if self.bought:
                if self.section == 'ships':
                    items = items_ships
                    settings.current_skin = self.purchase
                else:
                    items = items_cosmetics
                    settings.menu_background = self.purchase
                for i in items:
                    i.button.selected = False
                self.selected = True
            elif self.cost <= settings.money and not self.bought:
                self.bought = True
                settings.money -= self.cost

    def draw(self):
        """
        Draws button on a current section screen, taking into account current button state.
        """
        if self.selected:
            screen.blit(buy_button_elements['selected'], (self.x, self.y))
        elif self.bought:
            if self.hover:
                screen.blit(buy_button_elements['select_hover'], (self.x, self.y))
            else:
                screen.blit(buy_button_elements['select'], (self.x, self.y))
        else:
            if self.enough_money:
                if self.hover:
                    screen.blit(buy_button_elements['buy_enough_money_hover'], (self.x, self.y))
                else:
                    screen.blit(buy_button_elements['buy_enough_money'], (self.x, self.y))
            else:
                screen.blit(buy_button_elements['buy_not_enough_money'], (self.x, self.y))


class ShopUpgradeButton(settings.Button):
    def __init__(self, x, y, purchase, cost, upgrade):
        """
        Initializes button specified for upgrading items in shop.
        :param x: x coordinate of the button
        :param y: y coordinate of the button
        :param purchase: x coordinate of the button
        :param cost: cost of the item
        :param upgrade: value added to upgraded variable when button pressed
        """
        self.x = x
        self.y = y
        self.width = 100
        self.height = 100
        self.cost = cost
        self.maxed_out = False
        self.hover = False
        self.enough_money = False
        self.purchase = purchase
        self.upgrade = upgrade

    def act(self, event):
        """
        Detects if player pressed the button and acts based on its act parameter.
        :param event: pygame.MOUSEBUTTON event
        """
        if event.button == 1 and 0 <= event.pos[0] - self.x <= self.width and 0 <= event.pos[1] - self.y <= self.height:
            if self.cost <= settings.money and not self.maxed_out:
                settings.money -= self.cost
                delegate(self.purchase, self.upgrade)
                if int(delegate(self.purchase, 'return')) <= 1:
                    self.maxed_out = True
                self.cost = int(self.cost * 1.1)

    def draw(self):
        """
        Draws button on a current section screen, taking into account current button state.
        """
        if not self.maxed_out:
            if self.enough_money:
                if self.hover:
                    screen.blit(upgrade_button_elements['hover'], (self.x, self.y))
                else:
                    screen.blit(upgrade_button_elements['enough_money'], (self.x, self.y))
            else:
                screen.blit(upgrade_button_elements['not_enough_money'], (self.x, self.y))


class Item:
    def __init__(self, y, image, cost, purchase, name, capture):
        """
        Initialization of a block on which item is displayed.
        :param y: y coordinate of the block
        :param image: image which will be displayed on the block
        :param cost: cost of the item
        :param purchase: item which is displayed on the block for bying
        :param name: name of the item
        :param capture: caption of the item
        """
        self.x = 440
        self.y = y
        self.width = settings.WIDTH - 480
        self.height = 300
        self.button = ShopBuyButton(self.x + self.width - 500, self.y + self.height // 2, purchase, cost, 'ships')
        self.image = image
        self.phase = 0
        self.magnitude = 120
        self.name = name
        self.capture = capture

    def move(self, y, move):
        """
        Moves block based on the y parameter which corresponds to the rotation of the mouse wheel.
        :param y: value by which item is moved
        :param move: boolean value which shows blocks can move or not
        """
        if move:
            self.y += y
            self.button.y += y

    def draw_plate_and_button(self):
        """
        Draws plate on which all pictures and text is displayed.
        """
        screen.blit(item_plate['left_side'], (self.x, self.y))
        screen.blit(pygame.transform.scale(item_plate['plate'], (self.width - 100, self.height)), (self.x + 50, self.y))
        screen.blit(item_plate['right_side'], (self.x + self.width - 50, self.y))
        self.button.draw()


class ShipsItem(Item):
    def draw(self):
        """
        Draws a block with a ship, text and ShopBuyButton on it.
        """
        self.draw_plate_and_button()

        # Cost
        screen.blit(item_plate['price_tag'], (self.x + self.width - 500, self.y + 45))
        screen.blit(font.render(str(self.button.cost), True, DARK_GREEN), (self.x + self.width - 430, self.y + 45))

        # Text
        screen.blit(font_small.render(self.name, True, DARK_GREEN), (self.x + 100, self.y + 180))
        screen.blit(font_small.render(self.capture, True, DARK_GREEN), (self.x + 100, self.y + 220))

        # Image
        rot_image = pygame.transform.rotate(self.image,
                                            math.atan2(60, self.magnitude * math.cos(self.phase)) * 180 / math.pi - 90)
        w, h = rot_image.get_rect().size
        screen.blit(rot_image,
                    (self.x + 150 + self.magnitude + self.magnitude * math.sin(self.phase) - w // 2, self.y + 100 - h // 2))
        # Moving spaceship
        if self.button.hover or self.button.selected:
            self.phase += 0.02
            self.phase = self.phase % (2 * math.pi)


class UpgradesItem(Item):
    def __init__(self, x, y, cost, purchase, upgrade, name, capture):
        """
        Initialization of a block on which item is displayed.
        :param x: x coordinate of the block
        :param y: y coordinate of the block
        :param cost: cost of the item
        :param purchase: item for purchase
        :param upgrade: value by which purchase will be upgraded
        :param name: name of the item
        :param capture: capture of the item
        """
        self.x = x
        self.y = y
        self.width = (settings.WIDTH - 480) // 2 - 20
        self.height = 300
        self.button = ShopUpgradeButton(self.x + 100, self.y + 50, purchase, cost, upgrade)
        self.name = name
        self.capture = capture

    def draw(self):
        """
        Draws a block with text and ShopUpgradeButton on it.
        """
        self.draw_plate_and_button()

        if not self.button.maxed_out:
            # Cost
            screen.blit(item_plate['price_tag'], (self.x + 250, self.y + 45))
            screen.blit(font.render(str(self.button.cost), True, DARK_GREEN), (self.x + 320, self.y + 45))

            # Text
            screen.blit(font_small.render(self.name, True, DARK_GREEN), (self.x + 100, self.y + 180))
            screen.blit(font_small.render(var_text(self.capture, self.button.upgrade), True, DARK_GREEN),
                        (self.x + 100, self.y + 220))
        else:
            screen.blit(font.render('MAXED OUT', True, DARK_GREEN), (self.x + 100, self.y + 180))


class CosmeticsItem(Item):
    def __init__(self, y, image, cost, purchase, capture):
        """
        Initialization of a block on which item is displayed.
        :param y: y coordinate of the block
        :param image: image which will be displayed on the block
        :param cost: cost of the item
        :param purchase: item for purchase
        :param capture: capture of the item
        """
        self.x = 440
        self.y = y
        self.width = settings.WIDTH - 480
        self.height = 300
        self.button = ShopBuyButton(self.x + self.width - 500, self.y + self.height // 2, purchase, cost, 'cosmetics')
        self.image = image
        self.capture = capture

    def draw(self):
        """
        Draws a block with text, picture and ShopBuyButton on it.
        """
        self.draw_plate_and_button()

        # Cost
        screen.blit(item_plate['price_tag'], (self.x + self.width - 500, self.y + 45))
        screen.blit(font.render(str(self.button.cost), True, DARK_GREEN), (self.x + self.width - 430, self.y + 45))

        # Text
        screen.blit(font_small.render(self.capture, True, DARK_GREEN), (self.x + 100, self.y + 220))

        # Image
        sc_image = pygame.transform.scale(self.image, (int(150 / settings.HEIGHT * settings.WIDTH), 150))
        screen.blit(sc_image, (self.x + 100, self.y + 50))


# -------------------- Initialization functions --------------------


def load_images():
    """
    Loads all images which are going to be blit directly on screen.
    """
    global background

    # Shop background
    background_path = os.path.join('.', 'backgrounds', 'shop_background.jpg')
    background = pygame.image.load(background_path)
    background = pygame.transform.scale(background, settings.SIZE)

    # Section indicator
    menu_plate_path = os.path.join('.', 'interface_elements', 'section_indicator.png')
    menu_plate = pygame.image.load(menu_plate_path)
    left_block['menu_plate'] = pygame.transform.scale(menu_plate, (400, 1080))

    # Item plate
    shop_plate_path = os.path.join('.', 'interface_elements', 'shop_plate.png')
    item_plate['plate'] = pygame.image.load(shop_plate_path)

    left_side_path = os.path.join('.', 'interface_elements', 'left_side.png')
    left_side = pygame.image.load(left_side_path)
    item_plate['left_side'] = pygame.transform.scale(left_side, (50, 300))

    right_side_path = os.path.join('.', 'interface_elements', 'right_side.png')
    right_side = pygame.image.load(right_side_path)
    item_plate['right_side'] = pygame.transform.scale(right_side, (50, 300))

    price_tag_path = os.path.join('.', 'interface_elements', 'price_tag.png')
    item_plate['price_tag'] = pygame.image.load(price_tag_path)

    # Weapon icons
    gun_icon_150_path = os.path.join('.', 'interface_elements', 'gun_icon_150.png')
    weapon_icons['gun'] = pygame.image.load(gun_icon_150_path)
    plasma_icon_150_path = os.path.join('.', 'interface_elements', 'plasma_icon_150.png')
    weapon_icons['plasma'] = pygame.image.load(plasma_icon_150_path)
    laser_icon_150_path = os.path.join('.', 'interface_elements', 'laser_icon_150.png')
    weapon_icons['laser'] = pygame.image.load(laser_icon_150_path)

    gun_icon_50_path = os.path.join('.', 'interface_elements', 'gun_icon_50.png')
    weapon_icons['gun'] = pygame.image.load(gun_icon_50_path)
    plasma_icon_50_path = os.path.join('.', 'interface_elements', 'plasma_icon_50.png')
    weapon_icons['plasma'] = pygame.image.load(plasma_icon_50_path)
    laser_icon_50_path = os.path.join('.', 'interface_elements', 'laser_icon_50.png')
    weapon_icons['laser'] = pygame.image.load(laser_icon_50_path)


def load_fonts():
    """
    Loads all needed fonts.
    """
    global font, font_small

    font_path = os.path.join('.', 'interface_elements', 'Montserrat-Bold.ttf')
    font = pygame.font.Font(font_path, 55)
    font_small = pygame.font.Font(font_path, 30)


def load_buy_button_images():
    # Loading images for buttons
    button_size = (400, 100)

    buy_button_selected_path = os.path.join('.', 'interface_elements', 'buy_button_selected.png')
    buy_button_selected = pygame.image.load(buy_button_selected_path).convert_alpha()
    buy_button_elements['selected'] = pygame.transform.scale(buy_button_selected, button_size)

    buy_button_select_path = os.path.join('.', 'interface_elements', 'buy_button_select.png')
    buy_button_select = pygame.image.load(buy_button_select_path).convert_alpha()
    buy_button_elements['select'] = pygame.transform.scale(buy_button_select, button_size)

    buy_button_select_hover_path = os.path.join('.', 'interface_elements', 'buy_button_select_hover.png')
    buy_button_select_hover = pygame.image.load(buy_button_select_hover_path).convert_alpha()
    buy_button_elements['select_hover'] = pygame.transform.scale(buy_button_select_hover, button_size)

    buy_button_buy_enough_money_path = os.path.join('.', 'interface_elements', 'buy_button_buy_enough_money.png')
    buy_button_buy_enough_money = pygame.image.load(buy_button_buy_enough_money_path).convert_alpha()
    buy_button_elements['buy_enough_money'] = pygame.transform.scale(buy_button_buy_enough_money, button_size)

    buy_button_buy_enough_money_hover_path = os.path.join('.', 'interface_elements',
                                                          'buy_button_buy_enough_money_hover.png')
    buy_button_buy_enough_money_hover = pygame.image.load(buy_button_buy_enough_money_hover_path).convert_alpha()
    buy_button_elements['buy_enough_money_hover'] = pygame.transform.scale(buy_button_buy_enough_money_hover, button_size)

    buy_button_buy_not_enough_money_path = os.path.join('.', 'interface_elements',
                                                        'buy_button_buy_not_enough_money.png')
    buy_button_buy_not_enough_money = pygame.image.load(buy_button_buy_not_enough_money_path).convert_alpha()
    buy_button_elements['buy_not_enough_money'] = pygame.transform.scale(buy_button_buy_not_enough_money, button_size)


def load_upgrade_button_images():
    # Loading images for buttons
    upgrade_button_not_enough_money_path = os.path.join('.', 'interface_elements',
                                                        'upgrade_button_not_enough_money.png')
    upgrade_button_elements['not_enough_money'] = pygame.image.load(upgrade_button_not_enough_money_path)

    upgrade_button_enough_money_path = os.path.join('.', 'interface_elements', 'upgrade_button_enough_money.png')
    upgrade_button_elements['enough_money'] = pygame.image.load(upgrade_button_enough_money_path)

    upgrade_button_hover_path = os.path.join('.', 'interface_elements', 'upgrade_button_hover.png')
    upgrade_button_elements['hover'] = pygame.image.load(upgrade_button_hover_path)


def create_shop_menu_buttons():
    global buttons

    # Loading images for buttons
    ships_button_image_path = os.path.join('.', 'interface_elements', 'ships_button.png')
    upgrades_button_image_path = os.path.join('.', 'interface_elements', 'upgrades_button.png')
    cosmetics_button_image_path = os.path.join('.', 'interface_elements', 'cosmetics_button.png')
    ships_button_image = pygame.image.load(ships_button_image_path).convert_alpha()
    upgrades_button_image = pygame.image.load(upgrades_button_image_path).convert_alpha()
    cosmetics_button_image = pygame.image.load(cosmetics_button_image_path).convert_alpha()

    ships_button_image_hover_path = os.path.join('.', 'interface_elements', 'ships_button_hover.png')
    upgrades_button_image_hover_path = os.path.join('.', 'interface_elements', 'upgrades_button_hover.png')
    cosmetics_button_image_hover_path = os.path.join('.', 'interface_elements', 'cosmetics_button_hover.png')
    ships_button_image_hover = pygame.image.load(ships_button_image_hover_path).convert_alpha()
    upgrades_button_image_hover = pygame.image.load(upgrades_button_image_hover_path).convert_alpha()
    cosmetics_button_image_hover = pygame.image.load(cosmetics_button_image_hover_path).convert_alpha()

    ships_button_image_pressed_path = os.path.join('.', 'interface_elements', 'ships_button_pressed.png')
    upgrades_button_image_pressed_path = os.path.join('.', 'interface_elements', 'upgrades_button_pressed.png')
    cosmetics_button_image_pressed_path = os.path.join('.', 'interface_elements', 'cosmetics_button_pressed.png')
    ships_button_image_pressed = pygame.image.load(ships_button_image_pressed_path).convert_alpha()
    upgrades_button_image_pressed = pygame.image.load(upgrades_button_image_pressed_path).convert_alpha()
    cosmetics_button_image_pressed = pygame.image.load(cosmetics_button_image_pressed_path).convert_alpha()

    # Resizing images
    button_size = (300, 75)
    [ships_button_image, upgrades_button_image, cosmetics_button_image,
     ships_button_image_hover, upgrades_button_image_hover, cosmetics_button_image_hover,
     ships_button_image_pressed, upgrades_button_image_pressed, cosmetics_button_image_pressed] =\
        [pygame.transform.scale(image, button_size) for image in
         [ships_button_image, upgrades_button_image, cosmetics_button_image,
          ships_button_image_hover, upgrades_button_image_hover, cosmetics_button_image_hover,
          ships_button_image_pressed, upgrades_button_image_pressed, cosmetics_button_image_pressed]]

    # Creating button objects
    ships_button = ShopMenuButton(50, settings.HEIGHT // 2 - 145, button_size, 'switch_to_ships',
                                  ships_button_image, ships_button_image_hover, ships_button_image_pressed)
    upgrades_button = ShopMenuButton(50, settings.HEIGHT // 2 - 270, button_size, 'switch_to_upgrades',
                                     upgrades_button_image, upgrades_button_image_hover, upgrades_button_image_pressed)
    cosmetics_button = ShopMenuButton(50, settings.HEIGHT // 2 - 395, button_size, 'switch_to_cosmetics',
                                      cosmetics_button_image, cosmetics_button_image_hover,
                                      cosmetics_button_image_pressed)
    ships_button.pressed = True
    buttons += [cosmetics_button, upgrades_button, ships_button]


def create_ships_items():
    # Creating ItemsShips objects
    items_ships.append(ShipsItem(40, settings.skins[1].image, 2000, settings.skins[1],
                                 'Standard spaceship', 'Super is light ring'))

    items_ships.append(ShipsItem(380, settings.skins[0].image, 2000, settings.skins[0],
                                 'Zuckerberg machine', 'Super is teleportation'))


def create_upgrades_items():
    # Creating ItemsUpgrades objects
    items_upgrades.append(UpgradesItem(440, 40, 100, 0, 1, 'Increase gun DMG', ['from ', 0, ' to ', 0]))

    items_upgrades.append(UpgradesItem(440 + (settings.WIDTH - 480) // 2 + 20, 40, 1000, 1, -1,
                                       'Increase gun FR', ['from ', 1, ' to ', 1]))

    items_upgrades.append(UpgradesItem(440, 380, 20, 2, 1, 'Increase plasma DMG', ['from ', 2, ' to ', 2]))

    items_upgrades.append(UpgradesItem(440 + (settings.WIDTH - 480) // 2 + 20, 380, 100, 3, -1,
                                       'Increase plasma FR', ['from ', 3, ' to ', 3]))

    items_upgrades.append(UpgradesItem(440, 720, 1000, 4, 1, 'Increase laser DMG', ['from ', 4, ' to ', 4]))


def create_cosmetics_items():
    # Loading backgrounds for purchasing
    menu_background_1_path = os.path.join('.', 'backgrounds', 'menu_background_1.png')
    menu_background_1 = pygame.image.load(menu_background_1_path)

    menu_background_2_path = os.path.join('.', 'backgrounds', 'menu_background_2.jpg')
    menu_background_2 = pygame.image.load(menu_background_2_path)

    menu_background_3_path = os.path.join('.', 'backgrounds', 'menu_background_3.png')
    menu_background_3 = pygame.image.load(menu_background_3_path)

    menu_background_4_path = os.path.join('.', 'backgrounds', 'menu_background_4.png')
    menu_background_4 = pygame.image.load(menu_background_4_path)

    menu_background_5_path = os.path.join('.', 'backgrounds', 'menu_background_5.png')
    menu_background_5 = pygame.image.load(menu_background_5_path)

    menu_background_6_path = os.path.join('.', 'backgrounds', 'menu_background_6.png')
    menu_background_6 = pygame.image.load(menu_background_6_path)

    # Resizing images
    [menu_background_1, menu_background_2, menu_background_3,
     menu_background_4, menu_background_5, menu_background_6] =\
        [pygame.transform.scale(image, settings.SIZE) for image in
         [menu_background_1, menu_background_2, menu_background_3,
          menu_background_4, menu_background_5, menu_background_6]]

    # Creating CosmeticItems for backgrounds
    items_cosmetics.append(CosmeticsItem(40, menu_background_1, 200, menu_background_1, 'Standard background'))

    items_cosmetics.append(CosmeticsItem(40 + 340, menu_background_2, 200, menu_background_2, 'Green nebula'))

    items_cosmetics.append(CosmeticsItem(40 + 340 * 2, menu_background_3, 200, menu_background_3, 'Planet'))

    items_cosmetics.append(CosmeticsItem(40 + 340 * 3, menu_background_4, 200, menu_background_4, 'Purple nebula'))

    items_cosmetics.append(CosmeticsItem(40 + 340 * 4, menu_background_5, 200, menu_background_5, 'Planet and rockets'))

    items_cosmetics.append(CosmeticsItem(40 + 340 * 5, menu_background_6, 200, menu_background_6, 'Landscape'))


def init():
    global screen
    screen = pygame.Surface(settings.SIZE)

    # Loading data
    load_images()
    load_fonts()
    load_buy_button_images()
    load_upgrade_button_images()

    # Creating objects
    create_shop_menu_buttons()
    create_ships_items()
    create_upgrades_items()
    create_cosmetics_items()


# ----------------- functions which create screen -----------------


def create_screen():
    global screen, shop_section
    screen.blit(background, (0, 0))

    # Events
    dy = 0
    events = pygame.event.get()

    # Buttons in left-sided menu and blocks
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            for b in buttons:
                b.act(event)
        elif event.type == pygame.MOUSEMOTION:
            for b in buttons:
                b.hover_test(event)

    # Selection of section
    if shop_section == 'ships':
        current_items = items_ships
    elif shop_section == 'upgrades':
        current_items = items_upgrades
    elif shop_section == 'cosmetics':
        current_items = items_cosmetics

    # Money analysis
    for i in current_items:
        if i.button.cost <= settings.money:
            i.button.enough_money = True
        else:
            i.button.enough_money = False

    # Drawing left-sided menu
    screen.blit(left_block['menu_plate'], (0, int(settings.HEIGHT/2 - 540)))
    screen.blit(font.render(str(settings.money), True, DARK_GREEN), (200, int(settings.HEIGHT / 2) + 50 + 45 // 2))
    # Gun stats
    screen.blit(weapon_icons['gun'], (50, int(settings.HEIGHT / 2 + 175)))
    screen.blit(font_small.render('DMG: ' + str(settings.bullet_damage) + ' FR: ' +
                                  str(round(60 / settings.bullets_firerate, 2)),
                                  True, DARK_GREEN), (120, int(settings.HEIGHT / 2) + 185))
    # Plasma stats
    screen.blit(weapon_icons['plasma'], (50, int(settings.HEIGHT / 2 + 245)))
    screen.blit(font_small.render('DMG: ' + str(settings.plasma_ball_damage) + ' FR: ' +
                                  str(round(60 / settings.plasma_balls_firerate, 2)),
                                  True, DARK_GREEN), (120, int(settings.HEIGHT / 2) + 255))
    # Laser stats
    screen.blit(weapon_icons['laser'], (50, int(settings.HEIGHT / 2 + 315)))
    screen.blit(font_small.render('TIC DMG: ' + str(settings.laser_damage),
                                  True, DARK_GREEN), (120, int(settings.HEIGHT / 2) + 325))

    for b in buttons:
        if b.action == 'switch_to_' + shop_section:
            b.pressed = True
        else:
            b.pressed = False

    for b in buttons:
        b.draw()

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
    if (dy > 0 and current_items[0].y < 40) or (dy < 0 and current_items[len(current_items) - 1].y >
                                                settings.HEIGHT - current_items[len(current_items) - 1].height - 40):
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

