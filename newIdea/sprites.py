
import pygame as pg
import random
from settings import *
vec = pg.math.Vector2



class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.player_img
       # self.image = pg.transform.scale(self.image, (90, 60))
        #self.image = pg.Surface((50,50))
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *.70 / 2)
        #pg.draw.circle(self.image, RED, self.rect.center, self.radius) ## for collision dev
        self.pos = vec(game.WIDTH / 2, game.HEIGHT - 200)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.last_update = 0
        self.bullet_rate = BULLET_RATE
        self.bullet_count = BULLET_COUNT
        self.health = PLAYER_HEALTH
        self.last_death = pg.time.get_ticks()

    def add_health(self, amount):
        self.health += amount
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH

    def add_speed_bullet(self, amount):
        self.bullet_rate -= amount
        if self.bullet_rate < MIN_BULLET_RATE:
            self.bullet_rate = MIN_BULLET_RATE

    def add_bullet_amount(self):
        self.bullet_count += 1
        if self.bullet_count > 5:
            self.bullet_count = 5

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.bullet_rate:
            self.last_update = now
            self.game.shoot_snd.play()
            if self.bullet_count == 1:
                self.bullet = Bullet(self.game, self.rect.centerx, self.rect.top, 1, self.game.player_bullets, 0)
            if self.bullet_count == 2:
                self.bullet = Bullet(self.game, self.rect.left + 2, self.rect.top, 1, self.game.player_bullets, 0)
                self.bullet = Bullet(self.game, self.rect.right - 2, self.rect.top, 1, self.game.player_bullets, 0)
            if self.bullet_count == 3:
                self.bullet = Bullet(self.game, self.rect.left + 2, self.rect.top, 1, self.game.player_bullets, 0)
                self.bullet = Bullet(self.game, self.rect.right - 2, self.rect.top, 1, self.game.player_bullets, 0)
                self.bullet = Bullet(self.game, self.rect.centerx, self.rect.top - 4, 1, self.game.player_bullets, 0)
            if self.bullet_count == 4:
                self.bullet = Bullet(self.game, self.rect.left , self.rect.top, 1, self.game.player_bullets, 0)
                self.bullet = Bullet(self.game, self.rect.centerx -20, self.rect.top -10, 1, self.game.player_bullets, 0)
                self.bullet = Bullet(self.game, self.rect.right , self.rect.top, 1, self.game.player_bullets, 0)
                self.bullet = Bullet(self.game, self.rect.centerx +20, self.rect.top - 10, 1, self.game.player_bullets, 0)
            if self.bullet_count > 4:
                self.bullet = Bullet(self.game, self.rect.left, self.rect.top, 1, self.game.player_bullets, 0)
                self.bullet = Bullet(self.game, self.rect.centerx - 20, self.rect.top - 10, 1, self.game.player_bullets, 0)
                self.bullet = Bullet(self.game, self.rect.right, self.rect.top, 1, self.game.player_bullets, 0)
                self.bullet = Bullet(self.game, self.rect.centerx + 20, self.rect.top - 10, 1, self.game.player_bullets, 0)
                self.bullet = Bullet(self.game, self.rect.centerx, self.rect.top - 25, 1, self.game.player_bullets, 0)


    def limit_velocity(self, max_vel):
        min(-max_vel, max(self.vel.x, max_vel))
        min(-max_vel, max(self.vel.y, max_vel))
        if abs(self.vel.x) < .01:
            self.vel.x = 0
        if abs(self.vel.y) < .01:
            self.vel.y = 0


    def update(self):
        self.acc = vec(0, 0)  # Every time let the acceleration be 0 for easy updating
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:  # Click left button
            self.acc.x = -PLAYER_ACC  #
        if keys[pg.K_RIGHT]:  # right-button
            self.acc.x = PLAYER_ACC
        if keys[pg.K_UP]: # up-button
            self.acc.y = -PLAYER_ACC
        if keys[pg.K_DOWN]: # down-button
            self.acc.y = PLAYER_ACC
        if keys[pg.K_SPACE]: #space-button
            self.shoot()

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION  # Acceleration minus the acceleration provided by friction (easy to stop when not pressing)
        self.acc.y += self.vel.y * PLAYER_FRICTION  # Acceleration minus the acceleration provided by friction (easy to stop when not pressing)

        # equations of motion
        self.vel.x += self.acc.x * self.game.dt # *Time 1
        self.vel.y += self.acc.y * self.game.dt
        self.limit_velocity(2)

        self.pos.x += self.vel.x * self.game.dt + (0.5 * self.acc.x) * self.game.dt **2  # v0t + 1/2 A t^2
        self.pos.y += self.vel.y * self.game.dt + (0.5 * self.acc.y) * self.game.dt **2  # v0t + 1/2 A t^2

        if self.pos.x > self.game.WIDTH - self.rect.width / 2:
            self.pos.x = self.game.WIDTH - self.rect.width / 2
        if self.pos.x < self.rect.width / 2:
            self.pos.x = self.rect.width / 2
        if self.pos.y > self.game.HEIGHT - self.rect.height / 2:
            self.pos.y = self.game.HEIGHT - self.rect.height / 2

        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y


class Asteroid(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = ENEMY_LAYER
        self.groups = game.all_sprites, game.asteroids
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_orig = random.choice(self.game.asteroid_imgs)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *.35 / 2)
        #pg.draw.circle(self.image, RED, self.rect.center, self.radius)  ## for collision dev
        self.rect.x = random.randrange(0, game.WIDTH - self.rect.width)
        self.rect.y = random.randrange(-1500, -900)
        self.speedy = SPEED_Y
        self.speedx = SPEED_X
        self.rot = 0
        self.rot_speed = ROTATION_SPEED
        self.last_update = pg.time.get_ticks()
        self.health = 25

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > ROTATION_RATE:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
            new_image = pg.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


    def update(self):
        self.rotate()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > self.game.HEIGHT + 100 or self.rect.right < -100 or self.rect.left > self.game.WIDTH + 100:
            self.rect.x = random.randrange(0, self.game.WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)




