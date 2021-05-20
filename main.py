import random
import math

import pygame
from pygame import mixer

# Initialize the pygame
pygame.init()

# create the screen (X,Y) from top left of window
screen = pygame.display.set_mode((1000, 667))

# Background
background = pygame.image.load("background.jpg")

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders The Game")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 490
playerY = 560
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 10

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 936))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1)
    enemyY_change.append(40)

# Missile

# Ready - You can't see the bullet on the screen
# Fire - The missile is currently moving 
missileImg = pygame.image.load('missile.png')
missileX = 0
missileY = 560
missileX_change = 0
missileY_change = 1
missile_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

# Explosion
explosionImg = pygame.image.load('explosion64.png')

textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

# show score 
def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y)) # blit means draw

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (0, 0, 0))
    screen.blit(over_text, (310, 300))

def player(x, y):
    screen.blit(playerImg, (x, y)) # blit means draw

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y)) # blit means draw

def fire_missile(x, y):
    global missile_state
    missile_state = "fire"
    screen.blit(missileImg, (x+16, y+10))

def isCollision(enemyX, enemyY, missileX, missileY):
    distance = math.sqrt(math.pow(enemyX - missileX, 2) + math.pow(enemyY - missileY, 2)) 
    if distance < 27:
        screen.blit(explosionImg, (enemyX, enemyY))
        pygame.display.update()
        return True
    


# Game Loop -------------------------------------------------------------------------------------------------------------------

running = True
while running:
    # RGB - Red, Green, Blue
    screen.fill((0,0,250))
    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed check whether it's right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if missile_state == "ready":
                    missile_Sound = mixer.Sound('laser.wav')
                    missile_Sound.play()
                    missileX = playerX
                    fire_missile(missileX, missileY)
       
        if event.type == pygame.KEYUP:
           if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Keeps spaceship in bounds
    playerX += playerX_change

    if playerX <=0:
        playerX = 0
    elif playerX >= 936:
        playerX = 936

    
   
    for i in range(num_of_enemies):

        # Game over
        if enemyY[i] > 550:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        # Enemy movement
        enemyX[i] += enemyX_change[i]

         # Keeps enemy in bounds
        if enemyX[i] <=0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 936:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]
       
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], missileX, missileY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            missileY = 560
            missile_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 936)
            enemyY[i] = random.randint(50, 150)
       
        enemy(enemyX[i], enemyY[i], i)

    # Missile movement 
    if missile_state == "fire":
        fire_missile(missileX, missileY)
        missileY -= missileY_change
        if missileY == 0:
            missileY = 560
            missile_state = "ready"


    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
