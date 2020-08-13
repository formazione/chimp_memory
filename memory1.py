import pygame
import random

# all the possible positions for the numbers
pos = [(x, y) for x in range(1, 16) for y in range(1, 16)] 
# print(pos)
print(pos.pop(pos.index(random.choice(pos))))
# print(pos)

def game_init():
    global screen, font

    pygame.init()
    size = w, h = 800, 800
    screen = pygame.display.set_mode((size))
    pygame.display.set_caption("Memory Game")
    font = pygame.font.SysFont("Arial", 32)


class Square(pygame.sprite.Sprite):
    def __init__(self, number):
        super(Square, self).__init__()
        self.number = number
        self.make_image()

    def make_image(self):
        global font

        self.x, self.y = self.random_pos()
        self.image = pygame.Surface((50, 50))
        r, g, b = [random.randrange(128, 256) for x in range(3)]
        self.image.fill((r, g, b))
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        self.number = str(self.number)
        self.text = font.render(self.number, 1, (0, 0, 0))
        text_rect = self.text.get_rect(center=(50 // 2, 50 // 2))
        # text_rect = self.text.get_rect(center=(50 // 2, 50 // 2))
        self.image.blit(self.text, text_rect)

    def update(self):
        self.make_image()
        screen.blit(self.image, (self.x, self.y))

    def random_pos(self):
        position = random.choice(pos)
        x, y = position
        pos.pop(pos.index(position))
        # x = random.randrange(0, 16)
        # y = random.randrange(0, 16)
        x = x * 50
        y = y * 50

        return x, y


# global

g = pygame.sprite.Group()
num_order = []
score = 0

def mouse_collision(sprite):
    global num_order, score

    x, y = pygame.mouse.get_pos()
    if sprite.rect.collidepoint(x, y):
        print("touched")
        print(sprite.rect.collidepoint(x, y))
        print(sprite.number)
        num_order.append(sprite.number)
    if len(num_order) == len(g):
        print("fine")
        print(num_order)
        if num_order == [str(s.number) for s in g]:
            score += 1
            print("You won - Score: " + str(score))
            num_order = []
            g.add(Square(len(g) + 1))
        else:
            num_order = []
        g.update()
        screen.fill((0,0,0))
        text = font.render("Score: " + str(score), 1, (255, 244, 0))
        screen.blit(text, (0, 0))
def squares_init():
    for i in range(1, 4):
        g.add(Square(i))


def main():
    game_init()
    squares_init()
    clock = pygame.time.Clock()
    loop = 1
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    g.update()
                    screen.fill((0,0,0))
            if event.type == pygame.MOUSEBUTTONDOWN:
                for s in g:
                    mouse_collision(s)      
        g.draw(screen)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()


main()

