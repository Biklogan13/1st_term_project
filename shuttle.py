import pygame
import settings

screen = None

class Shuttle_skins:
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(image, (self.width, self.height))


class Shuttle:
    def __init__(self, surface):
        self.surface = surface
        self.x = settings.WIDTH/2
        self.y = settings.HEIGHT/2
        self.Vx = 0
        self.Vy = 0
        self.ax = 0
        self.ay = 0

    def draw(self, surface):
        self.surface = surface
        self.surface.blit(settings.current_skin.image, (self.x - settings.current_skin.x, self.y - settings.current_skin.y))

    def move(self):

        if pygame.key.get_pressed()[pygame.K_w]:
            self.ay = -0.2
        elif pygame.key.get_pressed()[pygame.K_s]:
            self.ay = 0.2
        else:
            self.ay = 0

        if self.ay == 0:
            if self.Vy > 0:
                self.Vy = -0.1
            if self.Vy < 0:
                self.Vy = 0.1
            if self.Vy < 0.2 and self.Vy > -0.2:
                self.Vy = 0

        if pygame.key.get_pressed()[pygame.K_a]:
            self.ax = -0.2
        elif pygame.key.get_pressed()[pygame.K_d]:
            self.ax = 0.2
        else:
            self.ax = 0

        if self.ax == 0:
            if self.Vx > 0:
                self.Vx = -0.1
            if self.Vx < 0:
                self.Vx = 0.1
            if self.Vx < 0.2 and self.Vx > -0.2:
                self.Vx = 0


        if self.ax >= 0 and self.Vx <= 5:
            self.Vx += self.ax
        if self.ax <= 0 and self.Vx >= -5:
            self.Vx += self.ax
        if self.ay >= 0 and self.Vy <= 5:
            self.Vy += self.ay
        if self.ay <= 0 and self.Vy >= -5:
            self.Vy += self.ay

        if self.Vx >= 0 and self.x <= settings.WIDTH:
            self.x += self.Vx
        if self.Vx <= 0 and self.x >= 0:
            self.x += self.Vx
        if self.Vy >= 0 and self.y <= settings.HEIGHT:
            self.y += self.Vy
        if self.Vy <= 0 and self.y >= 0:
            self.y += self.Vy

def init():
    global screen
    settings.spaceship = Shuttle(screen)
    skin1 = Shuttle_skins(55, 31, 109, 62, pygame.image.load('shuttle_skins/pngegg.png'))
    settings.current_skin = skin1
