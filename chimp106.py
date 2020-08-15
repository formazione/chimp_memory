'''  Possible positions on the grid 7 x 7

'''

import pygame
import random
import os


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



def hide_cards():
    global pos

    for sprite in g:
        bgd.fill((0, 244, 0))
        sprite.image.blit(bgd, (0, 0))

    # Rebuilds the positions to not empty it
    pos = [(x, y) for x in range(1, 8) for y in range(1, 8)]

def mouse_collision(sprite):
    global num_order, score, maxscore
    global counter_on, max_count, cards_visible
    global bonus

    def clear_screen():
        global num_order, counter_on, cards_visible
        num_order = []
        counter_on = 1
        cards_visible = 1

    x, y = pygame.mouse.get_pos()
    if sprite.rect.collidepoint(x, y):
        click.play()
        num_order.append(sprite.number)
        # Put the sprite out of the window
        sprite.rect = pygame.Rect(-50, -50, 50, 50)
        # if you make a mistake it repeats the level
        if sprite.number != str(len(num_order)):
            # cover the other tiles when you click the first
            clear_screen()
            score = score - 50
            # g.update()
            # creates a new image
            [s.make_image() for s in g]
            screen.fill((0,0,0))
            bgd.fill((255, 0, 0))
        # if you clicked the right number...
        else:
            score += 10
            # If the sequence is completed
            if len(num_order) == len(g):
                score += 100 + bonus
                if score > int(maxscore):
                    maxscore = score
                    set_score(maxscore)
                #print("You won - Score: " + str(score))
                g.add(Square(len(g) + 1))
                max_count = max_count + 10
                clear_screen()
                # this was g.update()
                [s.make_image() for s in g]
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
click = pygame.mixer.Sound("audio/click.wav")


def squares_init():
    for i in range(1, 4):
        g.add(Square(i))


counter = 0
counter_on = 1
max_count = 100
cards_visible = 1


def get_maxscore() -> int:
    filename = "maxscore.txt"
    if filename in os.listdir():
        with open(filename, "r") as file:
            val = file.read()
            if val == "":
                maxscore = 0
            else:
                maxscore = int(val)
    else:
        maxscore = 0
    return maxscore


def set_score(maxscore) -> None:

    with open("maxscore.txt", "w") as file:
        file.write(str(maxscore))


maxscore = get_maxscore()
def main():
    global counter_on, counter, max_count, cards_visible
    global bonus, click, score, g

    game_init()
    squares_init()
    music = pygame.mixer.music
    music.load("audio/soave2.wav")
    music.play(-1)
    #[s.make_image() for s in g]
    clock = pygame.time.Clock()
    loop = 1
    chimp = pygame.image.load("img/chimp.png")
    # pygame.mouse.set_visible(False)
    # soundtrack("sounds/soave.ogg")
    while loop:
        screen.fill((0, 0, 0))
        text = font.render("Memory: " + str(score), 1, (255, 244, 0))
        record = font.render("Record: " + str(maxscore), 1, (255, 244, 0))
        screen.blit(text, (0, 0))
        screen.blit(record, (150, 0))
        
        screen.blit(pygame.transform.scale(chimp, (400, 400)), (0, 0))
        if counter_on:
            text = font.render("time: " + str(max_count - counter), 1, (255, 244, 0))
            screen.blit(text, (300, 0))
            counter += 1
            if counter % 4 == 0:
                click.play()
        for event in pygame.event.get():
            # ========================================= QUIT
            if event.type == pygame.QUIT:
                loop = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    loop = 0
                if event.key == pygame.K_m:
                    music.stop()
                if event.key == pygame.K_r:
                    num_order = []
                    for s in g:
                        g.remove(s)
                    # squares_init()
                    screen.fill((0,0,0))
                    pos = [(x, y) for x in range(1, 8) for y in range(1, 8)]
                    couter = 0
                    counter_on = 1
                    score = 0
                    main()
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
