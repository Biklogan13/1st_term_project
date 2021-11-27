import pygame

import settings

buttons = []
screen = None
background = None


def init():
    global buttons, screen, background
    screen = pygame.Surface(settings.SIZE)

    background = pygame.image.load('backgrounds/menu_background.png').convert_alpha()
    background = pygame.transform.scale(background, settings.SIZE)

    play_image = pygame.image.load('buttons_images/play_button.png').convert_alpha()
    shop_image = pygame.image.load('buttons_images/shop_button.png').convert_alpha()
    exit_image = pygame.image.load('buttons_images/exit_button.png').convert_alpha()
    play_image = pygame.transform.scale(play_image, (400, 100))
    shop_image = pygame.transform.scale(shop_image, (400, 100))
    exit_image = pygame.transform.scale(exit_image, (400, 100))

    play_button = settings.Button(settings.WIDTH // 2 - 200, settings.HEIGHT // 2 - 200, 400, 100, 'switch_to_levels')
    play_button.image = play_image
    shop_button = settings.Button(settings.WIDTH // 2 - 200, settings.HEIGHT // 2 - 50, 400, 100, 'switch_to_shop')
    shop_button.image = shop_image
    exit_button = settings.Button(settings.WIDTH // 2 - 200, settings.HEIGHT // 2 + 100, 400, 100, 'exit')
    exit_button.image = exit_image
    buttons += [exit_button, shop_button, play_button]


def create_screen():
    global buttons, screen, background
    screen.blit(background, (0, 0))
    for b in buttons:
        b.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            for b in buttons:
                b.act(event)
    return screen

