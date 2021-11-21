import pygame

import settings

global SIZE, flag


class Button:
    def __init__(self, x, y, width, heigth, action, screen):
        self.x = x
        self.y = y
        self.width = width
        self.height = heigth
        self.action = action
        self.screen = screen
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

    def draw(self):
        pygame.draw.rect(self.screen, (255, 0, 0), (self.x, self.y, self.width, self.height))


def menu_screen():
    for b in settings.buttons:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            for b in settings.buttons:
                b.action(event)
    return screen

