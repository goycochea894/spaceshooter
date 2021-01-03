import random
import pygame as pg

# game options/settings
TITLE = 'SpaceJam'


FPS = 60
FONT_NAME = 'arial'

#define colors
WHITE = (255,255,255)
BLACK = (0 ,0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 140, 140)
LIGHTORANGE = (255, 229, 204)
RED2 = (95, 0, 0)
BGCOLOR = LIGHTBLUE
STAR_COLORS = [(255, 183, 14),(255, 255, 255), (181, 58, 5)]


#Layers
PLAYER_LAYER = 3
BOOSTER_LAYER = 1
ENEMY_LAYER = 2
EFFECT_LAYER = 4
STARS_LAYER = 0

# Asteroid settings
ROTATION_RATE = 30
SPEED_Y = random.randrange(1, 3)
SPEED_X = random.randrange(-3, 3)
ROTATION_SPEED = random.randrange(-10, 10)

# Alien settings
VEL_Y = random.randrange(3, 5)
VEL_X = VEL_Y
BULLET_RATE_A = 1500
A_BULLET_KNOCKBACK = 10

# boosters settings
HEALTH_UP_AMOUNT = 25
BULLET_RATE_AMOUNT = 50
MAX_BULLET_COUNT = 5

#Player settings
BULLET_RATE = 500
MIN_BULLET_RATE = 150
BULLET_COUNT = 1
PLAYER_HEALTH = 100
PLAYER_ACC = 1.4
PLAYER_FRICTION = -0.12

# boosters settings
BOOSTER1_RATE = random.randrange(15000, 30000)
BOOSTER2_RATE = random.randrange(15000, 30000)


# load images
ASTEROIDS_IMG = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png', '9.png', '10.png', '11.png',
                 '12.png', '13.png', '14.png', '15.png', '16.png', '17.png', '18.png', '19.png', '20.png', '21.png', '22.png',]
BULLETS_IMG = ['laserRed16.png', 'enemy_bullet.png']
BOOSTERS_IMG = ['bolt_bronze.png', 'bolt_gold.png', 'powerupGreen_star.png']
EXPLOSION_IMG = ['exp1.png','exp2.png','exp3.png','exp4.png','exp5.png','exp6.png','exp7.png',
                 'exp8.png','exp9.png''exp10.png','exp11.png','exp12.png','exp13.png','exp14.png']




