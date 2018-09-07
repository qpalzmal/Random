import pygame
import random
from os import path

WIDTH = 1000
HEIGHT = 500
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# marks the directory for the image and sounds folders
img_dir = path.join(path.dirname(__file__), "Images\\")
snd_dir = path.join(path.dirname(__file__), "Sound\\")

# opens and uses the score file containing high scores
score_read = open("High Score.txt", "r")

font_name = pygame.font.match_font("verdana")

# sets up the game
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
# imports lives image
lives_img = pygame.image.load(path.join(img_dir, "bird.png")).convert()
lives_img = pygame.transform.scale(lives_img, (40, 40))
lives_img.set_colorkey(BLACK)
# imports background image
background = pygame.image.load(path.join(img_dir, "background.png")).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
# imports water image
water_img = pygame.image.load(path.join(img_dir, "water.png")).convert()
water_img.set_colorkey(BLACK)
# imports all sounds to be used
game_music = pygame.mixer.music.load(path.join(snd_dir, "flappybirds music.mp3"))
pickup = pygame.mixer.Sound(path.join(snd_dir, "pickup.wav"))
crash = pygame.mixer.Sound(path.join(snd_dir, "crash.ogg"))
splash = pygame.mixer.Sound(path.join(snd_dir, "splash.wav"))

start_screen = pygame.image.load(path.join(img_dir, "startscreen.png")).convert()
start_screen = pygame.transform.scale(start_screen, (WIDTH, HEIGHT))

# different lists that contain series of images for animation
animation = {}
animation["coin"] = []
animation["bird"] = []
animation["rot_bird"] = []
animation["volume"] = []

# used to help correctly resize coins
x_scale = 50
x_scale_change = -13

# loop used for importing the coin image
for i in range(6):
    filename = "coin{}.png".format(i)
    image = pygame.image.load(path.join(img_dir, filename)).convert()
    image.set_colorkey(BLACK)
    image = pygame.transform.scale(image, (x_scale, 50))
    x_scale += x_scale_change
    if x_scale == 11:
        x_scale_change = 13
    animation["coin"].append(image)
# loop used for importing player image
for i in range(4):
    filename = "bird{}.png".format(i)
    image = pygame.image.load(path.join(img_dir, filename)).convert()  # bird img list
    image.set_colorkey(BLACK)
    image = pygame.transform.scale(image, (50, 40))
    animation["bird"].append(image)
# loop used for importing jumping player image
for i in range(4):
    filename = "bird{}.png".format(i)
    image = pygame.image.load(path.join(img_dir, filename)).convert()  # bird jumping img list
    image.set_colorkey(BLACK)
    image = pygame.transform.scale(image, (50, 40))
    image = pygame.transform.rotate(image, 22.5)
    animation["rot_bird"].append(image)
# loop used for importing volume image
for i in range(4):
    filename = "vol{}.png".format(i)
    image = pygame.image.load(path.join(img_dir, filename)).convert()  # volume img list
    image = pygame.transform.scale(image, (100, 50))
    image.set_colorkey(BLACK)
    animation["volume"].append(image)


