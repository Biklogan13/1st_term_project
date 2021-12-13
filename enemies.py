import pygame
import random
import settings
import ammunition
import math
import levels

kamikaze_image = None
mine_image = None
enemy_image = None
heavy_image = None
missile_image = None
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
        self.damage = 20

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

    def hittest(self, obj):
        if (self.x - obj.x)**2 + (self.y - obj.y)**2 <= (self.r + obj.r)**2:
            settings.spaceship.hp -= self.damage
            settings.spaceship.hit_timer = 10
            print('standard hit'+str(settings.spaceship.hp))
            return True
        else:
            return False


def death(self):
     for i in range(0, 5):
         levels.screen.blit(ammunition.blow[i], (self.x, self.y))


class Enemy_heavy:
    def __init__(self):
        self.surface = None
        self.x = random.randint(70, settings.WIDTH - 70)
        self.y = -70
        self.Vx = 0
        self.Vy = 0
        self.live = 200
        self.image = None
        self.r = 60
        self.phase = 0
        self.angle = 0
        self.damage = 20
        self.ticks = 0

    def move(self):
        if self.phase == 0:
            self.Vy = 5
            self.y += self. Vy
            if self.y >= 100:
                self.phase = 1
        if self.phase == 1:
            self.angle += (math.atan2(settings.spaceship.x - self.x, settings.spaceship.y - self.y) - self.angle) / 30
        self.ticks += 1

    def draw(self, screen):
        if self.live > 0:
            self.image = rot_center_square(heavy_image, -self.angle*360/(-2*math.pi) + 180)
            screen.blit(self.image, (self.x - 60, self.y - 60))

    def hittest(self, obj):
        if (self.x - obj.x)**2 + (self.y - obj.y)**2 <= (self.r + obj.r)**2:
            settings.spaceship.hp -= self.damage
            settings.spaceship.hit_timer = 10
            print('heavy hit'+str(settings.spaceship.hp))
            return True
        else:
            return False

    def shoot(self):
        if self.ticks % 180 == 0:
            for i in (-2, -1, 0, 1, 2):
                new_missile = Enemy_missile(self.x, self.y, self.angle + math.pi*i/12)
                settings.enemy_bullets.append(new_missile)




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
        self.damage = 50

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
        if (self.x - settings.spaceship.x) ** 2 + (self.y - settings.spaceship. y) ** 2 <= (self.r + settings.spaceship.r) ** 2:
            settings.spaceship.hp -= self.damage
            settings.spaceship.hit_timer = 10
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            print('kamikaze hit' + str(settings.spaceship.hp))
            return True
        else:
            return False

    def shoot(self):
        pass


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
        self.damage = 100

    def draw(self, screen):
        if self.live > 0:
            screen.blit(self.image, (self.x - 25, self.y - 25))

    def move(self):
        self.y += self.Vy

    def hittest(self, obj):
        if (self.x - settings.spaceship.x) ** 2 + (self.y - settings.spaceship. y) ** 2 <= (self.r + settings.spaceship.r) ** 2:
            settings.spaceship.hp -= self.damage
            settings.spaceship.hit_timer = 10
        if (self.x - obj.x)**2 + (self.y - obj.y)**2 <= (self.r + obj.r)**2:
            print('mine hit' + str(settings.spaceship.hp))
            return True
        else:
            return False

    def shoot(self):
        pass


class Enemy_missile():
    def __init__(self, x, y, angle):
        self.surface = None
        self.x = x
        self.y = y
        self.r = 30
        self.angle = angle
        self.Vx = 15*math.sin(self.angle)
        self.Vy = 15*math.cos(self.angle)
        self.live = 1
        self.timer = 150
        self.damage = 50

    def move(self):
        self.angle += (math.atan2(settings.spaceship.x - self.x, settings.spaceship.y - self.y) - self.angle) / 20
        self.Vx = 15 * math.sin(self.angle)
        self.Vy = 15 * math.cos(self.angle)
        self.x += self.Vx
        self.y += self.Vy

    def draw(self):
        if self.live > 0:
            self.surface = levels.screen
            self.image = rot_center_square(missile_image, self.angle * 360 / (2 * math.pi) - 180)
            self.surface.blit(self.image, (self.x - 30, self.y - 30))

    def hittest(self, obj):
        return (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2


def init():
    global mine_image, kamikaze_image, enemy_image, heavy_image, missile_image
    mine_image = pygame.image.load(settings.MINE_IMAGE_PATH).convert_alpha()
    mine_image = pygame.transform.scale(mine_image, (50, 50))
    kamikaze_image = pygame.image.load(settings.KAMIKADZE_IMAGE_PATH).convert_alpha()
    kamikaze_image = pygame.transform.scale(kamikaze_image, (30, 45))
    enemy_image = pygame.image.load(settings.ENEMY_IMAGE_PATH).convert_alpha()
    enemy_image = pygame.transform.scale(enemy_image, (100, 80))
    heavy_image = pygame.image.load(settings.HEAVY_IMAGE_PATH).convert_alpha()
    heavy_image = pygame.transform.scale(heavy_image, (120, 120))
    missile_image = pygame.image.load(settings.MISSILE_IMAGE_PATH).convert_alpha()
    missile_image = pygame.transform.scale(missile_image, (60, 60))


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


    if settings.tick_counter % 600 == 0:
        new_heavy = Enemy_heavy()
        settings.enemies.append(new_heavy)

    for d in ammunition.death:
        if d.frame == 5:
            ammunition.death.remove(d)
        d.play()


    for k in settings.enemies:
        if k.live <= 0:
            new_death = ammunition.death_animation(k.x, k.y)
            ammunition.death.append(new_death)
            settings.enemies.remove(k)
        if k.hittest(settings.spaceship):
            k.live -= 50
        for b in settings.bullets:
            if b.hittest(k):
                settings.bullets.remove(b)
                k.live -= settings.bullet_damage
        for p in settings.plasma_balls:
            if p.hittest(k):
                k.live -= settings.plasma_ball_damage
        if ammunition.laser.hittest(k):
            k.live -= settings.laser_damage
        for b in ammunition.lightrings:
            if b.hittest(k):
                k.live = 0

    for k in settings.enemies:
        if k.live >= 1:
            k.move()
            k.draw(screen)
            k.shoot()

    for b in settings.enemy_bullets:
        b.draw()
        b.move()
        if b.hittest(settings.spaceship):
            settings.spaceship.hp -= b.damage
            b.live = 0
            settings.spaceship.hit_timer = 10
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

def rot_center_square(image, angle):
    WIDTH = image.get_width()
    HEIGHT = image.get_height()
    orig_rect = image.get_rect() #width=min(WIDTH, HEIGHT), height=min(WIDTH, HEIGHT))
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    #print(orig_rect, rot_rect)
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

