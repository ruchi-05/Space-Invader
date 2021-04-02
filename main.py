import pygame
import random
import math
from pygame import mixer

# initializing pygame
pygame.init()

# creating a screen
screen = pygame.display.set_mode((800, 600))

# background image
background = pygame.image.load("background.png")

# background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# TITLE AND ICON
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# player
playerimg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_chng = 0

# Enemy

Enemyimg = []
enemyX = []
enemyY = []
enemyX_chng = []
enemyY_chng = []

num_of_enemies = 10
for i in range(num_of_enemies):
    Enemyimg.append(pygame.image.load("monsters.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(40, 150))
    enemyX_chng.append(2)
    enemyY_chng.append(40)

# bullet

# ready = it cant be seen
# fire = it is moving

bulletimg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_chng = 0
bulletY_chng = 10
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

#game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("SCORE : " + str(score_value), True, (255, 255, 255))
    screen.blit(score,(x,y))

def game_over_text():
    over = over_font.render("GAME OVER ", True, (255, 255, 255))
    screen.blit(over, (200,250))

def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(Enemyimg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = " fire "
    screen.blit(bulletimg, (x + 16, y + 10))


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# GAME LOOP(MAKES SURE THE GAME KEEPS RUNNING)
running = True
while running:

    # background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_chng = -5
            if event.key == pygame.K_RIGHT:
                playerX_chng = +5
            if event.key == pygame.K_SPACE :
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    # get the current coordinates of player and give to bullet
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_chng = 0

    # checking for boundaries so it doesnt go out of bounds
    playerX += playerX_chng

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):

        # game over
        if enemyY[i] > 480:
            for j in range (num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break


        enemyX[i] += enemyX_chng[i]
        if enemyX[i] <= 0:
            enemyX_chng[i] = 2
            enemyY[i] += enemyY_chng[i]
        elif enemyX[i] >= 736:
            enemyX_chng[i] = -2
            enemyY[i] += enemyY_chng[i]

        # collision
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(40, 150)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is " fire ":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_chng

    player(playerX, playerY)
    show_score(textX,testY)
    pygame.display.update()