# draws any text at specified point
def draw_text(surf, text, color, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# changes volume depending on what key was pressed
def volume():
    old_volume = pygame.mixer.music.get_volume()
    # increases volume if "." or "F3" was pressed
    if event.key == pygame.K_PERIOD or event.key == pygame.K_F3:
        new_volume = old_volume + .1
        if new_volume >= 1:
            new_volume = 1
        pygame.mixer.music.set_volume(new_volume)
    # decreases volume if "," or "F2" was pressed
    if event.key == pygame.K_COMMA or event.key == pygame.K_F2:
        new_volume = old_volume - .1
        if new_volume <= 0:
            new_volume = 0
        pygame.mixer.music.set_volume(new_volume)


# draws a series of the image
def draw_lives(surf, x, y, lives, img):
    for life in range(lives):
        img_rect = img.get_rect()
        if type == "lives":
            img_rect.x = x + 40 * life
        img_rect.y = y
        surf.blit(img, img_rect)


# spawns all the pipe sprites needed
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
        self.rect.centerx = WIDTH / 4
        self.rect.bottom = HEIGHT / 2
        # sets up motion numbers
        self.vel_y = 0
        self.MAX_VEL_Y = 7.5
        self.accel_y = .2
        # sets up jumping numbers
        self.current_jump = 0
        self.JUMP_MAX = -11
        self.jump_accel_up = -2
        self.jump_accel_down = 2
        self.last_jump = pygame.time.get_ticks()
        self.last_update = pygame.time.get_ticks()
        self.is_jumping = False
        self.is_max_jump = False

        self.lives = 2

    def update(self):
        self.animate()
        self.jump()
        # print(self.jumping)
        if ready:
            # constant movement in y direction with respect to acceleration
            self.vel_y += self.accel_y
            if self.vel_y > self.MAX_VEL_Y:
                self.vel_y = self.MAX_VEL_Y
            self.rect.y += self.vel_y + self.current_jump
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > HEIGHT and self.lives > 0:
                self.rect.bottom = HEIGHT
            # print(self.vel_y)

    def jump(self):
        # puts a delay for the jump
        now = pygame.time.get_ticks()
        if now - self.last_jump > 100:
            have_jump = True
        else:
            have_jump = False

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_SPACE] or keystate[pygame.K_UP] and have_jump and player.lives > 0:
            self.vel_y = 0
            self.is_jumping = True
            self.last_jump = pygame.time.get_ticks()

        if self.is_jumping:
            # makes player jump up till it reaches a jump limit
            if self.is_max_jump is False:
                self.current_jump += self.jump_accel_up
                # once it reaches the max jump height
                if self.current_jump < self.JUMP_MAX:
                    self.current_jump = self.JUMP_MAX
                    self.is_max_jump = True
            # makes the smooth fall/"jump" down after reaching the max jump
            elif self.is_max_jump:
                self.current_jump += self.jump_accel_down
        # makes it so fall/"jump" down won't keep affecting player
        if self.current_jump > 0:
            self.current_jump = 0
            self.is_jumping = False
            self.is_max_jump = False

    def animate(self):
        now = pygame.time.get_ticks()
        # checks to see if player is jumping
        if self.current_jump < 0 or self.vel_y < self.MAX_VEL_Y - 6 and ready:
            # jump animation
            if now - self.last_update > 50:
                self.index += 1
                if self.index >= len(animation["rot_bird"]):
                    self.index = 0
                self.image = animation["rot_bird"][self.index]
                self.last_update = now
        else:
            # regular animation/not jumping
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
        self.image = pygame.transform.scale(self.image, (50, HEIGHT))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        # makes the pipe spawn at a random y position
        self.rect.y = random.randrange(125, HEIGHT + 1)
        self.SPEED_X = -2.5

    def update(self):
        self.rect.centerx += self.SPEED_X
        if self.rect.x < 0 or player.lives <= 0:
            self.kill()

    def spawn(self):
        # spawns a top pipe when a bottom pipe spawns
        pipe = Top_Pipe(self.rect.centerx, self.rect.top - 125)
        all_sprites.add(pipe)
        pipes.add(pipe)
        # spawns a coin in between top pipe and bottom pipe when bottom pipe spawns
        coin = Coin(self.rect.centerx + 5, self.rect.top - 62.5)
        all_sprites.add(coin)
        coins.add(coin)


class Top_Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(img_dir, "pipe.png")).convert()
        self.image = pygame.transform.scale(self.image, (50, HEIGHT))
        self.image = pygame.transform.rotate(self.image, 180)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.SPEED_X = -2.5

    def update(self):
        self.rect.x += self.SPEED_X
        if self.rect.x < 0 or player.lives <= 0:
            self.kill()


