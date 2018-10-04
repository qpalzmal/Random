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
pygame.display.set_caption("Bullet Hell")
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = forsen
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT - 20
        self.speed_x = 0
        self.speed_y = 0

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.speed_x = 0
        self.speed_y = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -2
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 2
        if keystate[pygame.K_UP]:
            self.speed_y = -2
        if keystate[pygame.K_DOWN]:
            self.speed_y = 2
        if keystate[pygame.K_SPACE]:
            self.shoot()

        # bounds player inside on x-axis
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        # bounds player inside y-axis
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.bullets.add(bullet)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = forsen
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y


# build player and add it to the draw group
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)
all_sprites.add(bullets)


running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.draw(screen)
    hit_box = pygame.draw.circle(screen, RED, (player.rect.centerx, player.rect.centery), 5)
    all_sprites.update()
    pygame.display.flip()
    screen.fill(WHITE)

pygame.quit()
