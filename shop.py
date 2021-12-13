import pygame
import os
import math

import settings

# Colors
WHITE = (255, 255, 255)
DARK_GREEN = (1, 31, 38)

# Fonts
font_path = os.path.join('.', 'interface_elements', 'Montserrat-Bold.ttf')

# Creating global variables (variables needed for more than 1 frame but only in shop module)
buttons, items_ships, items_upgrades, items_cosmetics = [], [], [], []
buy_button_selected, buy_button_select, buy_button_select_hover, \
    buy_button_buy_enough_money, buy_button_buy_enough_money_hover,\
    buy_button_buy_not_enough_money = None, None, None, None, None, None
section_indicator = 'ships'
magnitude = 120
current_items = None
screen = None
font, font_small = None, None

# Images paths
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
price_tag_path = os.path.join('.', 'interface_elements', 'price_tag.png')
price_tag = pygame.image.load(price_tag_path)

gun_icon_50_path = os.path.join('.', 'interface_elements', 'gun_icon_50.png')
gun_icon_50 = pygame.image.load(gun_icon_50_path)
plasma_icon_50_path = os.path.join('.', 'interface_elements', 'plasma_icon_50.png')
plasma_icon_50 = pygame.image.load(plasma_icon_50_path)
laser_icon_50_path = os.path.join('.', 'interface_elements', 'laser_icon_50.png')
laser_icon_50 = pygame.image.load(laser_icon_50_path)

gun_icon_150_path = os.path.join('.', 'interface_elements', 'gun_icon_150.png')
gun_icon_150 = pygame.image.load(gun_icon_150_path)
plasma_icon_150_path = os.path.join('.', 'interface_elements', 'plasma_icon_150.png')
plasma_icon_150 = pygame.image.load(plasma_icon_150_path)
laser_icon_150_path = os.path.join('.', 'interface_elements', 'laser_icon_150.png')
laser_icon_150 = pygame.image.load(laser_icon_150_path)

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

upgrade_button_not_enough_money_path = os.path.join('.', 'interface_elements', 'upgrade_button_not_enough_money.png')
upgrade_button_not_enough_money = pygame.image.load(upgrade_button_not_enough_money_path)
upgrade_button_enough_money_path = os.path.join('.', 'interface_elements', 'upgrade_button_enough_money.png')
upgrade_button_enough_money = pygame.image.load(upgrade_button_enough_money_path)
upgrade_button_hover_path = os.path.join('.', 'interface_elements', 'upgrade_button_hover.png')
upgrade_button_hover = pygame.image.load(upgrade_button_hover_path)


