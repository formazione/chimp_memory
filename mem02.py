import pygame


class Sprite(pygame.sprite.Sprite):
    def __init__(self, image: str, pos: tuple = (0, 0), color=(0, 0, 0)):
        super(Sprite, self).__init__()
        if type(image) == str:
            self.image = pygame.image.load(image)
        else:
            self.image = image
            self.image.fill(color)
        self.x, self.y = pos
        self.w, self.h = self.image.get_size()
        self.rect = self.image.get_rect(center=(self.w // 2, self.h //2))
        self.number = 3
        g.add(self)


g = pygame.sprite.Group()
'''
To define a surface add:
- surface.: pygame.Surface((10, 10))
- position ex.: (19, 30)
- color = (255, 255, 255)
'''
player = Sprite(
    pygame.Surface((20, 20)),
    (0, 0),
    color = (255, 0, 0))
''' to define a surface with image:
pass a path to the image

player2 = Sprite("imgs/player.png")
'''


def mouse_collision(sprite):
    x, y = pygame.mouse.get_pos()
    if sprite.rect.collidepoint(x, y):
        print("touched")
        print(sprite.rect.collidepoint(x, y))
        print(sprite.number)


def main():
    size = w, h = 400, 500
    screen = pygame.display.set_mode((size))
    pygame.display.set_caption("Window title")
    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()
    loop = 1
    # start ================================
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                for s in g:
                    mouse_collision(s)

        g.draw(screen)
        pygame.display.update()
        clock.tick(60)
    # ================================== end
    pygame.quit()


main()

