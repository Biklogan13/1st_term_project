import pygame.mixer
import math
import pygame
import levels
import settings
import random
import os

laser = None
cannons = None
ult = 1
lightrings = []
light_ring_animation = []
objects_hit_by_laser = []
laser_min_hit = [3*settings.WIDTH, 0, 0, 0]
bullet_image, light_ring_image, plasma_ball_sprites = None, None, []

PLASMA_1_PATH = os.path.join('.', 'ammo_sprites', 'plasma_1.png')
PLASMA_2_PATH = os.path.join('.', 'ammo_sprites', 'plasma_2.png')
PLASMA_3_PATH = os.path.join('.', 'ammo_sprites', 'plasma_3.png')

PLASMA_BULLET_PATH = os.path.join('.', 'ammo_sprites', 'plasma_bullet.png')
LIGHT_RING_PATH = os.path.join('.', 'ammo_sprites', 'lightring.png')

LASER_SOUND_PATH = os.path.join('.', 'Sounds', 'LaserLaserBeam EE136601_preview-[AudioTrimmer.com].mp3')
CANNONS_SOUND_PATH = os.path.join('.', 'Sounds', 'ES_Cannon Blast 4.mp3')
PLASMAGUN_SOUND_PATH = os.path.join('.', 'Sounds', 'plasma_gun_powerup_01.mp3')
LIGHT_RING_SOUND_PATH = os.path.join('.', 'Sounds', 'Dio Brando - ZA WARUDO!.mp3')
EXPLOSION_SOUND = os.path.join('.', 'Sounds', 'explosion.mp3')

