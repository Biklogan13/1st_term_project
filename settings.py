import pygame

# Global variables which needed in many files
SIZE, WIDTH, HEIGHT, flag, running = 0, 0, 0, 'menu', True


# Common classes
class Button:
    def __init__(self, x, y, width, heigth, action):
        self.x = x
        self.y = y
        self.width = width
        self.height = heigth
        self.action = action
        self.image = None

    def act(self, event):
        global running, flag
        if 0 <= event.pos[0] - self.x <= self.width and 0 <= event.pos[1] - self.y <= self.height:
            if self.action == 'exit':
                pygame.quit()
                running = False
            elif self.action == 'switch_to_menu':
                flag = 'menu'
            elif self.action == 'switch_to_levels':
                flag = 'levels'
            if self.action == 'switch_to_shop':
                flag = 'shop'

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))




