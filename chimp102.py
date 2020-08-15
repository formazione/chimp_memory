import pygame
import random
from glob import glob

'''
        Possible positions on the grid 7 x 7

'''
pos = [(x, y) for x in range(1, 8) for y in range(1, 8)] 


def game_init():
    "Pygame init, screen and font"
    global screen, font, w, h

    pygame.init()
    size = w, h = 400, 400
    screen = pygame.display.set_mode((size))
    pygame.display.set_caption("Chimp Memory Game")
    font = pygame.font.SysFont("Arial", 20)


class Square(pygame.sprite.Sprite):
    def __init__(self, number):
        "The number seen on the sprite"
        super(Square, self).__init__()
        self.number = number
        self.make_image()

    def update(self):
        self.make_image()
        screen.blit(self.image, (self.x, self.y))
    
    def make_image(self):
        "get a random position and blit a number on a surface"
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

    def random_pos(self):
        "Return a tuple among 7x7 grid and del it from list"
        global pos

        position = random.choice(pos)

        print(f"{pos=}")
        print(f"{position=}")
        x, y = position
        # keeps deleting positions to avoid overlapping, 'til we got them
        del pos[pos.index(position)]
        x = x * 50
        y = y * 50
        return x, y


g = pygame.sprite.Group()
num_order = []
score = 0
# This covers the numbers...
bgd = pygame.Surface((50, 50))
bgd.fill((255, 0, 0))


def hide_cards():
    global pos

    for sprite in g:
        bgd.fill((0, 255, 0))
        sprite.image.blit(bgd, (0, 0))
    pos = [(x, y) for x in range(1, 8) for y in range(1, 8)]

def mouse_collision(sprite):
    global num_order, score, counter_on, max_count, cards_visible
    global bonus

    def clear_screen():
        global num_order, counter_on, cards_visible

        num_order = []
        counter_on = 1
        cards_visible = 1

    # Check the collision only when conter is off
    x, y = pygame.mouse.get_pos()
    if sprite.rect.collidepoint(x, y):
        click.play()
        print("touched")
        print(sprite.rect.collidepoint(x, y))
        print(sprite.number)
        # bgd.fill((0, 255, 0))
        # sprite.image.blit(bgd, (0, 0))
        num_order.append(sprite.number)
        sprite.rect = pygame.Rect(-50, -50, 50, 50)

        # Check if you are wrong as you type
        if sprite.number != str(len(num_order)):
            clear_screen()
            # num_order = []
            # counter_on = 1
            # pygame.mouse.set_visible(False)
            g.update()
            screen.fill((0,0,0))
            bgd.fill((255, 0, 0))

    if len(num_order) == len(g):
        print("fine")
        print(num_order)
        # ======== YOU GUESSED === Score: add bonus
        win = num_order == [str(s.number) for s in g]
        if win:
            # bonus is for clicking before counter stops
            # when you click... it memories the bonus in main()
            score += 100 + bonus
            print("You won - Score: " + str(score))
            g.add(Square(len(g) + 1))
            max_count = max_count + 10
            clear_screen()
        else:
            clear_screen()

        g.update()
        screen.fill((0,0,0))
        bgd.fill((255, 0, 0))



######################
#     sound init: load each sound individually         #
######################
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.mixer.quit()
pygame.mixer.init(22050, -16, 2, 512)
pygame.mixer.set_num_channels(32)
# The sounds: activate them with name.play()
click = pygame.mixer.Sound("click.wav")


def squares_init():
    for i in range(1, 4):
        g.add(Square(i))


counter = 0
counter_on = 1
max_count = 100
cards_visible = 1


def main():
    global counter_on, counter, max_count, cards_visible
    global bonus, click

    game_init()
    squares_init()
    clock = pygame.time.Clock()
    loop = 1
    chimp = pygame.image.load("img\\chimp.png")
    # pygame.mouse.set_visible(False)
    # soundtrack("sounds/soave.ogg")
    while loop:
        screen.fill((0, 0, 0))
        text = font.render("Livello: " + str(score), 1, (255, 244, 0))
        screen.blit(text, (0, 0))
        
        screen.blit(pygame.transform.scale(chimp, (400, 400)), (0, 0))
        if counter_on:
            text = font.render("time: " + str(max_count - counter), 1, (255, 244, 0))
            screen.blit(text, (200, 0))
            counter += 1
            if counter % 4 == 0:
                click.play()
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
                # Click mouse and stop the timer and hide the cards
                if cards_visible:
                    hide_cards()
                    # bonus to click early: add to score if win
                    bonus = max_count - counter
                    cards_visible = 0
                    counter_on = 0
                    counter = 0
                # This checks the cards you hit
                for s in g:
                    mouse_collision(s)    


        g.draw(screen)
        # Hides the number...
        if counter == max_count:
            hide_cards()
            counter = 0
            counter_on = 0

                # pygame.mouse.set_visible(True)
        pygame.display.update()
        clock.tick(20)

    pygame.quit()


main()
