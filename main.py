from concurrent.futures.thread import BrokenThreadPool
import pygame
import os
pygame.font.init()

WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # window size
pygame.display.set_caption("SPACE WAR")


BLUE = (20, 20, 200)
BLACK = (0,0,0)
WHITE = (255, 255, 255)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('arial', 100)

VEL = 5
FPS = 60

BULLET_VEL = 7
MAX_BULLETS = 5

YELLOW_HIT = pygame.USEREVENT + 1 # create a new event and adding + 1 too keep it unique
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png')) #use os.path.join to avoid going to path via slashes
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (60, 50)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (60, 50)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))



def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health): # draw all the stuff
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y)) # use blit when you want to draw a surface on the screen
    WIN.blit(RED_SPACESHIP, (red.x, red.y))


    for bullet in red_bullets:
        pygame.draw.rect(WIN, (255, 0, 0, 0), bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, (255, 255, 0, 0), bullet)

    pygame.display.update()



def yellow_handle_movement(keys_pressed, yellow):
        if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # LEFT
            yellow.x -= VEL
        if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: # RIGHT #after and statement, add yellow.width to prevent image from touching border
            yellow.x += VEL
        if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: # UP
            yellow.y -= VEL        
        if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT: # DOWN
            yellow.y += VEL

def red_handle_movement(keys_pressed, red):
        if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: # LEFT
            red.x -= VEL
        if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: # RIGHT
            red.x += VEL
        if keys_pressed[pygame.K_UP] and red.y - VEL : # UP
            red.y -= VEL        
        if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT: # DOWN
            red.y += VEL



def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)


def draw_winner():
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width/2, WIDTH/2 - draw_text.get_width/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main(): # create main game loop in the main function

    red = pygame.Rect(1000, 300, 60, 50)
    yellow = pygame.Rect(100, 300, 60, 50)

    red_bullets = [] # keep a list of all the bullets for each player
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock() # define clock object

    run = True # main game loop keeping window open
    while run:
        clock.tick(FPS) # control the speed of the while loop/second
        for event in pygame.event.get(): # loop through all events in python
            if event.type == pygame.QUIT: # if QUIT is the event that occurs, set run to False which quits game
                run = False
                pygame.quit

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x, yellow.y + yellow.height//2, 10, 5)
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2, 10, 5)
                    red_bullets.append(bullet)   
            
            if event.type == RED_HIT:
                red_health -= 1

            if event.type == YELLOW_HIT:
                yellow_health -= 1

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        
        if red_health <= 0:
            winner_text = "Red Wins!"
        
        if winner_text != "":
            draw_winner(winner_text)

        keys_pressed = pygame.key.get_pressed() # every time the while loop is running, it's going to tell us what keys are pressed
        
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    main()


if __name__ == "__main__": 
    main() # make sure that we run this main function only if we run this file directly