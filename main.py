import pygame
import random
import math
from pygame import mixer

# initialising pygame
pygame.init()
# pygame. -->access pygame module
# 600-->600 pixels of height -->800 pixels of width
screen = pygame.display.set_mode((800, 600))
# creating the screen
# game window created but went away after a few seconds
# if we use an infinite while loop the window does not respond as we don't have an event
# Game loop ,running always
# background
background = pygame.image.load('background.png')
mixer.music.load('background.wav')
mixer.music.play(-1)
pygame.display.set_caption('Space invaders')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
playerimg = pygame.image.load('player.png')
player_x = 370
player_y = 480
player_x_change = 0
enemyimg = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load('enemy.png'))
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(0.7)
    enemy_y_change.append(15)
bulletimg = pygame.image.load('bullet.png')
bullet_y = 480
bullet_x = 0
bullet_x_change = 0
bullet_y_change = 1.5
bullet_state = "ready"
score_value = 0
font = pygame.font.Font('paradise.otf', 40)  #
textX = 10
textY = 10
game_font = pygame.font.Font('freesansbold.ttf', 64)


def display_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))
def game_over_text():
    over_text = game_font.render("GAME OVER ", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))
def player(x, y):
    screen.blit(playerimg, (x, y))
def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))
def iscollision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + (math.pow(enemy_y - bullet_y, 2)))
    if distance < 27:
        return True
    else:
        return False


running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -1.5
            if not event.key != pygame.K_RIGHT:
                player_x_change = 1.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0
    # player movement
    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736
    # enemy movement
    for i in range(num_of_enemies):
        # game over
        if enemy_y[i] > 440:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            game_over_text()
            break
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 0.7
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -0.7
            enemy_y[i] += enemy_y_change[i]
        # collision
        collision = iscollision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 100
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(0, 100)
        enemy(enemy_x[i], enemy_y[i], i)
    # bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change
    player(player_x, player_y)
    display_score(textX, textY)
    pygame.display.update()