class Water(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(img_dir, "water.png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH + 50
        self.rect.centery = HEIGHT - 10
        self.SPEED_X = -2.5

    def update(self):
        self.rect.x += self.SPEED_X
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
        self.SPEED_X = -2.5
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.animate()
        self.rect.x += self.SPEED_X
        if self.rect.x < 0 or player.lives <= 0:
            self.kill()

    def animate(self):
        now = pygame.time.get_ticks()
        # makes the spinning coin animation
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

coin_spree = 0
score = 0
future_score = score + 5
# reads the high score file to import the highest score
high_score = int(score_read.readline())
for line in score_read:
    if int(line) > int(high_score):
        high_score = line
score_read.close()

pygame.mixer.music.play(-1)
game_volume = pygame.mixer.music.set_volume(1)

# booleans used for game start, showing instructions, and client running
ready = False
instructions = False
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                ready = True
                instructions = False
            if event.key == pygame.K_COMMA or event.key == pygame.K_F2 or pygame.K_PERIOD or pygame.K_F3:
                volume()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_BACKSPACE:
                instructions = not instructions

    all_sprites.update()
    current_volume = pygame.mixer.music.get_volume()
    # print(pygame.mixer.music.get_volume())

    # creats series of water at the bottom
    now = pygame.time.get_ticks()
    if now - last_water > 375:  # 375 for -2.5 speed 225 for 5 speed
        water = Water()
        all_sprites.add(water)
        last_water = now

    now = pygame.time.get_ticks()  # spawns pipes
    if now - last_pipe > spawn_delay and ready and player.lives > 0:
        if score < 10:
            if random.random() > .35:  # 65% spawn / 2.25 sec at scores 0 - 10
                spawn()
        elif score < 15:
            spawn_delay = 2000
            if random.random() > .25:  # 75% spawn / 2 sec at scores 10 - 15
                spawn()
        elif score < 20:
            spawn_delay = 1750
            if random.random() > .15:  # 85% spawn / 1.75 sec at score 15 - 20
                spawn()
        else:
            spawn_delay = 1500
            if random.random() > .05:  # 95% spawn / 1.5 sec at score 20 - infinity
                spawn()
        last_pipe = now

    # player pipe collision
    hits = pygame.sprite.spritecollide(player, pipes, True)
    for hit in hits:
        player.lives -= 1
        print(player.lives)
        coin_spree = 0
        # once it's game over, if score > high score, high score will be replaced and written into the high score file
        if player.lives <= 0 and int(high_score) < score:
            high_score = score
            score_append = open("Score.txt", "a")
            score_append.write("\n" + str(high_score))
            score_append.close()
        crash.play()

    # player coin collision
    hits = pygame.sprite.spritecollide(player, coins, True)
    for hit in hits:
        if player.lives > 0:
            score += 1
            coin_spree += 1
            pickup.play()
            # if player collects five coins with getting hit they get an extra life
            if coin_spree >= 5:
                player.lives += 1
                coin_spree = 0
        # sets a future score for when player reaches that they will get extra life
        if score >= future_score:
            player.lives += 1
            future_score = score + 5

    # makes player unable to move once they die
    if player.lives <= 0:
        player.jumping = False
        player.max_jump = False
        player.current_jump = 0
        player.vel_y = player.MAX_VEL_Y * 2
        # official end to game once they reach the bottom
        if player.rect.top > HEIGHT and ready is True:
            splash.play()
            ready = False

    screen.fill(BLACK)
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)

    # black start screen
    if instructions or (instructions is False and ready is False):
        screen.blit(start_screen, (0, 0))
    # writes the text for player score, high score, and the lives once game starts
    else:
        draw_text(screen, str(score), WHITE, 25, WIDTH / 2, HEIGHT / 4)
        draw_text(screen, ("High Score: " + str(high_score)), WHITE, 25, WIDTH / 2, 62.5)
        draw_lives(screen, 0, 5, player.lives, lives_img)

    # draws image for volume based on value
    if current_volume > .666:
        screen.blit(animation["volume"][0], (-10, 62.5))
    elif current_volume > .333:
        screen.blit(animation["volume"][1], (-10, 62.5))
    elif current_volume > 0:
        screen.blit(animation["volume"][2], (-10, 62.5))
    else:
        screen.blit(animation["volume"][3], (-10, 62.5))

    # text for instructions on how to play
    if instructions:
        draw_text(screen, '''Collect all the coins and avoid the pipes''',
                  WHITE, 20, WIDTH / 2, HEIGHT / 2 - 60)
        draw_text(screen, '''5 coins = extra life and 5 coins in a row without getting hit gives an extra life''',
                  WHITE, 20, WIDTH / 2, HEIGHT / 2 - 30)
        draw_text(screen, '''"Space" or "Up Arrow" to jump''', WHITE, 25, WIDTH / 2, HEIGHT / 2)
        draw_text(screen, '''"," to decrease volume, "." to increase volume''',
                  WHITE, 20, WIDTH / 2, HEIGHT / 2 + 30)
        draw_text(screen, '''"Enter" to start''', WHITE, 20, WIDTH / 2, HEIGHT / 2 + 60)

    # default start screen
    if ready is False and instructions is False:
        draw_text(screen, '''Press "Enter" to start''', WHITE, 25, WIDTH / 2, HEIGHT / 2 - 15)
        draw_text(screen, '''Hold "Backspace" to show instructions''', WHITE, 25, WIDTH / 2, HEIGHT / 2 + 15)
        player.rect.centerx = WIDTH / 4
        player.rect.bottom = HEIGHT / 2
        score = 0
        player.lives = 3

    pygame.display.flip()

pygame.quit()
