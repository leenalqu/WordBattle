#Coded by Jiaxi Huang (5670238)

#Import libraries
import pygame
import sys

#Initialize Pygame
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

    # Draw Boxes
    for i in range(CURRENT_WORD_BOXES):
        x = CURRENT_WORD_BOX_START_X + i * CURRENT_WORD_BOX_SPACING
        y = CURRENT_WORD_BOX_Y
        pygame.draw.rect(screen, BORDER_COLOR, (x, y, CURRENT_WORD_BOX_WIDTH, CURRENT_WORD_BOX_HEIGHT), 2)

#Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Draw Background
    screen.fill(BACKGROUND_COLOR)

    #Draw Sections
    draw_current_word()

    #Refresh Screen
    pygame.display.flip()

#Quit Pygame
pygame.quit()
sys.exit()
