
import pygame as pg
from settings import *
from sprites import *
from os import path

def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGHT = 300
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGHT
    outline_rect = pg.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 1, 2048)
        pg.init()
        self.screen_size = pg.display.Info()
        self.WIDTH = self.screen_size.current_w
        self.HEIGHT = self.screen_size.current_h
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.last_boost1 = pg.time.get_ticks()
        self.last_boost2 = pg.time.get_ticks()
        self.next_boost1 = 0
        self.next_boost2 = 0
        self.kills = 0


    def load_data(self):
        self.img_dir = path.join(path.dirname(__file__), 'img')
        self.exp_img_dir = path.join(path.dirname(__file__), 'explosions')
        self.asteroids_dir = path.join(path.dirname(__file__), 'asteroids')
        self.sound_dir = path.join(path.dirname(__file__), 'snd')
        self.bg_img = pg.image.load(path.join(self.img_dir, "dark-space.jpg")).convert_alpha()
        self.bg_img = pg.transform.scale(self.bg_img, (self.WIDTH, self.HEIGHT))
        self.bg_rect = self.bg_img.get_rect()
        self.player_img = pg.image.load(path.join(self.img_dir, 'spaceshipnew.png')).convert_alpha()
        self.alien_img = pg.image.load(path.join(self.img_dir, 'enemy1.png')).convert_alpha()

        # load sound effects
        self.shoot_snd = pg.mixer.Sound(path.join(self.sound_dir, 'laser-gun.wav'))
        self.shoot_snd.set_volume(0.09)
        self.explosion_snd = pg.mixer.Sound(path.join(self.sound_dir, 'explosion.flac'))
        self.explosion_snd.set_volume(0.09)
        self.healthup_snd = pg.mixer.Sound(path.join(self.sound_dir, 'health_pack.wav'))
        self.player_hit_snd = pg.mixer.Sound(path.join(self.sound_dir, 'falling-hit.wav'))
        self.player_hit_snd.set_volume(0.03)
        self.s_booster_snd = pg.mixer.Sound(path.join(self.sound_dir, 'sfx_zap.ogg'))
        self.b_booster_snd = pg.mixer.Sound(path.join(self.sound_dir, 'sfx_twoTone.ogg'))


        # asteroids images
        self.asteroid_imgs = []
        for img in ASTEROIDS_IMG:
            self.asteroid_imgs.append(pg.image.load(path.join(self.asteroids_dir, img)).convert_alpha())


        # bullet images
        self.bullet_imgs = []
        for img in BULLETS_IMG:
            self.bullet_imgs.append(pg.image.load(path.join(self.img_dir, img)).convert_alpha())

        # booster images
        self.booster_imgs = []
        for img in BOOSTERS_IMG:
            self.booster_imgs.append(pg.image.load(path.join(self.img_dir, img)).convert_alpha())

        # explosions img
        self.explosion_anim = {}
        self.explosion_anim['lg'] = []
        self.explosion_anim['sm'] = []
        for img in range(14):
            filename = 'exp{}.png'.format(img)
            img = pg.image.load(path.join(self.exp_img_dir, filename)).convert_alpha()
            img_lg = pg.transform.scale(img, (105, 105))
            self.explosion_anim['lg'].append(img_lg)
            img_sm = pg.transform.scale(img, (32, 32))
            self.explosion_anim['sm'].append(img_sm)

        # damage images
        self.damage_anim = {}
        self.damage_anim['pl'] = []
        for img in range(3):
            fname = 'playerShip1_damage{}.png'.format(img)
            img = pg.image.load(path.join(self.img_dir, fname)).convert_alpha()
            img_sized = pg.transform.scale(img, (85, 85))
            self.damage_anim['pl'].append(img_sized)


    def new(self):
        self.kills = 0
        self.dead = False
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.asteroids = pg.sprite.Group()
        self.player_bullets = pg.sprite.Group()
        self.alien_bullets = pg.sprite.Group()
        self.booster1 = pg.sprite.Group()
        self.booster2 = pg.sprite.Group()
        self.booster3 = pg.sprite.Group()
        self.aliens = pg.sprite.Group()
        self.stars = pg.sprite.Group()
        self.bosses = pg.sprite.Group()
        self.player = Player(self)
        pg.mixer.music.load(path.join(self.sound_dir, 'through_space.ogg'))

        #Spawn 1 asteroid for start
        for i in range(1):
            self.asteroid = Asteroid(self)

        #Spawn row 1 aliens
        for x in range(5):
            y_pos = random.randrange(-900, -200)
            x_pos = random.randrange(60, self.WIDTH - 60)
            self.alien = Alien(self, x_pos, y_pos, self.HEIGHT/4, -1)
        #Spawn row2 aliens
        for x in range(5):
            y_pos = random.randrange(-900, -200)
            x_pos = random.randrange(60, self.WIDTH - 60)
            self.alien = Alien(self, x_pos, y_pos, self.HEIGHT/8, 1)

        # spawn stars
        for x in range(500):
            y_pos = random.randrange(-400, self.HEIGHT)
            x_pos = random.randrange(0, self.WIDTH)
            BackStars(self,x_pos, y_pos, random.choice([1, -1]),
                      random.choice([60, 70, 80, 90, 100]), random.choice([4, 3, 2, 1, 0.5, 0.2, 0.1, 0.3, 0.4, 0.6]), random.choice(STAR_COLORS))
        self.run()


    def run(self):
        # Game loop
        pg.mixer.music.set_volume(0.06)
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) * .001 * FPS
            self.events()
            self.update()
            self.draw()


    def update(self):
        self.all_sprites.update()

        #spawn more stars:
        current_stars = []
        for star in self.stars:
            current_stars.append(star)
        if len(current_stars) < 500:
            y_pos = random.randrange(-900, -200)
            x_pos = random.randrange(0, self.WIDTH)
            BackStars(self, x_pos, y_pos, random.choice([1, -1]),
                      random.choice([60, 70, 80, 90, 100]), random.choice([4, 3, 2, 1, 0.5, 0.2, 0.1, 0.3, 0.4, 0.6]), random.choice(STAR_COLORS))

        # player hit booster
        boost1_hits = pg.sprite.spritecollide(self.player, self.booster1, False, pg.sprite.collide_circle)
        for hit in boost1_hits:
            if boost1_hits and self.player.bullet_rate > MIN_BULLET_RATE:
                self.s_booster_snd.play()
                hit.kill()
                self.player.add_speed_bullet(BULLET_RATE_AMOUNT)

        boost2_hits = pg.sprite.spritecollide(self.player, self.booster2, False, pg.sprite.collide_circle)
        for hit in boost2_hits:
            if boost2_hits and self.player.bullet_count < 5:
                self.b_booster_snd.play()
                hit.kill()
                self.player.add_bullet_amount()

        boost3_hits = pg.sprite.spritecollide(self.player, self.booster3, False, pg.sprite.collide_circle)
        for hit in boost3_hits:
            if boost3_hits and self.player.health < PLAYER_HEALTH:
                self.healthup_snd.play()
                hit.kill()
                self.player.add_health(25)


        # asteroid or alien hit player?
        asteroid_hits = pg.sprite.spritecollide(self.player, self.asteroids, False, pg.sprite.collide_circle)
        alien_bullet_hits_player = pg.sprite.spritecollide(self.player, self.alien_bullets, True, pg.sprite.collide_circle)
        alien_hits_player = pg.sprite.spritecollide(self.player, self.aliens, False, pg.sprite.collide_circle)
        if asteroid_hits or alien_bullet_hits_player or alien_hits_player:
            if asteroid_hits:
                self.player.health -= PLAYER_HEALTH
                self.player_kill(pg.time.get_ticks())

            elif alien_bullet_hits_player:
                self.player.vel.y += A_BULLET_KNOCKBACK * self.dt
                self.player.health -= PLAYER_HEALTH * random.uniform(0.1,0.3)
                ShipDmg(self, self.player.pos, 'pl')
                self.player_hit_snd.play()
                if self.player.health <= 0:
                    self.player_kill(pg.time.get_ticks())

            elif alien_hits_player:
                self.player.health -= PLAYER_HEALTH
                self.player_kill(pg.time.get_ticks())


        if self.player.health <= 0:
            # wait 2 seconds after death to start new game
            now = pg.time.get_ticks()
            if now - self.player.last_death >= 1000:
                self.player.last_death = now
                self.playing = False


        # bullet hit asteroid?
        hits = pg.sprite.groupcollide(self.asteroids, self.player_bullets, False, True, pg.sprite.collide_circle)
        for hit in hits:
            if self.asteroid.health > 0:
                self.asteroid.health -= self.player.bullet.damage
                self.asteroid.rot_speed *= -1
            else:
                hit.kill()
                self.explosion_snd.play()
                Explosion(self, hit.rect.center, 'lg')
                self.asteroid = Asteroid(self)

        # bullet hit aliens?
        hits = pg.sprite.groupcollide(self.aliens, self.player_bullets, True, True, pg.sprite.collide_circle)
        for hit in hits:
            self.kills += 1
            self.explosion_snd.play()
            Explosion(self, hit.rect.center, 'lg')
            if random.randrange(0, 101) < 1:
                Booster3(self, hit.rect.center)
            Alien(self, random.randrange(10, self.WIDTH - 100), -200, random.choice([self.HEIGHT/4, self.HEIGHT/8]), random.choice([1,-1]))


        # spawn booster 1
        now1 = pg.time.get_ticks()
        self.time_until_boost = now1 - self.last_boost1
        self.next_boost1 = BOOSTER1_RATE - self.time_until_boost
        if self.time_until_boost > BOOSTER1_RATE:
             self.last_boost1 = now1
             Booster1(self)


        # spawn booster 2
        now2 = pg.time.get_ticks()
        self.time_until_boost = now2 - self.last_boost2
        self.next_boost2 = BOOSTER2_RATE - self.time_until_boost
        if self.time_until_boost > BOOSTER2_RATE:
            self.last_boost2 = now2
            Booster2(self)


    def player_kill(self, time):
        self.player.last_death = time
        self.player.kill()
        self.explosion_snd.play()
        Explosion(self, self.player.pos, 'lg')



    def events(self):
        # Game loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        # Game loop - draw
        self.screen.fill(BLACK)
        #self.screen.blit(self.bg_img, self.bg_rect)
        self.all_sprites.draw(self.screen)
        self.draw_text("FPS: " + str(int(self.clock.get_fps())), 25, WHITE, self.WIDTH / 2, self.HEIGHT - 50)
        self.draw_text("Bullet rate: " + str(self.player.bullet_rate), 25, WHITE, self.WIDTH - 100, self.HEIGHT - 50)
        self.draw_text("next speed booster in: " + str(self.next_boost1 // 1000 +1), 25, WHITE, 120, self.HEIGHT - 50)
        self.draw_text("next bullet booster in: " + str(self.next_boost2 // 1000 +1), 25, WHITE, 120, self.HEIGHT - 100)
        self.draw_text("Kills: " + str(self.kills), 50, WHITE, 100, self.HEIGHT/16)
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        pg.display.flip()


    def show_start_screen(self):
        self.screen.fill(BLACK)
        self.draw_text(TITLE, 58, WHITE, self.WIDTH / 2, self.HEIGHT / 4)
        self.draw_text("Arrows to move, Space to fire", 40, WHITE, self.WIDTH / 2, self.HEIGHT / 2)
        self.draw_text("Press Enter to play", 40, WHITE, self.WIDTH / 2, self.HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()


    def show_go_screen(self):
        if not self.running:
            return
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", 58, WHITE, self.WIDTH / 2, self.HEIGHT / 4)
        self.draw_text("Kills: " + str(self.kills), 42, WHITE, self.WIDTH / 2, self.HEIGHT / 2 - 15)
        self.draw_text("Press Enter to play again", 42, WHITE, self.WIDTH / 2, self.HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()


    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                keys = pg.key.get_pressed()
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if keys[pg.K_RETURN]:
                    waiting = False

if __name__ == "__main__":
    g = Game() # instance of the game class
    g.show_start_screen()
    while g.running:
        g.new()
        g.show_go_screen()

    pg.quit()

