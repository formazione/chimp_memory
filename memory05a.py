import pygame
import random
from glob import glob

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
        # text_rect = self.text.get_rect(center=(50 // 2, 50 // 2))
        self.text = font.render(self.number, 1, (0, 0, 0))
        text_rect = self.text.get_rect(center=(50 // 2, 50 // 2))
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

bgd = pygame.Surface((50, 50))
bgd.fill((255, 0, 0))
def mouse_collision(sprite):
    global num_order, score, counter_on, max_count

    if counter_on == 0:
        
        x, y = pygame.mouse.get_pos()
        if sprite.rect.collidepoint(x, y):
            play("click")
            print("touched")
            print(sprite.rect.collidepoint(x, y))
            print(sprite.number)
            bgd.fill((0, 255, 0))
            sprite.image.blit(bgd, (0, 0))
            num_order.append(sprite.number)
            sprite.rect = pygame.Rect(-50, -50, 50, 50)

            # Check if you are wrong as you type
            if sprite.number != str(len(num_order)):
                num_order = []
                counter_on = 1
                pygame.mouse.set_visible(False)
                g.update()
                screen.fill((0,0,0))
                bgd.fill((255, 0, 0))

        if len(num_order) == len(g):
            print("fine")
            print(num_order)
            if num_order == [str(s.number) for s in g]:
                score += 1
                print("You won - Score: " + str(score))
                num_order = []
                g.add(Square(len(g) + 1))
                counter_on = 1
                max_count = max_count + 10
                pygame.mouse.set_visible(False)
            else:
                num_order = []
                counter_on = 1
                pygame.mouse.set_visible(False)
            g.update()
            screen.fill((0,0,0))
            bgd.fill((255, 0, 0))


######################
#     sound          #
######################
def init():
    "Initializing pygame and mixer"
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()
    pygame.mixer.quit()
    pygame.mixer.init(22050, -16, 2, 512)
    pygame.mixer.set_num_channels(32)
    # Load all sounds
    lsounds = glob("sounds\\*.mp3")
    print(lsounds)
    # Dictionary with all sounds, keys are the name of wav
    sounds = {}
    for sound in lsounds:
        sounds[sound.split("\\")[1][:-4]] = pygame.mixer.Sound(f"{sound}")
    return sounds
# =========================== ([ sounds ]) ============

sounds = init()

base = pygame.mixer.music
def soundtrack(filename, stop=0):
    "This load a base from sounds directory"
    base.load(filename)
    if stop == 1:
        base.stop()
    else:
        base.play(-1)

def play(sound):
    pygame.mixer.Sound.play(sounds[sound])

def squares_init():
    for i in range(1, 4):
        g.add(Square(i))

counter = 0
counter_on = 1
max_count = 100
def main():
    global counter_on, counter, max_count

    game_init()
    squares_init()
    clock = pygame.time.Clock()
    loop = 1
    pygame.mouse.set_visible(False)
    soundtrack("sounds/soave.ogg")
    while loop:
        screen.fill((0, 0, 0))
        text = font.render("Livello: " + str(score), 1, (255, 244, 0))
        screen.blit(text, (0, 0))
        if counter_on:
            text = font.render("time: " + str(max_count - counter), 1, (255, 244, 0))
            screen.blit(text, (200, 0))
            counter += 1
            if counter % 4 == 0:
                play("click")
        for event in pygame.event.get():
            # ========================================= QUIT
            if event.type == pygame.QUIT:
                loop = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    loop = 0
                if event.key == pygame.K_s:
                    g.update()
                    screen.fill((0,0,0))
            if event.type == pygame.MOUSEBUTTONDOWN:
                for s in g:
                    mouse_collision(s)      
        g.draw(screen)
        # Hides the number...
        if counter == max_count:
            for s in g:
                s.image.blit(bgd, (0, 0))
                counter = 0
                counter_on = 0

                pygame.mouse.set_visible(True)
        pygame.display.update()
        clock.tick(20)

    pygame.quit()


main()
