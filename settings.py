
def init_global():
    global SIZE, WIDTH, HEIGHT, flag
    SIZE, WIDTH, HEIGHT, flag = 0, 0, 0, 'menu'

def menu_init():
    menu_buttons = []
    screen = pygame.Surface(SIZE)
    screen.fill((0, 0, 0))
    exit_button = Button(SIZE[0] - 100, 0, 100, 100, 'exit')
    menu_buttons.append(exit_button)