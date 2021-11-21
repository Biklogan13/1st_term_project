import math
from random import choice
import random
import pygame

plasma_ball_sprites = []  # FIXME добавить спрайтов шариков

class Ball:
    def __init__(self, screen: pygame.Surface):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = gun.x
        self.y = gun.y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.live = 30
        self.angle = math.atan2(self.vy, self.vx)
        self.bullet = bullet

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """

        if self.y >= 2*HEIGHT - self.r:
            self.vy = 0
            self.vx = 0
        else:
            self.vy += 0.5
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        self.angle = math.atan2(self.vy, self.vx)
        #pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)
        self.bullet = rot_center(bullet, self.angle*360/(-2*math.pi))
        self.screen.blit(self.bullet, (self.x - 20, self.y - 20))

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """

        if (self.x - obj.x)**2 + (self.y - obj.y)**2 <= (self.r + obj.r)**2:
            return True
        else:
            return False

class Laser:
    def __init__(self):
        self.screen = screen
        self.angle = 0
        self.r = 0
        self.firing = 0
        self.color = GREY

    def fire_start(self):
        self.firing = 1

    def fire_end(self):
        self.firing = 0

    def draw(self):
        pygame.draw.line(self.screen, RED, (gun.x, gun.y), (gun.x + math.cos(self.angle) * 2*WIDTH, gun.y + math.sin(self.angle) * 2*WIDTH), width=20)
        pygame.draw.line(self.screen, ORANGE, (gun.x, gun.y), (gun.x + math.cos(self.angle) * 2*WIDTH, gun.y + math.sin(self.angle) * 2*WIDTH), width=8)
        pygame.draw.line(self.screen, YELLOW, (gun.x, gun.y), (gun.x + math.cos(self.angle) * 2*WIDTH, gun.y + math.sin(self.angle) * 2*WIDTH), width=2)
        self.screen.blit(ufo, (gun.x - 55, gun.y - 31))

    #def lensdraw(self):
    #        # y = 450, x = 20
    #    pygame.draw.line(self.screen, self.color, (20, (HEIGHT / 2)), (20 + math.cos(self.angle) * gun.f2_power, (HEIGHT / 2) + math.sin(self.angle) * gun.f2_power), width=10)

    def targetting(self, event):
        if event:
            self.angle = math.atan2((event.pos[1]-gun.y), (event.pos[0]-gun.x))
        if self.firing:
            self.color = RED
        else:
            self.color = GREY

    def hittest_laser(self, obj):
        if abs(math.sin(self.angle)*obj.x - math.cos(self.angle)*obj.y - math.sin(self.angle)*gun.x + math.cos(self.angle)*gun.y) <= 10 + obj.r and (pygame.mouse.get_pos()[0] - gun.x)*(obj.x - gun.x) > 0 and self.firing == 1:
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
        g - ускорение свободного падения
        """
        self.screen = screen
        self.x = gun.x
        self.y = gun.y
        self.r = 50
        self.vx = 0
        self.vy = 0
        self.g = 0
        self.timer = 300
        self.surf = pygame.transform.scale(plasma_balls_prites[1] (self.r, self.r))
        self.angle = math.atan2(self.vy, self.vx)

    def move(self):
        """Переместить шар по прошествии 1 кадра.

        Метод описывает перемещение шара за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на шар,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.y -= self.vy
        self.vy += self.g
        self.timer -= 1
        self.sprite_number += 1
        if (self.timer % 10):
            self.surf = pygame.transform.scale(plasma_balls_prites[self.sprite.number % 3](self.r, self.r))


    def draw(self):
        self.r = 50
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