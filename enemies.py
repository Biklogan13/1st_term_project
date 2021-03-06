import math
import os
import pygame
import random

import ammunition
import levels
import settings

# Global variables of enemies section
kamikaze_image = None
mine_image = None
enemy_image = None
heavy_image = None
missile_image = None
carrier_image = None

# Setting paths for enemy sprites
MINE_IMAGE_PATH = os.path.join('.', 'enemy_skins', 'mine.png')
KAMIKADZE_IMAGE_PATH = os.path.join('.', 'enemy_skins', 'kamikaze.PNG')
ENEMY_IMAGE_PATH = os.path.join('.', 'enemy_skins', 'enemy.PNG')
HEAVY_IMAGE_PATH = os.path.join('.', 'enemy_skins', 'heavy.png')
MISSILE_IMAGE_PATH = os.path.join('.', 'ammo_sprites', 'missile.png')
CARRIER_IMAGE_PATH = os.path.join('.', 'enemy_skins', 'carrier.png')


class Coin:
    def __init__(self, x, y, denomination):
        """
        Initialization function for the coin class
        :param x: initial x-coordinate of a coin
        :param y: initial y-coordinate of a coin
        :param denomination: value of a coin
        """
        self.x = x
        self.y = y
        self.r = 30
        self.denomination = denomination
        self.frame = 0

    def draw(self, screen):
        """
        A function which draws a coin
        :param screen: a surface which coin will be drawn on
        :return: None
        """
        levels.screen.blit(ammunition.coin_flip_animation[self.frame], (self.x - self.r, self.y - self.r))

    def move(self):
        """
        A function which moves a coin with speed relative to the distance to the spaceship
        :return: None
        """
        dist = ((settings.spaceship.x - self.x) ** 2 + (settings.spaceship.y - self.y) ** 2) ** 0.5
        if dist <= 200:
            self.x += int((settings.spaceship.x - self.x) * 0.1)
            self.y += int((settings.spaceship.y - self.y) * 0.1)
        self.frame += 1
        self.frame = self.frame % 28

    def hit_test(self):
        """
        A function which tests collision of a coin with a spaceship
        :return: bool, state of collision
        """
        if (self.x - settings.spaceship.x) ** 2 + (self.y - settings.spaceship.y) ** 2 \
                <= (self.r + settings.spaceship.r) ** 2:
            settings.money += self.denomination
            settings.super_charge += 10
            settings.coins.remove(self)
            ammunition.coin_flip_sound.play()


