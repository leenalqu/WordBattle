#Coded by Jiaxi Huang (5670238)

#Import libraries
import pygame
import sys

#Initialize Pygame
pygame.init()

#Config_Mode
MODE = -1
ANSWER_STATUS = 2
TURN_STATUS = 0

#Config_Settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (255, 255, 255)
BORDER_COLOR = (0, 0, 0)
BUTTON_COLOR = (190, 190, 190)
BUTTON_COLOR_INACTIVE = (247, 248, 250)
BUTTON_COLOR_ACTIVE_RIGHT = (87, 150, 92)
BUTTON_COLOR_ACTIVE_WRONG = (201, 79, 79)
TEXT_COLOR = (0, 0, 0)
TEXT_COLOR_BUTTON_ANSWER = (255, 255, 255)
TEXT_COLOR_BUTTON_SKIP = (255, 255, 255)
FONT_SIZE = 36
#Config_Settings_Test
BUTTON_COLOR_TEST_RIGHT = (255, 255, 255)
BUTTON_COLOR_TEST_WRONG = (255, 255, 255)

#Config_Welcome_Page
welcome_image = pygame.image.load("Welcome_Page.png")
welcome_image = pygame.transform.scale(welcome_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
show_welcome = True

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
elif MODE == -1:
    CURRENT_WORD_BOX_START_X = 210
    CURRENT_WORD_BOX_Y = 135
    CURRENT_WORD_BOXES = 4

#Config_Player_Cards
PLAYER_CARDS_TITLE = "YOUR CARDS"
PLAYER_CARDS_TITLE_POS = (SCREEN_WIDTH // 2, 295)
PLAYER_CARDS_BOX_WIDTH = 47.25
PLAYER_CARDS_BOX_HEIGHT = 66
PLAYER_CARDS_BOX_SPACING = 50
PLAYER_CARDS_BOX_START_X = 28
PLAYER_CARDS_BOX_Y = 330
PLAYER_CARDS_BOXES = 15

#Config_Table
if TURN_STATUS == 0:
    PLAYER_TURN_TITLE = "YOUR TURN"
elif TURN_STATUS == 1:
    PLAYER_TURN_TITLE = "COMPUTER'S TURN"
PLAYER_TURN_TITLE_POS = (SCREEN_WIDTH // 2, 415)
RIGHT_BUTTON_POS = (240, 450)
RIGHT_BUTTON_WIDTH = 150
RIGHT_BUTTON_HEIGHT = 50
RIGHT_BUTTON_TEXT = "RIGHT"
WRONG_BUTTON_POS = (410, 450)
WRONG_BUTTON_WIDTH = 150
WRONG_BUTTON_HEIGHT = 50
WRONG_BUTTON_TEXT = "WRONG"
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
elif MODE == -1:
    pygame.display.set_caption("Debug")

#Config_Font
font = pygame.font.Font(None, FONT_SIZE)

#Config_Timer
TIMER_EVENT = pygame.USEREVENT + 1
TIMER_DURATION = 15
TIMER_SECONDS = TIMER_DURATION
TIMER_X = 375
TIMER_Y = 10
SHOW_POPUP = False
GAME_PAUSED = False
pygame.time.set_timer(TIMER_EVENT, 1000)
popup_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 75, 300, 150)
button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 25, 100, 30)

#Config_Popup
POPUP_WIDTH = 350
POPUP_HEIGHT = 150
POPUP_POS_X = SCREEN_WIDTH // 2 - POPUP_WIDTH // 2
POPUP_POS_Y = SCREEN_HEIGHT // 2 - POPUP_HEIGHT // 2
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 30
BUTTON_POS_X = SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2
BUTTON_POS_Y = SCREEN_HEIGHT // 2 + 25
POPUP_BACKGROUND_COLOR = (255, 255, 255)
POPUP_BORDER_COLOR = (0, 0, 0)
BUTTON_COLOR = (190, 190, 190)
BUTTON_BORDER_COLOR = (0, 0, 0)
POPUP_TEXT = "Turn has changed"
BUTTON_TEXT = "OK"

#Function Section
def draw_timer():
    global TIMER_SECONDS, TURN_STATUS
    timer_text = font.render(f"00:{TIMER_SECONDS:02d}", True, TEXT_COLOR)
    screen.blit(timer_text, (TIMER_X, TIMER_Y))

def draw_current_word():
    #Draw Title
    text = font.render(CURRENT_WORD_TITLE, True, TEXT_COLOR)
    screen.blit(text, (CURRENT_WORD_TITLE_POS[0] - text.get_width() // 2, CURRENT_WORD_TITLE_POS[1]))

    # Draw Boxes
    for i in range(CURRENT_WORD_BOXES):
        x = CURRENT_WORD_BOX_START_X + i * CURRENT_WORD_BOX_SPACING
        y = CURRENT_WORD_BOX_Y
        pygame.draw.rect(screen, BORDER_COLOR, (x, y, CURRENT_WORD_BOX_WIDTH, CURRENT_WORD_BOX_HEIGHT), 2)

def draw_PLAYER_CARDS():
    #Draw Title
    text = font.render(PLAYER_CARDS_TITLE, True, TEXT_COLOR)
    screen.blit(text, (PLAYER_CARDS_TITLE_POS[0] - text.get_width() // 2, PLAYER_CARDS_TITLE_POS[1]))

    #Draw Boxes
    for i in range(PLAYER_CARDS_BOXES):
        x = PLAYER_CARDS_BOX_START_X + i * PLAYER_CARDS_BOX_SPACING
        y = PLAYER_CARDS_BOX_Y
        pygame.draw.rect(screen, BORDER_COLOR, (x, y, PLAYER_CARDS_BOX_WIDTH, PLAYER_CARDS_BOX_HEIGHT), 2)

def draw_player_table():
    #Draw Title
    text = font.render(PLAYER_TURN_TITLE, True, TEXT_COLOR)
    screen.blit(text, (PLAYER_TURN_TITLE_POS[0] - text.get_width() // 2, PLAYER_TURN_TITLE_POS[1]))

    if ANSWER_STATUS == -1:
        #Draw RIGHT_BUTTON
        RIGHT_BUTTON = pygame.Rect(RIGHT_BUTTON_POS[0], RIGHT_BUTTON_POS[1], RIGHT_BUTTON_WIDTH, RIGHT_BUTTON_HEIGHT)
        pygame.draw.rect(screen, BUTTON_COLOR_INACTIVE, RIGHT_BUTTON)
        text = font.render(RIGHT_BUTTON_TEXT, True, TEXT_COLOR_BUTTON_ANSWER)
        screen.blit(text, (RIGHT_BUTTON.centerx - text.get_width() // 2, RIGHT_BUTTON.centery - text.get_height() // 2))

        #Draw WRONG_BUTTON
        WRONG_BUTTON = pygame.Rect(WRONG_BUTTON_POS[0], WRONG_BUTTON_POS[1], WRONG_BUTTON_WIDTH, WRONG_BUTTON_HEIGHT)
        pygame.draw.rect(screen, BUTTON_COLOR_INACTIVE, WRONG_BUTTON)
        text = font.render(WRONG_BUTTON_TEXT, True, TEXT_COLOR_BUTTON_ANSWER)
        screen.blit(text, (WRONG_BUTTON.centerx - text.get_width() // 2, WRONG_BUTTON.centery - text.get_height() // 2))

        #Draw Skip_Button
        skip_button = pygame.Rect(SKIP_BUTTON_POS[0], SKIP_BUTTON_POS[1], SKIP_BUTTON_WIDTH, SKIP_BUTTON_HEIGHT)
        pygame.draw.rect(screen, BUTTON_COLOR, skip_button)
        text = font.render(SKIP_BUTTON_TEXT, True, TEXT_COLOR_BUTTON_SKIP)
        screen.blit(text, (skip_button.centerx - text.get_width() // 2, skip_button.centery - text.get_height() // 2))

    if ANSWER_STATUS == 0:
        # Draw RIGHT_BUTTON
        RIGHT_BUTTON = pygame.Rect(RIGHT_BUTTON_POS[0], RIGHT_BUTTON_POS[1], RIGHT_BUTTON_WIDTH, RIGHT_BUTTON_HEIGHT)
        pygame.draw.rect(screen, BUTTON_COLOR_INACTIVE, RIGHT_BUTTON)
        text = font.render(RIGHT_BUTTON_TEXT, True, TEXT_COLOR_BUTTON_ANSWER)
        screen.blit(text, (RIGHT_BUTTON.centerx - text.get_width() // 2, RIGHT_BUTTON.centery - text.get_height() // 2))

        # Draw WRONG_BUTTON
        WRONG_BUTTON = pygame.Rect(WRONG_BUTTON_POS[0], WRONG_BUTTON_POS[1], WRONG_BUTTON_WIDTH, WRONG_BUTTON_HEIGHT)
        pygame.draw.rect(screen, BUTTON_COLOR_ACTIVE_WRONG, WRONG_BUTTON)
        text = font.render(WRONG_BUTTON_TEXT, True, TEXT_COLOR_BUTTON_ANSWER)
        screen.blit(text, (WRONG_BUTTON.centerx - text.get_width() // 2, WRONG_BUTTON.centery - text.get_height() // 2))

        # Draw Skip_Button
        skip_button = pygame.Rect(SKIP_BUTTON_POS[0], SKIP_BUTTON_POS[1], SKIP_BUTTON_WIDTH, SKIP_BUTTON_HEIGHT)
        pygame.draw.rect(screen, BUTTON_COLOR, skip_button)
        text = font.render(SKIP_BUTTON_TEXT, True, TEXT_COLOR_BUTTON_SKIP)
        screen.blit(text, (skip_button.centerx - text.get_width() // 2, skip_button.centery - text.get_height() // 2))

    if ANSWER_STATUS == 1:
        # Draw RIGHT_BUTTON
        RIGHT_BUTTON = pygame.Rect(RIGHT_BUTTON_POS[0], RIGHT_BUTTON_POS[1], RIGHT_BUTTON_WIDTH, RIGHT_BUTTON_HEIGHT)
        pygame.draw.rect(screen, BUTTON_COLOR_ACTIVE_RIGHT, RIGHT_BUTTON)
        text = font.render(RIGHT_BUTTON_TEXT, True, TEXT_COLOR_BUTTON_ANSWER)
        screen.blit(text, (RIGHT_BUTTON.centerx - text.get_width() // 2, RIGHT_BUTTON.centery - text.get_height() // 2))

        # Draw WRONG_BUTTON
        WRONG_BUTTON = pygame.Rect(WRONG_BUTTON_POS[0], WRONG_BUTTON_POS[1], WRONG_BUTTON_WIDTH, WRONG_BUTTON_HEIGHT)
        pygame.draw.rect(screen, BUTTON_COLOR_INACTIVE, WRONG_BUTTON)
        text = font.render(WRONG_BUTTON_TEXT, True, TEXT_COLOR_BUTTON_ANSWER)
        screen.blit(text, (WRONG_BUTTON.centerx - text.get_width() // 2, WRONG_BUTTON.centery - text.get_height() // 2))

        # Draw Skip_Button
        skip_button = pygame.Rect(SKIP_BUTTON_POS[0], SKIP_BUTTON_POS[1], SKIP_BUTTON_WIDTH, SKIP_BUTTON_HEIGHT)
        pygame.draw.rect(screen, BUTTON_COLOR, skip_button)
        text = font.render(SKIP_BUTTON_TEXT, True, TEXT_COLOR_BUTTON_SKIP)
        screen.blit(text, (skip_button.centerx - text.get_width() // 2, skip_button.centery - text.get_height() // 2))

    if ANSWER_STATUS == 2:
        # Draw RIGHT_BUTTON
        RIGHT_BUTTON = pygame.Rect(RIGHT_BUTTON_POS[0], RIGHT_BUTTON_POS[1], RIGHT_BUTTON_WIDTH, RIGHT_BUTTON_HEIGHT)
        pygame.draw.rect(screen, BUTTON_COLOR_ACTIVE_RIGHT, RIGHT_BUTTON)
        text = font.render(RIGHT_BUTTON_TEXT, True, TEXT_COLOR_BUTTON_ANSWER)
        screen.blit(text, (RIGHT_BUTTON.centerx - text.get_width() // 2, RIGHT_BUTTON.centery - text.get_height() // 2))

        # Draw WRONG_BUTTON
        WRONG_BUTTON = pygame.Rect(WRONG_BUTTON_POS[0], WRONG_BUTTON_POS[1], WRONG_BUTTON_WIDTH, WRONG_BUTTON_HEIGHT)
        pygame.draw.rect(screen, BUTTON_COLOR_ACTIVE_WRONG, WRONG_BUTTON)
        text = font.render(WRONG_BUTTON_TEXT, True, TEXT_COLOR_BUTTON_ANSWER)
        screen.blit(text, (WRONG_BUTTON.centerx - text.get_width() // 2, WRONG_BUTTON.centery - text.get_height() // 2))

        # Draw Skip_Button
        skip_button = pygame.Rect(SKIP_BUTTON_POS[0], SKIP_BUTTON_POS[1], SKIP_BUTTON_WIDTH, SKIP_BUTTON_HEIGHT)
        pygame.draw.rect(screen, BUTTON_COLOR, skip_button)
        text = font.render(SKIP_BUTTON_TEXT, True, TEXT_COLOR_BUTTON_SKIP)
        screen.blit(text, (skip_button.centerx - text.get_width() // 2, skip_button.centery - text.get_height() // 2))

#Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #Pause Game when Welcome Page
        if show_welcome:
            if event.type == pygame.MOUSEBUTTONDOWN:
                show_welcome = False
        #Pause Game when Popup
        elif event.type == TIMER_EVENT:
            if TIMER_SECONDS > 0 and not GAME_PAUSED:
                TIMER_SECONDS -= 1
            else:
                TURN_STATUS = 1 - TURN_STATUS
                TIMER_SECONDS = TIMER_DURATION
                if TURN_STATUS == 0:
                    PLAYER_TURN_TITLE = "YOUR TURN"
                else:
                    PLAYER_TURN_TITLE = "COMPUTER'S TURN"
                SHOW_POPUP = True
                GAME_PAUSED = True
        #Continue Game when no Popup
        elif event.type == pygame.MOUSEBUTTONDOWN and SHOW_POPUP:
            if button_rect.collidepoint(event.pos):
                SHOW_POPUP = False
                GAME_PAUSED = False
        #Continue Game when no Welcome Page
        elif event.type == pygame.MOUSEBUTTONDOWN and show_welcome:
            show_welcome = False
            game_paused = False

    #Draw Background
    screen.fill(BACKGROUND_COLOR)

    #Draw Sections
    draw_current_word()
    draw_player_table()
    draw_timer()

    if show_welcome:
        screen.blit(welcome_image, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                show_welcome = False
        pygame.display.flip()
        continue

    if not GAME_PAUSED:
        draw_current_word()
        draw_PLAYER_CARDS()
        draw_player_table()
        draw_timer()

    if SHOW_POPUP:
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))
        screen.blit(s, (0, 0))
        pygame.draw.rect(screen, POPUP_BACKGROUND_COLOR, popup_rect)
        pygame.draw.rect(screen, POPUP_BORDER_COLOR, popup_rect, 2)
        popup_text_render = font.render(POPUP_TEXT, True, TEXT_COLOR)
        screen.blit(popup_text_render, (popup_rect.centerx - popup_text_render.get_width() // 2, popup_rect.centery - 40))
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
        pygame.draw.rect(screen, BUTTON_BORDER_COLOR, button_rect, 2)
        button_text_render = font.render(BUTTON_TEXT, True, TEXT_COLOR)
        screen.blit(button_text_render, (button_rect.centerx - button_text_render.get_width() // 2, button_rect.centery - button_text_render.get_height() // 2))

    #Refresh Screen
    pygame.display.flip()

#Quit Pygame
pygame.quit()
sys.exit()
