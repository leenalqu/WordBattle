# Coded by Jiaxi Huang (5670238)
# Libraries Used: pygame, sys, math, random, GameFunctions
# Data Structures: Lists, Tuples, Rectangles, Classes
# Programming Techniques: Object-Oriented Programming(OOP), Event-Driven Programming, State Management(boolean flags), Resource Management
# Others: UI Component Design, Theme System, Audio Management, Rendering Techniques

# The subsequent updates of this file are in main.py. 
# This file is only used as a record of my UI creation process. 
# Due to a change in the image names, it cannot be run temporarily. 
# Please go to main.py to check the effect


# Import libraries
import pygame
import sys
import math
import random
from GameFunctions import Game


class CardGameUI:
    """
    A comprehensive UI manager for a card-based word game using Pygame.
    
    This class handles all aspects of the game's user interface including:
    - Game initialization and resource loading
    - Screen rendering and display management
    - User input processing and event handling
    - Game state management and transitions
    - Card and letter manipulation
    - Timer and round management
    - Theme customization and visual styling
    - Sound effects and background music
    - Multiple game pages (welcome, rules, options, credits)
    - Popup dialogs and notifications
    
    The game allows players to swap letters between cards and a word,
    with turn-based gameplay alternating between the player and computer.
    It features a customizable theme system, sound controls, and a complete
    set of UI elements for game navigation and interaction.
    
    Attributes:
        screen: The main Pygame display surface
        timer_seconds: Current countdown timer value
        side_status: Indicates current turn (0=player, 1=computer)
        current_word_letters: Letters in the current word
        card_letters: Letters available on the playable cards
        selected_letters: Currently selected letters for play
        theme_setting: Current visual theme (0=dark, 1=light)
    """
    def __init__(self):
        """
        Initializes the CardGameUI class.
        
        Sets up the game environment including:
        - Pygame initialization
        - Screen configuration
        - UI elements and colors
        - Game state variables
        - Resource loading (images, fonts, sounds)
        - Card layout and positioning
        - Timer and round management
        - Theme settings
        - Button click areas
        """
        # Initialize Pygame
        pygame.init()
        pygame.mixer.init()
        self.timer_count = 2

        self.points = 2
        self.answer_status = 1
        self.theme_setting = 0

        # Configure Settings (use boolean flags to trace the game status)
        self.show_popup = False
        self.show_popup_remove = False
        self.game_paused = False
        self.show_welcome_page = True
        self.show_game_paused_page = False
        self.show_rules_page = False
        self.show_remove_page = False
        self.show_remove_page_1 = False
        self.show_first_role = False
        self.show_rules_page = False
        self.show_options_page = False
        self.show_credits_page = False

        # Configure Color
        # Color of Coordinate_Box
        self.text_color_coordinate = (33, 33, 33)
        # Color of Timer
        self.text_color_timer = (33, 33, 33)
        # Color of Popup
        self.popup_side_changer_color_background = self.popup_remove_color_background = (188, 173, 119)
        self.popup_side_changer_color_border = self.popup_remove_color_border = (33, 33, 33)
        self.popup_side_changer_color_button = self.popup_remove_color_button = (33, 33, 33)
        self.popup_side_changer_color_button_border = self.popup_remove_color_button_border = (33, 33, 33)
        self.popup_side_changer_color_text = self.popup_remove_color_text = (188, 173, 119)
        self.popup_side_changer_color_text_button = self.popup_remove_color_text_button = (33, 33, 33)
        # Color of ide_Status
        self.side_text_box_color = (33, 33, 33)
        # Color of Current_Word
        self.current_word_text_color = (33, 33, 33)
        # Color of Card_Letters
        self.card_text_color = (33, 33, 33)
        self.selected_letter_color = (240, 153, 31)
        # Color of Round_Counter
        self.round_text_color = (33, 33, 33)
        self.card_overlay_color = (33, 33, 33)

        # Configure Screen
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Debug Mode")

        # Configure Background
        self.background_0 = pygame.image.load("data/image/background_0.png")
        self.background_mute_0 = pygame.image.load("data/image/background_mute_0.png")
        self.current_background = self.background_0

        # Configure First_Role_Page
        self.player_first_0 = pygame.image.load("data/image/player_first_0.png")
        self.computer_first_0 = pygame.image.load("data/image/computer_first_0.png")
        self.player_first = self.player_first_0
        self.computer_first = self.computer_first_0
        value = random.randint(0, 1)  # Randomly generate 0 or 1 (replaced by the function in GameFunctions.py in the main.py)
        if value == 0:
            self.first_role = self.player_first
        else:
            self.first_role = self.computer_first

        # Load images
        self.image_welcome_page_0 = pygame.image.load("data/image/welcome_page_0.png")
        self.image_welcome_page_1 = pygame.image.load("data/image/welcome_page_1.png")
        self.image_welcome_page = self.image_welcome_page_0
        self.image_remove_page = pygame.image.load("data/image/remove_page.png")
        self.image_remove_page_1 = pygame.image.load("data/image/remove_page_1.png")
        self.image_game_paused_page_0 = pygame.image.load("data/image/game_paused_page_0.png")
        self.image_game_paused_page = self.image_game_paused_page_0
        self.image_rules_page_0 = pygame.image.load("data/image/rules_page_0.png")
        self.image_rules_page_1 = pygame.image.load("data/image/rules_page_1.png")
        self.image_rules_page = self.image_rules_page_0
        self.image_options_page_0 = pygame.image.load("data/image/options_page_0.png")
        self.image_options_page_1 = pygame.image.load("data/image/options_page_1.png")
        self.image_options_page = self.image_options_page_0
        self.image_credits_page_0 = pygame.image.load("data/image/credits_page_0.png")
        self.image_credits_page_1 = pygame.image.load("data/image/credits_page_1.png")
        self.image_credits_page = self.image_credits_page_0

        # Configure Font
        self.font_size_default = 24
        self.font_size_timer = 88
        self.font_size_round = 34
        self.font_default = pygame.font.Font("data/font/AaHuanMengKongJianXiangSuTi-2.ttf", self.font_size_default)
        self.font_timer = pygame.font.Font("data/font/AaHuanMengKongJianXiangSuTi-2.ttf", self.font_size_timer)
        self.font_round = pygame.font.Font("data/font/AaHuanMengKongJianXiangSuTi-2.ttf", self.font_size_round)

        # Configure Timer
        self.timer_event = pygame.USEREVENT + 1  # Custom event for timer
        self.timer_duration = 3
        self.timer_seconds = self.timer_duration
        self.timer_x = 301
        self.timer_y = 248
        pygame.time.set_timer(self.timer_event, 1000)
        self.popup_rect = pygame.Rect(self.screen_width // 2 - 150, self.screen_height // 2 - 75, 300, 150)
        self.popup_remove_rect = pygame.Rect(self.screen_width // 2 - 150, self.screen_height // 2 - 75, 300, 150)
        self.button_rect = pygame.Rect(self.screen_width // 2 - 50, self.screen_height // 2 + 25, 100, 30)

        # Configure Popup
        self.popup_side_changer_width = 350
        self.popup_side_changer_height = 150
        self.popup_side_changer_width_button = 100
        self.popup_side_changer_height_button = 30
        self.popup_side_changer_pos_x = self.screen_width // 2 - self.popup_side_changer_width // 2
        self.popup_side_changer_pos_y = self.screen_width // 2 - self.popup_side_changer_height // 2
        self.popup_side_changer_pos_x_button = self.screen_width // 2 - self.popup_side_changer_width_button // 2
        self.popup_side_changer_pos_y_button = self.screen_width // 2 + 25
        self.popup_side_changer_text = "Side has changed"
        self.popup_side_changer_text_button = "OK"

        # Configure Popup_Remove
        self.popup_remove_width = 350
        self.popup_remove_height = 150
        self.popup_remove_width_button = 100
        self.popup_remove_height_button = 30
        self.popup_remove_pos_x = self.screen_width // 2 - self.popup_side_changer_width // 2
        self.popup_remove_pos_y = self.screen_width // 2 - self.popup_side_changer_height // 2
        self.popup_remove_pos_x_button = self.screen_width // 2 - self.popup_side_changer_width_button // 2
        self.popup_remove_pos_y_button = self.screen_width // 2 + 25
        self.popup_remove_text = "Move this Card?"
        self.popup_remove_text_yes = "Yes"
        self.popup_remove_text_no = "No"

        self.remove_yes_button_rect = pygame.Rect(self.screen_width // 2 - 120, self.screen_height // 2 + 25, 100, 30)
        self.remove_no_button_rect = pygame.Rect(self.screen_width // 2 + 20, self.screen_height // 2 + 25, 100, 30)
        self.popup_remove_text_button = "OK"

        # Configure Side Status
        if self.first_role == self.player_first:
            self.side_status = 0
        else:
            self.side_status = 1
        self.update_side_text()
        self.side_text_box_pos = (self.screen_width // 2, 0)

        # Configure Current Word
        self.current_word_font_size = 88
        self.current_word_font = pygame.font.Font("data/font/AaHuanMengKongJianXiangSuTi-2.ttf",self.current_word_font_size)
        self.current_word_letter_1 = 'C'
        self.current_word_letter_2 = 'A'
        self.current_word_letter_3 = 'T'
        self.current_word_letters = [self.current_word_letter_1, self.current_word_letter_2, self.current_word_letter_3]
        self.current_word_positions = [] # List for storing the positions of each letter
        current_word_start_x = 256
        current_word_width = 95
        current_word_spacing = 5
        current_word_y = 110
        for i in range(3):
            self.current_word_positions.append(
                (current_word_start_x + i * (current_word_width + current_word_spacing), current_word_y))

            self.current_word_click_areas = [] # List for storing the click areas of each letter
            for i in range(3):
                x = current_word_start_x + i * (current_word_width + current_word_spacing)
                y = current_word_y
                self.current_word_click_areas.append((x, y, current_word_width, current_word_width))
                self.selected_current_word_letters = [] # List for storing the selected letters

        # Configure Card Letters (default letters for testing)
        self.card_font_size = 52
        self.card_font = pygame.font.Font("data/font/AaHuanMengKongJianXiangSuTi-2.ttf", self.card_font_size)
        self.visible_card_count = 15
        self.card_letter_1 = 'C'
        self.card_letter_2 = 'O'
        self.card_letter_3 = 'M'
        self.card_letter_4 = 'P'
        self.card_letter_5 = 'U'
        self.card_letter_6 = 'T'
        self.card_letter_7 = 'E'
        self.card_letter_8 = 'R'
        self.card_letter_9 = 'S'
        self.card_letter_10 = 'C'
        self.card_letter_11 = 'I'
        self.card_letter_12 = 'E'
        self.card_letter_13 = 'N'
        self.card_letter_14 = 'C'
        self.card_letter_15 = 'E'
        self.card_letters = [
            self.card_letter_1, self.card_letter_2, self.card_letter_3,
            self.card_letter_4, self.card_letter_5, self.card_letter_6,
            self.card_letter_7, self.card_letter_8, self.card_letter_9,
            self.card_letter_10, self.card_letter_11, self.card_letter_12,
            self.card_letter_13, self.card_letter_14, self.card_letter_15
        ]
        self.card_positions = [] # List for storing the positions of each card
        card_start_x = 28
        card_width = 49
        card_spacing = 1
        card_y = 449
        for i in range(15):
            self.card_positions.append((card_start_x + i * (card_width + card_spacing), card_y))

        # Configure Card Clickers
        self.card_click_areas = [] # List for storing the click areas of each card
        for i in range(15):
            x = card_start_x + i * (card_width + card_spacing)
            y = card_y
            self.card_click_areas.append((x, y, card_width, card_width))

        # Configure Selected Letters
        self.selected_letters = [] # List for storing the selected letters
        self.last_swapped_position = None
        self.original_letters = [] # List for storing the original order of letters
        self.used_card_positions = list(range(7, 15))

        # Configure Sound settings
        pygame.mixer.music.load("data/sound/background_music.wav")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        self.button_sound = pygame.mixer.Sound("data/sound/button_sound.wav")
        self.sound_enabled = True

        # Configure Click area
        # Config_Round_Counter
        self.popup_ok_clicks = 2
        self.current_round = 1
        self.round_text_pos = (119, 559)
        # Game_Paused_Button
        self.x_min_game_paused_page, self.y_min_game_paused_page = 472, 563
        self.x_max_game_paused_page, self.y_max_game_paused_page = 502, 593
        # Quit_Button
        self.x_min_quit, self.y_min_quit = 508, 563
        self.x_max_quit, self.y_max_quit = 538, 593
        # Sound_Button
        self.x_min_sound_button, self.y_min_sound_button = 436, 563
        self.x_max_sound_button, self.y_max_sound_button = 466, 593
        # Confirm_Button
        self.x_min_confirm_button, self.y_min_confirm_button = 666, 563
        self.x_max_confirm_button, self.y_max_confirm_button = 794, 593
        # Rules_Button
        self.x_min_rules_button, self.y_min_rules_button = 427, 525
        self.x_max_rules_button, self.y_max_rules_button = 527, 549
        # Back_Button
        self.x_min_back_button, self.y_min_back_button = 547, 563
        self.x_max_back_button, self.y_max_back_button = 660, 593
        # Theme
        self.x_min_theme_0_button, self.y_min_theme_0_button = 4, 4
        self.x_max_theme_0_button, self.y_max_theme_0_button = 22, 22
        self.x_min_theme_1_button, self.y_min_theme_1_button = 26, 4
        self.x_max_theme_1_button, self.y_max_theme_1_button = 44, 22
        # Play
        self.x_min_play_button, self.y_min_play_button = 56, 525
        self.x_max_play_button, self.y_max_play_button = 129, 549
        # Options
        self.x_min_options_button, self.y_min_options_button = 208, 525
        self.x_max_options_button, self.y_max_options_button = 341, 549
        # Credits
        self.x_min_credits_button, self.y_min_credits_button = 612, 525
        self.x_max_credits_button, self.y_max_credits_button = 744, 549

    def update_side_text(self):
        """
        Updates the side text box to display the current turn status.
        """
        if self.side_status == 0:
            self.side_text_box = "YOUR TURN"
        elif self.side_status == 1:
            self.side_text_box = "COMPUTER'S TURN"

    def update_theme(self):
        """
        Updates all visual elements according to the selected theme setting.
        """
        # The Color settings of Theme 0
        if self.theme_setting == 0:
            # Color_Coordinate_Box
            self.text_color_coordinate = (33, 33, 33)
            # Color_Timer
            self.text_color_timer = (33, 33, 33)
            # Color_Popup
            self.popup_side_changer_color_background = (188, 173, 119)
            self.popup_side_changer_color_border = (33, 33, 33)
            self.popup_side_changer_color_button = (33, 33, 33)
            self.popup_side_changer_color_button_border = (33, 33, 33)
            self.popup_side_changer_color_text = (188, 173, 119)
            self.popup_side_changer_color_text_button = (33, 33, 33)
            # Color_Side_Status
            self.side_text_box_color = (33, 33, 33)
            # Color_Current_Word
            self.current_word_text_color = (33, 33, 33)
            # Color_Card_Letters
            self.card_text_color = (33, 33, 33)
            self.selected_letter_color = (240, 153, 31)
            # Color_Round_Counter
            self.round_text_color = (33, 33, 33)
            # Overlay
            self.card_overlay_color = (33, 33, 33)
            # Pages
            self.image_welcome_page = self.image_welcome_page_0
            self.image_rules_page = self.image_rules_page_0
            self.image_options_page = self.image_options_page_0
            self.image_credits_page = self.image_credits_page_0
            self.current_background = self.background_0
            self.player_first = self.player_first_0
            self.computer_first = self.computer_first_0
            self.image_game_paused_page = self.image_game_paused_page_0

        # The Color settings of Theme 1
        elif self.theme_setting == 1:
            # Color_Coordinate_Box
            self.text_color_coordinate = (0, 49, 82)
            # Color_Timer
            self.text_color_timer = (228, 222, 215)
            # Color_Popup
            self.popup_side_changer_color_background = (228, 222, 215)
            self.popup_side_changer_color_border = (228, 222, 215)
            self.popup_side_changer_color_button = (0, 49, 82)
            self.popup_side_changer_color_button_border = (0, 49, 82)
            self.popup_side_changer_color_text = (228, 222, 215)
            self.popup_side_changer_color_text_button = (0, 49, 82)
            # Color_Side_Status
            self.side_text_box_color = (228, 222, 215)
            # Color_Current_Word
            self.current_word_text_color = (228, 222, 215)
            # Color_Card_Letters
            self.card_text_color = (228, 222, 215)
            self.selected_letter_color = (240, 153, 31)
            # Color_Round_Counter
            self.round_text_color = (228, 222, 215)
            # Overlay
            self.card_overlay_color = (33, 33, 33)
            # Pages
            self.image_welcome_page = self.image_welcome_page_1
            self.image_rules_page = self.image_rules_page_1
            self.image_options_page = self.image_options_page_1
            self.image_credits_page = self.image_credits_page_1
            self.current_background = self.background_0
            self.player_first = self.player_first_0
            self.computer_first = self.computer_first_0
            self.image_game_paused_page = self.image_game_paused_page_0

    def draw_timer(self):
        """
        Displays the remaining time in the format "00:XX" where XX is the seconds.
        """
        timer_text = self.font_timer.render(f"00:{self.timer_seconds:02d}", True, self.text_color_timer)  # Format the timer text
        self.screen.blit(timer_text, (self.timer_x, self.timer_y))

    def draw_side_text_box(self):
        """
        Displays either "YOUR TURN" or "COMPUTER'S TURN" at the top of the screen.
        """
        text = self.font_default.render(self.side_text_box, True, self.side_text_box_color)
        self.screen.blit(text, (self.side_text_box_pos[0] - text.get_width() // 2, self.side_text_box_pos[1]))

    def draw_current_word_letters(self):
        """
        Renders the letters of the current word on the screen.
        Displays each letter of the current word at its designated position.
        """
        for i, pos in enumerate(self.current_word_positions):  # Use enumerate to get both index and value
            letter_text = self.current_word_font.render(self.current_word_letters[i], True,self.current_word_text_color)
            text_x = pos[0] + 47 - letter_text.get_width() // 2
            text_y = pos[1] + 47 - letter_text.get_height() // 2
            self.screen.blit(letter_text, (text_x, text_y))

    def draw_card_letters(self):
        """
        Renders the letters on each visible card.
        Only draws letters for cards that haven't been used yet.
        """
        for i, pos in enumerate(self.card_positions[:self.visible_card_count]):  # Use enumerate to get both index and value
            # Only draw unused cards
            if i not in self.used_card_positions:
                letter_text = self.card_font.render(self.card_letters[i], True, self.card_text_color)
                text_x = pos[0] + 25 - letter_text.get_width() // 2
                text_y = pos[1] + 25 - letter_text.get_height() // 2
                self.screen.blit(letter_text, (text_x, text_y))

    def draw_selected_letters(self):
        """
        Renders the currently selected letters with highlighting.
        """
        font = self.card_font
        start_y = 443
        for i, letter in enumerate(self.selected_letters):  # Use enumerate to get both index and value
            if isinstance(letter, tuple):
                position, letter = letter
                text_x = self.card_positions[position][0] + 25 - font.size(letter)[0] // 2
            else:
                text_x = self.screen_width - 150 + i * 20
            letter_text = font.render(str(letter), True, self.selected_letter_color)  # Convert letter to string
            self.screen.blit(letter_text, (text_x, start_y))

    def draw_card_overlay(self):
        """
        Renders an overlay on cards that have been used.
        """
        for i, pos in enumerate(self.card_positions[:self.visible_card_count]):
            if i in self.used_card_positions:
                rect = pygame.Rect(pos[0], pos[1] - 10, 49, 70)
                pygame.draw.rect(self.screen, self.card_overlay_color, rect)

    def draw_coordinate_display(self):
        """
        Renders the current mouse coordinates on screen for debugging.
        """
        mouse_x, mouse_y = pygame.mouse.get_pos() # Get the current mouse position
        text = self.font_default.render(f"X: {mouse_x}, Y: {mouse_y}", True, self.text_color_coordinate)
        text_rect = text.get_rect()
        text_rect.topleft = (650, 0)
        self.screen.blit(text, text_rect)

    def draw_popup(self):
        """
        Renders the side-change notification popup.
        A triggle for next round.
        """
        s = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA) 
        s.fill((0, 0, 0, 128))  # Set the alpha value to 128
        self.screen.blit(s, (0, 0)) 
        pygame.draw.rect(self.screen, self.popup_side_changer_color_background, self.popup_rect)
        pygame.draw.rect(self.screen, self.popup_side_changer_color_border, self.popup_rect, 5)
        popup_text_render = self.font_default.render(self.popup_side_changer_text, True, self.popup_side_changer_color_text_button)
        self.screen.blit(popup_text_render, (self.popup_rect.centerx - popup_text_render.get_width() // 2, self.popup_rect.centery - 40))
        pygame.draw.rect(self.screen, self.popup_side_changer_color_button, self.button_rect)
        pygame.draw.rect(self.screen, self.popup_side_changer_color_button_border, self.button_rect, 2)
        button_text_render = self.font_default.render(self.popup_side_changer_text_button, True, self.popup_side_changer_color_text)
        self.screen.blit(button_text_render, (self.button_rect.centerx - button_text_render.get_width() // 2, self.button_rect.centery - button_text_render.get_height() // 2))

    def draw_popup_remove(self):
        """
        Renders the card removal confirmation popup.
        """
        s = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))
        self.screen.blit(s, (0, 0))
        pygame.draw.rect(self.screen, self.popup_remove_color_background, self.popup_rect)
        pygame.draw.rect(self.screen, self.popup_remove_color_border, self.popup_rect, 5)
        popup_text_render = self.font_default.render(self.popup_remove_text, True, self.popup_remove_color_text_button)
        self.screen.blit(popup_text_render, (self.popup_rect.centerx - popup_text_render.get_width() // 2, self.popup_rect.centery - 40))
        pygame.draw.rect(self.screen, self.popup_remove_color_button, self.remove_yes_button_rect)
        pygame.draw.rect(self.screen, self.popup_remove_color_button_border, self.remove_yes_button_rect, 2)
        yes_text_render = self.font_default.render(self.popup_remove_text_yes, True, self.popup_remove_color_text)
        self.screen.blit(yes_text_render, (self.remove_yes_button_rect.centerx - yes_text_render.get_width() // 2, self.remove_yes_button_rect.centery - yes_text_render.get_height() // 2))
        pygame.draw.rect(self.screen, self.popup_remove_color_button, self.remove_no_button_rect)
        pygame.draw.rect(self.screen, self.popup_remove_color_button_border, self.remove_no_button_rect, 2)
        no_text_render = self.font_default.render(self.popup_remove_text_no, True, self.popup_remove_color_text)
        self.screen.blit(no_text_render, (self.remove_no_button_rect.centerx - no_text_render.get_width() // 2, self.remove_no_button_rect.centery - no_text_render.get_height() // 2))

    def handle_button_click(self, mouse_x, mouse_y):
        """
        Handles button click events based on mouse coordinates.
        """
        # Theme_0_Button
        if self.x_min_theme_0_button <= mouse_x <= self.x_max_theme_0_button and self.y_min_theme_0_button <= mouse_y <= self.y_max_theme_0_button:
            if pygame.mouse.get_pressed()[0]: # Index [0] represents the left mouse button
                self.button_sound.play()
                self.theme_setting = 0
                if self.show_rules_page or self.show_options_page or self.show_credits_page:
                    self.show_welcome_page = True
                    self.show_rules_page = False
                    self.show_options_page = False
                    self.show_credits_page = False
                pygame.time.set_timer(self.timer_event, 0)
                self.update_theme()
        # Theme_1_Button
        if self.x_min_theme_1_button <= mouse_x <= self.x_max_theme_1_button and self.y_min_theme_1_button <= mouse_y <= self.y_max_theme_1_button:
            if pygame.mouse.get_pressed()[0]:
                self.button_sound.play()
                self.theme_setting = 1
                if self.show_rules_page or self.show_options_page or self.show_credits_page:
                    self.show_welcome_page = True
                    self.show_rules_page = False
                    self.show_options_page = False
                    self.show_credits_page = False
                pygame.time.set_timer(self.timer_event, 0)
                self.update_theme()
        # Quit_Button
        if self.x_min_quit <= mouse_x <= self.x_max_quit and self.y_min_quit <= mouse_y <= self.y_max_quit and not self.show_first_role:
            if pygame.mouse.get_pressed()[0]:
                self.button_sound.play()
                print("Quit")
                return False
        # Confirm_Button
        if self.x_min_confirm_button <= mouse_x <= self.x_max_confirm_button and self.y_min_confirm_button <= mouse_y <= self.y_max_confirm_button and not self.show_first_role:
            if pygame.mouse.get_pressed()[0] and self.side_status == 0:
                self.button_sound.play()
                self.timer_seconds = 0
        # Sound_Button
        if self.x_min_sound_button <= mouse_x <= self.x_max_sound_button and self.y_min_sound_button <= mouse_y <= self.y_max_sound_button and not self.show_first_role:
            if pygame.mouse.get_pressed()[0]:
                self.button_sound.play()
                if self.sound_enabled:
                    pygame.mixer.music.set_volume(0)
                    self.sound_enabled = False
                    if self.theme_setting == 0:
                        self.current_background = self.background_mute_0
                else:
                    pygame.mixer.music.set_volume(0.3)
                    self.sound_enabled = True
                    if self.theme_setting == 0:
                        self.current_background = self.background_0
                self.button_sound.play()
        return True

    def check_victory_condition(self):
        """
        Checks if the player has won the game.
        Remaining cards = 0
        """
        if self.visible_card_count == 0:
            print("Victory！")
            return True
        return False

    def check_failure_condition(self):
        """
        Checks if the player has lost the game.
        Remaining cards = 15
        """
        if self.visible_card_count == 15 and self.answer_status == 0:
            print("Defeat.")
            return True
        if self.answer_status == 0:
            print("Invalid Answer")
            return True
        return False

    def handle_card_click(self, mouse_x, mouse_y):
        """
        Handles clicks on card elements.
        """
        if self.show_remove_page:
            for i, (x, y, width, height) in enumerate(self.card_click_areas):
                if x <= mouse_x <= x + width and y <= mouse_y <= y + height:
                    if i not in self.used_card_positions:
                        self.selected_letters = [(i, self.card_letters[i])]
                        self.show_popup_remove = True
                        return True
            return False
        if self.side_status != 0 or self.game_paused:
            return
        for i, (x, y, width, height) in enumerate(self.card_click_areas):
            if x <= mouse_x <= x + width and y <= mouse_y <= y + height:
                if i not in self.used_card_positions:
                    selected_letter = self.card_letters[i]
                    self.selected_letters = [(i, selected_letter)]
                    print(f"Selected Letter: {selected_letter}")
                    return True
        return False

    def handle_current_word_click(self, mouse_x, mouse_y):
        """
        Handles clicks on the current word letters.
        """
        if self.side_status != 0 or self.game_paused:
            return
        for i, (x, y, width, height) in enumerate(self.current_word_click_areas):
            if x <= mouse_x <= x + width and y <= mouse_y <= y + height:
                if self.selected_letters:
                    card_position, card_letter = self.selected_letters[0]  # Unpack the tuple
                    current_letter = self.current_word_letters[i]  # Get the current letter
                    # Handle Previous Swap
                    if self.last_swapped_position is not None:
                        # Cannot swap same letter
                        if self.last_swapped_position == i:
                            if self.used_card_positions:
                                last_card_position = self.used_card_positions.pop()
                                print(f"Restored previous card at position {last_card_position}")
                        # Different Position Swap
                        else:
                            self.current_word_letters[self.last_swapped_position] = self.original_letters[
                                self.last_swapped_position]
                            if self.used_card_positions:
                                last_card_position = self.used_card_positions.pop()
                                print(f"Restored card at position {last_card_position}")
                            print(
                                f"Restored position {self.last_swapped_position} to {self.original_letters[self.last_swapped_position]}")

                    # Store Original Letters
                    if not self.original_letters:
                        self.original_letters = self.current_word_letters.copy()

                    # Update Current Word
                    self.current_word_letters[i] = card_letter  # Swap the letters
                    print(f"Swapped letters: {current_letter} -> {card_letter}")

                    # Update Swap Status
                    self.last_swapped_position = i  # Store the last swapped position
                    self.used_card_positions.append(card_position)
                    self.selected_letters = []  # Reset selected letters
                return True
        return False

    def handle_timer_event(self):
        """
        Handles timer tick events.
        Updates the timer countdown, changes sides when timer expires,
        updates points, and manages game state transitions between rounds.
        """
        if self.timer_seconds > 0 and not self.game_paused:
            self.timer_seconds -= 1
        else:
            self.side_status = 1 - self.side_status
            if self.answer_status == 1 and self.side_status == 1:
                self.points += 1
                print(f"Current Points: {self.points}")
            self.timer_seconds = self.timer_duration
            self.update_side_text()
            if self.points == 1 or self.points == 2:
                self.show_popup = True
                self.game_paused = True
                pygame.time.set_timer(self.timer_event, 0)
            elif self.points == 3:
                self.show_popup = True
                self.show_popup = False
                self.game_paused = True
                pygame.time.set_timer(self.timer_event, 0)
                self.show_remove_page = True
                self.game_paused = True
                print("Remove Mode")
                pygame.time.set_timer(self.timer_event, 0)
            elif self.points == 0 and self.side_status == 1:
                self.show_popup = False
            # Reset original letters and last swapped position at the end of each round
            self.original_letters = [] # Reset original letters
            self.last_swapped_position = None

    def handle_popup_click(self, pos):
        """
        Handles clicks on popup dialog buttons.
        """
        if self.show_popup:
            if self.button_rect.collidepoint(pos):
                self.button_sound.play()
                self.show_popup = False
                self.game_paused = False
                self.show_remove_page = False
                self.show_remove_page_1 = False
                self.popup_ok_clicks += 1
                self.current_round = math.floor(self.popup_ok_clicks / 2) 
                print(f"Current Round {self.popup_ok_clicks / 2}")
                pygame.time.set_timer(self.timer_event, 1000)

        if self.show_popup_remove:
            mouse_x, mouse_y = pos
            if self.remove_yes_button_rect.collidepoint(mouse_x, mouse_y):
                if pygame.mouse.get_pressed()[0]:
                    self.button_sound.play()
                    print("yes")
                    if self.selected_letters and isinstance(self.selected_letters[0], tuple):  # Check if the first element is a tuple
                        position, _ = self.selected_letters[0]
                        self.used_card_positions.append(position)
                    self.selected_letters = []  # Reset selected letters
                    self.show_popup_remove = False
                    self.show_remove_page = False
                    self.points = 0
                    self.side_status = 0
                    self.timer_seconds = self.timer_duration
                    self.show_remove_page_1 = True
                    pygame.time.set_timer(self.timer_event, 1000)
                    return True
            elif self.remove_no_button_rect.collidepoint(mouse_x, mouse_y):
                if pygame.mouse.get_pressed()[0]:
                    self.button_sound.play()
                    print("no")
                    self.show_popup_remove = False
                    pygame.time.set_timer(self.timer_event, 0)
                    return True
        return False

    def handle_events(self):
        """
        Processes all pygame events in the event queue.
        Handles quit events, mouse wheel events, mouse clicks on various
        game elements, and timer events. 
        Manages transitions between different game screens and states.
        """
        for event in pygame.event.get():
            # Quit_Event
            if event.type == pygame.QUIT:
                return False
            # Mouse_Wheel_Event
            elif event.type == pygame.MOUSEWHEEL:
                continue
            # Mouse_Click_Event
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if not self.handle_button_click(mouse_x, mouse_y):
                    return False
                # Interaction based on welcome page
                if self.show_welcome_page or self.show_rules_page or self.show_options_page or self.show_credits_page:
                    if event.type == pygame.MOUSEBUTTONDOWN and self.x_min_play_button <= mouse_x <= self.x_max_play_button and self.y_min_play_button <= mouse_y <= self.y_max_play_button:
                        self.button_sound.play()
                        self.show_welcome_page = False
                        self.show_rules_page = False
                        self.show_options_page = False
                        self.show_first_role = True
                        self.show_credits_page = False
                        pygame.time.set_timer(self.timer_event, 0)
                    elif event.type == pygame.MOUSEBUTTONDOWN and self.x_min_rules_button <= mouse_x <= self.x_max_rules_button and self.y_min_rules_button <= mouse_y <= self.y_max_rules_button:
                        self.button_sound.play()
                        self.show_welcome_page = False
                        self.show_rules_page = True
                        self.show_options_page = False
                        self.show_credits_page = False
                        pygame.time.set_timer(self.timer_event, 0)
                    elif event.type == pygame.MOUSEBUTTONDOWN and self.x_min_options_button <= mouse_x <= self.x_max_options_button and self.y_min_options_button <= mouse_y <= self.y_max_options_button:
                        self.button_sound.play()
                        self.show_welcome_page = False
                        self.show_rules_page = False
                        self.show_options_page = True
                        self.show_credits_page = False
                        pygame.time.set_timer(self.timer_event, 0)
                    elif event.type == pygame.MOUSEBUTTONDOWN and self.x_min_credits_button <= mouse_x <= self.x_max_credits_button and self.y_min_credits_button <= mouse_y <= self.y_max_credits_button:
                        self.button_sound.play()
                        self.show_welcome_page = False
                        self.show_rules_page = False
                        self.show_options_page = False
                        self.show_credits_page = True
                        pygame.time.set_timer(self.timer_event, 0)
                elif not (self.show_welcome_page or self.show_rules_page or self.show_options_page or self.show_credits_page) and self.x_min_game_paused_page <= mouse_x <= self.x_max_game_paused_page and self.y_min_game_paused_page <= mouse_y <= self.y_max_game_paused_page:
                    if event.type == pygame.MOUSEBUTTONDOWN and not self.show_game_paused_page:
                        self.button_sound.play()
                        self.game_paused = True
                        self.show_game_paused_page = True
                        print("Game Paused")
                        pygame.time.set_timer(self.timer_event, 0)
                    elif event.type == pygame.MOUSEBUTTONDOWN and self.show_game_paused_page:
                        self.button_sound.play()
                        self.game_paused = False
                        self.show_game_paused_page = False
                        print("Game Unpaused")
                        pygame.time.set_timer(self.timer_event, 1000)
                # Popup Click
                elif self.show_popup or self.show_popup_remove:
                    self.handle_popup_click(event.pos)
                # First Role Page Click
                elif self.show_first_role:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.button_sound.play()
                        self.show_first_role = False
                        pygame.time.set_timer(self.timer_event, 1000)
                # Popup Click
                elif self.show_popup:
                    self.handle_popup_click(event.pos)
                # Card Click
                else:
                    self.handle_card_click(mouse_x, mouse_y)
                    self.handle_current_word_click(mouse_x, mouse_y)
            # Timer Event
            elif event.type == self.timer_event:
                self.handle_timer_event()
        return True

    def draw_round_counter(self):
        """
        Renders the current round number on the screen.
        """
        round_text = self.font_round.render(str(self.current_round), True, self.round_text_color)
        self.screen.blit(round_text, self.round_text_pos)

    def draw(self):
        """
        Renders all game elements on the screen.
        """
        # Draw Background
        self.screen.blit(self.current_background, (0, 0))
        self.draw_timer()
        self.draw_side_text_box()
        self.draw_coordinate_display()
        self.draw_current_word_letters()
        self.draw_card_letters()
        self.draw_selected_letters()
        self.draw_round_counter()
        self.draw_card_overlay()
        # Draw Game_Status
        if not self.game_paused:
            self.draw_side_text_box()
            self.draw_timer()
        # Draw Welcome_Page
        if self.show_welcome_page:
            self.screen.blit(self.image_welcome_page, (0, 0))
            pygame.time.set_timer(self.timer_event, 0)
            pygame.display.flip()
            return
        if self.show_first_role:
            self.screen.blit(self.first_role, (0, 0))
        if self.show_options_page:
            self.screen.blit(self.image_options_page, (0, 0))
        if self.show_remove_page_1:
            self.screen.blit(self.image_remove_page_1, (0, 0))
        if self.show_remove_page:
            self.screen.blit(self.image_remove_page, (0, 0))
            self.draw_card_letters()
            self.draw_selected_letters()
            self.draw_card_overlay()
            if self.show_popup_remove:
                self.draw_popup_remove()
        if self.show_credits_page:
            self.screen.blit(self.image_credits_page, (0, 0))
        # Draw Game Pages
        if self.show_game_paused_page:
            self.screen.blit(self.image_game_paused_page, (0, 0))
            pygame.time.set_timer(self.timer_event, 0)
        if self.show_popup:
            self.draw_popup()
        if self.show_popup_remove:
            self.draw_popup_remove()
        if self.show_rules_page:
            self.screen.blit(self.image_rules_page, (0, 0))
        # Update Screen
        pygame.display.flip() 

    def run(self):
        """
        Main game loop that runs the entire game.
        """
        running = True
        while running:
            running = self.handle_events()
            self.draw()
        # Quit Pygame
        pygame.mixer.music.stop()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = CardGameUI()
    game.run()