class Item:
    def __init__(self, x, y, width, height, image, cost, purchase, name, capture):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        if width == settings.WIDTH - 480:
            self.button = ShopButton(self.x + self.width - 500, self.y + self.height // 2, 400, 100, purchase, cost)
        else:
            self.button = ShopButton(self.x + 100, self.y + 50, 100, 100, purchase, cost)
        self.image = image
        self.phase = 0
        self.name = name
        self.capture = capture

    def move(self, y, move):
        if move:
            self.y += y
            self.button.y += y

    def draw(self):
        # Plate
        screen.blit(left_side, (self.x, self.y))
        screen.blit(pygame.transform.scale(shop_plate, (self.width - 100, self.height)), (self.x + 50, self.y))
        screen.blit(right_side, (self.x + self.width - 50, self.y))
        # Button
        self.button.draw()
        # Content
        if settings.shop_section == 'ships':
            # Cost
            screen.blit(price_tag, (self.x + self.width - 500, self.y + 45))
            screen.blit(font.render(str(self.button.cost), True, DARK_GREEN), (self.x + self.width - 430, self.y + 45))
            # Text
            screen.blit(font_small.render(self.name, True, DARK_GREEN), (self.x + 100, self.y + 180))
            screen.blit(font_small.render(self.capture, True, DARK_GREEN), (self.x + 100, self.y + 220))
            # Image
            rot_image = pygame.transform.rotate(self.image,
                                            math.atan2(60, magnitude * math.cos(self.phase)) * 180 / math.pi - 90)
            w, h = rot_image.get_rect().size
            screen.blit(rot_image,
                    (self.x + 150 + magnitude + magnitude * math.sin(self.phase) - w // 2, self.y + 100 - h // 2))
            if self.button.hover or self.button.selected:
                self.phase += 0.02
                self.phase = self.phase % (2 * math.pi)
        elif settings.shop_section == 'upgrades':
            # Cost
            screen.blit(price_tag, (self.x + 250, self.y + 45))
            screen.blit(font.render(str(self.button.cost), True, DARK_GREEN), (self.x + 320, self.y + 45))
            # Text
            screen.blit(font_small.render(self.name, True, DARK_GREEN), (self.x + 100, self.y + 180))
            screen.blit(font_small.render(var_text(self.capture, self.button.upgrade), True, DARK_GREEN), (self.x + 100, self.y + 220))


class ShopButton(settings.Button):
    def __init__(self, x, y, width, height, purchase, cost):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.cost = cost
        self.bought = False
        self.hover = False
        self.selected = False
        self.enough_money = False
        self.purchase = purchase
        self.upgrade = 0

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
                if settings.shop_section == 'upgrades':
                    delegate(self.purchase, self.upgrade)
                    self.bought = False
                    self.cost = int(self.cost*1.1)

    def draw(self):
        if settings.shop_section == 'upgrades':
            if self.enough_money:
                if self.hover:
                    screen.blit(upgrade_button_hover, (self.x, self.y))
                else:
                    screen.blit(upgrade_button_enough_money, (self.x, self.y))
            else:
                screen.blit(upgrade_button_not_enough_money, (self.x, self.y))
        else:
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


def var_text(arr, plus):
    ret = ''
    mult = 0
    for i in range(len(arr)):
        if type(arr[i]) is int:
            if plus > 0:
                ret += str(int(delegate(arr[i], 'return')) + mult * plus)
            else:
                ret += str(round((60 / (int(delegate(arr[i], 'return')) + mult * plus)), 2))
            mult = 1
        else:
            ret += arr[i]
    return ret


def delegate(marker, value):
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


def init():
    global buttons, screen, background, section_indicator, shop_plate, left_side, right_side, price_tag,\
        buy_button_selected, buy_button_select, buy_button_select_hover, buy_button_buy_enough_money,\
        buy_button_buy_enough_money_hover, buy_button_buy_not_enough_money, font, font_small

    settings.shop_section = 'ships'

    # Font
    font = pygame.font.Font(font_path, 55)
    font_small = pygame.font.Font(font_path, 30)

    # Creating screen and transforming images
    screen = pygame.Surface(settings.SIZE)
    background = pygame.transform.scale(background, settings.SIZE)
    left_side = pygame.transform.scale(left_side, (50, 300))
    right_side = pygame.transform.scale(right_side, (50, 300))
    section_indicator = pygame.transform.scale(section_indicator, (400, 1080))

    # Creating Items
    # Ships
    items_ships.append(Item(440, 40, settings.WIDTH - 480, 300, settings.skins[1].image, 100, settings.skins[1],
                            'Standard spaceship', 'Super is lightring'))

    items_ships.append(Item(440, 380, settings.WIDTH - 480, 300, settings.skins[0].image, 100, settings.skins[0],
                            'Zuckerberg machine', 'Super is teleportation'))
    # Upgrades
    items_upgrades.append(Item(440, 40, (settings.WIDTH - 480) // 2 - 20, 300, None, 100, 0, 'Increase gun DMG',
                               ['from ', 0, ' to ', 0]))
    items_upgrades[0].button.upgrade = 1

    items_upgrades.append(Item(440 + (settings.WIDTH - 480) // 2 + 20, 40, (settings.WIDTH - 480) // 2 - 20, 300, None,
                               100, 1, 'Increase gun FR', ['from ', 1, ' to ', 1]))
    items_upgrades[1].button.upgrade = -1

    items_upgrades.append(Item(440, 380, (settings.WIDTH - 480) // 2 - 20, 300, None, 100, 2, 'Increase plasma DMG',
                               ['from ', 2, ' to ', 2]))
    items_upgrades[2].button.upgrade = 1

    items_upgrades.append(Item(440 + (settings.WIDTH - 480) // 2 + 20, 380, (settings.WIDTH - 480) // 2 - 20, 300, None,
                               100, 3, 'Increase plasma FR', ['from ', 3, ' to ', 3]))
    items_upgrades[3].button.upgrade = -1

    items_upgrades.append(Item(440, 720, (settings.WIDTH - 480) // 2 - 20, 300, None, 100, 4, 'Increase laser DMG',
                               ['from ', 4, ' to ', 4]))
    items_upgrades[4].button.upgrade = 1

    # Cosmetics

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
        (buy_button_selected, buy_button_select, buy_button_select_hover,
         buy_button_buy_enough_money, buy_button_buy_enough_money_hover, buy_button_buy_not_enough_money)]


def create_screen():
    global buttons, screen, items_ships, items_upgrades, items_cosmetics, section_indicator, current_items
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

    # Drawing left-sided menu
    screen.blit(section_indicator, (0, int(settings.HEIGHT/2 - 540)))
    screen.blit(font.render(str(settings.money), True, DARK_GREEN), (200, int(settings.HEIGHT / 2) + 50 + 45 // 2))
    # Gun stats
    screen.blit(gun_icon_50, (50, int(settings.HEIGHT / 2 + 175)))
    screen.blit(font_small.render('DMG: ' + str(settings.bullet_damage) + ' FR: ' +
                                  str(round(settings.bullets_firerate, 1)),
                                  True, DARK_GREEN), (120, int(settings.HEIGHT / 2) + 185))
    # Plasma stats
    screen.blit(plasma_icon_50, (50, int(settings.HEIGHT / 2 + 245)))
    screen.blit(font_small.render('DMG: ' + str(settings.plasma_ball_damage) + ' FR: ' +
                                  str(round(60 / settings.plasma_balls_firerate, 2)),
                                  True, DARK_GREEN), (120, int(settings.HEIGHT / 2) + 255))
    # Laser stats
    screen.blit(laser_icon_50, (50, int(settings.HEIGHT / 2 + 315)))
    screen.blit(font_small.render('TIC DMG: ' + str(settings.laser_damage),
                                  True, DARK_GREEN), (120, int(settings.HEIGHT / 2) + 325))

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
    if (dy > 0 and current_items[0].y < 40) or (dy < 0 and current_items[len(current_items) - 1].y > settings.HEIGHT - current_items[len(current_items) - 1].height - 40):
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

