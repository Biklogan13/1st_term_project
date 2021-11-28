import pygame

# Global variables which needed in many files
SIZE, WIDTH, HEIGHT, flag, running = 0, 0, 0, 'menu', True
current_skin, spaceship, enemies, tick_counter = None, None, [], 0
light_rings, bullets, laser, plasma_balls, ammo, bullet_image, light_ring_image, plasma_ball_sprites, laaser_sound, cannon_sound = [], [], None, [], 0, None, None, [], None, None
seconds = 0
# Common classes
class Button:
    def __init__(self, x, y, width, height, action):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.action = action
        self.image = None
        self.image_hover = None
        self.hover = False

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
        if self.image is None:
            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
        elif self.hover:
            screen.blit(self.image_hover, (self.x, self.y))
        else:
            screen.blit(self.image, (self.x, self.y))

    def hover_test(self, event):
        if 0 <= event.pos[0] - self.x <= self.width and 0 <= event.pos[1] - self.y <= self.height:
            self.hover = True
        else:
            self.hover = False



