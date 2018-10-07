from BHSprites import *
from BHSettings import *


def main():

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snus Hell")
    clock = pygame.time.Clock()



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


if __name__ == "__main__":
    main()