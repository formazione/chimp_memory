import pygame


size = w, h = 400, 500
screen = pygame.display.set_mode((size))
pygame.display.set_caption("Window title")


def main():
    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()
    loop = 1
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = 0
        pygame.display.update()
        clock.tick(60)

    pygame.quit()


main()


