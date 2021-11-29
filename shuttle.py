import pygame

import enemies
import settings
import math

screen = None
speed_decay = 0

class Shuttle_skins:
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

    def draw(self, surface):
        self.surface = surface
        self.r = max(settings.current_skin.width / 2, settings.current_skin.height / 2)
        #rot_center(settings.current_skin.image, math.atan2(self.Vy, self.Vx))
        self.surface.blit(rot_center(settings.current_skin.image, math.atan2(30, self.Vx)*180/math.pi - 90), (self.x - settings.current_skin.x, self.y - settings.current_skin.y))

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

    def move_mouse(self):
        #pygame.mouse.set_visible(False)
        self.x = pygame.mouse.get_pos()[0]
        self.y = pygame.mouse.get_pos()[1]


def init():
    global screen
    settings.spaceship = Shuttle(screen)
    skin_test = Shuttle_skins(55, 31, 109, 62, pygame.image.load('shuttle_skins/pngegg.png').convert_alpha())
    skin1 = Shuttle_skins(50, 50, 100, 100, pygame.image.load('shuttle_skins/spaceship.pod_.1.red_.png').convert_alpha())
    settings.current_skin = skin1

def processing(screen):
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
