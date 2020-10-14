import pygame
from pygame import mixer
import random
import os

pygame.init()



# Declaring colors
white = (255, 255, 255)
lime = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
cyan = (0, 255, 255)

# Creating Windows
screen_width = 900
screen_height = 600
GameWindow = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Game Title
pygame.display.set_caption("SnakeWithJayman")
pygame.display.update()

# Background Images
bgimg = pygame.image.load('background.png')
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

welimg = pygame.image.load('welcome.png')
welimg = pygame.transform.scale(welimg, (screen_width, screen_height)).convert_alpha()

overimg = pygame.image.load('GameOver.jpg')
overimg = pygame.transform.scale(overimg, (screen_width, screen_height)).convert_alpha()

# Background Sound
mixer.init()

# Showing score on screen
font = pygame.font.SysFont(None, 50, bold=True, italic=True)
def screen_text(text, color, x, y):
    text = font.render(text, True, color)
    GameWindow.blit(text, [x, y])


# Plotting Snake
def plot_snake(gamewindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gamewindow, color, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        GameWindow.fill((230,239,220))
        GameWindow.blit(welimg, (0,0))
        screen_text('Developer: Jayman', (127,255,20), 360, 70)
        screen_text('Press Enter To Continue', (20, 230, 190), 70, 480)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    mixer.music.load('sound.mp3')
                    mixer.music.play()
                    loop()

        pygame.display.update()
        clock.tick(60)


# Game loop
def loop():
    # Declaring Game Variables
    game_over = False
    exit_game = False

    #Snake Variables
    snake_x = 50
    snake_y = 60
    snake_size = 13

    velocity_x = 0
    velocity_y = 0
    vel_value = 3

    # Food Variables
    food_x = random.randint(30, screen_width / 2)
    food_y = random.randint(30, screen_height / 2)

    score = 0
    fps = 40

    # Reading highscore file
    if not os.path.exists('highscore.txt'):
        with open('highscore.txt', 'w') as f:
            f.write('0')

    with open('highscore.txt') as f:
        hscore = f.read()

    snk_list = []
    snk_length = 1

    while not exit_game:
        if game_over:
            with open('highscore.txt', 'w') as f:
                f.write(str(hscore))

            GameWindow.fill(cyan)
            GameWindow.blit(overimg, (0,0))
            screen_text(f"Score: {score}", (100,200,100), 350, 320)
            screen_text('Press Enter To Continue...', (100, 200, 100), 200, 540)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                    mixer.music.stop()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        mixer.music.stop()
                        welcome()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        velocity_x = -vel_value
                        velocity_y = 0

                    if event.key == pygame.K_RIGHT:
                        velocity_x = vel_value
                        velocity_y = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = vel_value
                        velocity_x = 0

                    if event.key == pygame.K_UP:
                        velocity_y = -vel_value
                        velocity_x = 0

            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - food_x) < 6 and abs(snake_y - food_y) < 6:
                score += 10
                food_x = random.randint(30, screen_width/2)
                food_y = random.randint(30, screen_height/2)
                snk_length += 4
                vel_value += 0.3

                if score > int(hscore):
                    hscore = score

            GameWindow.fill(black)
            GameWindow.blit(bgimg, (0,0))
            screen_text(f"Score: {score}" + '  HighScore:' + str(hscore), cyan, 240, 5)
            pygame.draw.rect(GameWindow, red, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_width:
                game_over = True
                mixer.music.stop()
                mixer.music.load('over.mp3')
                mixer.music.play()

            if head in snk_list[:-1]:
                game_over = True
                mixer.music.stop()
                mixer.music.load('over.mp3')
                mixer.music.play()

            plot_snake(GameWindow, (127,255,20), snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

welcome()