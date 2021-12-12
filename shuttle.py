import pygame

import levels
import settings
import math

screen = None
speed_decay = 0


class ShuttleSkins:
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(image, (width, height))


class Shuttle:
    def __init__(self, surface):
        self.surface = surface
        self.x = settings.WIDTH/2
        self.y = settings.HEIGHT/2
        self.Vx = 0
        self.Vy = 0
        self.ax = 0
        self.ay = 0
        self.r = 0
        self.hp = 2500
        self.max_hp = 2500
        self.hit_timer = 0

    def draw(self, surface):
        self.surface = surface
        self.r = max(settings.current_skin.width / 2, settings.current_skin.height / 2)
        #rot_center(settings.current_skin.image, math.atan2(self.Vy, self.Vx))
        image = settings.current_skin.image
        if self.hit_timer > 0:
            image = levels.red_image(image)
        self.surface.blit(rot_center(image, math.atan2(20 - self.Vy, self.Vx)*180/math.pi - 90), (self.x - settings.current_skin.x, self.y - settings.current_skin.y))

    def move(self):
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
            if self.Vy < speed_decay*2 and self.Vy > -speed_decay*2:
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
            if self.Vx < speed_decay*2 and self.Vx > -speed_decay*2:
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
        #pygame.mouse.set_visible(False)
        self.x = pygame.mouse.get_pos()[0]
        self.y = pygame.mouse.get_pos()[1]


def init():
    global screen
    settings.spaceship = Shuttle(screen)
    skin_test = ShuttleSkins(55, 31, 109, 62, pygame.image.load('shuttle_skins/pngegg.png').convert_alpha())
    gunship = ShuttleSkins(50, 50, 100, 100, pygame.image.load('shuttle_skins/gunship.png').convert_alpha())
    settings.skins = [skin_test, gunship]
    settings.current_skin = settings.skins[0]

def processing(screen):
    if settings.spaceship.hit_timer > 0:
        settings.spaceship.hit_timer -= 1
    settings.spaceship.draw(screen)
    settings.spaceship.move()

def rot_center(image, angle):
    WIDTH = image.get_width()
    HEIGHT = image.get_height()
    orig_rect = image.get_rect() #width=min(WIDTH, HEIGHT), height=min(WIDTH, HEIGHT))
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect()
    rot_rect.center = rot_image.get_rect().center
    #print(orig_rect, rot_rect)
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image
