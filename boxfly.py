import pygame
import os
import random

# variables
score = 0
highscore = 0
row = 2
deathtimer = 0
obstavel = 4
timertimer = 0
x = 0
box_x = 50
obstacle_timer = 0
cooldown = False
double = 1
bad = False
death = False
title_running = True



pygame.init()
pygame.mixer.init()


WIDTH, HEIGHT = 600, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("hmmmm")

up = 125
middle = 225
down = 325

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
LIME = 0, 255, 0
BLUE = 0, 0, 255
YELLOW = 255, 255, 0
CYAN = 0, 255, 255
MAGENTA = 255, 0, 255
SILVER = 192, 192, 192
GREY = 128, 128, 128
DARKGREY = 64, 64, 64
MAROON = 128, 0, 0
OLIVE = 128, 128, 0
GREEN = 0, 128, 0
PURPLE = 128, 0, 128
TEAL = 0, 128, 128
NAVY = 0, 0, 128
SKYBLUE = 135, 206, 235

SCORE_SOUND = pygame.mixer.Sound(os.path.join("gametestassets", "pickupCoin.wav"))
BAD_SOUND = pygame.mixer.Sound(os.path.join("gametestassets", "warrior_laugh.wav"))


FONT = pygame.font.SysFont("russoone", 40)
BIGFONT = pygame.font.SysFont("russoone", 60)


FPS = 60


if __name__ == "__main__":
    player = pygame.Rect(100, middle, 50, 50)

    obstacles = []

    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # checks if title screen is running
        if title_running == True:
            # checks if a key is pressed
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                title_running = False

            WIN.fill(SKYBLUE)
            titletext = BIGFONT.render("boxes flying and stuff", 1, BLACK)
            keytext = FONT.render("press any key to begin", 1, BLACK)
            WIN.blit(titletext, (50, 50))
            WIN.blit(keytext, (50, 110))
            box = pygame.Rect(box_x, 300, 50, 50)
            box_x += 1
            pygame.draw.rect(WIN, NAVY, box)
        else:
            # movement between rows and checks if the player is dead
            keys_pressed = pygame.key.get_pressed()
            if death == False:
                if keys_pressed[pygame.K_w] and row > 1 and cooldown == False:
                    row -= 1
                    cooldown = True
                if keys_pressed[pygame.K_s] and row < 3 and cooldown == False:
                    row += 1
                    cooldown = True

            # cooldown on movement to prevent just holding keys down
            if cooldown == True:
                x += 1
                if x == 10:
                    x = 0
                    cooldown = False

            if row == 1:
                player.y = up
            elif row == 2:
                player.y = middle
            elif row == 3:
                player.y = down

            # spawning obstacles
            if death != True:
                obstacle_timer += 1
                # generating a random number to decide if there are multiple obstacles
                double = random.randint(2, 3)
                # this only runs if there are 2 obstacles
                if obstacle_timer == 60 and double == 3:
                    rand = random.randint(1,3)
                    if rand == 1:
                        oy = up
                    elif rand == 2:
                        oy = middle
                    elif rand == 3:
                        oy = down
                    obstacle = pygame.Rect(600, oy - 25, 100, 100)
                    obstacles.append(obstacle)
                # this always runs
                if obstacle_timer == 60:
                    obstacle_timer = 0
                    rand = random.randint(1, 3)
                    if rand == 1:
                        oy = up
                    elif rand == 2:
                        oy = middle
                    elif rand == 3:
                        oy = down
                    obstacle = pygame.Rect(600, oy - 25, 100, 100)
                    obstacles.append(obstacle)
                    obstacle_timer = 0

            timertimer += 1
            if timertimer == 120:
                timertimer = 0
                obstavel += 0.2

            WIN.fill(SKYBLUE)

            pygame.draw.rect(WIN, NAVY, player)
            for obstacle in obstacles:
                # draws and moves obstacles
                pygame.draw.rect(WIN, RED, obstacle)
                obstacle.x -= obstavel
                # score system
                if player.x == obstacle.x:
                    if bad == False:
                        score += 1
                        SCORE_SOUND.play()
                    bad = True
                else:
                    bad = False
                if player.colliderect(obstacle):
                    death = True
            if death == True:
                deathtext = FONT.render("You died!", 1, BLACK)
                BAD_SOUND.play()
                WIN.blit(deathtext, (10, 70))
                obstacles = []
                deathtimer += 1
                if deathtimer == 60:
                    deathtimer = 0
                    if score > highscore:
                        highscore = score
                    score = 0
                    death = False

            scoretext = FONT.render("Score: " + str(score), 1, BLACK)
            WIN.blit(scoretext, (10, 10))
            highscoretext = FONT.render("Highscore: " + str(highscore), 1, BLACK)
            WIN.blit(highscoretext, (10, 40))


        pygame.display.update()
