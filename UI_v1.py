#Coded by Jiaxi Huang (5670238)

#Import libraries
import pygame
import sys

#Initialize Pygame
pygame.init()

#Config_Mode
MODE = 1

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
CURRENT_WORD_TITLE_POS = (SCREEN_WIDTH // 2, 100)
CURRENT_WORD_BOX_WIDTH = 81.9
CURRENT_WORD_BOX_HEIGHT = 114.4
CURRENT_WORD_BOX_SPACING = 100
if MODE == 0:
    CURRENT_WORD_BOX_START_X = 260
    CURRENT_WORD_BOX_Y = 135
    CURRENT_WORD_BOXES = 3
elif MODE == 1:
    CURRENT_WORD_BOX_START_X = 210
    CURRENT_WORD_BOX_Y = 135
    CURRENT_WORD_BOXES = 4

#Config_Table
PLAYER_TURN_TITLE = "YOUR TURN"
PLAYER_TURN_TITLE_POS = (SCREEN_WIDTH // 2, 415)
CORRECT_BUTTON_POS = (240, 450)
CORRECT_BUTTON_WIDTH = 150
CORRECT_BUTTON_HEIGHT = 50
CORRECT_BUTTON_TEXT = "CORRECT"
FAILED_BUTTON_POS = (410, 450)
FAILED_BUTTON_WIDTH = 150
FAILED_BUTTON_HEIGHT = 50
FAILED_BUTTON_TEXT = "FAILED"
SKIP_BUTTON_POS = (350, 520)
SKIP_BUTTON_WIDTH = 100
SKIP_BUTTON_HEIGHT = 40
SKIP_BUTTON_TEXT = "SKIP"

#Config_Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
if MODE == 0:
    pygame.display.set_caption("Three-Letter Card Game")
elif MODE == 1:
    pygame.display.set_caption("Four-Letter Card Game")

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

def draw_player_table():
    #Draw Title
    text = font.render(PLAYER_TURN_TITLE, True, TEXT_COLOR)
    screen.blit(text, (PLAYER_TURN_TITLE_POS[0] - text.get_width() // 2, PLAYER_TURN_TITLE_POS[1]))

    #Draw Correct_Button
    correct_button = pygame.Rect(CORRECT_BUTTON_POS[0], CORRECT_BUTTON_POS[1], CORRECT_BUTTON_WIDTH, CORRECT_BUTTON_HEIGHT)
    pygame.draw.rect(screen, BUTTON_COLOR, correct_button)
    text = font.render(CORRECT_BUTTON_TEXT, True, TEXT_COLOR)
    screen.blit(text, (correct_button.centerx - text.get_width() // 2, correct_button.centery - text.get_height() // 2))

    #Draw Failed_Button
    failed_button = pygame.Rect(FAILED_BUTTON_POS[0], FAILED_BUTTON_POS[1], FAILED_BUTTON_WIDTH, FAILED_BUTTON_HEIGHT)
    pygame.draw.rect(screen, BUTTON_COLOR, failed_button)
    text = font.render(FAILED_BUTTON_TEXT, True, TEXT_COLOR)
    screen.blit(text, (failed_button.centerx - text.get_width() // 2, failed_button.centery - text.get_height() // 2))

    #Draw Skip_Button
    skip_button = pygame.Rect(SKIP_BUTTON_POS[0], SKIP_BUTTON_POS[1], SKIP_BUTTON_WIDTH, SKIP_BUTTON_HEIGHT)
    pygame.draw.rect(screen, BUTTON_COLOR, skip_button)
    text = font.render(SKIP_BUTTON_TEXT, True, TEXT_COLOR)
    screen.blit(text, (skip_button.centerx - text.get_width() // 2, skip_button.centery - text.get_height() // 2))

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
    draw_player_table()

    #Refresh Screen
    pygame.display.flip()

#Quit Pygame
pygame.quit()
sys.exit()
