import pygame
import os

WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # window size
pygame.display.set_caption("SPACE WAR")

BLUE = (20, 20, 200)
VEL = 5

FPS = 60

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png')) #use os.path.join to avoid going to path via slashes
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (60, 50)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (60, 50)), 270)

def draw_window(red, yellow): # draw all the stuff
    WIN.fill(BLUE)
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y)) # use blit when you want to draw a surface on the screen
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    pygame.display.update()


def main(): # create main game loop in the main function

    red = pygame.Rect(700, 300, 60, 50)
    yellow = pygame.Rect(100, 300, 60, 50)

    clock = pygame.time.Clock() # define clock object

    run = True # main game loop keeping window open
    while run:
        clock.tick(FPS) # control the speed of the while loop/second
        for event in pygame.event.get(): # loop through all events in python
            if event.type == pygame.QUIT: # if QUIT is the event that occurs, set run to False which quits game
                run = False

        keys_pressed = pygame.key.get_pressed() # every time the while loop is running, it's going to tell us what keys are pressed
        if keys_pressed[pygame.K_a]: # LEFT
            yellow.x -= VEL
        if keys_pressed[pygame.K_d]: # RIGHT
            yellow.x += VEL
        if keys_pressed[pygame.K_w]: # UP
            yellow.y += VEL        
        if keys_pressed[pygame.K_s]: # DOWN
            yellow.y += VEL


        draw_window(red, yellow)

    pygame.quit


if __name__ == "__main__": 
    main() # make sure that we run this main function only if we run this file directly