import pygame
import random
from pygame import mixer

# initiate pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))  # Width, Length

background = pygame.image.load("background.jpg")

# Game Over
game_over_font = pygame.font.Font("freesansbold.ttf", 64)


def print_game_over():
    game_over = game_over_font.render(" Game Over", True, (255, 255, 255))
    screen.blit(game_over, (200, 250))


# Score
show_score = 0
font = pygame.font.Font("freesansbold.ttf", 32)

textX = 10
textY = 10


def print_score(x, y):
    score = font.render("Score : " + str(show_score), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("player.png")
playerX = 380
playerY = 500

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 5
for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 730))
    enemyY.append(random.randint(50, 100))
    enemyX_change.append(0.1)
    enemyY_change.append(30)

bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 500
bulletX_change = 0
bulletY_change = 0.3
bullet_state = 'ready'


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(ex, ey, bx, by):
    distance = ((ex - bx) ** 2 + (ey - by) ** 2) ** 0.5
    if distance < 30:
        return True
    else:
        return False


# Game loop
running = True

playerX_change = 0

while running:
    # RGB - Red, Green, Blue
    screen.fill((0, 0, 0))

    # Background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    bullet(playerX, bulletY)
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Boundary Check
    if playerX <= 0:
        playerX = 0
    elif playerX >= 730:
        playerX = 730

    for i in range(no_of_enemies):

        if enemyY[i] >= 460:
            for j in range(no_of_enemies):
                enemyY[j] = 2000
            print_game_over()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 735:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            show_score += 10
            enemyX[i] = random.randint(0, 730)
            enemyY[i] = random.randint(50, 100)
            enemy(enemyX[i], enemyY[i], i)
        enemy(enemyX[i], enemyY[i], i)
    player(playerX, playerY)
    print_score(textX, textY)
    pygame.display.update()
