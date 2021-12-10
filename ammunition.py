import pygame.mixer
import math
import pygame
import levels
import settings
import random

laser = None
cannons = None
ult = 1
lightrings = []
light_ring_animation = []


def init():
    global laser, cannons, laser_sound, plasma_gun_sound, light_ring_image

    plasma_ball_1 = pygame.image.load(settings.PLASMA_1_PATH)
    plasma_ball_1.set_colorkey((255, 255, 255))
    plasma_ball_2 = pygame.image.load(settings.PLASMA_2_PATH)
    plasma_ball_2.set_colorkey((255, 255, 255))
    plasma_ball_3 = pygame.image.load(settings.PLASMA_3_PATH)
    plasma_ball_3.set_colorkey((255, 255, 255))
    plasma_ball_sprites = [plasma_ball_1, plasma_ball_2, plasma_ball_3]

    bullet_image = pygame.image.load(settings.PLASMA_BULLET_PATH)
    bullet_image = pygame.transform.scale(bullet_image, (80, 40))
    settings.bullet_image = bullet_image

    light_ring_image = pygame.image.load(settings.LIGHT_RING_PATH)
    light_ring_image.set_colorkey((255, 255, 255))
    settings.plasma_ball_sprites = plasma_ball_sprites

    pygame.mixer.init()
    laser_sound = pygame.mixer.Sound(settings.LASER_SOUND_PATH)
    cannons = pygame.mixer.Sound(settings.CANNONS_SOUND_PATH)
    plasma_gun_sound = pygame.mixer.Sound(settings.PLASMAGUN_SOUND_PATH)
    pygame.mixer.Sound.set_volume(cannons, 0.2)
    pygame.mixer.Sound.set_volume(laser_sound, 0.02)
    pygame.mixer.Sound.set_volume(plasma_gun_sound, 0.05)
    settings.RED = 0xFF0000
    settings.YELLOW = 0xFFC91F
    settings.ORANGE = (255, 165, 0)
    laser = Laser(levels.screen)

    for i in range(0, 101):
        light_ring_animation.append(pygame.transform.scale(light_ring_image, (30 * i, 30 * i)))


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
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.live = 30
        self.angle = math.atan2(self.vy, self.vx)
        self.bullet = settings.bullet_image
        self.timer = 150

    def move(self):
        """Переместить пулю по прошествии единицы времени.

        Метод описывает перемещение пули за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy.
        """
        self.timer -= 1
        if self.y >= 2 * settings.HEIGHT - self.r:
            self.vy = 0
            self.vx = 0
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        self.angle = math.atan2(self.vy, self.vx)
        self.bullet = rot_center(settings.bullet_image, self.angle * 360 / (-2 * math.pi))
        self.screen.blit(self.bullet, (self.x - 20, self.y - 20))

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения пули и цели. В противном случае возвращает False.
        """

        return (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2


class Laser:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.angle = 0
        self.r = 50
        self.firing = 0
        self.color = settings.YELLOW

    def fire_start(self):
        self.firing = 1

    def fire_end(self):
        self.firing = 0

    def draw(self):
        pygame.draw.line(self.screen, settings.RED, (settings.spaceship.x, settings.spaceship.y), (
            settings.spaceship.x + math.cos(self.angle) * 2 * settings.WIDTH,
            settings.spaceship.y + math.sin(self.angle) * 2 * settings.WIDTH), width=20)
        pygame.draw.line(self.screen, settings.ORANGE, (settings.spaceship.x, settings.spaceship.y), (
            settings.spaceship.x + math.cos(self.angle) * 2 * settings.WIDTH,
            settings.spaceship.y + math.sin(self.angle) * 2 * settings.WIDTH), width=8)
        pygame.draw.line(self.screen, settings.YELLOW, (settings.spaceship.x, settings.spaceship.y), (
            settings.spaceship.x + math.cos(self.angle) * 2 * settings.WIDTH,
            settings.spaceship.y + math.sin(self.angle) * 2 * settings.WIDTH), width=2)

    def targetting(self):
        self.angle = math.atan2((pygame.mouse.get_pos()[1] - settings.spaceship.y),
                                (pygame.mouse.get_pos()[0] - settings.spaceship.x))

    def hittest(self, obj):
        if abs(math.sin(self.angle) * obj.x - math.cos(self.angle) * obj.y - math.sin(
                self.angle) * settings.spaceship.x + math.cos(self.angle) * settings.spaceship.y) <= 15 + obj.r and (
                pygame.mouse.get_pos()[0] - settings.spaceship.x) * (
                obj.x - settings.spaceship.x) > 0 and self.firing == 1:
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
        self.r = 50
        self.vx = 0
        self.vy = 0
        self.timer = 900
        self.surf = pygame.transform.scale(settings.plasma_ball_sprites[1], (2 * self.r, 2 * self.r))
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
            self.surf = pygame.transform.scale(settings.plasma_ball_sprites[self.sprite_number],
                                               (2 * self.r, 2 * self.r))

    def draw(self):
        self.screen.blit(self.surf, (self.x - self.r, self.y - self.r))

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли шар с целью.
        Args:
            obj: цель
        Returns:
            Возвращает True в случае столкновения цели и шара. В противном случае возвращает False.
        """
        return (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2


class Lightring:
    """кольцо молний, убивающее всех"""

    def __init__(self, screen):
        self.screen = levels.screen
        self.x = settings.spaceship.x
        self.y = settings.spaceship.y
        self.r = 100
        self.v = 10
        self.surf = pygame.transform.scale(light_ring_image, (self.r, self.r))
        self.timer = 100
        self.k = 0

    def move(self):
        self.r += self.v
        self.surf = light_ring_animation[self.k]
        self.timer -= 1
        self.k += 1
    def draw(self):
        self.screen.blit(self.surf, (self.x - self.r / 2, self.y - self.r / 2))

    def hittest(self, obj):
        return (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r - 500 + obj.r) ** 2



def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


def processing(screen, events):
    global cannons, ult

    for b in settings.bullets:
        b.draw()
        b.move()
        if b.timer <= 0:
            settings.bullets.remove(b)

    if settings.ammo == 0:
        if settings.seconds % settings.bullets_firerate == 0:
            new_bullet = Bullet(levels.screen)
            new_bullet.angle = math.atan2(
                (pygame.mouse.get_pos()[1] - settings.spaceship.y),
                (pygame.mouse.get_pos()[0] - settings.spaceship.x)) + random.randint(-10, 10) * 0.008
            new_bullet.vx = 50 * math.cos(new_bullet.angle)
            new_bullet.vy = 50 * math.sin(new_bullet.angle)
            settings.bullets.append(new_bullet)
            pygame.mixer.Sound.set_volume(cannons, 0.1)
            cannons.play()

    for b in settings.plasma_balls:
        b.draw()
        b.move()
        if b.timer <= 0:
            settings.plasma_balls.remove(b)
    if settings.ammo == 1:
        plasma_gun_sound.play()
        if settings.seconds % settings.plasma_balls_firerate == 0:
            new_ball = Plasma_ball(levels.screen)
            new_ball.angle = math.atan2(
                (pygame.mouse.get_pos()[1] - settings.spaceship.y),
                (pygame.mouse.get_pos()[0] - settings.spaceship.x)) + random.randint(-10, 10) * 0.008
            new_ball.vx = 10 * math.cos(new_ball.angle)
            new_ball.vy = 10 * math.sin(new_ball.angle)
            settings.plasma_balls.append(new_ball)

    if settings.ammo == 2:
        laser.fire_start()
        laser.angle = math.atan2((pygame.mouse.get_pos()[1] - settings.spaceship.y),
                                 (pygame.mouse.get_pos()[0] - settings.spaceship.x))
        laser.draw()
        laser_sound.play()
    else:
        laser_sound.stop()
        laser.fire_end()

    for b in lightrings:
        b.draw()
        b.move()
        if b.timer <= 0:
            lightrings.remove(b)

    for event in events:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if ult == 1:
                new_lightring = Lightring(levels.screen)
                new_lightring.v = 30
                lightrings.append(new_lightring)
            elif ult == 2:
                settings.spaceship.x += settings.dash_range * math.cos(
                    math.atan2(pygame.mouse.get_pos()[1] - settings.spaceship.y,
                               pygame.mouse.get_pos()[0] - settings.spaceship.x))
                settings.spaceship.y += settings.dash_range * math.sin(
                    math.atan2(pygame.mouse.get_pos()[1] - settings.spaceship.y,
                               pygame.mouse.get_pos()[0] - settings.spaceship.x))



    if pygame.mouse.get_pressed()[0]:
        settings.ammo = levels.ammo_type
    else:
        settings.ammo = 0
        settings.seconds = 0
    settings.seconds += 1