class Bullet(pg.sprite.Sprite):
    def __init__(self,game, x, y, dir, group, img):
        self._layer = ENEMY_LAYER
        self.groups = game.all_sprites, group
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.bullet_imgs[img]
        #self.image = pg.Surface((10,20))
        #self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        self.rect.bottom = y
        self.rect.centerx = x
        self.vely_p = -30
        self.vely_a = -15
        self.dir = dir
        self.damage = 25


    def update(self):
        if self.dir == 1:
            self.rect.y += self.vely_p * self.dir * self.game.dt
        if self.dir == -1:
            self.rect.y += self.vely_a * self.dir * self.game.dt
        if self.rect.bottom < -5 or self.rect.bottom > self.game.HEIGHT + 5:
            self.kill()

class Booster1(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = BOOSTER_LAYER
        self.groups = game.all_sprites, game.booster1
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.booster_imgs[1]
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width  / 2)
        self.rect.x = random.randrange(0, game.WIDTH - self.rect.width)
        self.rect.y = -5
        self.vel_y = 5

    def update(self):
        self.rect.y += self.vel_y * self.game.dt
        if self.rect.y > self.game.HEIGHT + 20:
            self.kill()

class Booster2(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = BOOSTER_LAYER
        self.groups = game.all_sprites, game.booster2
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.booster_imgs[0]
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        self.rect.x = random.randrange(0, game.WIDTH - self.rect.width)
        self.rect.y = -5
        self.vel_y = 5

    def update(self):
        self.rect.y += self.vel_y * self.game.dt
        if self.rect.y > self.game.HEIGHT + 20:
            self.kill()

class Booster3(pg.sprite.Sprite): # health
    def __init__(self, game, center):
        self._layer = BOOSTER_LAYER
        self.groups = game.all_sprites, game.booster3
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.booster_imgs[2]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.radius = int(self.rect.width / 2)
        self.vel_y = 5

    def update(self):
        self.rect.y += self.vel_y * self.game.dt
        if self.rect.y > self.game.HEIGHT + 20:
            self.kill()


class ShipDmg(pg.sprite.Sprite):
    def __init__(self, game, center, size):
        self._layer = EFFECT_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.size = size
        self.image = self.game.damage_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.game.damage_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.game.damage_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Explosion(pg.sprite.Sprite):
    def __init__(self, game, center, size):
        self._layer = ENEMY_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.size = size
        self.image = self.game.explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 20


    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.game.explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.game.explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Alien(pg.sprite.Sprite):
    def __init__(self, game, x, y, max_height, dirx):
        self._layer = ENEMY_LAYER
        self.groups = game.all_sprites, game.aliens
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.alien_img
        self.image = pg.transform.scale(self.image, (100, 80))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        self.pos = vec(x,y)
        self.rect.x = x
        self.rect.y = y
        self.max_height = max_height
        self.vel_x = VEL_X * dirx
        self.vel_y = VEL_Y
        self.last_update = 0
        self.bullet_rate = random.randrange(500, 2500)
        self.health = 25


    def update(self):

        self.pos.x += self.vel_x * self.game.dt
        self.pos.y += self.vel_y * self.game.dt

        if self.pos.y > self.max_height:
            self.pos.y = self.max_height
            self.shoot()
        if self.pos.x > self.game.WIDTH + 300:
            self.pos.x = 0
        if self.pos.x < -300:
            self.pos.x = self.game.WIDTH + 300
        self.rect.center = self.pos

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.bullet_rate:
            self.last_update = now
            # self.game.shoot_snd.play()
            self.bullet = Bullet(self.game, self.rect.centerx, self.rect.bottom +50, -1, self.game.alien_bullets, 1)

class BackStars(pg.sprite.Sprite):
    def __init__(self, game, x, y, dir, alpha, size, color):
        self._layer = STARS_LAYER
        self.groups = game.all_sprites, game.stars
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((size,size))
        self.image.fill(color)
        self.image.set_alpha(alpha)
        self.rect = self.image.get_rect()
        self.dir = dir
        self.rect.centerx = x
        self.rect.centery = y
        self.vel_y = 5
        self.vel_x = random.randrange(1, 5)

    def update(self):
        self.rect.centery += self.vel_y * self.game.dt
       # self.rect.centerx += self.vel_x * self.game.dt * self.dir
        if self.rect.top > self.game.HEIGHT:
            self.kill()


class MotherShip(pg.sprite.Sprite):
    def __init__(self, game, player):
        self._layer = ENEMY_LAYER
        self.groups = game.all_sprites, game.bosses
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.player  = player
        self.image = pg.Surface((150, 150))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = self.game.WIDTH / 2
        self.rect.y = -1000
        self.health = 1500
        self.vel_x = 1
        self.vel_y = 1
        self.dir = 1

    def update(self):
        self.rect.centery += self.vel_y * self.game.dt
        if self.rect.centery >= self.game.HEIGHT/2:
            self.vel_y = 0
            self.rect.centerx += self.vel_x * self.dir * self.game.dt
            if self.vel_x > 0 and self.rect.right >= self.game.WIDTH - 500:
                self.dir *= -1
            if self.vel_x < 0 and self.rect.left <= 500:
                self.dir *= -1

