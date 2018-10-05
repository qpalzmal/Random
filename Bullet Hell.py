import pygame

# sets up the environment
WIDTH = 300
HEIGHT = 600
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


forsen = pygame.image.load("forsenE.png")

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snus Hell")
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(forsen, (25, 25))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed_x = 0
        self.speed_y = 0
        self.shoot_delay = pygame.time.get_ticks()
        self.health = 100

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.speed_x = 0
        self.speed_y = 0

        # all keys the player can use to do stuff
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_SPACE]:
            self.shoot()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speed_x = -4
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speed_x = 4
        if keystate[pygame.K_UP] or keystate[pygame.K_w]:
            self.speed_y = -0
        if keystate[pygame.K_DOWN] or keystate[pygame.K_s]:
            self.speed_y = 0

        # bounds player inside screen on x-axis
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        # bounds player inside screen y-axis
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.shoot_delay > 200:
            bullet = Bullet(self.rect.centerx, self.rect.centery + 12, "up")
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.shoot_delay = now


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(forsen, (10, 10))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        # direction the bullet moves based on who shot it
        if direction.lower() == "up":
            self.speed_y = -6
        else:
            self.speed_y = 6

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(forsen, (25, 25))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = 20
        self.shoot_delay = pygame.time.get_ticks()
        self.health = 1000

    def update(self):
        self.shoot()
        self.rect.centerx = player.rect.centerx

        # bounds enemy inside screen on x-axis
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.shoot_delay > 200:
            bullet = Bullet(self.rect.centerx, self.rect.top, "down")
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.shoot_delay = now


# build player and add it to the draw group
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

player = Player(WIDTH / 2, HEIGHT - 20)
enemy = Enemy()

all_sprites.add(player)
all_sprites.add(enemy)
all_sprites.add(enemy)

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    
    screen.fill(WHITE)
    all_sprites.draw(screen)
    hit_box = pygame.draw.circle(screen, RED, (player.rect.centerx, player.rect.centery), 5)
    pygame.display.flip()

pygame.quit()
