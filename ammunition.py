import pygame.mixer
import math
import pygame
import menu
import shop
import levels
import shuttle
import enemies
import settings
import random
def init():

    plasma_ball_1 = pygame.image.load('ammo_sprites/plasma_1.png')
    plasma_ball_1.set_colorkey((255, 255, 255))
    plasma_ball_2 = pygame.image.load('ammo_sprites/plasma_2.png')
    plasma_ball_2.set_colorkey((255, 255, 255))
    plasma_ball_3 = pygame.image.load('ammo_sprites/plasma_3.png')
    plasma_ball_3.set_colorkey((255, 255, 255))
    plasma_ball_sprites = [plasma_ball_1, plasma_ball_2, plasma_ball_3]

    bullet_image = pygame.image.load('ammo_sprites/bullets-clip-art-129.png')
    bullet_image = pygame.transform.scale(bullet_image, (40, 40))
    settings.bullet_image = bullet_image

    lightring = pygame.image.load('ammo_sprites/lightring.png')
    lightring.set_colorkey((255, 255, 255))
    settings.plasma_ball_sprites = plasma_ball_sprites
    settings.light_ring_image = lightring


    pygame.mixer.init()
    laser_sound = pygame.mixer.Sound('Sounds/LaserLaserBeam EE136601_preview-[AudioTrimmer.com].mp3')
    settings.laser_sound = laser_sound
    cannon_sound = pygame.mixer.Sound('Sounds/ES_Cannon Blast 4.mp3')
    settings.cannon_sound = cannon_sound
    pygame.mixer.Sound.set_volume(settings.cannon_sound, 0.6)
    pygame.mixer.Sound.set_volume(settings.laser_sound, 0.6)
    settings.RED = 0xFF0000
    settings.YELLOW = 0xFFC91F
    settings.ORANGE = (255, 165, 0)





