class Shuttle:
    def __init__(self, surface):
        self.surface = surface
        self.x = WIDTH/2
        self.y = HEIGHT/2
        self.skin =

    def draw(self, surface, skin):
        self.surface = surface
        self.surface.blit(skin.draw(), (self.x - skin.x, self.y - skin.y))

class Shuttle_skins:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
    def draw(self):
        return self.image