class EnemyStandart:
    def __init__(self, heading):
        """
        Initialization function for the standart enemy class
        :param heading: initial direction of movement, clockwise if 0, counterclockwise if 1
        """
        self.surface = None
        if heading == 1:
            self.x = random.randint(settings.HEIGHT / 2 + 100 + 50, settings.WIDTH + settings.HEIGHT / 2 + 100 - 50)
        else:
            self.x = random.randint(-settings.HEIGHT / 2 - 100 + 50, settings.WIDTH - settings.HEIGHT / 2 - 100 - 50)
        self.y = -100
        self.Vx = 0
        self.Vy = 10
        self.live = 100
        self.image = enemy_image
        self.r = 40
        self.angle = 0
        self.phase = 1
        self.ticks = 0
        self.heading = heading
        self.targetting = 0
        self.damage = 20

    def draw(self, screen):
        """
        A function which draws a standart enemy
        :param screen: a surface which image of a standart enemy will be drawn on
        :return: None
        """

        self.image = rot_center(enemy_image, self.angle * 360 / (-2 * math.pi) - 90)
        screen.blit(self.image, (self.x - 40, self.y - 40))

    def move(self):
        """
        A function which moves a standart enemy
        :return: None
        """
        self.angle = math.atan2(self.Vy, self.Vx)
        if self.y < settings.HEIGHT / 2 - 8:
            self.Vx += - self.heading * (self.Vx ** 2 + self.Vy ** 2) * math.sin(self.angle) / (
                    settings.HEIGHT / 2 + 100)
            self.Vy += self.heading * (self.Vx ** 2 + self.Vy ** 2) * math.cos(self.angle) / (settings.HEIGHT / 2 + 100)
            self.x += self.Vx
            self.y += self.Vy
        else:
            self.phase = 2

        if self.phase == 2:
            self.ticks += 1
            if self.ticks >= 30:
                self.phase = 3

        if self.phase == 3 and self.live >= 0:
            self.Vx += self.heading * (self.Vx ** 2 + self.Vy ** 2) * math.sin(self.angle) / (settings.HEIGHT / 2 + 100)
            self.Vy += - self.heading * (self.Vx ** 2 + self.Vy ** 2) * math.cos(self.angle) / (
                    settings.HEIGHT / 2 + 100)
            self.x += self.Vx
            self.y += self.Vy

    def shoot(self):
        """
        A function which makes a standart enemy shoot
        :return: None
        """
        if self.phase == 2:
            self.targetting = math.atan2(settings.spaceship.y - self.y, settings.spaceship.x - self.x)
            if self.ticks % settings.standart_enemy_bullet_firerate == 0:
                ammunition.cannons.play()
                new_bullet = ammunition.Bullet(levels.screen)
                new_bullet.damage = settings.standart_enemy_bullet_damage
                new_bullet.angle = self.targetting + random.randint(-10, 10) * 0.008
                new_bullet.x = self.x
                new_bullet.y = self.y
                new_bullet.vx = 50 * math.cos(new_bullet.angle)
                new_bullet.vy = 50 * math.sin(new_bullet.angle)
                settings.enemy_bullets.append(new_bullet)

    def hit_test(self, obj):
        """
        A function which tests collision of a standart enemy with a given object
        :param obj: an object which the collision will be tested with
        :return: bool, state of collision
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            settings.spaceship.hp -= self.damage
            settings.spaceship.hit_timer = 10
            print('standard hit' + str(settings.spaceship.hp))
            return True
        else:
            return False


class EnemyHeavy:
    def __init__(self):
        """
        Initialization function for the heavy enemy class
        """
        self.surface = None
        self.x = random.randint(70, settings.WIDTH - 70)
        self.y = -70
        self.Vx = 0
        self.Vy = 0
        self.live = 300
        self.image = heavy_image
        self.r = 60
        self.phase = 0
        self.angle = 0
        self.damage = 20
        self.ticks = 0

    def move(self):
        """
        A function which moves a heavy enemy
        :return: None
        """
        if self.phase == 0:
            self.Vy = 5
            self.y += self.Vy
            if self.y >= 300:
                self.phase = 1
        if self.phase == 1:
            self.angle += (math.atan2(settings.spaceship.x - self.x, settings.spaceship.y - self.y) - self.angle) / 30
        self.ticks += 1

    def draw(self, screen):
        """
        A function which draws a heavy enemy
        :param screen: a surface which image of a heavy enemy will be drawn on
        :return: None
        """
        if self.live > 0:
            self.image = rot_center_square(heavy_image, -self.angle * 360 / (-2 * math.pi) + 180)
            screen.blit(self.image, (self.x - 60, self.y - 60))

    def hit_test(self, obj):
        """
        A function which tests collision of a heavy enemy with a given object
        :param obj: an object which the collision will be tested with
        :return: bool, state of collision
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            settings.spaceship.hp -= self.damage
            settings.spaceship.hit_timer = 10
            print('heavy hit' + str(settings.spaceship.hp))
            return True
        else:
            return False

    def shoot(self):
        """
        A function which makes a heavy enemy launch rockets
        :return: None
        """
        if self.ticks % 180 == 0:
            for i in (-2, -1, 0, 1, 2):
                new_missile = EnemyMissile(self.x, self.y, self.angle + math.pi * i / 12)
                settings.enemies.append(new_missile)


