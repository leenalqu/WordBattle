# CardGame: Word Battle
# Computer Science - Warwick International Foundation Programme 2024-2025
# Credits (listed in alphabetical order by last name):
# ALJUBRAN, RAGHAD - GameFunctions.py
# ALQURASHI, LEEN - GameSettings.py and Mainloop.py and combined_code_file.py
# ALWAZZAN, HASAN - BotFunctions.py
# HUANG, JIAXI - CardGameUI.py and combined_code_file.py

# In Developing...
# Automatic sorting of player cards (GameFunctions.py)
# Bot difficulty settings (BotFunctions.py)
# New card interaction method
# Used card returned to stack
# Bug fixes

# Import libraries
import os
import sys
import math
import pygame
import random
from BotFunctions import Bot
from GameFunctions import Game
from GameSettings import GameSettings


class GameProgress:
    """
    Card Game User Interface Class

    This class manages the game's graphical interface, event handling, and game states.
    Contains all visual elements, audio controls, and interaction logic.
    Implements single-player vs computer turn-based gameplay with multiple themes and difficulty settings.

    Main Attributes:
        screen_width (int): Game window width, default 800 pixels
        screen_height (int): Game window height, default 600 pixels
        show_popup (bool): Whether to display popup
        game_paused (bool): Whether game is paused
        current_round (int): Current round number
        side_status (int): Current active player (0 for player, 1 for computer)
        points (int): Current player score
        theme_setting (int): Theme setting (0 for default theme, 1 for dark theme)
        sound_enabled (bool): Whether sound is enabled

    Main Methods:
        draw(): Render all game elements to screen
            - Draw background, UI elements, cards
            - Display popups and special interfaces based on game state
            - Update display content

        draw_cards(): Draw player's hand cards
            - Center display remaining cards
            - Exclude used cards
            - Update click areas

        handle_card_click(mouse_x, mouse_y): Handle card selection events
            - Calculate valid click areas
            - Filter used cards
            - Update selection status

        organize_cards(): Rearrange card positions
            - Move cards to fill empty slots
            - Maintain relative order
            - Update usage status

        add_penalty_card(): Draw new card from deck
            - Randomly select unused letter
            - Place in player's hand empty slot
            - Update deck status

        run(): Launch and maintain main game loop
            - Continuously process events and update display
            - Control game flow
            - Handle game end
    """

    def __init__(self):

        # Initialize Pygame
        pygame.init()
        pygame.mixer.init()

        # Configure Screen Settings
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Word Battle")

        # Game logic setup
        self.logic = Game()
        self.game_settings = GameSettings()
        card_stack = self.logic.card_stack()
        self.deck = card_stack
        print("\n[__init__] --- Game Initialization In Progress ---")
        print("[__init__] Initial Deck Content:", card_stack)

        # Generate the starting word
        self.current_word = self.logic.word_generator().upper()
        self.word_letters = list(self.current_word)
        self.current_word = self.logic.word_generator().upper()
        self.word_letters = list(self.current_word)

        # Generate the players' cards
        player_cards = [card_stack.pop().upper() for _ in range(self.game_settings.START_CARDS_AMOUNT)]
        print(f"[__init__] Player's Cards: {player_cards}")
        computer_cards = [card_stack.pop().lower() for _ in range(self.game_settings.START_CARDS_AMOUNT)]
        print(f"[__init__] Computer's Cards: {computer_cards}")
        print("[__init__] --- Game Initialization Completed ---\n")

        # Initialize bot
        self.bot = Bot(Bot.Difficulty.EASY, computer_cards)

        # Configure settings
        self.points = 1
        self.side_status = 0
        self.computer_points = 0
        self.bot_correct_answers = 0
        self.player_answer_status = None
        self.computer_answer_status = None
        self.theme_setting = 0
        self.game_paused = False

        # Configure Pages
        self.show_popup = False
        self.show_popup_remove = False
        self.show_popup_bot_difficulty = False
        self.show_welcome_page = True
        self.show_options_page = False
        self.show_rules_page = False
        self.show_credits_page = False
        self.show_player_first = False
        self.show_computer_first = False
        self.show_game_paused_page = False
        self.show_remove_page = False
        self.show_remove_page_mode = False
        self.show_rules_main_page = False
        self.show_victory_page = False
        self.show_defeat_page = False

        self.value = self.logic.coin_flip()
        print(f"[__init__] {self.value}")

        # Configure Default Theme Settings
        # Color_Coordinate_Box
        self.text_color_coordinate = (33, 33, 33)

        # Color_Timer
        self.text_color_timer = (33, 33, 33)

        # Color_Popup
        self.popup_color_background = self.popup_color_background = (188, 173, 119)
        self.popup_color_border = self.popup_color_border = (33, 33, 33)
        self.popup_color_button = self.popup_color_button = (33, 33, 33)
        self.popup_color_button_border = self.popup_color_button_border = (33, 33, 33)
        self.popup_color_text = self.popup_color_text = (188, 173, 119)
        self.popup_color_text_button = self.popup_color_text_button = (33, 33, 33)

        # Color_Side_Status
        self.side_text_box_color = (33, 33, 33)

        # Color_Current_Word
        self.current_word_text_color = (33, 33, 33)

        # Color_Card_Letters
        self.card_text_color = (33, 33, 33)
        self.selected_card_color = (240, 153, 31)

        # Color_Round_Counter
        self.round_text_color = (33, 33, 33)
        self.card_overlay_color = (33, 33, 33)

        # Color_block
        self.point_block_color = (188, 173, 119)

        # Color sound
        self.test_color = (188, 173, 119)

        # Config_Background
        self.background_0 = pygame.image.load("data/image/background_0.png")
        self.background_mute_0 = pygame.image.load("data/image/background_mute_0.png")
        self.background_1 = pygame.image.load("data/image/background_1.png")
        self.background_mute_1 = pygame.image.load("data/image/background_mute_1.png")
        self.current_background = self.background_0
        self.current_background_mute = self.background_mute_0

        # Config_Welcome_Page
        self.image_welcome_page_0 = pygame.image.load("data/image/welcome_page_0.png")
        self.image_welcome_page_1 = pygame.image.load("data/image/welcome_page_1.png")
        self.image_welcome_page = self.image_welcome_page_0

        # Config_Rules_Page
        self.image_rules_page_0 = pygame.image.load("data/image/rules_page_0.png")
        self.image_rules_page_1 = pygame.image.load("data/image/rules_page_1.png")
        self.image_rules_page = self.image_rules_page_0

        # Config_Options_Page
        self.image_options_page_0 = pygame.image.load("data/image/options_page_0.png")
        self.image_options_page_1 = pygame.image.load("data/image/options_page_1.png")
        self.image_options_page = self.image_options_page_0

        # Options Page Boxes
        self.options_box1_rect = pygame.Rect(672, 178, 18, 18)
        self.options_box2_rect = pygame.Rect(709, 318, 18, 18)
        self.options_click_sound = 1
        self.options_background_music = 1

        # Config_Credits_Page
        self.image_credits_page_0 = pygame.image.load("data/image/credits_page_0.png")
        self.image_credits_page_1 = pygame.image.load("data/image/credits_page_1.png")
        self.image_credits_page = self.image_credits_page_0

        # Config_First_Role
        self.player_first_0 = pygame.image.load("data/image/player_first_0.png")
        self.player_first_1 = pygame.image.load("data/image/player_first_1.png")
        self.computer_first_0 = pygame.image.load("data/image/computer_first_0.png")
        self.computer_first_1 = pygame.image.load("data/image/computer_first_1.png")
        self.player_first = self.player_first_0
        self.computer_first = self.computer_first_0
        if self.value == "Head":
            self.side_status = 0
            self.player_first = self.player_first_0

            # Player goes first.
            print("[__init__] Player First")
        elif self.value == "Tail":
            self.side_status = 1
            self.computer_first = self.computer_first_0

            # Computer goes first.
            print("[__init__] Computer First")

        # Config_Remove_Page
        self.image_remove_page_0 = pygame.image.load("data/image/remove_page_0.png")
        self.image_remove_page_mode_0 = pygame.image.load("data/image/remove_page_mode_0.png")
        self.image_remove_page_1 = pygame.image.load("data/image/remove_page_1.png")
        self.image_remove_page_mode_1 = pygame.image.load("data/image/remove_page_mode_1.png")
        self.image_remove_page = self.image_remove_page_0
        self.image_remove_page_mode = self.image_remove_page_mode_0

        # Config_Pause_Page
        self.image_game_paused_page_0 = pygame.image.load("data/image/game_paused_page_0.png")
        self.image_game_paused_page_1 = pygame.image.load("data/image/game_paused_page_1.png")
        self.image_game_paused_page = self.image_game_paused_page_0
        self.paused_page_mark = 0

        # Config_Rules_Main_Page
        self.image_rules_main_page_0 = pygame.image.load("data/image/rules_main_page_0.png")
        self.image_rules_main_page_1 = pygame.image.load("data/image/rules_main_page_1.png")
        self.image_rules_main_page = self.image_rules_main_page_0

        # Config_Credits_Page
        self.image_victory_page_0 = pygame.image.load("data/image/victory_0.png")
        self.image_victory_page_1 = pygame.image.load("data/image/victory_1.png")
        self.image_defeat_page_0 = pygame.image.load("data/image/defeat_0.png")
        self.image_defeat_page_1 = pygame.image.load("data/image/defeat_1.png")
        self.image_victory_page = self.image_victory_page_0
        self.image_defeat_page = self.image_defeat_page_0

        # Config_Sound
        self.background_music_0 = "data/sound/background_music_0.wav"
        self.background_music_1 = "data/sound/background_music_1.wav"
        pygame.mixer.music.load(self.background_music_0)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        self.button_sound = pygame.mixer.Sound("data/sound/button_sound.wav")
        self.sound_enabled = True
        self.sound_mark_click_sound = 1
        self.sound_mark_background_music = 1

        # Config_Font
        self.font_size_default = 24
        self.font_size_timer = 88
        self.font_size_round = 34
        self.font_default = pygame.font.Font("data/font/AaHuanMengKongJianXiangSuTi-2.ttf", self.font_size_default)
        self.font_timer = pygame.font.Font("data/font/AaHuanMengKongJianXiangSuTi-2.ttf", self.font_size_timer)
        self.font_round = pygame.font.Font("data/font/AaHuanMengKongJianXiangSuTi-2.ttf", self.font_size_round)

        # Config_Timer
        self.timer_event = pygame.USEREVENT + 1
        self.timer_seconds = self.game_settings.TURN_TIME_LIMIT
        self.timer_x = 301
        self.timer_y = 248
        pygame.time.set_timer(self.timer_event, 1000)

        # Config_Popup
        self.popup_side_changer_width = 350
        self.popup_side_changer_height = 150
        self.popup_side_changer_width_button = 100
        self.popup_side_changer_height_button = 30
        self.popup_rect = pygame.Rect(self.screen_width // 2 - self.popup_side_changer_width // 2,
                                      self.screen_height // 2 - self.popup_side_changer_height // 2,
                                      self.popup_side_changer_width,
                                      self.popup_side_changer_height
                                      )
        self.popup_remove_rect = pygame.Rect(self.screen_width // 2 - 150, self.screen_height // 2 - 75, 300, 150)
        self.button_rect = pygame.Rect(self.screen_width // 2 - 50, self.screen_height // 2 + 25, 100, 30)
        self.popup_side_changer_pos_x = self.screen_width // 2 - self.popup_side_changer_width // 2
        self.popup_side_changer_pos_y = self.screen_width // 2 - self.popup_side_changer_height // 2
        self.popup_side_changer_pos_x_button = self.screen_width // 2 - self.popup_side_changer_width_button // 2
        self.popup_side_changer_pos_y_button = self.screen_width // 2 + 25
        self.popup_side_changer_text = ""
        self.popup_side_changer_text_button = ""
        self.popup_side_changer_text_player = "Player Invalid Answer"
        self.popup_side_changer_text_button_player = "OK"
        self.popup_side_changer_text_computer = "Computer Invalid Answer"
        self.popup_side_changer_text_button_computer = "OK"

        # Config_Popup_Remove
        self.popup_remove_width = 350
        self.popup_remove_height = 150
        self.popup_remove_width_button = 100
        self.popup_remove_height_button = 30
        self.popup_rect_remove = pygame.Rect(self.screen_width // 2 - 150, self.screen_height // 2 - 75, 300, 150)
        self.popup_remove_pos_x = self.screen_width // 2 - self.popup_side_changer_width // 2
        self.popup_remove_pos_y = self.screen_width // 2 - self.popup_side_changer_height // 2
        self.popup_remove_pos_x_button = self.screen_width // 2 - self.popup_side_changer_width_button // 2
        self.popup_remove_pos_y_button = self.screen_width // 2 + 25
        self.popup_remove_text = "Remove this Card?"
        self.popup_remove_text_yes = "Yes"
        self.popup_remove_text_no = "No"
        self.remove_yes_button_rect = pygame.Rect(self.screen_width // 2 - 120, self.screen_height // 2 + 25, 100, 30)
        self.remove_no_button_rect = pygame.Rect(self.screen_width // 2 + 20, self.screen_height // 2 + 25, 100, 30)
        self.popup_remove_text_button = "OK"
        self.update_side_text()
        print("[__init__] Side Text Updated")
        self.update_popup_text()
        print("[__init__] Popup Text Updated")
        self.side_text_box_pos = (self.screen_width // 2, 0)

        # Config_popup_bot_difficulty
        self.popup_bot_difficulty_width = 380
        self.popup_bot_difficulty_height = 150
        self.popup_rect_bot_difficulty = pygame.Rect(self.screen_width // 2 - self.popup_bot_difficulty_width // 2,
                                                     self.screen_height // 2 - self.popup_bot_difficulty_height // 2,
                                                     self.popup_bot_difficulty_width, self.popup_bot_difficulty_height
                                                     # height
                                                     )
        self.difficulty_button_width = 100
        self.difficulty_button_height = 30
        self.popup_bot_difficulty_pos_x = self.screen_width // 2 - self.popup_bot_difficulty_width // 2
        self.popup_bot_difficulty_pos_y = self.screen_width // 2 - self.popup_bot_difficulty_height // 2

        self.easy_button_rect = pygame.Rect(self.screen_width // 2 - 170, self.screen_height // 2 + 25, 100, 30)
        self.medium_button_rect = pygame.Rect(self.screen_width // 2 - 50, self.screen_height // 2 + 25, 100, 30)
        self.hard_button_rect = pygame.Rect(self.screen_width // 2 + 70, self.screen_height // 2 + 25, 100, 30)

        # config_word
        self.current_word_font_size = 88
        self.current_word_font = pygame.font.Font("data/font/AaHuanMengKongJianXiangSuTi-2.ttf",
                                                  self.current_word_font_size)
        self.current_word_letter_1 = self.word_letters[0]
        self.current_word_letter_2 = self.word_letters[1]
        self.current_word_letter_3 = self.word_letters[2]
        self.word_letters = [self.current_word_letter_1, self.current_word_letter_2, self.current_word_letter_3]
        self.word_positions = []
        current_word_start_x = 256
        current_word_width = 95
        current_word_spacing = 5
        current_word_y = 110
        for i in range(3):
            self.word_positions.append(
                (current_word_start_x + i * (current_word_width + current_word_spacing), current_word_y))
            self.word_click_areas = []
            for i in range(3):
                x = current_word_start_x + i * (current_word_width + current_word_spacing)
                y = current_word_y
                self.word_click_areas.append((x, y, current_word_width, current_word_width))
                self.selected_word_letters = []

        # Config_Card_Letters
        self.card_font_size = 52
        self.card_font = pygame.font.Font("data/font/AaHuanMengKongJianXiangSuTi-2.ttf", self.card_font_size)

        # Initialize card letters array with empty slots
        self.card_letters = [''] * 15

        # Fill initial player cards
        for i in range(len(player_cards)):
            self.card_letters[i] = player_cards[i]
        self.card_positions = []
        card_start_x = 28
        card_width = 49
        card_spacing = 1
        card_y = 449
        for i in range(15):
            self.card_positions.append((card_start_x + i * (card_width + card_spacing), card_y))

        # Config_Card_Clickers
        self.card_click_areas = []
        for i in range(15):
            x = card_start_x + i * (card_width + card_spacing)
            y = card_y
            self.card_click_areas.append((x, y, card_width, card_width))

        # Config_selected_card
        self.selected_card = []
        self.last_swapped_position = None
        self.original_cards = []
        self.used_card_positions = list(range(7, 15))
        self.previous_word_letters = self.word_letters.copy()
        self.previous_used_card_positions = self.used_card_positions.copy()
        self.replaced_positions = set()
        self.star_card_active = False

        # Config_Points
        self.max_points = 3
        self.point_block_length = 55
        self.point_block_height = 17
        self.point_block_spacing = 3
        self.point_block_y = 570
        self.point_block_start_x = 238

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
        self.x_min_rules_button, self.y_min_rules_button = 455, 525
        self.x_max_rules_button, self.y_max_rules_button = 555, 549

        # Rules_Button
        self.x_min_rules_main_button, self.y_min_rules_main_button = 547, 563
        self.x_max_rules_main_button, self.y_max_rules_main_button = 660, 593

        # Back_Button
        self.x_min_back_button, self.y_min_back_button = 547, 563
        self.x_max_back_button, self.y_max_back_button = 660, 593

        # Theme
        self.x_min_theme_0_button, self.y_min_theme_0_button = 95, 70
        self.x_max_theme_0_button, self.y_max_theme_0_button = 318, 240
        self.x_min_theme_1_button, self.y_min_theme_1_button = 95, 263
        self.x_max_theme_1_button, self.y_max_theme_1_button = 318, 433
        self.x_min_click_sound_button, self.y_min_click_sound_button = 672, 178
        self.x_max_click_sound_button, self.y_max_click_sound_button = 690, 196
        self.x_min_background_music_button, self.y_min_background_music_button = 709, 318
        self.x_max_background_music_button, self.y_max_background_music_button = 727, 336

        # Play
        self.x_min_play_button, self.y_min_play_button = 64, 525
        self.x_max_play_button, self.y_max_play_button = 137, 549

        # Options
        self.x_min_options_button, self.y_min_options_button = 237, 525
        self.x_max_options_button, self.y_max_options_button = 370, 549

        # Credits
        self.x_min_credits_button, self.y_min_credits_button = 638, 525
        self.x_max_credits_button, self.y_max_credits_button = 770, 549

    def update_side_text(self):
        """
        Update the display text for current active player

        Updates to show "YOUR TURN" or "COMPUTER'S TURN" based on side_status value
        """
        if self.side_status == 0:
            self.side_text_box = "YOUR TURN"

            # self.popup_side_changer_text = self.popup_side_changer_text_player
            self.popup_side_changer_text_button = self.popup_side_changer_text_button_player
        elif self.side_status == 1:
            self.side_text_box = "COMPUTER'S TURN"

            # self.popup_side_changer_text = self.popup_side_changer_text_computer
            self.popup_side_changer_text_button = self.popup_side_changer_text_button_computer

    def update_popup_text(self):
        if self.side_status == 0:
            if self.player_answer_status == 0:
                self.popup_side_changer_text_player = "Player Invalid Answer"
            elif self.player_answer_status == 1:
                self.popup_side_changer_text_player = "Player Valid Answer"
            self.popup_side_changer_text = self.popup_side_changer_text_player
            print("[update_popup_text] Player Popup Text Updated.")
        else:
            if self.computer_answer_status == 0:
                self.popup_side_changer_text_computer = "Computer Invalid Answer"
            elif self.computer_answer_status == 1:
                self.popup_side_changer_text_computer = "Computer Valid Answer"
            self.popup_side_changer_text = self.popup_side_changer_text_computer
            print("[update_popup_text] Computer Popup Text Updated.")

    def add_penalty_card(self):
        """
        Draw a random card from the deck and add it to player's hand.

        Selects a random letter from the remaining cards in the deck
        that aren't already in the player's hand. The card is then
        placed in the first available empty slot in the player's hand.

        Returns:
            str: The letter drawn from the deck, or None if no cards remain.
        """
        if self.player_answer_status == 0 or self.computer_answer_status == 0:
            penalty_card = self.deck.pop()
            print(f"[add_penalty_card] Penalty Card: {penalty_card}")

            if self.side_status == 0:
                for i in range(1, 15):
                    if self.card_letters[i] == '':
                        self.card_letters[i] = penalty_card.upper()
                        if i in self.used_card_positions:
                            self.used_card_positions.remove(i)
                        break
            elif self.side_status == 1:
                self.bot.cards.append(penalty_card)
            return penalty_card

        else:
            print("[add_penalty_card] No remaining card in deck.")
            return None

    def organize_cards(self):
        """
        Rearrange cards to fill empty spaces in the player's hand.

        Moves all non-empty cards forward to fill any gaps, maintaining
        their relative order. Updates the used card positions list and
        saves the previous state for potential rollback.
        """
        new_card_letters = [''] * len(self.card_letters)

        non_empty_cards = []
        for i in range(len(self.card_letters)):
            if self.card_letters[i] != '' and i not in self.used_card_positions:
                non_empty_cards.append(self.card_letters[i])

        for i, card in enumerate(non_empty_cards):
            if i < len(new_card_letters):
                new_card_letters[i] = card

        self.card_letters = new_card_letters

        self.used_card_positions = [i for i in range(len(self.card_letters)) if
                                    i >= len(non_empty_cards) or self.card_letters[i] == '']

        self.previous_word_letters = self.word_letters.copy()
        self.previous_used_card_positions = self.used_card_positions.copy()

        print("[organize_cards] Cards moved forward.")
        print("[organize_cards] Current Cards (Player):", self.card_letters)
        print("[organize_cards] Used Position (Player):", self.used_card_positions)
        # print("[organize_cards] Number of Remaining Positions (Player):", len(self.used_card_positions))

    def update_theme(self):
        """
        Update the game's visual theme based on current theme setting.

        Changes colors, backgrounds, and UI elements according to the
        selected theme (0 for default theme, other values for alternate theme).
        Affects text colors, popup styles, backgrounds, and page images.
        """
        # Config_Color
        if self.theme_setting == 0:

            # Color_Coordinate_Box
            self.text_color_coordinate = (33, 33, 33)

            # Color_Timer
            self.text_color_timer = (33, 33, 33)

            # Color_Popup
            self.popup_color_background = (188, 173, 119)
            self.popup_color_border = (33, 33, 33)
            self.popup_color_button = (33, 33, 33)
            self.popup_color_button_border = (33, 33, 33)
            self.popup_color_text = (188, 173, 119)
            self.popup_color_text_button = (33, 33, 33)

            # Color_Side_Status
            self.side_text_box_color = (33, 33, 33)

            # Color_Current_Word
            self.current_word_text_color = (33, 33, 33)

            # Color_Card_Letters
            self.card_text_color = (33, 33, 33)
            self.selected_card_color = (240, 153, 31)

            # Color_Round_Counter
            self.round_text_color = (33, 33, 33)

            # Overlay
            self.card_overlay_color = (33, 33, 33)
            self.point_block_color = (188, 173, 119)

            # Color sound
            self.test_color = (188, 173, 119)

            # Pages
            self.image_welcome_page = self.image_welcome_page_0
            self.image_rules_page = self.image_rules_page_0
            self.image_options_page = self.image_options_page_0
            self.image_credits_page = self.image_credits_page_0
            self.current_background = self.background_0
            self.current_background_mute = self.background_mute_0
            self.player_first = self.player_first_0
            self.computer_first = self.computer_first_0
            self.image_game_paused_page = self.image_game_paused_page_0
            self.image_rules_main_page = self.image_rules_main_page_0
            self.image_victory_page = self.image_victory_page_0
            self.image_defeat_page = self.image_defeat_page_0
            self.image_remove_page = self.image_remove_page_0
            self.image_remove_page_mode = self.image_remove_page_mode_0
            if self.sound_enabled:
                pygame.mixer.music.load(self.background_music_0)
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.3)

        elif self.theme_setting == 1:

            # Color_Coordinate_Box
            self.text_color_coordinate = (0, 49, 82)

            # Color_Timer
            self.text_color_timer = (228, 222, 215)

            # Color_Popup
            self.popup_color_background = (228, 222, 215)
            self.popup_color_border = (0, 49, 82)
            self.popup_color_button = (0, 49, 82)
            self.popup_color_button_border = (0, 49, 82)
            self.popup_color_text = (228, 222, 215)
            self.popup_color_text_button = (0, 49, 82)

            # Color_Side_Status
            self.side_text_box_color = (228, 222, 215)

            # Color_Current_Word
            self.current_word_text_color = (228, 222, 215)

            # Color_Card_Letters
            self.card_text_color = (0, 49, 82)
            self.selected_card_color = (240, 153, 31)

            # Color_Round_Counter
            self.round_text_color = (228, 222, 215)

            # Overlay
            self.card_overlay_color = (0, 49, 82)
            self.point_block_color = (0, 49, 82)

            # Color sound
            self.test_color = (0, 49, 82)

            # Pages
            self.image_welcome_page = self.image_welcome_page_1
            self.image_rules_page = self.image_rules_page_1
            self.image_options_page = self.image_options_page_1
            self.image_credits_page = self.image_credits_page_1
            self.current_background = self.background_1
            self.current_background_mute = self.background_mute_1
            self.player_first = self.player_first_1
            self.computer_first = self.computer_first_1
            self.image_game_paused_page = self.image_game_paused_page_1
            self.image_rules_main_page = self.image_rules_main_page_1
            self.image_victory_page = self.image_victory_page_1
            self.image_defeat_page = self.image_defeat_page_1
            self.image_remove_page = self.image_remove_page_1
            self.image_remove_page_mode = self.image_remove_page_mode_1
            if self.sound_enabled:
                pygame.mixer.music.load(self.background_music_1)
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.3)

    def draw_timer(self):
        """
        Draw game timer

        Displays remaining time on screen in "00:XX" format
        """
        timer_text = self.font_timer.render(f"00:{self.timer_seconds:02d}", True, self.text_color_timer)
        self.screen.blit(timer_text, (self.timer_x, self.timer_y))

    def draw_points(self):
        """
        Draw points blocks

        Display current points using blue blocks arranged horizontally, maximum 8 blocks
        Display from left to right, points reduction removes blocks from left to right
        """
        # Draw_Points_Blocks
        for i in range(self.max_points):

            # Calculate_Block_Position
            x = self.point_block_start_x + i * (self.point_block_length + self.point_block_spacing)
            rect = pygame.Rect(x, self.point_block_y, self.point_block_length, self.point_block_height)

            # Draw_Active_Blocks
            if i >= (self.max_points - (self.points - 1)):
                pygame.draw.rect(self.screen, self.point_block_color, rect)

    def draw_side_status(self):
        """
        Draw the current side status text box

        Renders and displays the current player's turn status at the top of the screen
        """
        # Draw Title
        text = self.font_default.render(self.side_text_box, True, self.side_text_box_color)
        self.screen.blit(text, (self.side_text_box_pos[0] - text.get_width() // 2, self.side_text_box_pos[1]))

    def draw_word(self):
        """
        Draw the current word letters in the game

        Renders each letter of the current word in the designated positions
        with proper centering and spacing
        """
        for i, pos in enumerate(self.word_positions):
            letter_text = self.current_word_font.render(self.word_letters[i], True,
                                                        self.current_word_text_color)
            text_x = pos[0] + 47 - letter_text.get_width() // 2
            text_y = pos[1] + 47 - letter_text.get_height() // 2
            self.screen.blit(letter_text, (text_x, text_y))

    def draw_cards(self):
        """
        Draw the card letters in a centered layout

        Dynamically positions and renders available card letters:
            - Centers remaining cards based on total available space
            - Excludes previously used cards from display
            - Updates click areas for each visible card
            - Maintains consistent spacing between cards

        Card positions are calculated using:
            - Total screen width
            - Number of unused cards
            - Card width and spacing
            - Historical card usage data
        """
        for i, pos in enumerate(self.card_positions[:self.game_settings.MAX_CARDS]):

            # Only draw unused cards
            if i not in self.used_card_positions:
                letter_text = self.card_font.render(self.card_letters[i], True, self.card_text_color)
                text_x = pos[0] + 25 - letter_text.get_width() // 2
                text_y = pos[1] + 25 - letter_text.get_height() // 2
                self.screen.blit(letter_text, (text_x, text_y))

    def draw_selected_card(self):
        font = self.card_font
        start_y = 443
        for i, letter in enumerate(self.selected_card):
            if isinstance(letter, tuple):
                position, letter = letter
                text_x = self.card_positions[position][0] + 25 - font.size(letter)[0] // 2
            else:
                text_x = self.screen_width - 150 + i * 20
            letter_text = font.render(str(letter), True, self.selected_card_color)
            self.screen.blit(letter_text, (text_x, start_y))

    def draw_card_overlay(self):
        for i, pos in enumerate(self.card_positions[:self.game_settings.MAX_CARDS]):
            if i in self.used_card_positions:
                rect = pygame.Rect(pos[0], pos[1] - 10, 49, 70)
                pygame.draw.rect(self.screen, self.card_overlay_color, rect)

    def draw_coordinate_display(self):
        """
        Draw mouse coordinate display

        Shows the current X and Y coordinates of the mouse cursor
        in the top-left corner of the screen
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        text = self.font_default.render(f"X: {mouse_x}, Y: {mouse_y}", True, self.text_color_coordinate)
        text_rect = text.get_rect()
        text_rect.topleft = (650, 0)
        self.screen.blit(text, text_rect)

    def draw_popup(self):
        """
        Draw the side change popup

        Creates a semi-transparent overlay and displays a popup message
        when the active player changes, with an OK button to dismiss
        """
        s = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))
        self.screen.blit(s, (0, 0))
        pygame.draw.rect(self.screen, self.popup_color_background, self.popup_rect)
        pygame.draw.rect(self.screen, self.popup_color_border, self.popup_rect, 5)
        popup_text_render = self.font_default.render(self.popup_side_changer_text, True,
                                                     self.popup_color_text_button)
        self.screen.blit(popup_text_render,
                         (self.popup_rect.centerx - popup_text_render.get_width() // 2, self.popup_rect.centery - 40))
        pygame.draw.rect(self.screen, self.popup_color_button, self.button_rect)
        pygame.draw.rect(self.screen, self.popup_color_button_border, self.button_rect, 2)
        button_text_render = self.font_default.render(self.popup_side_changer_text_button, True,
                                                      self.popup_color_text)
        self.screen.blit(button_text_render, (self.button_rect.centerx - button_text_render.get_width() // 2,
                                              self.button_rect.centery - button_text_render.get_height() // 2))

    def draw_popup_remove(self):
        """
        Draw the remove mode popup

        Same content as above
        """
        s = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))
        self.screen.blit(s, (0, 0))

        pygame.draw.rect(self.screen, self.popup_color_background, self.popup_rect_remove)
        pygame.draw.rect(self.screen, self.popup_color_border, self.popup_rect_remove, 5)

        popup_text_render = self.font_default.render(self.popup_remove_text, True, self.popup_color_text_button)
        self.screen.blit(popup_text_render,
                         (self.popup_rect_remove.centerx - popup_text_render.get_width() // 2,
                          self.popup_rect_remove.centery - 40))

        pygame.draw.rect(self.screen, self.popup_color_button, self.remove_yes_button_rect)
        pygame.draw.rect(self.screen, self.popup_color_button_border, self.remove_yes_button_rect, 2)
        yes_text_render = self.font_default.render(self.popup_remove_text_yes, True, self.popup_color_text)
        self.screen.blit(yes_text_render, (self.remove_yes_button_rect.centerx - yes_text_render.get_width() // 2,
                                           self.remove_yes_button_rect.centery - yes_text_render.get_height() // 2))

        pygame.draw.rect(self.screen, self.popup_color_button, self.remove_no_button_rect)
        pygame.draw.rect(self.screen, self.popup_color_button_border, self.remove_no_button_rect, 2)
        no_text_render = self.font_default.render(self.popup_remove_text_no, True, self.popup_color_text)
        self.screen.blit(no_text_render, (self.remove_no_button_rect.centerx - no_text_render.get_width() // 2,
                                          self.remove_no_button_rect.centery - no_text_render.get_height() // 2))

    def draw_popup_bot_difficulty(self):
        """
        Draw the bot difficulty selection popup

        Displays a popup with three difficulty options: EASY, MEDIUM, HARD
        """
        s = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))
        self.screen.blit(s, (0, 0))

        pygame.draw.rect(self.screen, self.popup_color_background, self.popup_rect_bot_difficulty)
        pygame.draw.rect(self.screen, self.popup_color_border, self.popup_rect_bot_difficulty, 5)

        popup_text_render = self.font_default.render("GAME DIFFICULTY SELECTION", True, self.popup_color_text_button)
        self.screen.blit(popup_text_render,
                         (self.popup_rect_bot_difficulty.centerx - popup_text_render.get_width() // 2,
                          self.popup_rect_bot_difficulty.centery - 40))

        for button, text in [(self.easy_button_rect, "EASY"),
                             (self.medium_button_rect, "MEDIUM"),
                             (self.hard_button_rect, "HARD")]:
            pygame.draw.rect(self.screen, self.popup_color_button, button)
            pygame.draw.rect(self.screen, self.popup_color_button_border, button, 2)
            button_text = self.font_default.render(text, True, self.popup_color_text)
            text_rect = button_text.get_rect(center=button.center)
            self.screen.blit(button_text, text_rect)

    def handle_bot_turn(self):
        if self.side_status == 1 and not self.game_paused:
            current_word = "".join(self.word_letters).lower()
            print(f"[handle_bot_turn] Current Word: {str(current_word).upper()}")
            bot_output = self.bot.play_turn(current_word, self.timer_seconds)
            match bot_output:
                case self.bot.Output.THINKING:
                    print(f"[handle_bot_turn] Bot Output: {bot_output}")
                    print(f"[handle_bot_turn] Computer Cards: {self.bot.cards}")
                    print(f"[handle_bot_turn] Will Computer answer: {self.bot.current_turn_will_answer_or_not}")
                    print(f"[handle_bot_turn] Next Word: {self.bot.current_turn_answer}")
                    print(f"[handle_bot_turn] Answer Time: {self.bot.current_turn_answer_time}")
                    print(f"[handle_bot_turn] Ran Initial Code: {self.bot.ran_current_turn_code}")
                    print()
                    return
                case _:
                    computer_answer, computer_used_letter = bot_output
                    if not computer_answer:
                        print("[handle_bot_turn] Computer failed to make a word.")
                        self.add_penalty_card()
                    else:
                        self.word_letters = list(computer_answer.upper())
                        print(f"[handle_bot_turn] {bot_output} answered")
                        print(f"[handle_bot_turn] Computer Used Card:", computer_used_letter)

                        if computer_answer and computer_used_letter:
                            if computer_used_letter in self.bot.cards:
                                self.bot.cards.remove(computer_used_letter)
                                print(f"[handle_bot_turn] Card {computer_used_letter} removed from computer's hand")
                                print(f"[handle_bot_turn] Computer Cards(after removed used card): {self.bot.cards}")
                            self.deck.append(computer_used_letter)
                            print(f"[handle_bot_turn] Card {computer_used_letter} returned to deck")
                    self.timer_seconds = 0
                    if self.computer_points == 3:
                        self.bot.discard_card()
                        print("[handle_bot_turn] Computer discarded a card")
                    return

    def handle_button_click(self, mouse_x, mouse_y):
        """
        Handle all button click events

        Parameters:
            mouse_x (int): X coordinate of mouse click
            mouse_y (int): Y coordinate of mouse click

        Returns:
            bool: False if quit button is clicked, True otherwise

        Processes clicks on:
            - Welcome page and story pages
            - Back button
            - Rules button
            - Quit button
            - Game_Paused button
            - Confirm button
            - Sound toggle button
            - Remove button (Developing)
        """

        # Theme_0_Button
        if self.x_min_theme_0_button <= mouse_x <= self.x_max_theme_0_button and self.y_min_theme_0_button <= mouse_y <= self.y_max_theme_0_button:
            if pygame.mouse.get_pressed()[0] and self.show_options_page and self.theme_setting == 1:
                self.button_sound.play()
                print("[handle_button_click] Theme_0_Button Clicked")
                self.theme_setting = 0
                # if self.show_rules_page or self.show_options_page or self.show_credits_page:
                # self.show_welcome_page = True
                # self.show_rules_page = False
                # self.show_options_page = False
                # self.show_credits_page = False
                # pygame.time.set_timer(self.timer_event, 0)
                self.update_theme()
            elif pygame.mouse.get_pressed()[0] and self.show_options_page and self.theme_setting == 0:
                self.button_sound.play()
                pass

        # Theme_1_Button
        if self.x_min_theme_1_button <= mouse_x <= self.x_max_theme_1_button and self.y_min_theme_1_button <= mouse_y <= self.y_max_theme_1_button:
            if pygame.mouse.get_pressed()[0] and self.show_options_page and self.theme_setting == 0:
                self.button_sound.play()
                print("[handle_button_click] Theme_1_Button Clicked")
                self.theme_setting = 1
                # if self.show_rules_page or self.show_options_page or self.show_credits_page:
                # self.show_welcome_page = True
                # self.show_rules_page = False
                # self.show_options_page = False
                # self.show_credits_page = False
                # pygame.time.set_timer(self.timer_event, 0)
                self.update_theme()
            elif pygame.mouse.get_pressed()[0] and self.show_options_page and self.theme_setting == 1:
                self.button_sound.play()
                pass
        if self.x_min_click_sound_button <= mouse_x <= self.x_max_click_sound_button and self.y_min_click_sound_button <= mouse_y <= self.y_max_click_sound_button:
            if pygame.mouse.get_pressed()[0] and self.show_options_page:
                self.button_sound.play()
                self.options_click_sound = 1 - self.options_click_sound
                if self.options_click_sound == 1:
                    self.button_sound.set_volume(1.0)
                elif self.options_click_sound == 0:
                    self.button_sound.set_volume(0.0)
                print("[handle_button_click] Click Sound Button Clicked")

        if self.x_min_background_music_button <= mouse_x <= self.x_max_background_music_button and self.y_min_background_music_button <= mouse_y <= self.y_max_background_music_button:
            if pygame.mouse.get_pressed()[0] and self.show_options_page:
                self.button_sound.play()
                self.options_background_music = 1 - self.options_background_music
                if self.options_background_music == 1:
                    self.sound_enabled = True
                    pygame.mixer.music.set_volume(0.3)
                elif self.options_background_music == 0:
                    self.sound_enabled = False
                    pygame.mixer.music.set_volume(0)
                print("[handle_button_click] Background Music Button Clicked")

        # Quit_Button
        if self.x_min_quit <= mouse_x <= self.x_max_quit and self.y_min_quit <= mouse_y <= self.y_max_quit and not (
                self.show_welcome_page or self.show_rules_page or self.show_options_page or self.show_credits_page or self.show_computer_first or self.show_player_first or self.show_remove_page or self.show_remove_page_mode or self.show_victory_page or self.show_defeat_page or self.show_rules_main_page):
            if pygame.mouse.get_pressed()[0]:
                self.button_sound.play()
                print("[handle_button_click] Quit")
                return False

        # Confirm_Button
        if self.x_min_confirm_button <= mouse_x <= self.x_max_confirm_button and self.y_min_confirm_button <= mouse_y <= self.y_max_confirm_button and not (
                self.show_welcome_page or self.show_rules_page or self.show_options_page or self.show_credits_page or self.show_computer_first or self.show_player_first):
            if pygame.mouse.get_pressed()[0] and self.side_status == 0:
                self.button_sound.play()
                self.timer_seconds = 0
            elif pygame.mouse.get_pressed()[0] and self.show_game_paused_page:
                print("[handle_button_click] Restart Game.")
                python = sys.executable
                script = os.path.abspath(__file__)
                pygame.quit()
                os.execv(python, [python, script])

        # Sound_Button
        if self.x_min_sound_button <= mouse_x <= self.x_max_sound_button and self.y_min_sound_button <= mouse_y <= self.y_max_sound_button and not (
                self.show_welcome_page or self.show_rules_page or self.show_options_page or self.show_credits_page or self.show_computer_first or self.show_player_first or self.show_rules_main_page):
            if pygame.mouse.get_pressed()[0]:
                self.button_sound.play()
                if self.sound_enabled:
                    if self.sound_mark_click_sound == 1:
                        self.button_sound.set_volume(0.0)
                    if self.sound_mark_background_music == 1:
                        pygame.mixer.music.set_volume(0.0)
                    self.sound_enabled = False
                    if self.theme_setting == 0:
                        self.current_background = self.background_mute_0
                    if self.theme_setting == 1:
                        self.current_background = self.background_mute_1
                else:
                    if self.sound_mark_click_sound == 1:
                        self.button_sound.set_volume(1.0)
                    if self.sound_mark_background_music == 1:
                        pygame.mixer.music.set_volume(0.3)
                    self.sound_enabled = True
                    if self.theme_setting == 0:
                        self.current_background = self.background_0
                    if self.theme_setting == 1:
                        self.current_background = self.background_1
                self.button_sound.play()
        return True

    def check_victory_condition(self):
        """
        Check if the player has won the game.

        Victory occurs when all card positions are used (no cards left).
        When victory is achieved, displays the victory page and stops the timer.

        Returns:
            bool: True if victory condition is met, False otherwise.
        """
        if len(self.used_card_positions) == 15 or len(self.bot.cards) == 15:
            self.show_victory_page = True
            pygame.time.set_timer(self.timer_event, 0)
            self.game_paused = True
            self.show_victory_page = True
            pygame.time.set_timer(self.timer_event, 0)
            self.game_paused = True
            print("[check_victory_condition] Victory")
            return True
        # else:
        # print("No Victory")
        return False

    def check_failure_condition(self):
        """
        Check if the player has lost the game.

        Defeat occurs when there are no used card positions (all positions filled).
        When defeat is detected, displays the defeat page and stops the timer.

        Returns:
            bool: True if failure condition is met, False otherwise.
        """
        if len(self.used_card_positions) == 0 or len(self.bot.cards) == 0:
            self.show_defeat_page = True
            pygame.time.set_timer(self.timer_event, 0)
            self.game_paused = True
            print("[check_failure_condition] Defeat")
            return True

        # else:
        # print("No Defeat")
        return False

    def handle_card_click(self, mouse_x, mouse_y):
        """
        Handle card selection events

        Processes mouse clicks on card positions with dynamic centering:
            - Calculates valid click areas based on centered layout
            - Filters out previously used cards
            - Updates selection state for valid clicks

        Parameters:
            mouse_x (int): X coordinate of mouse click
            mouse_y (int): Y coordinate of mouse click

        Returns:
            bool: True if a card was selected, False otherwise

        Side effects:
            - Updates self.selected_card when a valid card is clicked
        """
        if self.show_remove_page:
            for i, (x, y, width, height) in enumerate(self.card_click_areas):
                if x <= mouse_x <= x + width and y <= mouse_y <= y + height:
                    if i not in self.used_card_positions:
                        self.selected_card = [(i, self.card_letters[i])]
                        self.show_popup_remove = True
                        return True
            return False

        if self.side_status != 0 or self.game_paused:
            return
        for i, (x, y, width, height) in enumerate(self.card_click_areas):
            if x <= mouse_x <= x + width and y <= mouse_y <= y + height:
                if i not in self.used_card_positions:
                    selected_card = self.card_letters[i]
                    self.selected_card = [(i, selected_card)]
                    print(f"[handle_card_click] Selected Letter: {selected_card}")
                    return True
        return False

    def handle_word_click(self, mouse_x, mouse_y):
        """
        Handle letter swapping in the current word

        Parameters:
            mouse_x (int): X coordinate of mouse click
            mouse_y (int): Y coordinate of mouse click

        Returns:
            bool: True if a swap was performed, False otherwise

        Manages the swapping of letters between selected card and current word,
        including handling of previous swaps and position restoration
        """
        if self.game_paused or self.side_status == 1:
            return

        elif self.side_status == 0:
            for i, (x, y, width, height) in enumerate(self.word_click_areas):
                if x <= mouse_x <= x + width and y <= mouse_y <= y + height:
                    if self.selected_card:
                        card_position, card_letter = self.selected_card[0]
                        current_letter = self.word_letters[i]

                        if i in self.replaced_positions:
                            print(
                                f"[handle_word_click] Position {i} has already been replaced and cannot be replaced again")
                            return False

                        # Check if the letters are the same as those in the original word
                        if card_letter.lower() == self.previous_word_letters[i].lower():
                            print(f"[handle_word_click] Cannot use same card：{card_letter}")
                            return False
                        if current_letter == card_letter:
                            print(f"[handle_word_click] Cannot use same card {card_letter} ")
                            self.selected_card = []
                            return True

                        # Handle_Previous_Swap
                        elif self.last_swapped_position is not None:

                            # Same_Position_Swap
                            if self.last_swapped_position == i:
                                if self.used_card_positions:
                                    last_card_position = self.used_card_positions.pop()
                                    print(
                                        f"[handle_word_click] Restored previous card at position {last_card_position}")

                            # Different_Position_Swap
                            else:
                                self.word_letters[self.last_swapped_position] = self.original_cards[
                                    self.last_swapped_position]
                                if self.used_card_positions:
                                    last_card_position = self.used_card_positions.pop()
                                    print(f"[handle_word_click] Restored card at position {last_card_position}")
                                print(
                                    f"[handle_word_click] Restored position {self.last_swapped_position} to {self.original_cards[self.last_swapped_position]}")

                        # Store_original_cards
                        elif not self.original_cards:
                            self.original_cards = self.word_letters.copy()

                        # Update_Current_Word
                        self.word_letters[i] = card_letter
                        print(f"[handle_word_click] Swapped letters: {current_letter} -> {card_letter}")
                        print(f"[handle_word_click] Current Word: {''.join(self.word_letters)}")

                        # Update_Swap_Status
                        self.last_swapped_position = i
                        self.used_card_positions.append(card_position)
                        self.selected_card = []

                    return True
            return False

    def check_word_validity(self):
        """
        Verify if the current word exists in the dictionary.

        Uses GameFunctions' check_exists function to verify if the player's word is valid.
        If valid:
            - Sets player_answer_status to 1
            - Sets computer_answer_status to 1
            - Saves current state
        If invalid:
            - Sets player_answer_status to 0
            - Sets computer_answer_status to 0
            - Restores previous state
        """
        current_word_str = ''.join(self.word_letters).lower()
        if self.logic.check_exists(current_word_str):  # Valid Word
            if self.side_status == 0:  # Player
                self.player_answer_status = 1
                print(f"[check_word_validity] Player answer checked: {self.player_answer_status}")
                replaced_letter = None
                for i, letter in enumerate(self.word_letters):
                    if letter != self.previous_word_letters[i]:
                        replaced_letter = letter
                        print(f"[check_word_validity] Player used letter: {letter}")
                        self.deck.append(letter.lower())
                        print(f"[check_word_validity] {letter} returned to deck")
                self.previous_word_letters = self.word_letters.copy()
                self.previous_used_card_positions = self.used_card_positions.copy()
                print("[check_word_validity] Answer check: Valid Word")
            elif self.side_status == 1:
                if self.bot.current_turn_will_answer_or_not:
                    if not self.bot.current_turn_answer == None:
                        self.computer_answer_status = 1
                        print(
                            f"[check_word_validity] Computer answer checked(will answer and not NONE): {self.computer_answer_status}")
                    else:
                        self.computer_answer_status = 0
                        print(
                            f"[check_word_validity] Computer answer checked(will answer but NONE): {self.computer_answer_status}")
                else:
                    self.computer_answer_status = 0
                    print(f"[check_word_validity] Computer answer checked(no answer): {self.computer_answer_status}")
        else:
            if self.side_status == 0:
                self.player_answer_status = 0
                print(f"[check_word_validity] Player answer checked: {self.player_answer_status}")
                self.word_letters = self.previous_word_letters.copy()
                self.used_card_positions = self.previous_used_card_positions.copy()
                print("[check_word_validity] Answer check: Invalid Word")
            elif self.side_status == 1:
                self.computer_answer_status = 0
                print(f"[check_word_validity] Computer answer checked: {self.computer_answer_status}")

    def handle_timer_event(self):
        """
        Handle timer events and round transitions

        Manages the game timer, round transitions, and updates game state
        when timer runs out. Includes:
            - Countdown management (15 seconds per turn)
            - Round completion logging
            - Card usage history tracking
            - Player turn switching
            - Game state reset between rounds

        Side effects:
            - Updates self.used_cards_history
            - Resets current round data
            - Toggles player turns
            - Triggers side change popup
        """
        if self.timer_seconds > 0 and not self.game_paused:
            self.timer_seconds -= 1
        else:
            if self.side_status == 0:  # Player
                print("[handle_timer_event] Current Word:", self.word_letters)
                print("[handle_timer_event] Previous Word:", self.previous_word_letters)
                if not self.show_remove_page and not self.show_remove_page_mode:
                    if self.word_letters == self.previous_word_letters:  # No word change
                        print("[handle_timer_event] No Word Changed.")
                        self.player_answer_status = 0
                        print(
                            f"[handle_timer_event] Player answer checked(no word change): {self.player_answer_status}")
                        self.add_penalty_card()
                        pass
                    else:
                        print("[handle_timer_event] Word Changed.")
                        self.check_word_validity()
                        print("[handle_timer_event] Word validity checked.")
                        self.update_side_text()
                        if self.player_answer_status == 1:
                            self.points += 1
                            print("[handle_timer_event] Player Points added one.")
                            print(f"[handle_timer_event] Player Points: {self.points}")
                            # print("Current Word:", self.word_letters)
                            # print("Previous Word:", self.previous_word_letters)
                        elif self.player_answer_status == 0:
                            self.add_penalty_card()
                        self.update_popup_text()
                        print(f"[handle_timer_event] Popup Text Updated.")
            elif self.side_status == 1:  # Computer
                self.check_word_validity()
                self.update_popup_text()
                print(f"[handle_timer_event] Popup Text Updated.")
                self.update_side_text()
                if self.computer_answer_status == 1:
                    self.computer_points += 1
                    print("[handle_timer_event] Computer Points added one.")
                    print(f"[handle_timer_event] Computer Points: {self.computer_points}")
                self.bot.end_turn()
            print(f"[handle_timer_event] Side Status(0-Player 1-Computer): {self.side_status}")
            print(f"[handle_timer_event] Player answer status: {self.player_answer_status}")
            print(f"[handle_timer_event] Computer answer status: {self.computer_answer_status}")
            self.side_status = 1 - self.side_status

            self.check_failure_condition()
            self.check_victory_condition()

            self.timer_seconds = self.game_settings.TURN_TIME_LIMIT

            if self.points == 0 or self.points == 1 or self.points == 2 or self.points == 3:
                self.show_popup = True
                self.game_paused = True
                pygame.time.set_timer(self.timer_event, 0)
            elif self.points == 4:
                self.show_popup = False
                self.show_remove_page = True
                self.game_paused = True
                pygame.time.set_timer(self.timer_event, 0)
                print("[handle_timer_event] --- Remove Mode Enables ---")
                print("[handle_timer_event] Remove mode: Enable")
                # pygame.time.set_timer(self.timer_event, 0)

            # Reset original letters and last swapped position at the end of each round
            self.original_cards = []
            self.last_swapped_position = None

    def handle_popup_click(self, pos):
        """
        Handle mouse clicks on popup windows.

        Processes user interactions with popup windows, including
        confirmation popups and card removal popups. Updates game state
        based on user choices.

        Args:
            pos (tuple): The (x, y) coordinates of the mouse click.

        Returns:
            bool: True if the popup interaction was successful, False otherwise.
        """
        if self.show_popup:
            if self.button_rect.collidepoint(pos):
                self.button_sound.play()
                self.organize_cards()
                self.update_side_text()

                # print(f"[handle_popup_click] Side Text Updated")
                print(f"[handle_popup_click] Card Stack: {self.deck}")
                self.show_popup = False
                self.game_paused = False
                self.show_remove_page = False
                self.show_remove_page_mode = False
                self.popup_ok_clicks += 1
                self.current_round = math.floor(self.popup_ok_clicks / 2)

                if '*' in self.word_letters:
                    print("[handle_popup_click] Star card detected! New word will be generated.")
                    self.star_card_active = True

                # If the star card is activated, generate new word
                if self.star_card_active:
                    self.current_word = self.logic.word_generator().upper()
                    self.word_letters = list(self.current_word)
                    self.previous_word_letters = self.word_letters.copy()
                    self.star_card_active = False
                    print(f"[handle_popup_click] Due to the star card, the new word is: {self.current_word}")

                self.replaced_positions.clear()

                if self.side_status == 0:
                    print("[handle_popup_click] --- Computer Turn Ends ---\n")
                    print("\n[handle_popup_click] --- Player Turn Starts ---")
                    print(f"[handle_popup_click] Current Round {self.popup_ok_clicks / 2}")
                    print(f"[handle_popup_click] Current Points: {self.points}")
                else:
                    print("[handle_popup_click] --- Player Turn Ends ---")
                    print("[handle_popup_click] --- Computer Turn Starts ---")
                pygame.time.set_timer(self.timer_event, 1000)

        elif self.show_popup_remove:
            mouse_x, mouse_y = pos
            if self.remove_yes_button_rect.collidepoint(mouse_x, mouse_y):
                if pygame.mouse.get_pressed()[0]:
                    self.button_sound.play()
                    self.side_status = 0
                    print("[handle_popup_click] Removal Successful\n[handle_popup_click] Remove mode: Disable")
                    print("[handle_popup_click] --- Remove Mode Disables ---")
                    if self.selected_card and isinstance(self.selected_card[0], tuple):
                        position, _ = self.selected_card[0]
                        self.used_card_positions.append(position)
                    self.selected_card = []
                    self.show_popup_remove = False
                    self.show_remove_page = False
                    self.points = 0
                    self.timer_seconds = self.game_settings.TURN_TIME_LIMIT
                    self.show_remove_page_mode = True
                    pygame.time.set_timer(self.timer_event, 1000)
                    return True

            elif self.remove_no_button_rect.collidepoint(mouse_x, mouse_y):
                if pygame.mouse.get_pressed()[0]:
                    self.button_sound.play()
                    print("[handle_popup_click] Cancel")
                    self.show_popup_remove = False
                    pygame.time.set_timer(self.timer_event, 0)
                    return True

        elif self.show_popup_bot_difficulty:
            mouse_x, mouse_y = pos
            if self.easy_button_rect.collidepoint(mouse_x, mouse_y):
                self.button_sound.play()
                self.bot = Bot(Bot.Difficulty.EASY, self.bot.cards)
                self.show_popup_bot_difficulty = False
                print(f"[handle_popup_click] Bot difficulty EASY")
            elif self.medium_button_rect.collidepoint(mouse_x, mouse_y):
                self.button_sound.play()
                self.bot = Bot(Bot.Difficulty.MEDIUM, self.bot.cards)
                self.show_popup_bot_difficulty = False
                print(f"[handle_popup_click] Bot difficulty MEDIUM")
            elif self.hard_button_rect.collidepoint(mouse_x, mouse_y):
                self.button_sound.play()
                self.bot = Bot(Bot.Difficulty.HARD, self.bot.cards)
                self.show_popup_bot_difficulty = False
                print(f"[handle_popup_click] Bot difficulty HARD")
            return True

        return False

    def handle_events(self):
        """
        Process all game events.

        Handles all pygame events including mouse clicks, timer events,
        and quit events. Manages navigation between different game screens
        and user interactions with game elements.

        Returns:
            bool: True if the game should continue running, False if it should quit.
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

                # print("[handle_events] Click")
                if not self.handle_button_click(mouse_x, mouse_y):
                    return False

                if self.show_victory_page or self.show_defeat_page:
                    if self.x_min_quit <= mouse_x <= self.x_max_quit and self.y_min_quit <= mouse_y <= self.y_max_quit:
                        pygame.quit()
                        sys.exit()
                    continue

                if not self.show_welcome_page or self.show_rules_page or self.show_options_page or self.show_credits_page:
                    self.handle_card_click(mouse_x, mouse_y)
                    self.handle_word_click(mouse_x, mouse_y)

                # Welcome_Page_Click
                if self.show_welcome_page or self.show_rules_page or self.show_options_page or self.show_credits_page:
                    if self.x_min_play_button <= mouse_x <= self.x_max_play_button and self.y_min_play_button <= mouse_y <= self.y_max_play_button:
                        if self.show_rules_page or self.show_options_page or self.show_credits_page:
                            self.button_sound.play()
                            self.show_welcome_page = True
                            self.show_rules_page = False
                            self.show_options_page = False
                            self.show_credits_page = False
                        elif self.show_welcome_page:

                            self.button_sound.play()
                            self.show_popup_bot_difficulty = True
                            self.show_welcome_page = False
                            self.show_rules_page = False
                            self.show_options_page = False
                            if self.side_status == 0:
                                self.show_player_first = True
                                self.show_computer_first = False
                            elif self.side_status == 1:
                                self.show_player_first = False
                                self.show_computer_first = True
                            self.show_credits_page = False
                        pygame.time.set_timer(self.timer_event, 0)
                    elif self.x_min_rules_button <= mouse_x <= self.x_max_rules_button and self.y_min_rules_button <= mouse_y <= self.y_max_rules_button:
                        self.button_sound.play()
                        self.show_welcome_page = False
                        self.show_rules_page = True
                        self.show_options_page = False
                        self.show_credits_page = False
                        pygame.time.set_timer(self.timer_event, 0)
                    elif self.x_min_options_button <= mouse_x <= self.x_max_options_button and self.y_min_options_button <= mouse_y <= self.y_max_options_button:
                        self.button_sound.play()
                        self.show_welcome_page = False
                        self.show_rules_page = False
                        self.show_options_page = True
                        self.show_credits_page = False
                        pygame.time.set_timer(self.timer_event, 0)
                    elif self.x_min_credits_button <= mouse_x <= self.x_max_credits_button and self.y_min_credits_button <= mouse_y <= self.y_max_credits_button:
                        self.button_sound.play()
                        self.show_welcome_page = False
                        self.show_rules_page = False
                        self.show_options_page = False
                        self.show_credits_page = True
                        pygame.time.set_timer(self.timer_event, 0)

                # Popup_Click
                elif self.show_popup or self.show_popup_remove or self.show_popup_bot_difficulty:
                    self.handle_popup_click(event.pos)

                # First_Role_Page_Click
                elif (self.show_computer_first or self.show_player_first) and not self.show_popup_bot_difficulty:
                    self.button_sound.play()
                    self.show_computer_first = False
                    self.show_player_first = False
                    if self.side_status == 0:
                        print("[handle_events] --- Player Turn Starts ---")
                    elif self.side_status == 1:
                        print("[handle_events] --- Computer Turn Starts ---")
                    pygame.time.set_timer(self.timer_event, 1000)

                elif not (
                        self.show_welcome_page or self.show_rules_page or self.show_options_page or self.show_credits_page) and self.x_min_game_paused_page <= mouse_x <= self.x_max_game_paused_page and self.y_min_game_paused_page <= mouse_y <= self.y_max_game_paused_page:
                    if not self.show_game_paused_page and not (
                            self.show_computer_first and self.show_player_first) and not self.show_rules_main_page:
                        self.button_sound.play()
                        self.game_paused = True
                        self.show_game_paused_page = True
                        print("[handle_events] Game Paused")
                        pygame.time.set_timer(self.timer_event, 0)
                    elif self.show_rules_main_page and not self.show_game_paused_page:
                        self.button_sound.play()
                        self.show_rules_main_page = False
                        pygame.time.set_timer(self.timer_event, 1000)
                    elif self.show_game_paused_page:
                        self.button_sound.play()
                        self.game_paused = False
                        self.show_game_paused_page = False
                        print("[handle_events] Game Unpaused")
                        pygame.time.set_timer(self.timer_event, 1000)

                elif self.show_game_paused_page and self.x_min_rules_main_button <= mouse_x <= self.x_max_rules_main_button and self.y_min_rules_main_button <= mouse_y <= self.y_max_rules_main_button:
                    self.button_sound.play()
                    self.show_rules_main_page = True
                    self.show_game_paused_page = False
                    self.paused_page_mark = 1
                    pygame.time.set_timer(self.timer_event, 0)

                elif not (
                        self.show_welcome_page or self.show_rules_page or self.show_options_page or self.show_credits_page):
                    if self.x_min_rules_main_button <= mouse_x <= self.x_max_rules_main_button and self.y_min_rules_main_button <= mouse_y <= self.y_max_rules_main_button and not self.show_rules_page:
                        self.button_sound.play()
                        self.show_rules_main_page = True
                        self.show_game_paused_page = False
                        pygame.time.set_timer(self.timer_event, 0)
                    elif self.show_rules_main_page:
                        if self.paused_page_mark == 1:
                            self.button_sound.play()
                            self.show_rules_main_page = False
                            self.show_game_paused_page = True
                            self.paused_page_mark = 0
                            pygame.time.set_timer(self.timer_event, 0)
                        else:
                            self.button_sound.play()
                            self.show_rules_main_page = False
                            pygame.time.set_timer(self.timer_event, 1000)

                # restart
            # Timer_Event
            elif event.type == self.timer_event:
                if not (self.show_victory_page or self.show_defeat_page):
                    self.handle_timer_event()
                    self.handle_bot_turn()
        return True

    def draw_round_counter(self):
        """
        Draw the current round number on the screen.

        Renders the current round number using the round font
        at the designated position on the screen.
        """
        round_text = self.font_round.render(str(self.current_round), True, self.round_text_color)
        self.screen.blit(round_text, self.round_text_pos)

    def draw(self):
        """
        Render all game elements on the screen.

        Draws the game background, UI elements, cards, and any active
        popups or special screens based on the current game state.
        Updates the display after drawing all elements.
        """
        # Draw_Background
        if self.sound_enabled:
            self.screen.blit(self.current_background, (0, 0))
        elif not self.sound_enabled:
            self.screen.blit(self.current_background_mute, (0, 0))
        self.draw_timer()
        self.draw_side_status()
        self.draw_coordinate_display()
        self.draw_word()
        self.draw_cards()
        self.draw_selected_card()
        self.draw_round_counter()
        self.draw_card_overlay()
        self.draw_points()

        # Draw_Game_Status
        if not self.game_paused:
            self.draw_side_status()
            self.draw_timer()

        # Draw_Welcome_Page
        if self.show_welcome_page:
            self.screen.blit(self.image_welcome_page, (0, 0))
            pygame.time.set_timer(self.timer_event, 0)
            pygame.display.flip()
            return

        if self.show_player_first:
            self.screen.blit(self.player_first, (0, 0))

        if self.show_computer_first:
            self.screen.blit(self.computer_first, (0, 0))

        if self.show_options_page:
            self.screen.blit(self.image_options_page, (0, 0))
            if self.options_click_sound == 1:
                self.sound_mark_click_sound = 1
                pygame.draw.rect(self.screen, self.test_color, self.options_box1_rect)
                # print("[draw] Options Box 1 checked")
            else:
                self.sound_mark_click_sound = 0

            if self.options_background_music == 1:
                self.sound_mark_background_music = 1
                pygame.draw.rect(self.screen, self.test_color, self.options_box2_rect)
                # print("[draw] Options Box 2 checked")
            else:
                self.sound_mark_background_music = 0

        if self.show_remove_page_mode:
            self.screen.blit(self.image_remove_page_mode, (0, 0))

        if self.show_rules_main_page:
            self.screen.blit(self.image_rules_main_page, (0, 0))

        if self.show_remove_page:
            self.screen.blit(self.image_remove_page, (0, 0))
            self.draw_cards()
            self.draw_selected_card()
            self.draw_card_overlay()

        if self.show_credits_page:
            self.screen.blit(self.image_credits_page, (0, 0))

        if self.show_victory_page:
            self.screen.blit(self.image_victory_page, (0, 0))

        if self.show_defeat_page:
            self.screen.blit(self.image_defeat_page, (0, 0))

        if self.show_game_paused_page:
            self.screen.blit(self.image_game_paused_page, (0, 0))
            pygame.time.set_timer(self.timer_event, 0)

        if self.show_popup and not (self.show_victory_page or self.show_defeat_page):
            self.draw_popup()

        if self.show_popup_remove:
            self.draw_popup_remove()

        if self.show_popup_bot_difficulty:
            self.draw_popup_bot_difficulty()

        if self.show_rules_page:
            self.screen.blit(self.image_rules_page, (0, 0))

        # Update_Screen
        pygame.display.flip()

    def run(self):
        """
        Start and maintain the main game loop.

        Continuously processes events and updates the display
        until the game is exited. Handles cleanup when the game ends.
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
    game = GameProgress()
    game.run()