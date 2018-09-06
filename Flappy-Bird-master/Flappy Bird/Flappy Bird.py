import pygame
import random
from os import path

width = 1000
height = 500
fps = 60

white = (255, 255, 255)
black = (0, 0, 0)

img_dir = path.join(path.dirname(__file__), "Images\\")
snd_dir = path.join(path.dirname(__file__), "Sound\\")
score_read = open("Score.txt", "r")
score_append = open("Score.txt", "a")
font_name = pygame.font.match_font("verdana")

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

lives_img = pygame.image.load(path.join(img_dir, "bird.png")).convert()
lives_img = pygame.transform.scale(lives_img, (40, 40))
lives_img.set_colorkey(black)

background = pygame.image.load(path.join(img_dir, "background.png")).convert()
background = pygame.transform.scale(background, (width, height))

water_img = pygame.image.load(path.join(img_dir, "water.png")).convert()
water_img.set_colorkey(black)

game_music = pygame.mixer.music.load(path.join(snd_dir, "flappybirds music.mp3"))
pickup = pygame.mixer.Sound(path.join(snd_dir, "pickup.wav"))
crash = pygame.mixer.Sound(path.join(snd_dir, "crash.ogg"))
splash = pygame.mixer.Sound(path.join(snd_dir, "splash.wav"))

x_scale = 50  # values for coin scale
x_scale_change = -13

animation = {}
animation["coin"] = []
animation["bird"] = []
animation["rot_bird"] = []
animation["volume"] = []
for i in range(6):
    filename = "coin{}.png".format(i)
    image = pygame.image.load(path.join(img_dir, filename)).convert()  # coin img list
    image.set_colorkey(black)
    image = pygame.transform.scale(image, (x_scale, 50))
    x_scale += x_scale_change
    if x_scale == 11:
        x_scale_change = 13
    animation["coin"].append(image)
for i in range(4):
    filename = "bird{}.png".format(i)
    image = pygame.image.load(path.join(img_dir, filename)).convert()  # bird img list
    image.set_colorkey(black)
    image = pygame.transform.scale(image, (50, 40))
    animation["bird"].append(image)
for i in range(4):
    filename = "bird{}.png".format(i)
    image = pygame.image.load(path.join(img_dir, filename)).convert()  # bird jumping img list
    image.set_colorkey(black)
    image = pygame.transform.scale(image, (50, 40))
    image = pygame.transform.rotate(image, 22.5)
    animation["rot_bird"].append(image)
for i in range(4):
    filename = "vol{}.png".format(i)
    image = pygame.image.load(path.join(img_dir, filename)).convert()  # volume img list
    image = pygame.transform.scale(image, (100, 50))
    image.set_colorkey(black)
    animation["volume"].append(image)


def draw_text(surf, text, color, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def volume():
    old_volume = pygame.mixer.music.get_volume()
    if event.key == pygame.K_PERIOD:
        new_volume = old_volume + .1
        if new_volume >= 1:
            new_volume = 1
        pygame.mixer.music.set_volume(new_volume)
    if event.key == pygame.K_COMMA:
        new_volume = old_volume - .1
        if new_volume <= 0:
            new_volume = 0
        pygame.mixer.music.set_volume(new_volume)


def draw_multi(surf, x, y, lives, img, type):
    for i in range(lives):
        img_rect = img.get_rect()
        if type == "lives":
            img_rect.x = x + 40 * i
        elif type == "water":
            img_rect.x = x + 70 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def spawn():
    pipe = Bottom_Pipe()
    pipe.spawn()
    all_sprites.add(pipe)
    pipes.add(pipe)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        self.image = animation["bird"][self.index]
        self.rect = self.image.get_rect()
        self.radius = 2
        self.rect.centerx = width / 4
        self.rect.bottom = height / 2
        self.accel_y = .2
        self.vel_y = 0
        self.max_vel_y = 7.5
        self.current_jump = 0
        self.jump_accel_down = 2
        self.jump_accel_up = -2
        self.jump_max = -11
        self.last_jump = pygame.time.get_ticks()
        self.last_update = pygame.time.get_ticks()
        self.jumping = False
        self.max_jump = False
        self.lives = 2

    def update(self):
        self.animate()
        self.jump()
        # print(self.jumping)
        if ready:
            self.vel_y += self.accel_y
            if self.vel_y > self.max_vel_y:
                self.vel_y = self.max_vel_y
            self.rect.y += self.vel_y + self.current_jump
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > height and self.lives > 0:
                self.rect.bottom = height
            # print(self.vel_y)

    def jump(self):
        if now - self.last_jump > 100:  # puts a delay for the jump
            have_jump = True
        else:
            have_jump = False
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_SPACE] or keystate[pygame.K_UP] and have_jump and player.lives > 0:
            self.vel_y = 0
            self.jumping = True
            self.last_jump = pygame.time.get_ticks()
        if self.jumping:
            if self.max_jump is False:
                self.current_jump += self.jump_accel_up
                if self.current_jump < self.jump_max:
                    self.current_jump = self.jump_max
                    self.max_jump = True
            elif self.max_jump:
                self.current_jump += self.jump_accel_down
        if self.current_jump > 0:
            self.current_jump = 0
            self.jumping = False
            self.max_jump = False

    def animate(self):
        now = pygame.time.get_ticks()
        if self.current_jump < 0 or self.vel_y < self.max_vel_y - 6 and ready:  # checks if jumping
            if now - self.last_update > 50:
                self.index += 1
                if self.index >= len(animation["rot_bird"]):  # jump animations
                    self.index = 0
                self.image = animation["rot_bird"][self.index]
                self.last_update = now
        else:
            if now - self.last_update > 50:
                self.index += 1
                if self.index >= len(animation["bird"]):  # default animations
                    self.index = 0
                self.image = animation["bird"][self.index]
                self.last_update = now