class EnemyCarrier:
    def __init__(self):
        """
        Initialization function for the enemy carrier class
        """
        self.surface = None
        self.x = settings.WIDTH + 300
        self.y = 0
        self.Vx = 0
        self.Vy = 0
        self.live = 500
        self.image = carrier_image
        self.a = 190
        self.b = 300
        self.r = 90
        self.l = math.sqrt((settings.WIDTH / 2 + 300) ** 2 + (3 * settings.HEIGHT) ** 2)
        self.angle = math.atan2(settings.WIDTH / 2 + 300, 3 * settings.HEIGHT)
        self.phase = 1
        self.ticks = 0
        self.firing = 0
        self.damage = 100

    def move(self):
        """
        A function which moves an enemy carrier
        :return: None
        """
        if self.x >= -300:
            self.x = settings.WIDTH / 2 + self.l * math.sin(self.angle)
            self.y = -3 * settings.HEIGHT + self.l * math.cos(self.angle)
            self.angle -= 0.1 * 2 * math.pi / 360
        if self.x < -300:
            self.live = 0
        self.ticks += 1

    def draw(self, screen):
        """
        A function which draws an enemy carrier
        :param screen: a surface which image of an enemy carrier will be drawn on
        :return: None
        """
        if self.live > 0:
            self.image = rot_center_square(carrier_image, self.angle * 360 / (2 * math.pi) + 90)
            screen.blit(self.image, (self.x - 150, self.y - 150))
            # pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.r)

    def shoot(self):
        """
        A function which makes an enemy carrier launch kamikazes
        :return: None
        """
        if 0 < self.x < settings.WIDTH and self.ticks % 20 == 0:
            i = random.random()
            new_kamikaze = EnemyKamikaze()
            new_kamikaze.x = self.x + (i - 0.5) * 200 * math.cos(self.angle)
            new_kamikaze.y = self.y + (i - 0.5) * 200 * math.sin(self.angle)
            settings.enemies.append(new_kamikaze)

    def hit_test(self, obj):
        """
        A function which tests collision of an enemy carrier with a given object
        :param obj: an object which the collision will be tested with
        :return: bool, state of collision
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            settings.spaceship.hp -= self.damage
            settings.spaceship.hit_timer = 10
            print('carrier hit' + str(settings.spaceship.hp))
            return True
        else:
            return False


class EnemyKamikaze:
    def __init__(self):
        """
        Initialization function for the enemy kamikaze class
        """
        self.surface = None
        if random.randint(1, 2) == 1:
            self.x = -20
        else:
            self.x = settings.WIDTH + 20
        self.y = random.randint(15, settings.HEIGHT - 15)
        self.Vx = 0
        self.Vy = 0
        self.live = 1
        self.image = kamikaze_image
        self.angle = 0
        self.r = 22.5
        self.phase = 0
        self.damage = 50

    def draw(self, screen):
        """
        A function which draws a kamikaze
        :param screen: a surface which image of a kamikaze will be drawn on
        :return: None
        """
        if self.live > 0:
            self.image = rot_center(kamikaze_image, self.angle * 360 / (-2 * math.pi) - 90)
            screen.blit(self.image, (self.x - 15, self.y - 15))

    def move(self):
        """
        A function which moves an enemy kamikaze
        :return: None
        """
        self.angle = math.atan2(settings.spaceship.y - self.y, settings.spaceship.x - self.x)
        self.Vx = 12 * math.cos(self.angle)
        self.Vy = 12 * math.sin(self.angle)
        self.x += self.Vx
        self.y += self.Vy

    def hit_test(self, obj):
        """
        A function which tests collision of an enemy kamikaze with a given object
        :param obj: an object which the collision will be tested with
        :return: bool, state of collision
        """
        if (self.x - settings.spaceship.x) ** 2 + (self.y - settings.spaceship.y) ** 2 <= (
                self.r + settings.spaceship.r) ** 2:
            settings.spaceship.hp -= self.damage
            settings.spaceship.hit_timer = 10
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            print('kamikaze hit' + str(settings.spaceship.hp))
            return True
        else:
            return False

    def shoot(self):
        """
        A function inherent to all enemies which does nothing
        :return: None
        """
        pass


class Mine:
    def __init__(self):
        """
        Initialization function for the mine class
        """
        self.surface = None
        self.x = random.randint(25, settings.WIDTH - 25)
        self.y = -100
        self.Vx = 0
        self.Vy = 5
        self.live = 1
        self.image = mine_image
        self.r = 25
        self.phase = 0
        self.damage = 100

    def draw(self, screen):
        """
        A function which draws a mine
        :param screen: a surface which image of a mine will be drawn on
        :return: None
        """
        if self.live > 0:
            screen.blit(self.image, (self.x - 25, self.y - 25))

    def move(self):
        """
        A finction which moves a mine
        :return: None
        """
        self.y += self.Vy

    def hit_test(self, obj):
        """
        A function which tests collision of a mine with a given object
        :param obj: an object which the collision will be tested with
        :return: bool, state of collision
        """
        if (self.x - settings.spaceship.x) ** 2 + (self.y - settings.spaceship.y) ** 2 <= (
                self.r + settings.spaceship.r) ** 2:
            settings.spaceship.hp -= self.damage
            settings.spaceship.hit_timer = 10
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            print('mine hit' + str(settings.spaceship.hp))
            return True
        else:
            return False

    def shoot(self):
        """
        A function inherent to all enemies which does nothing
        :return:  None
        """
        pass


class EnemyMissile:
    def __init__(self, x, y, angle):
        """
        Initialization function for the enemy missile class
        :param x: initial x-coordinate of an enemy missile
        :param y: initial y-coordinate of an enemy missile
        :param angle: initial angle of an enemy missile
        """
        self.surface = None
        self.image = None
        self.x = x
        self.y = y
        self.r = 30
        self.angle = angle
        self.Vx = 15 * math.sin(self.angle)
        self.Vy = 15 * math.cos(self.angle)
        self.live = 1
        self.timer = 150
        self.damage = settings.enemy_missile_damage
        self.steering = 0
        self.phase = 0

    def move(self):
        """
        A function which moves an enemy missile
        :return: None
        """
        self.steering = math.atan2(settings.spaceship.x - self.x, settings.spaceship.y - self.y)
        x1 = math.cos(self.steering)
        y1 = math.sin(self.steering)

        for i in range(3):
            x0 = (math.cos(self.angle) + x1) / 2
            y0 = (math.sin(self.angle) + y1) / 2
            if x0 == 0 and y0 == 0:
                x0 = 0.1 * math.sin(self.steering)
                y0 = -0.1 * math.cos(self.steering)
            x1 = math.copysign(math.sqrt(1 / (1 + y0 ** 2 / x0 ** 2)), x0)
            y1 = math.copysign(math.sqrt(1 / (1 + x0 ** 2 / y0 ** 2)), y0)

        self.angle = math.atan2(y1, x1)
        self.Vx = 15 * math.sin(self.angle)
        self.Vy = 15 * math.cos(self.angle)
        self.x += self.Vx
        self.y += self.Vy

    def draw(self, screen):
        """
        A function which draws an enemy missile
        :param screen: a surface which image of a mine will be drawn on
        :return: None
        """
        if self.live > 0:
            self.surface = screen
            self.image = rot_center_square(missile_image, self.angle * 360 / (2 * math.pi) - 180)
            self.surface.blit(self.image, (self.x - 30, self.y - 30))

    def hit_test(self, obj):
        """
        A function which tests collision of an enemy missile with a given object
        :param obj: an object which the collision will be tested with
        :return: bool, state of collision
        """
        return (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2

    def shoot(self):
        """
        A function inherent to all enemies which does nothing
        :return:  None
        """
        pass


def init():
    """
    Initialization function which loads enemy sprites
    :return: None
    """
    global mine_image, kamikaze_image, enemy_image, heavy_image, missile_image, carrier_image
    mine_image = pygame.image.load(MINE_IMAGE_PATH).convert_alpha()
    mine_image = pygame.transform.scale(mine_image, (50, 50))
    kamikaze_image = pygame.image.load(KAMIKADZE_IMAGE_PATH).convert_alpha()
    kamikaze_image = pygame.transform.scale(kamikaze_image, (30, 45))
    enemy_image = pygame.image.load(ENEMY_IMAGE_PATH).convert_alpha()
    enemy_image = pygame.transform.scale(enemy_image, (100, 80))
    heavy_image = pygame.image.load(HEAVY_IMAGE_PATH).convert_alpha()
    heavy_image = pygame.transform.scale(heavy_image, (120, 120))
    missile_image = pygame.image.load(MISSILE_IMAGE_PATH).convert_alpha()
    missile_image = pygame.transform.scale(missile_image, (60, 60))
    carrier_image = pygame.image.load(CARRIER_IMAGE_PATH).convert_alpha()
    carrier_image = pygame.transform.scale(carrier_image, (300, 300))


def processing(screen):
    """
    A function which processes enemy actions
    :param screen: a surface which enemies will be drawn on
    :return: None
    """
    if settings.tick_counter % 60 == 0:
        new_mine = Mine()
        settings.enemies.append(new_mine)

    if settings.tick_counter % 120 == 0:
        new_kamikaze = EnemyKamikaze()
        settings.enemies.append(new_kamikaze)

    if settings.tick_counter % 240 == 0:
        heading = random.choice([-1, 1])
        for i in range(3):
            new_enemy = EnemyStandart(heading)
            settings.enemies.append(new_enemy)

    if settings.tick_counter % 600 == 0:
        new_heavy = EnemyHeavy()
        settings.enemies.append(new_heavy)

    if settings.tick_counter % 1200 == 0:
        new_carrier = EnemyCarrier()
        settings.enemies.append(new_carrier)

    for d in ammunition.death:
        if d.frame == 5:
            ammunition.death.remove(d)
        d.play()

    if settings.super_charge >= 100:
        settings.super_charge = 100

    for k in settings.enemies:
        if k.live <= 0:
            new_death = ammunition.DeathAnimation(k.x, k.y)
            ammunition.death.append(new_death)
            settings.enemies.remove(k)
            settings.coins.append(Coin(k.x, k.y, 100))
        if k.hit_test(settings.spaceship):
            k.live -= 50
        for b in settings.bullets:
            if b.hit_test(k):
                settings.bullets.remove(b)
                k.live -= settings.bullet_damage
        for p in settings.plasma_balls:
            indicator = 0
            if p.hit_test(k):
                for i in range(len(p.hit_by_plasma_ball)):
                    if p.hit_by_plasma_ball[i] == k:
                        indicator += 1
                if indicator == 0:
                    k.live -= settings.plasma_ball_damage
                    p.hit_by_plasma_ball.append(k)

        if ammunition.laser.hit_test(k):
            k.live -= settings.laser_damage
        for b in ammunition.light_rings:
            if b.hit_test(k):
                k.live = 0

    for k in settings.enemies:
        if k.live >= 1:
            k.move()
            k.draw(screen)
            k.shoot()
            if k.y >= settings.HEIGHT:
                settings.enemies.remove(k)

    for b in settings.enemy_bullets:
        b.draw()
        b.move()
        if b.hit_test(settings.spaceship):
            settings.spaceship.hp -= b.damage
            b.live = 0
            settings.spaceship.hit_timer = 10
        if b.timer <= 0:
            settings.enemy_bullets.remove(b)

    for c in settings.coins:
        c.move()
        c.draw(screen)
        c.hit_test()


def rot_center(image, angle):
    """
    Rotates an image around the center of it's rectangle
    :param image: an image which needs to be rotated
    :param angle: an angle to rotate
    :return:
    """
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


def rot_center_square(image, angle):
    """
    Rotates a square image around it's center
    :param image: an image which needs to be rotated
    :param angle: an angle to rotate
    :return:
    """
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image
