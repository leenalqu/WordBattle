#Coded by Jiaxi Huang
import pygame
import sys

pygame.init()

#Config_Settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (255, 255, 255)
BORDER_COLOR = (0, 0, 0)
BUTTON_COLOR = (200, 200, 200)
TEXT_COLOR = (0, 0, 0)
FONT_SIZE = 36

#Config_Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Letter Card Game")

#Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Draw Background
    screen.fill(BACKGROUND_COLOR)

#QuitS
pygame.quit()
sys.exit()