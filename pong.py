import pygame, sys, random

def ball_animation():
    global BALL_SPEED_X, BALL_SPEED_Y, player_score, opponent_score, score_time

    # move because add position and it's looped
    ball.x += BALL_SPEED_X
    ball.y += BALL_SPEED_Y

    # border
    if ball.x <= 0:
        pygame.mixer.Sound.play(score_sound)
        player_score += 1
        score_time = pygame.time.get_ticks()

    if ball.x >= SCREEN_WIDTH:
        pygame.mixer.Sound.play(score_sound)
        opponent_score += 1
        score_time = pygame.time.get_ticks()

    if ball.y <= 0 or ball.y >= SCREEN_HEIGHT:
        pygame.mixer.Sound.play(pong_sound)
        BALL_SPEED_Y *= -1


    # collision with player or opponent
    if ball.colliderect(player) and BALL_SPEED_X > 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.right - player.left) < 10:
            BALL_SPEED_X *= -1
        elif abs(ball.bottom - player.top) < 10 and BALL_SPEED_Y > 0:
            BALL_SPEED_Y *= -1
        elif abs(ball.top - player.bottom) < 10 and BALL_SPEED_Y < 0:
            BALL_SPEED_Y *= -1

    if ball.colliderect(opponent) and BALL_SPEED_X < 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.left - opponent.right) < 10:
            BALL_SPEED_X *= -1
        elif abs(ball.bottom - opponent.top) < 10 and BALL_SPEED_Y > 0:
            BALL_SPEED_Y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and BALL_SPEED_Y < 0:
            BALL_SPEED_Y *= -1
        


def player_animation():
    # fix player position
    if player.top <= 0:
        player.top = 0
    if player.bottom >= SCREEN_HEIGHT:
        player.bottom = SCREEN_HEIGHT

    player.y += player_speed

def opponent_ai():
    # chase ball ai
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed

def opponent_animation():
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= SCREEN_HEIGHT:
        opponent.bottom = SCREEN_HEIGHT

def ball_restart():
    global BALL_SPEED_X, BALL_SPEED_Y, score_time

    ball.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    current_time = pygame.time.get_ticks()

    if (current_time - score_time) < 700:
        number_three = game_font.render("3", False, LIGHT_GREY)
        screen.blit(number_three, (SCREEN_WIDTH / 2 -10, SCREEN_HEIGHT / 2 + 20))

    if 700 < (current_time - score_time) < 1400:
        number_two = game_font.render("2", False, LIGHT_GREY)
        screen.blit(number_two, (SCREEN_WIDTH / 2 -10, SCREEN_HEIGHT / 2 + 20))

    if 1400 < (current_time - score_time) < 2100:
        number_one = game_font.render("1", False, LIGHT_GREY)
        screen.blit(number_one, (SCREEN_WIDTH / 2 -10, SCREEN_HEIGHT / 2 + 20))


    # stops for 2100ms
    if (current_time - score_time) < 2100:
        BALL_SPEED_X, BALL_SPEED_Y = 0, 0
    else:
        BALL_SPEED_X = 7 * random.choice((-1, 1))
        BALL_SPEED_Y = 7 * random.choice((-1, 1))
        score_time = None




# general setup
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

# setting up main window
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("pong game")


# game rect
ball = pygame.Rect(SCREEN_WIDTH / 2 - 15, SCREEN_HEIGHT / 2 - 15, 30, 30)
player = pygame.Rect(SCREEN_WIDTH - 20, SCREEN_HEIGHT / 2 - 70, 10, 140)
opponent = pygame.Rect(10, SCREEN_HEIGHT / 2 - 70, 10, 140)


BG_COLOR = pygame.Color('grey12')
LIGHT_GREY = (200, 200, 200)

# ball speed
BALL_SPEED_X = 7 * random.choice((-1, 1))
BALL_SPEED_Y = 7 * random.choice((-1, 1))


# player speed
player_speed = 0
# opponent speed
opponent_speed = 10


# text variables
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 32) # create font

# score timer
score_time = 1

# sound
pong_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")




while True:
    # handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_speed -= 7
            if event.key == pygame.K_DOWN:
                player_speed += 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player_speed += 7
            if event.key == pygame.K_DOWN:
                player_speed -= 7

    ball_animation()
    player_animation()
    opponent_ai()
    opponent_animation()

    #visuals
    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, LIGHT_GREY, player)
    pygame.draw.rect(screen, LIGHT_GREY, opponent)
    pygame.draw.ellipse(screen, LIGHT_GREY, ball)
    pygame.draw.aaline(screen, LIGHT_GREY, (SCREEN_WIDTH / 2, 0), (SCREEN_WIDTH/2, SCREEN_HEIGHT))

    # score time
    if score_time:
        ball_restart()

    # render player text render
    player_text = game_font.render(f"{player_score}", False, LIGHT_GREY) # create surface and draw font
    screen.blit(player_text, (660, 470)) # put that surface into screen surface
    # render opponent text
    opponent_text = game_font.render(f"{opponent_score}", False, LIGHT_GREY) # create surface and draw font
    screen.blit(opponent_text, (600, 470)) # put that surface into screen surface



    # update the window
    pygame.display.flip()
    clock.tick(60)