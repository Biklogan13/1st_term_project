import pygame


def init_global():
    global SIZE, WIDTH, HEIGHT, flag
    SIZE, WIDTH, HEIGHT, flag = 0, 0, 0, 'menu'


# Common classes
class Button:
    def __init__(self, x, y, width, heigth, action):
        self.x = x
        self.y = y
        self.width = width
        self.height = heigth
        self.action = action
        self.image = None

    def action(self, event):
        if event.pos[0] - self.x <= self.width and event.pos[1] - self.y <= self.height:
            if self.action == 'exit':
                pygame.quit()
            elif self.action == 'switch_to_menu':
                pass
            elif self.action == 'switch_to_levels':
                pass
            if self.action == 'switch_to_shop':
                pass

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))