def init():
    global laser, cannons, laser_sound, plasma_gun_sound, light_ring_image, light_ring_sound, blow, death, explosion_sound

    death = []
    blow = []
    for i in range(1, 7):
        blow.append(pygame.image.load(os.path.join('.', 'blow', 'blow' + str(i) + '.png')))
    print(len(blow))

    plasma_ball_1 = pygame.image.load(PLASMA_1_PATH)
    plasma_ball_1.set_colorkey((255, 255, 255))
    plasma_ball_2 = pygame.image.load(PLASMA_2_PATH)
    plasma_ball_2.set_colorkey((255, 255, 255))
    plasma_ball_3 = pygame.image.load(PLASMA_3_PATH)
    plasma_ball_3.set_colorkey((255, 255, 255))
    plasma_ball_sprites = [plasma_ball_1, plasma_ball_2, plasma_ball_3]

    bullet_image = pygame.image.load(PLASMA_BULLET_PATH)
    bullet_image = pygame.transform.scale(bullet_image, (80, 40))
    settings.bullet_image = bullet_image

    light_ring_image = pygame.image.load(LIGHT_RING_PATH)
    light_ring_image.set_colorkey((255, 255, 255))
    settings.plasma_ball_sprites = plasma_ball_sprites

    pygame.mixer.init()
    explosion_sound = pygame.mixer.Sound(EXPLOSION_SOUND)
    laser_sound = pygame.mixer.Sound(LASER_SOUND_PATH)
    cannons = pygame.mixer.Sound(CANNONS_SOUND_PATH)
    plasma_gun_sound = pygame.mixer.Sound(PLASMAGUN_SOUND_PATH)
    light_ring_sound = pygame.mixer.Sound(LIGHT_RING_SOUND_PATH)
    pygame.mixer.Sound.set_volume(light_ring_sound, 10000000)
    pygame.mixer.Sound.set_volume(cannons, 0.02)
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
        """
        Constructor of the Bullet class.
        :param screen: surface where bullet is being drawn
        :param self.x: x coordinate of the bullet
        :param self.y: y coordinate of the bullet
        :param self.r: radius of the bullet
        :param self.vx: x velocity of the bullet
        :param self.vy: y velocity of the bullet
        :param self.timer: number of frames that  bullet can live
        :param self.damage: damage that bullet deals
        :param self.angle: angle of shot
        :param self.bullet: the surface with image on it
        """
        self.screen = screen
        self.x = settings.spaceship.x
        self.y = settings.spaceship.y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.angle = math.atan2(self.vy, self.vx)
        self.bullet = settings.bullet_image
        self.timer = 150
        self.damage = settings.bullet_damage

    def move(self):
        """Move the bullet after a unit of time.

         The method describes the movement of the bullet in one redraw frame. In other words, it updates the values
         self.x and self.y considering the rates of self.vx and self.vy.
        """
        self.timer -= 1
        if self.y >= 2 * settings.HEIGHT - self.r:
            self.vy = 0
            self.vx = 0
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        """
        Draws an image of a bullet with it's center in coordinates x,y
        """
        self.angle = math.atan2(self.vy, self.vx)
        self.bullet = rot_center(settings.bullet_image, self.angle * 360 / (-2 * math.pi))
        self.screen.blit(self.bullet, (self.x - self.r, self.y - self.r))

    def hittest(self, obj):
        """The function checks if the given object collides with the target described in the obj.

         Args:
             obj: The object to check for collision.
         Returns:
             Returns True if the bullet collides with the target. Returns False otherwise.
        """

        return (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2


class Laser:
    def __init__(self, screen: pygame.Surface):
        """
        Constructor of the Laser class.
        :param self.screen: surface where laser is being drawn
        :param self.angle: angle of the fire
        :param self.firing: firing indicator
        :param self.hitting:
        """
        self.screen = screen
        self.angle = 0

        self.firing = 0
        self.hitting = 0

    def fire_start(self):
        self.firing = 1

    def fire_end(self):
        self.firing = 0

    def draw(self):
        if self.hitting == 0:
            pygame.draw.line(self.screen, settings.RED, (settings.spaceship.x + 50 * math.cos(self.angle),
                             settings.spaceship.y + 50 * math.sin(self.angle) + 20), (
                             settings.spaceship.x + math.cos(self.angle) * 2 * settings.WIDTH,
                             settings.spaceship.y + math.sin(self.angle) * 2 * settings.WIDTH), width=20)
            pygame.draw.circle(self.screen, settings.RED, (settings.spaceship.x + 50 * math.cos(self.angle),
                               settings.spaceship.y + 50 * math.sin(self.angle) + 20), 12, 0)
            pygame.draw.line(self.screen, settings.ORANGE, (settings.spaceship.x + 50 * math.cos(self.angle),
                             settings.spaceship.y + 50 * math.sin(self.angle) + 20),
                             (settings.spaceship.x + math.cos(self.angle) * 2 * settings.WIDTH,
                             settings.spaceship.y + math.sin(self.angle) * 2 * settings.WIDTH), width=8)
            pygame.draw.circle(self.screen, settings.ORANGE, (settings.spaceship.x + 50 * math.cos(self.angle),
                               settings.spaceship.y + 50 * math.sin(self.angle) + 20), 4, 0)
            pygame.draw.line(self.screen, settings.YELLOW, (settings.spaceship.x + 50 * math.cos(self.angle),
                             settings.spaceship.y + 50 * math.sin(self.angle) + 20), (
                             settings.spaceship.x + math.cos(self.angle) * 2 * settings.WIDTH,
                             settings.spaceship.y + math.sin(self.angle) * 2 * settings.WIDTH), width=2)
            pygame.draw.circle(self.screen, settings.YELLOW, (settings.spaceship.x + 50 * math.cos(self.angle),
                               settings.spaceship.y + 50 * math.sin(self.angle) + 20), 1, 0)
        if self.hitting == 1:
            for obj in objects_hit_by_laser:
                if math.sqrt((obj.x - settings.spaceship.x)**2 + (obj.y - settings.spaceship.y)**2) <= laser_min_hit[0]\
                        and obj.live > 0:
                    laser_min_hit[0] = math.sqrt((obj.x - settings.spaceship.x)**2 + (obj.y - settings.spaceship.y)**2)
                    laser_min_hit[1] = obj.x
                    laser_min_hit[2] = obj.y
                    laser_min_hit[3] = obj.r

            pygame.draw.line(self.screen, settings.RED, (settings.spaceship.x + 50 * math.cos(self.angle),
                                                         settings.spaceship.y + 50 * math.sin(self.angle) + 20), (
                                 settings.spaceship.x + math.cos(self.angle) * laser_min_hit[0],
                                 settings.spaceship.y + math.sin(self.angle) * laser_min_hit[0]), width=20)
            pygame.draw.circle(self.screen, settings.RED, (settings.spaceship.x + 50 * math.cos(self.angle),
                                                           settings.spaceship.y + 50 * math.sin(self.angle) + 20), 12, 0)
            pygame.draw.line(self.screen, settings.ORANGE, (settings.spaceship.x + 50 * math.cos(self.angle),
                                                            settings.spaceship.y + 50 * math.sin(self.angle) + 20),
                             (settings.spaceship.x + math.cos(self.angle) * laser_min_hit[0],
                              settings.spaceship.y + math.sin(self.angle) * laser_min_hit[0]), width=8)
            pygame.draw.circle(self.screen, settings.ORANGE, (settings.spaceship.x + 50 * math.cos(self.angle),
                                                              settings.spaceship.y + 50 * math.sin(self.angle) + 20), 4, 0)
            pygame.draw.line(self.screen, settings.YELLOW, (settings.spaceship.x + 50 * math.cos(self.angle),
                                                            settings.spaceship.y + 50 * math.sin(self.angle) + 20), (
                                 settings.spaceship.x + math.cos(self.angle) * laser_min_hit[0],
                                 settings.spaceship.y + math.sin(self.angle) * laser_min_hit[0]), width=2)
            pygame.draw.circle(self.screen, settings.YELLOW, (settings.spaceship.x + 50 * math.cos(self.angle),
                                                              settings.spaceship.y + 50 * math.sin(self.angle) + 20), 1, 0)


    def targetting(self):
        """
        Changes firing angle to follow the cursor
        """
        self.angle = math.atan2((pygame.mouse.get_pos()[1] - settings.spaceship.y),
                                (pygame.mouse.get_pos()[0] - settings.spaceship.x))

    def hittest(self, obj):
        """
         The function checks if the laser gets the target described in the obj.

         Args:
             obj: The object to check for collision.
         Returns:
             Returns True if laser gets the target. Returns False otherwise.
        """
        if abs(math.sin(self.angle) * obj.x - math.cos(self.angle) * obj.y - math.sin(
                self.angle) * settings.spaceship.x + math.cos(self.angle) * settings.spaceship.y) <= 15 + obj.r and (
                pygame.mouse.get_pos()[0] - settings.spaceship.x) * (
                obj.x - settings.spaceship.x) > 0 and (
                pygame.mouse.get_pos()[1] - settings.spaceship.y) * (
                obj.y - settings.spaceship.y) > 0 and self.firing == 1:
            objects_hit_by_laser.append(obj)
            self.hitting = 0
            return True
        else:
            return False
            laser_min_hit = 3*settings.WIDTH
            self.hitting = 0


class Plasma_ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """
        Constructor of the Plasma_ball class.
        :param screen: surface where ball is being drawn
        :param self.x: x coordinate of the ball
        :param self.y: y coordinate of the ball
        :param self.r: radius of the ball
        :param self.vx: x velocity of the ball
        :param self.vy: y velocity of the ball
        :param self.timer: number of frames that  ball can live
        :param self.damage: damage that ball deals
        :param self.angle: angle of shot
        :param self.sprite_number: number of the frame if animation
        :param hitted: list of object that plasma ball have already hit
        :param self.surf: the surface with image on it
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
        self.hitted = []

    def move(self):
        """
        Move the ball after 1 frame.
        The method describes the movement of the bullet in one redraw frame. In other worlds, it updates the values
        self.x and self.y taking into account the velocities of self.vx and self.vy, changing frame of an animation
        every 10 in-game frames
        """
        self.x += self.vx
        self.y += self.vy
        self.timer -= 1
        if self.timer % 10 == 0:
            self.sprite_number += 1
            self.sprite_number = self.sprite_number % 2
            self.surf = pygame.transform.scale(settings.plasma_ball_sprites[self.sprite_number],
                                               (2 * self.r, 2 * self.r))

    def draw(self):
        """
        Draws a plasma ball with it's center coordinates x,y.
        """
        self.screen.blit(self.surf, (self.x - self.r, self.y - self.r))

    def hittest(self, obj):
        """
        The function checks if the ball collides with the target.
         Args:
             obj: target
         Returns:
             Returns True if the target and ball collide. Returns False otherwise.
        """
        return (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2


class Lightring:
    def __init__(self, screen):
        """
        Constructor of the class Lightring.
        :param self.screen: surface, where image is being drawn
        :param self.x: x coordinate of the lightring center
        :param self.y: y coordinate of the lightring center
        :param self.r: lightring's radius
        :param self.v: lightring's velocity
        :param self.surf: image of the ring
        :param self.timer: number of frames that lightring lives
        :param self.k: animation frame number
        """
        self.screen = levels.screen
        self.x = settings.spaceship.x
        self.y = settings.spaceship.y
        self.r = 100
        self.v = 10
        self.surf = pygame.transform.scale(light_ring_image, (self.r, self.r))
        self.timer = 100
        self.k = 0

    def move(self):
        """
        widens radius of the ring and changes the frame of animation.
        """
        self.r += self.v
        self.surf = light_ring_animation[self.k]
        self.timer -= 1
        self.k += 1

    def draw(self):
        """
        draws ring on the screen.
        """
        self.screen.blit(self.surf, (self.x - self.r / 2, self.y - self.r / 2))

    def hittest(self, obj):
        """
        Checks collision with the target.
        :param obj: target
        :return: True if collision passed, otherwise returns False
        """
        return (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r - 500 + obj.r) ** 2


class death_animation:
    def __init__(self, x, y):
        """
        death animation class constructor
        :param self.x: x coordinate of death animation
        :param self.y: y coordinate of death animation
        :param self.frame: number of frame in animation
        """
        self.x = x - 150
        self.y = y - 150
        self.frame = 0
        explosion_sound.play()

    def play(self):
        """
        changes frames of animation every 2 frames
        """
        levels.screen.blit(blow[self.frame], (self.x, self.y))
        if settings.tick_counter % 2 == 0:
            self.frame += 1


def rot_center(image, angle):
    """
    Rotates relative to the center of the image
    :param image: original image
    :param angle: angle of rotation
    :return: rotated image
    """
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


def processing(screen, events):
    """
    includes all allies shooting mechanics.
    ult 1 is lightring
    ult 2 if teleport
    :param screen:
    :param events:
    :return:
    """
    global cannons, ult

    for b in settings.bullets:
        b.draw()
        b.move()
        if b.timer <= 0:
            settings.bullets.remove(b)

    if settings.ammo == 0:
        if settings.seconds == settings.bullets_firerate:
            cannons.play()
        if settings.seconds > settings.bullets_firerate:
            new_bullet = Bullet(levels.screen)
            new_bullet.angle = math.atan2(
                (pygame.mouse.get_pos()[1] - settings.spaceship.y),
                (pygame.mouse.get_pos()[0] - settings.spaceship.x)) + random.randint(-10, 10) * 0.008
            new_bullet.vx = 50 * math.cos(new_bullet.angle)
            new_bullet.vy = 50 * math.sin(new_bullet.angle)
            new_bullet.x = settings.spaceship.x + 100 * math.cos(new_bullet.angle) - 20
            new_bullet.y = settings.spaceship.y + 100 * math.sin(new_bullet.angle)
            settings.bullets.append(new_bullet)
            settings.seconds = 0

    for b in settings.plasma_balls:
        b.draw()
        b.move()
        if b.timer <= 0:
            settings.plasma_balls.remove(b)
    if settings.ammo == 1:
        if settings.seconds == 1:
            plasma_gun_sound.play()
        if settings.seconds > settings.plasma_balls_firerate:
            new_ball = Plasma_ball(levels.screen)
            new_ball.angle = math.atan2(
                (pygame.mouse.get_pos()[1] - settings.spaceship.y),
                (pygame.mouse.get_pos()[0] - settings.spaceship.x)) + random.randint(-10, 10) * 0.008
            new_ball.vx = 10 * math.cos(new_ball.angle)
            new_ball.vy = 10 * math.sin(new_ball.angle)
            new_ball.x = settings.spaceship.x + 100 * math.cos(new_ball.angle) - 20
            new_ball.y = settings.spaceship.y + 100 * math.sin(new_ball.angle)
            settings.plasma_balls.append(new_ball)
            settings.seconds = 0

    if settings.ammo == 2:
        laser.fire_start()
        laser.angle = math.atan2((pygame.mouse.get_pos()[1] - settings.spaceship.y),
                                 (pygame.mouse.get_pos()[0] - settings.spaceship.x))
        laser.draw()
    else:
        laser.fire_end()

    for b in lightrings:
        b.draw()
        b.move()
        if b.timer <= 0:
            lightrings.remove(b)

    for event in events:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if settings.current_skin.super == 0:
                new_lightring = Lightring(levels.screen)
                new_lightring.v = 30
                lightrings.append(new_lightring)
                light_ring_sound.play()
            elif settings.current_skin.super == 1:
                settings.spaceship.x = pygame.mouse.get_pos()[0]
                settings.spaceship.y = pygame.mouse.get_pos()[1]
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            settings.ammo = levels.ammo_type
            settings.seconds = 0
            if  levels.ammo_type == 2:
                laser_sound.play()
        elif event.type == pygame.MOUSEBUTTONUP:
            settings.ammo = None
            laser_sound.stop()

    settings.seconds += 1