class Bullet:
    def __init__(self, screen: pygame.Surface):
        """ Конструктор класса bullet

        Args:
        x - начальное положение пули по горизонтали
        y - начальное положение пули по вертикали
        """
        self.screen = screen
        self.x = settings.spaceship.x
        self.y = settings.spaceship.y
        self.r = 3
        self.vx = 0
        self.vy = 0
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.live = 30
        self.angle = math.atan2(self.vy, self.vx)
        self.bullet = settings.bullet_image
        self.timer = 50

    def move(self):
        """Переместить пулю по прошествии единицы времени.

        Метод описывает перемещение пули за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy.
        """
        self.timer -= 1
        if self.y >= 2*settings.HEIGHT - self.r:
            self.vy = 0
            self.vx = 0
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        self.angle = math.atan2(self.vy, self.vx)
        self.bullet = rot_center(settings.bullet_image, self.angle*360/(-2*math.pi))
        self.screen.blit(self.bullet, (self.x - 20, self.y - 20))

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения пули и цели. В противном случае возвращает False.
        """

        if (self.x - obj.x)**2 + (self.y - obj.y)**2 <= (self.r + obj.r)**2:
            return True
        else:
            return False

class Laser:
    def __init__(self):
        self.screen = levels.screen
        self.angle = 0
        self.r = 0
        self.firing = 0
        self.color = settings.YELLOW

    def fire_start(self):
        self.firing = 1

    def fire_end(self):
        self.firing = 0

    def draw(self):
        pygame.draw.line(self.screen, settings.RED, (settings.spaceship.x, settings.spaceship.y), (settings.spaceship.x + math.cos(self.angle) * 2*settings.WIDTH, settings.spaceship.y + math.sin(self.angle) * 2*settings.WIDTH), width=20)
        pygame.draw.line(self.screen, settings.ORANGE, (settings.spaceship.x, settings.spaceship.y), (settings.spaceship.x + math.cos(self.angle) * 2*settings.WIDTH, settings.spaceship.y + math.sin(self.angle) * 2*settings.WIDTH), width=8)
        pygame.draw.line(self.screen, settings.YELLOW, (settings.spaceship.x, settings.spaceship.y), (settings.spaceship.x + math.cos(self.angle) * 2*settings.WIDTH, settings.spaceship.y + math.sin(self.angle) * 2*settings.WIDTH), width=2)
        self.screen.blit(settings.current_skin.image, (settings.spaceship.x - 55, settings.spaceship.y - 31))


    def targetting(self, event):
        if event:
            self.angle = math.atan2((event.pos[1]-settings.spaceship.y), (event.pos[0]-settings.spaceship.x))


    def hittest_laser(self, obj):
        if abs(math.sin(self.angle)*obj.x - math.cos(self.angle)*obj.y - math.sin(self.angle)*settings.spaceship.x + math.cos(self.angle)*settings.spaceship.y) <= 10 + obj.r and (pygame.mouse.get_pos()[0] - settings.spaceship.x)*(obj.x - settings.spaceship.x) > 0 and self.firing == 1:
            return True
        else:
            return False


class Plasma_ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса Plasma_ball

        Args:
        x - начальное положение шара по горизонтали
        y - начальное положение шара по вертикали
        angle - угол выстрела
        surf - поверхность, на которой рисуется шар
        """
        self.screen = screen
        self.x = settings.spaceship.x
        self.y = settings.spaceship.y
        self.r = 100
        self.vx = 0
        self.vy = 0
        self.timer = 300
        self.surf = pygame.transform.scale(settings.plasma_ball_sprites[1], (self.r, self.r))
        self.angle = math.atan2(self.vy, self.vx)
        self.sprite_number = 1

    def move(self):
        """Переместить шар по прошествии 1 кадра.

        Метод описывает перемещение шара за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на шар,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.y += self.vy
        self.timer -= 1
        if (self.timer % 10 == 0):
            self.sprite_number += 1
            self.sprite_number = self.sprite_number % 2
            self.surf = pygame.transform.scale(settings.plasma_ball_sprites[self.sprite_number], (self.r, self.r))


    def draw(self):
        self.r = 100
        self.screen.blit(self.surf, (self.x - 25, self.y - 25))

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли шар с целью.
        Args:
            obj: цель
        Returns:
            Возвращает True в случае столкновения цели и шара. В противном случае возвращает False.
        """
        if (self.x - obj.x)**2 + (self.y - obj.y)**2 <= (self.r + obj.r)**2:
            return True
        else:
            return False


class Lightring:
    """кольцо молний, убивающее всех"""
    def __init__(self, screen):
        self.screen = levels.screen
        self.x = settings.spaceship.x
        self.y = settings.spaceship.y
        self.r = 100
        self.v = 10
        self.surf = pygame.transform.scale(settings.light_ring_image, (self.r, self.r))


    def move(self):
        self.x = settings.spaceship.x
        self.y = settings.spaceship.y
        self.r += self.v
        self.surf = pygame.transform.scale(settings.light_ring_image, (self.r, self.r))


    def draw(self):

        self.screen.blit(self.surf, (self.x - self.r, self.y - self.r))

    def hittest(self, obj):

        if (self.x - obj.x)**2 + (self.y - obj.y)**2 <= (self.r + obj.r)**2:
            return True
        else:
            return False


def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


def processing(screen):
    for b in settings.bullets:
        b.draw()
        b.move()
        if b.timer <= 0:
            settings.bullets.remove(b)
    if settings.ammo == 1:
        if settings.seconds % settings.bullets_firerate == 0:
            new_bullet = Bullet(levels.screen)
            new_bullet.angle = math.atan2((pygame.mouse.get_pos()[1] - settings.spaceship.y), (pygame.mouse.get_pos()[0] - settings.spaceship.x)) + random.randint(-10, 10) * 0.008
            new_bullet.vx = 30 * math.cos(new_bullet.angle)
            new_bullet.vy = 30 * math.sin(new_bullet.angle)
            settings.bullets.append(new_bullet)

    if pygame.key.get_pressed()[pygame.K_SPACE]:
        settings.ammo = 1
    else:
        settings.ammo = 0
        settings.seconds = 0
    settings.spaceship.draw(screen)
    settings.seconds += 1
