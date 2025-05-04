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
import string
from enum import Enum
from BotFunctions import Bot
from GameFunctions import Game
from CardGameUI import CardGameUI
from GameSettings import game_settings


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
        card_stack = self.logic.card_stack()
        self.deck = card_stack
        print("\n--- Game Initialization In Progress ---")
        print("Initial Deck Content:", card_stack)

        # Generate the starting word
        self.current_word = self.logic.word_generator().upper()
        self.current_word_letters = list(self.current_word)
        self.current_word = self.logic.word_generator().upper()
        self.current_word_letters = list(self.current_word)

        # Generate the players' cards
        player_cards = [card_stack.pop().upper() for _ in range(game_settings.START_CARDS_AMOUNT)]
        print("Player's Cards:", player_cards)
        computer_cards = [card_stack.pop().upper() for _ in range(game_settings.START_CARDS_AMOUNT)]
        print("Computer's Cards:", computer_cards)
        print("--- Game Initialization Completed ---\n")

        # Initialize bot
        self.bot = Bot(Bot.Difficulty.MEDIUM, computer_cards)

        # Configure settings
        self.points = 0
        self.bot_correct_answers = 0
        self.answer_status = 0
        self.theme_setting = 0
        self.game_paused = False

        # Configure Pages
        self.show_popup = False
        self.show_popup_remove = False
        self.show_welcome_page = True
        self.show_options_page = False
        self.show_rules_page = False
        self.show_credits_page = False
        self.show_first_role = False
        self.show_game_paused_page = False
        self.show_remove_page = False
        self.show_remove_page_mode = False
        self.show_rules_main_page = False
        self.show_victory_page = False
        self.show_defeat_page = False

        # Configure Default Theme Settings
        # Color_Coordinate_Box
        self.text_color_coordinate = (33, 33, 33)
        # Color_Timer
        self.text_color_timer = (33, 33, 33)
        # Color_Popup
        self.popup_side_changer_color_background = self.popup_remove_color_background = (188, 173, 119)
        self.popup_side_changer_color_border = self.popup_remove_color_border = (33, 33, 33)
        self.popup_side_changer_color_button = self.popup_remove_color_button = (33, 33, 33)
        self.popup_side_changer_color_button_border = self.popup_remove_color_button_border = (33, 33, 33)
        self.popup_side_changer_color_text = self.popup_remove_color_text = (188, 173, 119)
        self.popup_side_changer_color_text_button = self.popup_remove_color_text_button = (33, 33, 33)
        # Color_Side_Status
        self.side_text_box_color = (33, 33, 33)
        # Color_Current_Word
        self.current_word_text_color = (33, 33, 33)
        # Color_Card_Letters
        self.card_text_color = (33, 33, 33)
        self.selected_letter_color = (240, 153, 31)
        # Color_Round_Counter
        self.round_text_color = (33, 33, 33)
        self.card_overlay_color = (33, 33, 33)

        # Config_Background
        self.background_0 = pygame.image.load("data/image/background_0.png")
        self.background_mute_0 = pygame.image.load("data/image/background_mute_0.png")
        self.background_1 = pygame.image.load("data/image/background_1.png")
        self.background_mute_1 = pygame.image.load("data/image/background_mute_1.png")
        self.current_background = self.background_0
        self.current_background_mute = self.background_mute_0
        # Config_First_Role
        self.player_first_0 = pygame.image.load("data/image/player_first_0.png")
        self.player_first_1 = pygame.image.load("data/image/player_first_1.png")
        self.computer_first_0 = pygame.image.load("data/image/computer_first_0.png")
        self.computer_first_1 = pygame.image.load("data/image/computer_first_1.png")
        self.player_first = self.player_first_0
        self.computer_first = self.computer_first_0
        value = self.logic.coin_flip()
        if value == 0:
            self.first_role = self.player_first
        else:
            self.first_role = self.computer_first
        # Config_Welcome_Page
        self.image_welcome_page_0 = pygame.image.load("data/image/welcome_page_0.png")
        self.image_welcome_page_1 = pygame.image.load("data/image/welcome_page_1.png")
        self.image_welcome_page = self.image_welcome_page_0
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
        # Config_Rules_Page
        self.image_rules_page_0 = pygame.image.load("data/image/rules_page_0.png")
        self.image_rules_page_1 = pygame.image.load("data/image/rules_page_1.png")
        self.image_rules_page = self.image_rules_page_0
        # Config_Rules_Main_Page
        self.image_rules_main_page_0 = pygame.image.load("data/image/rules_main_page_0.png")
        self.image_rules_main_page_1 = pygame.image.load("data/image/rules_main_page_1.png")
        self.image_rules_main_page = self.image_rules_main_page_0
        # Config_Options_Page
        self.image_options_page_0 = pygame.image.load("data/image/options_page_0.png")
        self.image_options_page_1 = pygame.image.load("data/image/options_page_1.png")
        self.image_options_page = self.image_options_page_0
        # Config_Credits_Page
        self.image_credits_page_0 = pygame.image.load("data/image/credits_page_0.png")
        self.image_credits_page_1 = pygame.image.load("data/image/credits_page_1.png")
        self.image_credits_page = self.image_credits_page_0
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
        # Config_Font
        self.font_size_default = 24
        self.font_size_timer = 88
        self.font_size_round = 34
        self.font_default = pygame.font.Font("data/font/AaHuanMengKongJianXiangSuTi-2.ttf", self.font_size_default)
        self.font_timer = pygame.font.Font("data/font/AaHuanMengKongJianXiangSuTi-2.ttf", self.font_size_timer)
        self.font_round = pygame.font.Font("data/font/AaHuanMengKongJianXiangSuTi-2.ttf", self.font_size_round)
        # Config_Timer
        self.timer_event = pygame.USEREVENT + 1
        self.timer_seconds = game_settings.TURN_TIME_LIMIT
        self.timer_x = 301
        self.timer_y = 248
        pygame.time.set_timer(self.timer_event, 1000)
        self.popup_rect = pygame.Rect(self.screen_width // 2 - 150, self.screen_height // 2 - 75, 300, 150)
        self.popup_remove_rect = pygame.Rect(self.screen_width // 2 - 150, self.screen_height // 2 - 75, 300, 150)
        self.button_rect = pygame.Rect(self.screen_width // 2 - 50, self.screen_height // 2 + 25, 100, 30)
        # Config_Popup
        self.popup_side_changer_width = 350
        self.popup_side_changer_height = 150
        self.popup_side_changer_width_button = 100
        self.popup_side_changer_height_button = 30
        self.popup_side_changer_pos_x = self.screen_width // 2 - self.popup_side_changer_width // 2
        self.popup_side_changer_pos_y = self.screen_width // 2 - self.popup_side_changer_height // 2
        self.popup_side_changer_pos_x_button = self.screen_width // 2 - self.popup_side_changer_width_button // 2
        self.popup_side_changer_pos_y_button = self.screen_width // 2 + 25
        self.popup_side_changer_text = ""
        self.popup_side_changer_text_player = "COMPUTER THINKING"
        self.popup_side_changer_text_computer = "IT IS YOUR TURN"
        self.popup_side_changer_text_button = ""
        self.popup_side_changer_text_button_player = "WAIT"
        self.popup_side_changer_text_button_computer = "GO"
        # Config_Popup_Remove
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

        # Config_Side_Status
        if self.first_role == self.player_first:
            self.side_status = 0
        else:
            self.side_status = 1
        self.update_side_text()
        self.side_text_box_pos = (self.screen_width // 2, 0)
        # Config_Current_Word
        self.current_word_font_size = 88
        self.current_word_font = pygame.font.Font("data/font/AaHuanMengKongJianXiangSuTi-2.ttf",
                                                  self.current_word_font_size)
        self.current_word_letter_1 = self.current_word_letters[0]
        self.current_word_letter_2 = self.current_word_letters[1]
        self.current_word_letter_3 = self.current_word_letters[2]
        self.current_word_letters = [self.current_word_letter_1, self.current_word_letter_2, self.current_word_letter_3]
        self.current_word_positions = []
        current_word_start_x = 256
        current_word_width = 95
        current_word_spacing = 5
        current_word_y = 110
        for i in range(3):
            self.current_word_positions.append(
                (current_word_start_x + i * (current_word_width + current_word_spacing), current_word_y))
            self.current_word_click_areas = []
            for i in range(3):
                x = current_word_start_x + i * (current_word_width + current_word_spacing)
                y = current_word_y
                self.current_word_click_areas.append((x, y, current_word_width, current_word_width))
                self.selected_current_word_letters = []
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
        # Config_Selected_Letters
        self.selected_letters = []
        self.last_swapped_position = None
        self.original_letters = []
        self.used_card_positions = list(range(7, 15))
        self.previous_word_letters = self.current_word_letters.copy()
        self.previous_used_card_positions = self.used_card_positions.copy()
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
        self.x_min_theme_0_button, self.y_min_theme_0_button = 4, 4
        self.x_max_theme_0_button, self.y_max_theme_0_button = 22, 22
        self.x_min_theme_1_button, self.y_min_theme_1_button = 26, 4
        self.x_max_theme_1_button, self.y_max_theme_1_button = 44, 22
        # Play
        self.x_min_play_button, self.y_min_play_button = 64, 525
        self.x_max_play_button, self.y_max_play_button = 137, 549
        # Options
        self.x_min_options_button, self.y_min_options_button = 237, 525
        self.x_max_options_button, self.y_max_options_button = 370, 549
        # Credits
        self.x_min_credits_button, self.y_min_credits_button = 638, 525
        self.x_max_credits_button, self.y_max_credits_button = 770, 549

    def handle_bot_turn(self):
        """
        Process the turn logic of robots

        The robot will decide whether to answer based on the difficulty setting, calculate the answer time, and replace words in the vocabulary
        """
        if self.show_first_role:
            return
        print("--- Player Turn Ends ---")
        print("\n--- Computer Turn Starts ---")
        # print("Computer is thinking...")
        current_word = "".join(self.current_word_letters)
        print(f"Current Word: {current_word}")
        difficulty_settings = self.bot.difficulty_settings[self.bot.difficulty_level]
        will_answer = random.random() < difficulty_settings["ANSWER_PROBABILITY"]

        if not will_answer:
            print("Computer decided to skip this turn.")
            # self.side_status = 0
            # self.update_side_text()
            # self.timer_seconds = game_settings.TURN_TIME_LIMIT
            self.timer_seconds = 0
            # self.show_popup = True
            print("--- Computer Turn Ends ---\n")
            return

        answer_time = random.gauss(difficulty_settings["AVERAGE_ANSWER_TIME"],
                                   difficulty_settings["VARIANCE_ANSWER_TIME"])
        answer_time = max(0.5, min(answer_time, 5.0))
        print(f"Computer will answer in {answer_time:.2f} seconds")
        pygame.time.wait(int(answer_time * 1000))
        bot_cards = [card.upper() for card in self.bot.cards]
        print(f"Computer Cards: {bot_cards}")

        if bot_cards:
            letter_frequencies = self.bot.letter_frequencies
            cards_with_freq = []
            for card in bot_cards:
                if card.lower() in letter_frequencies:
                    cards_with_freq.append((card, letter_frequencies[card.lower()]))
                else:
                    cards_with_freq.append((card, 0.0))

            # loot
            sorted_cards = sorted(cards_with_freq, key=lambda x: x[1], reverse=True)
            sorted_card_list = [card for card, _ in sorted_cards]
            print(f"Computer Cards Sorted By Frequency: {sorted_card_list}")

            # choose cards
            high_freq_card = sorted_card_list[0]
            print(
                f"Highest Frequency Card: {high_freq_card} (Frequency: {letter_frequencies.get(high_freq_card.lower(), 'Special Card')}%)")

            # ramdom position
            random_position = random.randint(0, len(self.current_word_letters) - 1)
            replaced_letter = self.current_word_letters[random_position]
            print(
                f"Computer chose {random_position + 1}，replaced '{replaced_letter}' (Frequency: {letter_frequencies.get(replaced_letter.lower(), '未知')}%)")

            # replacing letter
            self.current_word_letters[random_position] = high_freq_card
            new_word = "".join(self.current_word_letters)
            print(f"Computer used '{high_freq_card}' to replace '{replaced_letter}'")
            print(f"Computer turned '{current_word}' into '{new_word}'")

            # check exist
            if self.logic.check_exists(new_word.lower()):
                # remove used cards
                if high_freq_card in self.bot.cards:
                    self.bot.cards.remove(high_freq_card)
                    print(f"Computer removed '{high_freq_card}'")
                    print(f"Computer Remaining Cards: {self.bot.cards}")
                    print(f"Computer Card Empty Position: {15 - len(self.bot.cards)}")
                    # points
                    self.bot_correct_answers += 1
                    print(f"Computer Points: {self.bot_correct_answers}")

                # Points check
                if self.bot_correct_answers >= 3:
                    print("Computer reaches 3 points and removes the worst card.")
                    try:
                        self.bot.discard_card()
                        print("Successfully removed the worst card.")
                    except Exception as e:
                        print(f"Error removing card: {e}")
                        if self.bot.cards:
                            random_card = random.choice(self.bot.cards)
                            self.bot.cards.remove(random_card)
                            print(f"Randomly removed the card: {random_card}")
                    self.bot_correct_answers = 0
            else:
                print(f"New Word '{new_word}' Invalid.")
                # Penalty
                if self.deck:
                    new_card = self.deck.pop().upper()
                    self.bot.add_card(new_card)
                    print(f"Computer receives penalty card: {new_card}")
                    print(f"Computer Current Card: {self.bot.cards}")
                else:
                    print("Card Stack Empty")
                # Restore original words
                self.current_word_letters = list(current_word)
            # Switch back to player turn
            # self.timer_seconds = 0
            # self.show_popup = True
            # self.side_status = 0
            # self.update_side_text()
            # self.timer_seconds = game_settings.TURN_TIME_LIMIT

            # Display turn switch pop-up window
            # self.show_popup = True
        else:
            print("No Computer cards available.")

            # Switch back to player turn
            # self.side_status = 0
            # self.update_side_text()
            # self.timer_seconds = game_settings.TURN_TIME_LIMIT

            # Display turn switch pop-up window
            self.show_popup = True

        print("--- Computer Turn Ends ---\n")
        self.timer_seconds = 0

    def update_side_text(self):
        """
        Update the display text for current active player

        Updates to show "YOUR TURN" or "COMPUTER'S TURN" based on side_status value
        """
        if self.side_status == 0:
            self.side_text_box = "YOUR TURN"
            self.popup_side_changer_text = self.popup_side_changer_text_player
            self.popup_side_changer_text_button = self.popup_side_changer_text_button_player
        else:
            self.side_text_box = "COMPUTER'S TURN"
            self.popup_side_changer_text = self.popup_side_changer_text_computer
            self.popup_side_changer_text_button = self.popup_side_changer_text_button_computer

    def add_penalty_card(self):
        """
        Draw a random card from the deck and add it to player's hand.

        Selects a random letter from the remaining cards in the deck
        that aren't already in the player's hand. The card is then
        placed in the first available empty slot in the player's hand.

        Returns:
            str: The letter drawn from the deck, or None if no cards remain.
        """
        used_letters = set()
        for letter in self.card_letters:
            if letter:  # Only add non-empty letters
                used_letters.add(letter.upper())

        remaining_letters = [letter.upper() for letter in self.deck if letter.upper() not in used_letters]
        if self.answer_status == 0:

            if remaining_letters:
                random_card = random.choice(remaining_letters)
                print(f"The letters drawn from the deck of cards: {random_card}")

                for i in range(1, 15):
                    if self.card_letters[i] == '':
                        self.card_letters[i] = random_card
                        if i in self.used_card_positions:
                            self.used_card_positions.remove(i)
                        break
                return random_card
            else:
                print("There are no remaining letters to draw from the deck of cards.")
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

        self.previous_word_letters = self.current_word_letters.copy()
        self.previous_used_card_positions = self.used_card_positions.copy()

        print("The card has been moved forward to fill the vacancy.")
        print("Current Cards (Player):", self.card_letters)
        print("Used Position (Player):", self.used_card_positions)
        print("Number of Remaining Positions (Player):", len(self.used_card_positions))

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

        else:
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
            self.card_text_color = (0, 49, 82)
            self.selected_letter_color = (240, 153, 31)
            # Color_Round_Counter
            self.round_text_color = (228, 222, 215)
            # Overlay
            self.card_overlay_color = (0, 49, 82)
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
        for i, pos in enumerate(self.current_word_positions):
            letter_text = self.current_word_font.render(self.current_word_letters[i], True,
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
        for i, pos in enumerate(self.card_positions[:game_settings.MAX_CARDS]):
            # Only draw unused cards
            if i not in self.used_card_positions:
                letter_text = self.card_font.render(self.card_letters[i], True, self.card_text_color)
                text_x = pos[0] + 25 - letter_text.get_width() // 2
                text_y = pos[1] + 25 - letter_text.get_height() // 2
                self.screen.blit(letter_text, (text_x, text_y))

    def draw_selected_letters(self):
        font = self.card_font
        start_y = 443
        for i, letter in enumerate(self.selected_letters):
            if isinstance(letter, tuple):
                position, letter = letter
                text_x = self.card_positions[position][0] + 25 - font.size(letter)[0] // 2
            else:
                text_x = self.screen_width - 150 + i * 20
            letter_text = font.render(str(letter), True, self.selected_letter_color)
            self.screen.blit(letter_text, (text_x, start_y))

    def draw_card_overlay(self):
        for i, pos in enumerate(self.card_positions[:game_settings.MAX_CARDS]):
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
        pygame.draw.rect(self.screen, self.popup_side_changer_color_background, self.popup_rect)
        pygame.draw.rect(self.screen, self.popup_side_changer_color_border, self.popup_rect, 5)
        popup_text_render = self.font_default.render(self.popup_side_changer_text, True,
                                                     self.popup_side_changer_color_text_button)
        self.screen.blit(popup_text_render,
                         (self.popup_rect.centerx - popup_text_render.get_width() // 2, self.popup_rect.centery - 40))
        pygame.draw.rect(self.screen, self.popup_side_changer_color_button, self.button_rect)
        pygame.draw.rect(self.screen, self.popup_side_changer_color_button_border, self.button_rect, 2)
        button_text_render = self.font_default.render(self.popup_side_changer_text_button, True,
                                                      self.popup_side_changer_color_text)
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

        pygame.draw.rect(self.screen, self.popup_remove_color_background, self.popup_rect)
        pygame.draw.rect(self.screen, self.popup_remove_color_border, self.popup_rect, 5)

        popup_text_render = self.font_default.render(self.popup_remove_text, True, self.popup_remove_color_text_button)
        self.screen.blit(popup_text_render,
                         (self.popup_rect.centerx - popup_text_render.get_width() // 2, self.popup_rect.centery - 40))

        pygame.draw.rect(self.screen, self.popup_remove_color_button, self.remove_yes_button_rect)
        pygame.draw.rect(self.screen, self.popup_remove_color_button_border, self.remove_yes_button_rect, 2)
        yes_text_render = self.font_default.render(self.popup_remove_text_yes, True, self.popup_remove_color_text)
        self.screen.blit(yes_text_render, (self.remove_yes_button_rect.centerx - yes_text_render.get_width() // 2,
                                           self.remove_yes_button_rect.centery - yes_text_render.get_height() // 2))

        pygame.draw.rect(self.screen, self.popup_remove_color_button, self.remove_no_button_rect)
        pygame.draw.rect(self.screen, self.popup_remove_color_button_border, self.remove_no_button_rect, 2)
        no_text_render = self.font_default.render(self.popup_remove_text_no, True, self.popup_remove_color_text)
        self.screen.blit(no_text_render, (self.remove_no_button_rect.centerx - no_text_render.get_width() // 2,
                                          self.remove_no_button_rect.centery - no_text_render.get_height() // 2))

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
            if pygame.mouse.get_pressed()[0]:
                self.button_sound.play()
                self.theme_setting = 0
                if self.show_rules_page or self.show_options_page or self.show_credits_page:
                    self.show_welcome_page = True
                    self.show_rules_page = False
                    self.show_options_page = False
                    self.show_credits_page = False
                # pygame.time.set_timer(self.timer_event, 0)
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
                # pygame.time.set_timer(self.timer_event, 0)
                self.update_theme()

        # Quit_Button
        if self.x_min_quit <= mouse_x <= self.x_max_quit and self.y_min_quit <= mouse_y <= self.y_max_quit and not (
                self.show_welcome_page or self.show_rules_page or self.show_options_page or self.show_credits_page or self.show_first_role):
            if pygame.mouse.get_pressed()[0]:
                self.button_sound.play()
                print("Quit")
                return False

        # Confirm_Button
        if self.x_min_confirm_button <= mouse_x <= self.x_max_confirm_button and self.y_min_confirm_button <= mouse_y <= self.y_max_confirm_button and not (
                self.show_welcome_page or self.show_rules_page or self.show_options_page or self.show_credits_page or self.show_first_role):
            if pygame.mouse.get_pressed()[0] and self.side_status == 0:
                self.button_sound.play()
                self.timer_seconds = 0

        # Sound_Button
        if self.x_min_sound_button <= mouse_x <= self.x_max_sound_button and self.y_min_sound_button <= mouse_y <= self.y_max_sound_button and not (
                self.show_welcome_page or self.show_rules_page or self.show_options_page or self.show_credits_page or self.show_first_role):
            if pygame.mouse.get_pressed()[0]:
                self.button_sound.play()
                if self.sound_enabled:
                    pygame.mixer.music.set_volume(0)
                    self.sound_enabled = False
                    if self.theme_setting == 0:
                        self.current_background = self.background_mute_0
                    if self.theme_setting == 1:
                        self.current_background = self.background_mute_1
                else:
                    pygame.mixer.music.set_volume(0.3)
                    self.sound_enabled = True
                    if self.theme_setting == 0:
                        self.current_background = self.background_0
                    if self.theme_setting == 1:
                        self.current_background = self.background_1
                self.button_sound.play()
        return True

        # Conditions

    def check_victory_condition(self):
        """
        Check if the player has won the game.

        Victory occurs when all card positions are used (no cards left).
        When victory is achieved, displays the victory page and stops the timer.

        Returns:
            bool: True if victory condition is met, False otherwise.
        """
        if len(self.used_card_positions) == 15:
            self.show_victory_page = True
            pygame.time.set_timer(self.timer_event, 0)
            self.game_paused = True
            print("Victory")
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
        if len(self.used_card_positions) == 0:
            self.show_defeat_page = True
            pygame.time.set_timer(self.timer_event, 0)
            self.game_paused = True
            print("Defeat")
            return True
        # else:
        # print("No Defeat")
        return False

    # Handle_Card_Click
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
            - Updates self.selected_letters when a valid card is clicked
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

    # handle_word_click
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
        if self.side_status != 0 or self.game_paused:
            return
        for i, (x, y, width, height) in enumerate(self.current_word_click_areas):
            if x <= mouse_x <= x + width and y <= mouse_y <= y + height:
                if self.selected_letters:
                    card_position, card_letter = self.selected_letters[0]
                    current_letter = self.current_word_letters[i]

                    # Handle_Previous_Swap
                    if self.last_swapped_position is not None:
                        # Same_Position_Swap
                        if self.last_swapped_position == i:
                            if self.used_card_positions:
                                last_card_position = self.used_card_positions.pop()
                                print(f"Restored previous card at position {last_card_position}")
                        # Different_Position_Swap
                        else:
                            self.current_word_letters[self.last_swapped_position] = self.original_letters[
                                self.last_swapped_position]
                            if self.used_card_positions:
                                last_card_position = self.used_card_positions.pop()
                                print(f"Restored card at position {last_card_position}")
                            print(
                                f"Restored position {self.last_swapped_position} to {self.original_letters[self.last_swapped_position]}")

                    # Store_Original_Letters
                    if not self.original_letters:
                        self.original_letters = self.current_word_letters.copy()

                    # Update_Current_Word
                    self.current_word_letters[i] = card_letter
                    print(f"Swapped letters: {current_letter} -> {card_letter}")
                    print(f"Current Word: {''.join(self.current_word_letters)}")

                    # Update_Swap_Status
                    self.last_swapped_position = i
                    self.used_card_positions.append(card_position)
                    self.selected_letters = []
                return True
        return False

    def check_word_validity(self):
        """
        Verify if the current word exists in the dictionary.

        Uses GameFunctions' check_exists function to verify if the player's word is valid.
        If valid:
            - Sets answer_status to 1
            - Saves current state
        If invalid:
            - Sets answer_status to 0
            - Restores previous state
        """
        current_word_str = ''.join(self.current_word_letters).lower()
        if self.logic.check_exists(current_word_str):
            self.answer_status = 1
            if self.side_status == 0:
                self.previous_word_letters = self.current_word_letters.copy()
                self.previous_used_card_positions = self.used_card_positions.copy()
            # print("Answer check: Valid Word")
        else:
            self.answer_status = 0
            if self.side_status == 0:
                self.current_word_letters = self.previous_word_letters.copy()
                self.used_card_positions = self.previous_used_card_positions.copy()
            # print("Answer check: Invalid Word")

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

            if self.side_status == 0:
                self.check_word_validity()
                if self.answer_status == 1:
                    self.points += 1
            self.side_status = 1 - self.side_status

            self.check_failure_condition()
            self.check_victory_condition()

            self.timer_seconds = game_settings.TURN_TIME_LIMIT

            if self.points == 0 or self.points == 1 or self.points == 2 or self.points == 3:
                self.show_popup = True
                self.game_paused = True
                pygame.time.set_timer(self.timer_event, 0)
            elif self.points == 4:
                self.show_popup = False
                self.game_paused = True
                pygame.time.set_timer(self.timer_event, 0)
                self.show_remove_page = True
                self.game_paused = True
                print("--- Remove Mode Enables ---")
                print("Remove mode: Enable")
                pygame.time.set_timer(self.timer_event, 0)

            #  Reset original letters and last swapped position at the end of each round
            self.original_letters = []
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
                self.add_penalty_card()
                self.organize_cards()
                self.update_side_text()
                self.show_popup = False
                self.game_paused = False
                self.show_remove_page = False
                self.show_remove_page_mode = False
                self.popup_ok_clicks += 1
                self.current_round = math.floor(self.popup_ok_clicks / 2)

                if self.side_status == 0:
                    print("--- Player Turn Starts ---")
                    print(f"Current Round {self.popup_ok_clicks / 2}")
                    print(f"Current Points: {self.points}")
                else:
                    self.handle_bot_turn()

                pygame.time.set_timer(self.timer_event, 1000)
        if self.show_popup_remove:
            mouse_x, mouse_y = pos
            if self.remove_yes_button_rect.collidepoint(mouse_x, mouse_y):
                if pygame.mouse.get_pressed()[0]:
                    self.button_sound.play()
                    self.side_status = 0
                    print("Removal Successful\nRemove mode: Disable")
                    print("--- Remove Mode Disables ---")
                    if self.selected_letters and isinstance(self.selected_letters[0], tuple):
                        position, _ = self.selected_letters[0]
                        self.used_card_positions.append(position)
                    self.selected_letters = []
                    self.show_popup_remove = False
                    self.show_remove_page = False
                    self.points = 0
                    self.timer_seconds = game_settings.TURN_TIME_LIMIT
                    self.show_remove_page_mode = True
                    pygame.time.set_timer(self.timer_event, 1000)
                    return True

            elif self.remove_no_button_rect.collidepoint(mouse_x, mouse_y):
                if pygame.mouse.get_pressed()[0]:
                    self.button_sound.play()
                    print("Cancel")
                    self.show_popup_remove = False
                    pygame.time.set_timer(self.timer_event, 0)
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
                if not self.handle_button_click(mouse_x, mouse_y):
                    return False

                if self.show_victory_page or self.show_defeat_page:
                    if self.x_min_quit <= mouse_x <= self.x_max_quit and self.y_min_quit <= mouse_y <= self.y_max_quit:
                        return False
                    continue

                if not self.show_welcome_page or self.show_rules_page or self.show_options_page or self.show_credits_page:
                    self.handle_card_click(mouse_x, mouse_y)
                    self.handle_word_click(mouse_x, mouse_y)
                # Welcome_Page_Click
                if self.show_welcome_page or self.show_rules_page or self.show_options_page or self.show_credits_page:
                    if self.x_min_play_button <= mouse_x <= self.x_max_play_button and self.y_min_play_button <= mouse_y <= self.y_max_play_button:
                        self.button_sound.play()
                        self.show_welcome_page = False
                        self.show_rules_page = False
                        self.show_options_page = False
                        self.show_first_role = True
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
                elif self.show_popup or self.show_popup_remove:
                    self.handle_popup_click(event.pos)

                # First_Role_Page_Click
                elif self.show_first_role:
                    self.button_sound.play()
                    self.show_first_role = False
                    if self.side_status == 0:
                        print("--- Player Turn Starts ---")
                    else:
                        self.handle_bot_turn()
                    pygame.time.set_timer(self.timer_event, 1000)

                elif not (
                        self.show_welcome_page or self.show_rules_page or self.show_options_page or self.show_credits_page) and self.x_min_game_paused_page <= mouse_x <= self.x_max_game_paused_page and self.y_min_game_paused_page <= mouse_y <= self.y_max_game_paused_page:
                    if not self.show_game_paused_page and not self.show_first_role:
                        self.button_sound.play()
                        self.game_paused = True
                        self.show_game_paused_page = True
                        print("Game Paused")
                        pygame.time.set_timer(self.timer_event, 0)
                    elif self.show_game_paused_page:
                        self.button_sound.play()
                        self.game_paused = False
                        self.show_game_paused_page = False
                        print("Game Unpaused")
                        pygame.time.set_timer(self.timer_event, 1000)

                elif not (
                        self.show_welcome_page or self.show_rules_page or self.show_options_page or self.show_credits_page):
                    if self.x_min_rules_main_button <= mouse_x <= self.x_max_rules_main_button and self.y_min_rules_main_button <= mouse_y <= self.y_max_rules_main_button and not self.show_rules_page:
                        self.show_rules_main_page = True
                        self.show_game_paused_page = False
                        pygame.time.set_timer(self.timer_event, 0)
                    elif self.show_rules_main_page:
                        self.show_rules_main_page = False
                        pygame.time.set_timer(self.timer_event, 1000)

            # Timer_Event
            elif event.type == self.timer_event:
                if not (self.show_victory_page or self.show_defeat_page):
                    self.handle_timer_event()
        return True

    # Draw_Round_Counter
    def draw_round_counter(self):
        """
        Draw the current round number on the screen.

        Renders the current round number using the round font
        at the designated position on the screen.
        """
        round_text = self.font_round.render(str(self.current_round), True, self.round_text_color)
        self.screen.blit(round_text, self.round_text_pos)

    # Draw_Game_Screen
    def draw(self):
        """
        Render all game elements on the screen.

        Draws the game background, UI elements, cards, and any active
        popups or special screens based on the current game state.
        Updates the display after drawing all elements.
        """
        # Draw_Background
        self.screen.blit(self.current_background, (0, 0))
        self.draw_timer()
        self.draw_side_status()
        # self.draw_coordinate_display()
        self.draw_word()
        self.draw_cards()
        self.draw_selected_letters()
        self.draw_round_counter()
        self.draw_card_overlay()

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

        if self.show_first_role:
            self.screen.blit(self.first_role, (0, 0))

        if self.show_options_page:
            self.screen.blit(self.image_options_page, (0, 0))

        if self.show_remove_page_mode:
            self.screen.blit(self.image_remove_page_mode, (0, 0))

        if self.show_rules_main_page:
            self.screen.blit(self.image_rules_main_page, (0, 0))

        if self.show_remove_page:
            self.screen.blit(self.image_remove_page, (0, 0))
            self.draw_cards()
            self.draw_selected_letters()
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