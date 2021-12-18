import math
import pygame

import levels
import settings

screen = None
speed_decay = 0


class ShuttleSkins:
    def __init__(self, x, y, width, height, image, super):
        """
        Initialization function for the shuttle skin class
        :param x: x-offset of the skin
        :param y: y-offset if the skin
        :param width: width of the skin
        :param height: height if the skin
        :param image: skin sprite
        :param super: number of the skin super
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(image, (width, height))
        self.super = super


class Shuttle:
    def __init__(self, surface):
        """
        Initialization function for the shuttle class
        :param surface: a surface the shuttle will initially be drawn on
        """
        self.surface = surface
        self.x = settings.WIDTH / 2
        self.y = settings.HEIGHT / 2
        self.Vx = 0
        self.Vy = 0
        self.ax = 0
        self.ay = 0
        self.r = 0
        self.hp = 10000
        self.max_hp = 10000
        self.hit_timer = 0

    def draw(self, surface):
        """
        A function which draws the shuttle
        :param surface: a surface which the shuttle will be drawn on
        :return:
        """
        self.surface = surface
        self.r = max(settings.current_skin.width / 2, settings.current_skin.height / 2)
        image = settings.current_skin.image
        if self.hit_timer > 0:
            image = levels.red_image(image)
        self.surface.blit(rot_center_square(image, math.atan2(20 - self.Vy, self.Vx) * 180 / math.pi - 90),
                          (self.x - settings.current_skin.x, self.y - settings.current_skin.y))

    def move(self):
        """
        A function which moves the shuttle
        :return:
        """
        global speed_decay

        if pygame.key.get_pressed()[pygame.K_w]:
            self.ay = -1
        elif pygame.key.get_pressed()[pygame.K_s]:
            self.ay = 1
        else:
            self.ay = 0

        if self.ay == 0:
            if self.Vy > 0:
                self.Vy -= speed_decay
            if self.Vy < 0:
                self.Vy += speed_decay
            if self.Vy < speed_decay * 2 and self.Vy > -speed_decay * 2:
                self.Vy = 0

        if pygame.key.get_pressed()[pygame.K_a]:
            self.ax = -1
        elif pygame.key.get_pressed()[pygame.K_d]:
            self.ax = 1
        else:
            self.ax = 0

        if self.ax == 0:
            if self.Vx > 0:
                self.Vx -= speed_decay
            if self.Vx < 0:
                self.Vx += speed_decay
            if self.Vx < speed_decay * 2 and self.Vx > -speed_decay * 2:
                self.Vx = 0

        if self.ax >= 0 and self.Vx < 10:
            self.Vx += self.ax
        if self.ax <= 0 and self.Vx > -10:
            self.Vx += self.ax
        if self.ay >= 0 and self.Vy < 10:
            self.Vy += self.ay
        if self.ay <= 0 and self.Vy > -10:
            self.Vy += self.ay

        if self.Vx >= 0 and self.x <= settings.WIDTH - settings.current_skin.x:
            self.x += self.Vx
        if self.Vx <= 0 and self.x >= settings.current_skin.x:
            self.x += self.Vx
        if self.Vy >= 0 and self.y <= settings.HEIGHT - settings.current_skin.y:
            self.y += self.Vy
        if self.Vy <= 0 and self.y >= settings.current_skin.y:
            self.y += self.Vy

        if self.x > settings.WIDTH:
            self.x = settings.WIDTH
        if self.y > settings.HEIGHT:
            self.y = settings.HEIGHT
        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0

    def move_mouse(self):
        """
        A test function to move the shuttle with a mouse
        :return:
        """
        self.x = pygame.mouse.get_pos()[0]
        self.y = pygame.mouse.get_pos()[1]


def init():
    """
    Initialization function which loads shuttle skins
    :return:
    """
    global screen
    settings.spaceship = Shuttle(screen)
    gunship = ShuttleSkins(50, 50, 100, 100, pygame.image.load('shuttle_skins/gunship.png').convert_alpha(), 0)
    teleporter = ShuttleSkins(55, 31, 110, 110, pygame.image.load('shuttle_skins/pngegg.png').convert_alpha(), 1)
    lasership = ShuttleSkins(50, 50, 100, 100, pygame.image.load('shuttle_skins/lasership.png').convert_alpha(), 2)
    rocketship = ShuttleSkins(50, 50, 100, 100, pygame.image.load('shuttle_skins/rocketship.png').convert_alpha(), 3)
    settings.skins = [teleporter, gunship, lasership, rocketship]
    settings.current_skin = settings.skins[1]


def processing(screen):
    """
    A function which processes shuttle actions
    :param screen:
    :return:
    """
    if settings.spaceship.hit_timer > 0:
        settings.spaceship.hit_timer -= 1
    settings.spaceship.draw(screen)
    settings.spaceship.move()


def rot_center(image, angle):
    """
    Rotates an image around the center of it's rectangle
    :param image: an image which needs to be rotated
    :param angle: an angle to rotate
    :return:
    """
    WIDTH = image.get_width()
    HEIGHT = image.get_height()
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


def rot_center_square(image, angle):
    """
    Rotates a square image around it's center
    :param image: an image which needs to be rotated
    :param angle: an angle to rotate
    :return:
    """
    WIDTH = image.get_width()
    HEIGHT = image.get_height()
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image
