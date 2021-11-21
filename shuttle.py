import pygame
import settings

class Shuttle:
    def __init__(self, surface):
        self.surface = surface
        self.x = WIDTH/2
        self.y = HEIGHT/2
        self.Vx = 0
        self.Vy = 0
        self.ax = 0
        self.ay = 0

    def draw(self, surface, skin):
        self.surface = surface
        self.surface.blit(current_skin.image, (self.x - skin.x, self.y - skin.y))

    def move(self):

        if pygame.key.get_pressed()[pygame.K_w]:
            self.ay = -1
        elif pygame.key.get_pressed()[pygame.K_s]:
            self.ay = 1
        else:
            self.ay = 0

        if pygame.key.get_pressed()[pygame.K_a]:
            self.ax = -1
        elif pygame.key.get_pressed()[pygame.K_d]:
            self.ax = 1
        else:
            self.ax = 0

        if self.ax >= 0:
            if self.Vx <= 10:
                self.Vx += self.ax
        if self.ax <= 0:
            if self.Vx >= -10:
                self.Vx += self.ax
        if self.ay >= 0:
            if self.Vy <= 10:
                self.Vy += self.ay
        if self.ay <= 0:
            if self.Vy >= -10:
                self.Vy += self.ay

        if self.Vx >= 0:
            if self.x <= WIDTH:
                self.x += self.Vx
        if self.Vx <= 0:
            if self.x >= 0:
                self.x += self.Vx
        if self.Vy >= 0:
            if self.y <= HEIGHT:
                self.y += self.Vy
        if self.Vy <= 0:
            if self.y >= 0:
                self.y += self.Vy


class Shuttle_skins:
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(image, (self.width, self.height))

skin1 = Shuttle_skins(55, 31, 109, 62, pygame.image.load('shuttle_skins/pngegg.png'))
current_skin = skin1
