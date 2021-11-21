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
        self.surface.blit(current_skin.draw(), (self.x - skin.x, self.y - skin.y))

    def move(self, ax, ay):
        self.ax = ax
        self.ay = ay
        self.Vx += ax
        self.Vy += ay
        self.x += self.Vx
        self.y += self.Vy

class Shuttle_skins:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
    def draw(self):
        return self.image

skin1 = Shuttle_skins(55, 31, pygame.image.load('shuttle_skins/pngegg.png'))
current_skin = skin1