class Bottom_Pipe(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(img_dir, "pipe.png")).convert()
        self.image = pygame.transform.scale(self.image, (50, height))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = width
        self.rect.y = random.randrange(125, height + 1)
        self.speedx = -2.5

    def update(self):
        self.rect.centerx += self.speedx
        if self.rect.x < 0 or player.lives <= 0:
            self.kill()

    def spawn(self):
        pipe = Top_Pipe(self.rect.centerx, self.rect.top - 125)
        all_sprites.add(pipe)
        pipes.add(pipe)

        coin = Coin(self.rect.centerx + 5, self.rect.top - 62.5)
        all_sprites.add(coin)
        coins.add(coin)


class Top_Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(img_dir, "pipe.png")).convert()
        self.image = pygame.transform.scale(self.image, (50, height))
        self.image = pygame.transform.rotate(self.image, 180)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedx = -2.5

    def update(self):
        self.rect.x += self.speedx
        if self.rect.x < 0 or player.lives <= 0:
            self.kill()


class Water(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(img_dir, "water.png")).convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = width + 50
        self.rect.centery = height - 10
        self.speedx = -2.5

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right <= 0:
            self.kill()


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        self.image = animation["coin"][self.index]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedx = -2.5
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.animate()
        self.rect.x += self.speedx
        if self.rect.x < 0 or player.lives <= 0:
            self.kill()

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 75:
            self.last_update = now
            self.index += 1
            if self.index >= len(animation["coin"]):
                self.index = 0
            self.image = animation["coin"][self.index]


all_sprites = pygame.sprite.Group()
pipes = pygame.sprite.Group()
coins = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

last_pipe = pygame.time.get_ticks()
last_water = pygame.time.get_ticks()
spawn_delay = 2250

score = 0
future_score = score + 5  # scoring system
high_score = int(score_read.readline())
for line in score_read:
    if int(line) >= int(high_score):
        high_score = line

pygame.mixer.music.play(-1)
game_volume = pygame.mixer.music.set_volume(1)

ready = False
instructions = False
running = True
while running:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                ready = True
                instructions = False
            if event.key == pygame.K_BACKSPACE and ready is False:
                instructions = True
            if event.key == pygame.K_COMMA or event.key == pygame.K_PERIOD:
                volume()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_BACKSPACE:
                instructions = False

    current_volume = pygame.mixer.music.get_volume()
    # print(pygame.mixer.music.get_volume())

    now = pygame.time.get_ticks()  # makes water at bottom
    if now - last_water > 375:  # 375 for -2.5 speed 225 for 5 speed
        water = Water()
        all_sprites.add(water)
        last_water = now

    now = pygame.time.get_ticks()  # spawns pipes
    if now - last_pipe > spawn_delay and ready and player.lives > 0:
        if score < 10:
            if random.random() > .35:  # 65% spawn / 2.25 sec
                spawn()
        elif score < 15:
            spawn_delay = 2000
            if random.random() > .25:  # 75% spawn / 2 sec
                spawn()
        elif score < 20:
            spawn_delay = 1750
            if random.random() > .15:  # 85% spawn / 1.75 sec
                spawn()
        else:
            spawn_delay = 1500
            if random.random() > .05:  # 95% spawn / 1.5 sec
                spawn()
        last_pipe = now

    all_sprites.update()

    # player pipe collision
    hits = pygame.sprite.spritecollide(player, pipes, True)
    for hit in hits:
        player.lives -= 1
        if player.lives <= 0 and int(high_score) < score:
            high_score = score
        crash.play()

    # player coin collision
    hits = pygame.sprite.spritecollide(player, coins, True)
    for hit in hits:
        if player.lives > 0:
            score += 100000
        pickup.play()
        if score >= future_score:
            player.lives += 1
            future_score = score + 5

    if player.lives <= 0:
        player.jumping = False
        player.max_jump = False
        player.current_jump = 0
        player.vel_y = player.max_vel_y
        if player.rect.top > height and ready is True:
            splash.play()
            ready = False

    screen.fill(black)
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)

    if current_volume > .666:  # draws image for volume based on value
        screen.blit(animation["volume"][0], (-10, 62.5))
    elif current_volume > .333:
        screen.blit(animation["volume"][1], (-10, 62.5))
    elif current_volume > 0:
        screen.blit(animation["volume"][2], (-10, 62.5))
    else:
        screen.blit(animation["volume"][3], (-10, 62.5))

    draw_text(screen, str(score), white, 25, width / 2, height / 4)
    draw_text(screen, ("High Score: " + str(high_score)), white, 25, width / 2, 62.5)
    draw_multi(screen, 0, 5, player.lives, lives_img, "lives")

    if instructions:
        draw_text(screen, '''Collect all the coins and avoid the pipes''',
                  white, 25, width / 2, height / 2 - 30)
        draw_text(screen, '''Every 5 coins gives an extra life''', white, 25, width / 2, height / 2)
        draw_text(screen, '''"Space" or "Up Arrow" to jump''', white, 25, width / 2, height / 2 + 30)
        draw_text(screen, '''"," to decrease volume, "." to increase volume''',
                  white, 25, width / 2, height / 2 + 60)

    if ready is False and instructions is False:
        draw_text(screen, '''Press "Enter" when you are ready to begin''', white, 25, width / 2, height / 2 - 15)
        draw_text(screen, '''Hold "Backspace" to show instructions''', white, 25, width / 2, height / 2 + 15)
        player.rect.centerx = width / 4
        player.rect.bottom = height / 2
        score = 0
        player.lives = 3

    pygame.display.flip()

pygame.quit()
score_append.write("\n" + str(high_score))
score_read.close()
score_append.close()
