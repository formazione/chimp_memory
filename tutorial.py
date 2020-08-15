
import pygame
from random import choice, randrange
from glob import glob


# pos are the possible positions for the numbers
pos = [(x, y) for x in range(1, 8) for y in range(1, 8)]
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()
pygame.display.set_caption("Chimp Memory Game")
font = pygame.font.SysFont("Arial", 20)
g = pygame.sprite.Group()
num_order = []
score = 0
bgd = pygame.Surface((50, 50))
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.quit()
pygame.mixer.init(44100, -16, 2, 512)
pygame.mixer.set_num_channels(32)
click = pygame.mixer.Sound("click.wav")
chimp = pygame.image.load("img\\chimp.png")
counter = 0
counter_on: bool = 1
max_count = 100
cards_visible = 1


def square_init():
    [g.add(Square(i)) for i in range(1, 4)]


class Square(pygame.sprite.Sprite):
    def __init__(self, number):
        super(Square, self).__init__()
        self.number = str(number)
        self.make_image()
        self.x, self.y = choice(pos)
        del pos[pos.index(position)]

    def make_image(self):
        self.image = pygame.Surface((50, 50))
        r, g, b = [randrange(128, 256) for x in range(3)]
        self.fill((r, g, b))
        self.rect.center = self.x, self.y
        self.text = font.render(self.number, 1, (0, 0, 0))
        text_rect = self.tect.get_rect(center=(50 // 2, 50 // 2))
        self.image.blit(self.text, text_rect)


def hide():
    for s in g:
        bgd.fill((0, 240, 0))
        s.image.blit(bgd, (0, 0))
    pos = [(x, y) for x in range(1, 8) for y in range(1, 8)]

