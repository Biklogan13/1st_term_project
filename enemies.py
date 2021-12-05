import pygame
import random
import settings
import ammunition
import math
import levels

kamikaze_image = None
mine_image = None
enemy_image = None
enemy_counter = 0

class Enemy_standart:
    def __init__(self, heading):
        self.surface = None
        if heading == 1:
            self.x = random.randint(settings.HEIGHT/2 + 100 + 50, settings.WIDTH + settings.HEIGHT/2 + 100 - 50)
        else:
            self.x = random.randint(-settings.HEIGHT/2 - 100 + 50, settings.WIDTH - settings.HEIGHT/2 - 100 - 50)
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

    def draw(self, screen):

            self.image = rot_center(enemy_image, self.angle*360/(-2*math.pi) - 90)
            screen.blit(self.image, (self.x - 40, self.y - 40))

    def move(self):

            self.angle = math.atan2(self.Vy, self.Vx)
            if self.y < settings.HEIGHT/2 - 8:
                self.Vx += - self.heading*(self.Vx**2 + self.Vy**2) * math.sin(self.angle) / (settings.HEIGHT/2 + 100)
                self.Vy += self.heading*(self.Vx**2 + self.Vy**2) * math.cos(self.angle) / (settings.HEIGHT/2 + 100)
                self.x += self.Vx
                self.y += self.Vy
            else:
                self.phase = 2

            if self.phase == 2:
                self.ticks += 1
                if self.ticks >= 30:
                    self.phase = 3

            if self.phase == 3 and self.live >= 0:
                self.Vx += self.heading*(self.Vx ** 2 + self.Vy ** 2) * math.sin(self.angle) / (settings.HEIGHT / 2 + 100)
                self.Vy += - self.heading*(self.Vx ** 2 + self.Vy ** 2) * math.cos(self.angle) / (settings.HEIGHT / 2 + 100)
                self.x += self.Vx
                self.y += self.Vy

            if self.y >= settings.HEIGHT:
                self.live = 0

    def shoot(self):
        self.targetting = math.atan2(settings.spaceship.y - self.y, settings.spaceship.x - self.x)
        if self.ticks % settings.bullets_firerate == 0:
            new_bullet = ammunition.Bullet(levels.screen)
            new_bullet.angle = self.targetting + random.randint(-10, 10) * 0.008
            new_bullet.x = self.x
            new_bullet.y = self.y
            new_bullet.vx = 50 * math.cos(new_bullet.angle)
            new_bullet.vy = 50 * math.sin(new_bullet.angle)
            settings.enemy_bullets.append(new_bullet)

    def hittest(self, obj):
        if (self.x - obj.x)**2 + (self.y - obj.y)**2 <= (self.r + obj.r)**2:
            return True
        else:
            return False

class Enemy_heavy:
    def __init__(self):
        self.surface = None
        self.x = 0
        self.y = 0
        self.Vx = 0
        self.Vy = 0
        self.live = 100
        self.image = None
        self.r = 0
        self.phase = 0

class Enemy_kamikaze:
    def __init__(self):
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

    def draw(self, screen):
        if self.live > 0:
            self.image = rot_center(kamikaze_image, self.angle*360/(-2*math.pi) - 90)
            screen.blit(self.image, (self.x - 15, self.y - 15))

    def move(self):
        self.angle = math.atan2(settings.spaceship.y - self.y, settings.spaceship.x - self.x)
        self.Vx = 12*math.cos(self.angle)
        self.Vy = 12*math.sin(self.angle)
        self.x += self.Vx
        self.y += self.Vy

    def hittest(self, obj):
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            return True
        else:
            return False

class Mine:
    def __init__(self):
        self.surface = None
        self.x = random.randint(25, settings.WIDTH - 25)
        self.y = -100
        self.Vx = 0
        self.Vy = 5
        self.live = 1
        self.image = mine_image
        self.r = 25
        self.phase = 0

    def draw(self, screen):
        if self.live > 0:
            screen.blit(self.image, (self.x - 25, self.y - 25))

    def move(self):
        self.y += self.Vy

    def hittest(self, obj):
        if (self.x - obj.x)**2 + (self.y - obj.y)**2 <= (self.r + obj.r)**2:
            return True
        else:
            return False

def init():
    global mine_image, kamikaze_image, enemy_image
    mine_image = pygame.image.load('enemy_skins/mine.png').convert_alpha()
    mine_image = pygame.transform.scale(mine_image, (50, 50))
    kamikaze_image = pygame.image.load('enemy_skins/kamikaze.PNG').convert_alpha()
    kamikaze_image = pygame.transform.scale(kamikaze_image, (30, 45))
    enemy_image = pygame.image.load('enemy_skins/enemy.PNG').convert_alpha()
    enemy_image = pygame.transform.scale(enemy_image, (100, 80))

def processing(screen):
    global enemy_counter
    if settings.tick_counter % 60 == 0:
        new_mine = Mine()
        #nemy_counter += 1
        #if len(settings.enemies) < 100:
        settings.enemies.append(new_mine)
        #else:
        #settings.enemies[enemy_counter % 100] = new_mine
    if settings.tick_counter % 120 == 0:
        new_kamikaze = Enemy_kamikaze()
        #enemy_counter += 1
        #if len(settings.enemies) < 100:
        settings.enemies.append(new_kamikaze)
        #else:
        #settings.enemies[enemy_counter % 99] = new_kamikaze

    if settings.tick_counter % 240 == 0:
        heading = random.choice([-1, 1])
        for i in range(3):
            new_enemy = Enemy_standart(heading)
            settings.enemies.append(new_enemy)

    for k in settings.enemies:
        if k.live <= 0:
            settings.enemies.remove(k)
        if k.hittest(settings.spaceship):
            k.live -= 50
        for b in settings.bullets:
            if k.hittest(b):
                settings.bullets.remove(b)
                k.live -= 20
        for p in settings.plasma_balls:
            if k.hittest(p):
                k.live -= 100
        if ammunition.laser.hittest(k):
            k.live -= 1
        for b in ammunition.lightrings:
            if b.hittest(k):
                k.live = 0

    for k in settings.enemies:
        if k.live >= 1:
            k.move()
            k.draw(screen)
            if k.phase == 2:
                k.shoot()

    for b in settings.enemy_bullets:
        b.draw()
        b.move()
        if b.timer <= 0:
            settings.enemy_bullets.remove(b)

def rot_center(image, angle):
    WIDTH = image.get_width()
    HEIGHT = image.get_height()
    orig_rect = image.get_rect() #width=min(WIDTH, HEIGHT), height=min(WIDTH, HEIGHT))
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect()
    rot_rect.center = rot_image.get_rect().center
    #print(orig_rect, rot_rect)
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image