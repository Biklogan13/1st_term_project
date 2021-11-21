import pygame


global SIZE, flag


class Button:
    def __init__(self, x, y, width, heigth, action, screen):
        self.x = x
        self.y = y
        self.width = width
        self.height = heigth
        self.action = action
        self.screen = screen
        self.image = Nan

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


def menu_init():
    screen = pygame.Surface(SIZE)
    screen.fill((0, 0, 0))
    exit_button = Button(SIZE[0] - 100, 0, 100, 100, 'exit')


def menu_screen():
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            for b in buttons:
                b.action(event)
    pygame.screen.draw.rect
    return screen

