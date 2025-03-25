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

#Config_Current_Word
CURRENT_WORD_TITLE = "CURRENT WORD"
CURRENT_WORD_TITLE_POS = (SCREEN_WIDTH // 2, 85)
CURRENT_WORD_BOX_WIDTH = 81.9
CURRENT_WORD_BOX_HEIGHT = 114.4
CURRENT_WORD_BOX_SPACING = 100
CURRENT_WORD_BOX_START_X = 210
CURRENT_WORD_BOX_Y = 120
CURRENT_WORD_BOXES = 4

#Config_Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Letter Card Game")

#Config_Font
font = pygame.font.Font(None, FONT_SIZE)

def draw_current_word():
    #Draw Title
    text = font.render(CURRENT_WORD_TITLE, True, TEXT_COLOR)
    screen.blit(text, (CURRENT_WORD_TITLE_POS[0] - text.get_width() // 2, CURRENT_WORD_TITLE_POS[1]))

#Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Draw Background
    screen.fill(BACKGROUND_COLOR)

    # Draw sections
    draw_current_word()

#Quit
pygame.quit()
sys.exit()
