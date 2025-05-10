# Import libraries
import os
import sys
import math
import random

import pygame

from BotFunctions import Bot
from GameFunctions import Game
from GameSettings import GameSettings
from NotificationBar import NotificationBar


class GameProgress:
    """
    Card Game User Interface Class.

    Manages the game's graphical interface, event handling, and game states.
    Contains all visual elements, audio controls, and interaction logic.
    Implements single-player vs computer turn-based gameplay with multiple
    themes and difficulty settings.

    Attributes:
    -----------
        screen_width : int
            Game window width, default 800 pixels.
        screen_height : int
            Game window height, default 600 pixels.
        show_popup : bool
            Whether to display popup.
        game_paused : bool
            Whether the game is paused.
        current_round : int
            Current round number.
        side_status : int
            Current active player (0 for player, 1 for computer).
        points : int
            Current player score.
        theme_setting : int
            Theme setting (0 for default theme, 1 for dark theme).
        sound_enabled : bool
            Whether sound is enabled.

    Methods:
    --------
        draw():
            Render all game elements to screen
        draw_cards():
            Draw player's hand cards
        handle_card_click(mouse_x, mouse_y):
            Handle card selection events
        organize_cards():
            Rearrange card positions
        add_penalty_card():
            Draw new card from deck
        run():
            Launch and maintain main game loop
    """

    def __init__(self):
        # Initialize pygame.
        pygame.init()
        pygame.mixer.init()

        # Set up screen configuration.
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )
        pygame.display.set_caption("Word Battle")

        # Initialize game logic and settings.
        self.logic = Game()
        self.game_settings = GameSettings()
        self.notification = NotificationBar(
            self.screen_width, self.screen_height
        )

        # Prepare card deck.
        self.card_stack = self.logic.card_stack()
        self.deck = self.card_stack
        print(f"\n[__init__] --- Game Initialization in progress ---")
        print(f"[__init__] Initial Deck content:", self.card_stack)

        # Initialize the word generator.
        self.word = self.logic.word_generator().upper()
        self.word_cards = list(self.word)
        self.word = self.logic.word_generator().upper()
        self.word_cards = list(self.word)

        # Pass cards for player 1 and player 2.
        self.player_cards_initial = [
            self.card_stack.pop().upper()
            for _ in range(self.game_settings.START_CARDS_AMOUNT)
        ]
        print(f"[__init__] Player's Cards: {self.player_cards_initial}")

        self.computer_cards_initial = [
            self.card_stack.pop().lower()
            for _ in range(self.game_settings.START_CARDS_AMOUNT)
        ]
        print(f"[__init__] Computer's Cards: {self.computer_cards_initial}")

        # Configure 15 card slots for the player.
        self.player_cards = [''] * 15
        for i in range(len(self.player_cards_initial)):
            self.player_cards[i] = self.player_cards_initial[i]

        # Set up card display positions.
        self.card_positions = []
        self.player_card_x = 28
        self.player_card_y = 449
        self.player_card_width = 49
        self.player_card_spacing = 1

        for i in range(15):
            self.card_positions.append(
                (
                    self.player_card_x + i * (
                        self.player_card_width + self.player_card_spacing
                    ),
                    self.player_card_y
                )
            )
        
        # Configure card click areas.
        self.card_click_areas = []
        for i in range(15):
            x = self.player_card_x + i * (
                    self.player_card_width + self.player_card_spacing
            )
            y = self.player_card_y
            self.card_click_areas.append(
                (x, y, self.player_card_width, self.player_card_width)
            )

        # Initialize the bot.
        self.bot = Bot(Bot.Difficulty.EASY, self.computer_cards_initial)

        # Configure initial variables.
        self.points = 1
        self.side_status = 0
        self.computer_points = 0
        self.bot_correct_answers = 0
        self.theme_setting = 0
        self.player_answer_status = None
        self.computer_answer_status = None
        self.game_paused = False

        # Configure initial page.
        self.show_welcome_page = True
        self.show_options_page = False
        self.show_rules_page = False
        self.show_credits_page = False
        self.show_player_first_page = False
        self.show_computer_first_page = False
        self.show_popup = False
        self.show_popup_remove = False
        self.show_popup_bot_difficulty = False
        self.show_game_paused_page = False
        self.show_rules_main_page = False
        self.show_remove_page = False
        self.show_remove_page_mode = False
        self.show_victory_page = False
        self.show_defeat_page = False

        # Configure default theme settings.
        self.color_text_coordinate = (33, 33, 33)
        self.color_text_timer = (33, 33, 33)
        self.color_text_side_box = (33, 33, 33)
        self.color_text_word = (33, 33, 33)
        self.color_text_cards = (33, 33, 33)
        self.color_text_selected_card = (240, 153, 31)
        self.color_text_round = (33, 33, 33)
        self.color_popup_background = (188, 173, 119)
        self.color_popup_border = (33, 33, 33)
        self.color_popup_button = (33, 33, 33)
        self.color_popup_button_border = (33, 33, 33)
        self.color_popup_text = (188, 173, 119)
        self.color_popup_text_button = (33, 33, 33)
        self.color_card_overlay = (33, 33, 33)
        self.color_point_block = (188, 173, 119)
        self.color_option_button = (188, 173, 119)

        # Load images.
        self.image_background_0 = pygame.image.load(
            "data/image/background_0.png"
        )
        self.image_background_1 = pygame.image.load(
            "data/image/background_1.png"
        )
        self.image_background_mute_0 = pygame.image.load(
            "data/image/background_mute_0.png"
        )
        self.image_background_mute_1 = pygame.image.load(
            "data/image/background_mute_1.png"
        )
        self.image_welcome_page_0 = pygame.image.load(
            "data/image/welcome_page_0.png"
        )
        self.image_welcome_page_1 = pygame.image.load(
            "data/image/welcome_page_1.png"
        )
        self.image_rules_page_0 = pygame.image.load(
            "data/image/rules_page_0.png"
        )
        self.image_rules_page_1 = pygame.image.load(
            "data/image/rules_page_1.png"
        )
        self.image_options_page_0 = pygame.image.load(
            "data/image/options_page_0.png"
        )
        self.image_options_page_1 = pygame.image.load(
            "data/image/options_page_1.png"
        )
        self.image_credits_page_0 = pygame.image.load(
            "data/image/credits_page_0.png"
        )
        self.image_credits_page_1 = pygame.image.load(
            "data/image/credits_page_1.png"
        )
        self.image_player_first_0 = pygame.image.load(
            "data/image/player_first_0.png"
        )
        self.image_player_first_1 = pygame.image.load(
            "data/image/player_first_1.png"
        )
        self.image_computer_first_0 = pygame.image.load(
            "data/image/computer_first_0.png"
        )
        self.image_computer_first_1 = pygame.image.load(
            "data/image/computer_first_1.png"
        )
        self.image_remove_page_0 = pygame.image.load(
            "data/image/remove_page_0.png"
        )
        self.image_remove_page_mode_0 = pygame.image.load(
            "data/image/remove_page_mode_0.png"
        )
        self.image_remove_page_1 = pygame.image.load(
            "data/image/remove_page_1.png"
        )
        self.image_remove_page_mode_1 = pygame.image.load(
            "data/image/remove_page_mode_1.png"
        )
        self.image_game_paused_page_0 = pygame.image.load(
            "data/image/game_paused_page_0.png"
        )
        self.image_game_paused_page_1 = pygame.image.load(
            "data/image/game_paused_page_1.png"
        )
        self.image_rules_main_page_0 = pygame.image.load(
            "data/image/rules_main_page_0.png"
        )
        self.image_rules_main_page_1 = pygame.image.load(
            "data/image/rules_main_page_1.png"
        )
        self.image_victory_page_0 = pygame.image.load(
            "data/image/victory_0.png"
        )
        self.image_victory_page_1 = pygame.image.load(
            "data/image/victory_1.png"
        )
        self.image_defeat_page_0 = pygame.image.load(
            "data/image/defeat_0.png"
        )
        self.image_defeat_page_1 = pygame.image.load(
            "data/image/defeat_1.png"
        )
        
        # Configure default images.
        self.image_current_background = self.image_background_0
        self.image_current_background_mute = self.image_background_mute_0
        self.image_welcome_page = self.image_welcome_page_0
        self.image_rules_page = self.image_rules_page_0
        self.image_options_page = self.image_options_page_0
        self.image_credits_page = self.image_credits_page_0
        self.image_player_first_page = self.image_player_first_0
        self.image_computer_first_page = self.image_computer_first_0
        self.image_remove_page = self.image_remove_page_0
        self.image_remove_mode_page = self.image_remove_page_mode_0
        self.image_game_paused_page = self.image_game_paused_page_0
        self.image_rules_main_page = self.image_rules_main_page_0
        self.image_victory_page = self.image_victory_page_0
        self.image_defeat_page = self.image_defeat_page_0

        # Load audios.
        self.background_music_0 = "data/sound/background_music_0.wav"
        self.background_music_1 = "data/sound/background_music_1.wav"
        self.button_sound = pygame.mixer.Sound("data/sound/button_sound.wav")
        self.sound_enabled = True

        pygame.mixer.music.load(self.background_music_0)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        # Configure fonts.
        self.font_size_default = 24
        self.font_size_timer = 88
        self.font_size_round = 34
        self.font_size_cards = 52
        self.font_size_word = 88

        # Load fonts.
        self.font_default = pygame.font.Font(
            "data/font/AaHuanMengKongJianXiangSuTi-2.ttf", self.font_size_default
        )
        self.font_timer = pygame.font.Font(
            "data/font/AaHuanMengKongJianXiangSuTi-2.ttf", self.font_size_timer
        )
        self.font_round = pygame.font.Font(
            "data/font/AaHuanMengKongJianXiangSuTi-2.ttf", self.font_size_round
        )
        self.font_cards = pygame.font.Font(
            "data/font/AaHuanMengKongJianXiangSuTi-2.ttf", self.font_size_cards
        )
        self.font_word = pygame.font.Font(
            "data/font/AaHuanMengKongJianXiangSuTi-2.ttf", self.font_size_word
        )

        #Configure first-hand player.
        self.value = self.logic.coin_flip()
        print(f"[__init__] {self.value}")

        if self.value == "Head":
            self.side_status = 0
            self.image_player_first_page = self.image_player_first_0
            print(f"[__init__] Player goes first")

        elif self.value == "Tail":
            self.side_status = 1
            self.image_computer_first_page = self.image_computer_first_0
            print(f"[__init__] Computer goes first")

        # Configure selection buttons.
        self.options_box1_rect = pygame.Rect(672, 178, 18, 18)
        self.options_box2_rect = pygame.Rect(709, 318, 18, 18)
        self.options_click_sound = 1
        self.options_background_music = 1

        # Configure timer.
        self.timer_x = 301
        self.timer_y = 248
        self.timer_event = pygame.USEREVENT + 1
        self.timer_seconds = self.game_settings.TURN_TIME_LIMIT
        pygame.time.set_timer(self.timer_event, 1000)

        # Configure popup.
        self.popup_side_changer_width = 800
        self.popup_side_changer_height = 123
        self.popup_side_changer_width_button = 260
        self.popup_side_changer_height_button = 30
        self.popup_rect = pygame.Rect(self.screen_width // 2 - self.popup_side_changer_width // 2, self.screen_height // 2 - self.popup_side_changer_height // 2, self.popup_side_changer_width, self.popup_side_changer_height)
        self.popup_button_rect = pygame.Rect(self.screen_width // 2 - self.popup_side_changer_width_button // 2, self.screen_height // 2 - self.popup_side_changer_height_button // 2 + 25, self.popup_side_changer_width_button, self.popup_side_changer_height_button)
        self.popup_side_changer_pos_x = self.screen_width // 2 - self.popup_side_changer_width // 2
        self.popup_side_changer_pos_y = self.screen_width // 2 - self.popup_side_changer_height // 2
        self.popup_side_changer_pos_x_button = self.screen_width // 2 - self.popup_side_changer_width_button // 2
        self.popup_side_changer_pos_y_button = self.screen_width // 2 + 25
        self.popup_side_changer_text = None
        self.popup_side_changer_text_button = None
        self.popup_side_changer_text_player = "Player Invalid Answer"
        self.popup_side_changer_text_computer = "Computer Invalid Answer"
        self.popup_side_changer_text_button_player = "COMPUTER'S TURN"
        self.popup_side_changer_text_button_computer = "START MY TURN"

        # Configure popup (remove mode).
        self.popup_remove_width = 300
        self.popup_remove_height = 123
        self.popup_remove_width_button = 100
        self.popup_remove_height_button = 30
        self.popup_remove_rect = pygame.Rect(self.screen_width // 2 - self.popup_remove_width // 2, self.screen_height // 2 - self.popup_remove_height // 2, self.popup_remove_width, self.popup_remove_height)
        self.popup_remove_pos_x = self.screen_width // 2 - self.popup_side_changer_width // 2
        self.popup_remove_pos_y = self.screen_width // 2 - self.popup_side_changer_height // 2
        self.popup_remove_pos_x_button = self.screen_width // 2 - self.popup_side_changer_width_button // 2
        self.popup_remove_pos_y_button = self.screen_width // 2 + 25
        self.popup_remove_yes_button_rect = pygame.Rect(self.screen_width // 2 - 120, self.screen_height // 2 + 10, self.popup_remove_width_button, self.popup_remove_height_button)
        self.popup_remove_no_button_rect = pygame.Rect(self.screen_width // 2 + 20, self.screen_height // 2 + 10, self.popup_remove_width_button, self.popup_remove_height_button)
        self.popup_remove_text = "REMOVE THIS CARD?"
        self.popup_remove_text_yes = "Yes"
        self.popup_remove_text_no = "No"
        self.popup_remove_text_button = "OK"
        
       # Configure popup (bot difficulty).
        self.popup_bot_difficulty_width = 800
        self.popup_bot_difficulty_height = 123
        self.popup_bot_difficulty_difficulty_button_width = 100
        self.popup_bot_difficulty_difficulty_button_height = 30
        self.popup_bot_difficulty_rect = pygame.Rect(self.screen_width // 2 - self.popup_bot_difficulty_width // 2, self.screen_height // 2 - self.popup_bot_difficulty_height // 2, self.popup_bot_difficulty_width, self.popup_bot_difficulty_height)
        self.popup_bot_difficulty_pos_x = self.screen_width // 2 - self.popup_bot_difficulty_width // 2
        self.popup_bot_difficulty_pos_y = self.screen_width // 2 - self.popup_bot_difficulty_height // 2
        self.popup_bot_difficulty_easy_button_rect = pygame.Rect(self.screen_width // 2 - 170, self.screen_height // 2 + 10, self.popup_bot_difficulty_difficulty_button_width, self.popup_bot_difficulty_difficulty_button_height)
        self.popup_bot_difficulty_medium_button_rect = pygame.Rect(self.screen_width // 2 - 50, self.screen_height // 2 + 10, self.popup_bot_difficulty_difficulty_button_width, self.popup_bot_difficulty_difficulty_button_height)
        self.popup_bot_difficulty_hard_button_rect = pygame.Rect(self.screen_width // 2 + 70, self.screen_height // 2 + 10, self.popup_bot_difficulty_difficulty_button_width, self.popup_bot_difficulty_difficulty_button_height)

        # Configure word.
        self.word_card_1 = self.word_cards[0]
        self.word_card_2 = self.word_cards[1]
        self.word_card_3 = self.word_cards[2]
        self.word_cards = [self.word_card_1, self.word_card_2, self.word_card_3]
        self.word_card_positions = []
        self.word_card_x = 256
        self.word_card_y = 110
        self.word_card_width = 95
        self.word_card_spacing = 5
        for i in range(3):
            self.word_card_positions.append((self.word_card_x + i * (self.word_card_width + self.word_card_spacing), self.word_card_y))
            self.word_click_areas = []
            for i in range(3):
                x = self.word_card_x + i * (self.word_card_width + self.word_card_spacing)
                y = self.word_card_y
                self.word_click_areas.append((x, y, self.word_card_width, self.word_card_width))
                self.selected_word_cards = []

        # Configure side text box
        self.side_text = None
        self.side_text_box_pos = (self.screen_width // 2, 0)
        
        # Configure selected cards
        self.selected_card = []
        self.original_cards = []
        self.replaced_positions = []
        self.star_card_active = False
        self.last_swapped_position = None
        self.used_card_positions = list(range(7, 15))
        self.previous_word_cards = self.word_cards.copy()
        self.previous_used_card_positions = self.used_card_positions.copy()

        # Configure points
        self.point_maximum = 3
        self.point_block_x = 238
        self.point_block_y = 570
        self.point_block_length = 55
        self.point_block_height = 17
        self.point_block_spacing = 3

        # Configure round counter
        self.round = 1
        self.round_text_pos = (119, 559)
        self.round_counter_popup_click_count = 2
        
        # Configure click area of buttons
        self.x_min_game_paused_page, self.y_min_game_paused_page = 472, 563
        self.x_max_game_paused_page, self.y_max_game_paused_page = 502, 593
        self.x_min_quit_button, self.y_min_quit_button = 508, 563
        self.x_max_quit_button, self.y_max_quit_button = 538, 593
        self.x_min_sound_button, self.y_min_sound_button = 436, 563
        self.x_max_sound_button, self.y_max_sound_button = 466, 593
        self.x_min_confirm_button, self.y_min_confirm_button = 666, 563
        self.x_max_confirm_button, self.y_max_confirm_button = 794, 593
        self.x_min_rules_button, self.y_min_rules_button = 455, 525
        self.x_max_rules_button, self.y_max_rules_button = 555, 549
        self.x_min_rules_main_button, self.y_min_rules_main_button = 547, 563
        self.x_max_rules_main_button, self.y_max_rules_main_button = 660, 593
        self.x_min_back_button, self.y_min_back_button = 547, 563
        self.x_max_back_button, self.y_max_back_button = 660, 593
        self.x_min_theme_0_button, self.y_min_theme_0_button = 95, 70
        self.x_max_theme_0_button, self.y_max_theme_0_button = 318, 240
        self.x_min_theme_1_button, self.y_min_theme_1_button = 95, 263
        self.x_max_theme_1_button, self.y_max_theme_1_button = 318, 433
        self.x_min_click_sound_button, self.y_min_click_sound_button = 672, 178
        self.x_max_click_sound_button, self.y_max_click_sound_button = 690, 196
        self.x_min_background_music_button, self.y_min_background_music_button = 709, 318
        self.x_max_background_music_button, self.y_max_background_music_button = 727, 336
        self.x_min_play_button, self.y_min_play_button = 64, 525
        self.x_max_play_button, self.y_max_play_button = 137, 549
        self.x_min_options_button, self.y_min_options_button = 237, 525
        self.x_max_options_button, self.y_max_options_button = 370, 549
        self.x_min_credits_button, self.y_min_credits_button = 638, 525
        self.x_max_credits_button, self.y_max_credits_button = 770, 549

        # Configure markers
        self.marker_click_sound_enable = 1
        self.marker_background_music_enable = 1
        self.marker_game_paused_page_enable = 0

        # Initialize updates
        self.notification.update_message_box()
        print(f"[__init__] Notification Bar updated")
        self.update_side_text()
        print(f"[__init__] Side text (All) updated")
        self.update_popup_text()
        print(f"[__init__] Popup text (All) updated")

        # Initial section end marker
        print(f"[__init__] --- Game initialization completed ---\n")

    def update_side_text(self):
        """
        Update the display text for current active player.

        Updates to show "YOUR TURN" or "COMPUTER'S TURN" based on side_status value.
        """
        if self.side_status == 0:
            self.side_text_box = "YOUR TURN"
            self.popup_side_changer_text_button = (
                self.popup_side_changer_text_button_player
            )

        elif self.side_status == 1:
            self.side_text_box = "COMPUTER'S TURN"
            self.popup_side_changer_text_button = (
                self.popup_side_changer_text_button_computer
            )

    def update_popup_text(self):
        """
        Update popup text for the latest player or computer action.

        Shows whether the last attempt was successful or not.
        """
        if self.side_status == 0:
            if self.player_answer_status == 0:
                self.popup_side_changer_text_player = (
                    "YOU ANSWERED UNSUCCESSFULLY (+1 CARD)"
                )
            elif self.player_answer_status == 1:
                self.popup_side_changer_text_player = "YOU ANSWERED SUCCESSFULLY"
            self.popup_side_changer_text = self.popup_side_changer_text_player
            print(f"[update_popup_text] Popup text (Player) updated")

        elif self.side_status == 1:
            if self.computer_answer_status == 0:
                self.popup_side_changer_text_computer = (
                    "COMPUTER ANSWERED UNSUCCESSFULLY (+1 CARD)"
                )
            elif self.computer_answer_status == 1:
                self.popup_side_changer_text_computer = (
                    "COMPUTER ANSWERED SUCCESSFULLY"
                )
            self.popup_side_changer_text = self.popup_side_changer_text_computer
            print(f"[update_popup_text] Popup text (Computer) updated")

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
            print(f"[add_penalty_card] Penalty card {penalty_card} generated")

            if self.side_status == 0:
                for i in range(1, 15):
                    if self.player_cards[i] == '':
                        self.player_cards[i] = penalty_card.upper()
                        print(f"[add_penalty_card] Penalty card is added to player's cards")
                        if i in self.used_card_positions:
                            self.used_card_positions.remove(i)
                        break
            return penalty_card

        else:
            print(f"[add_penalty_card] No remaining card in Deck.")
            return None

    def organize_cards(self):
        """
        Rearrange cards to fill empty spaces in the player's hand.

        Moves all non-empty cards forward to fill any gaps, maintaining
        their relative order. Updates the used card positions list and
        saves the previous state for potential rollback.
        """
        new_previous_cards = [''] * len(self.player_cards)
        non_empty_cards = []

        for i in range(len(self.player_cards)):
            if self.player_cards[i] != '' and i not in self.used_card_positions:
                non_empty_cards.append(self.player_cards[i])

        for i, card in enumerate(non_empty_cards):
            if i < len(new_previous_cards):
                new_previous_cards[i] = card

        self.player_cards = new_previous_cards
        self.used_card_positions = [
            i for i in range(len(self.player_cards))
            if i >= len(non_empty_cards) or self.player_cards[i] == ''
        ]
        self.previous_word_cards = self.word_cards.copy()
        self.previous_used_card_positions = self.used_card_positions.copy()

        print(f"[organize_cards] Cards (Player) organizing completed")
        print(f"[organize_cards] Current Cards (Player): {self.player_cards}")
        print(f"[organize_cards] Used Position (Player): {self.used_card_positions}")
        print(f"[organize_cards] Used Position (Player): {len(self.used_card_positions)}")

    def update_theme(self):
        """
        Update the game's visual theme based on current theme setting.

        Changes colors, backgrounds, and UI elements according to the
        selected theme (0 for default theme, other values for alternate theme).
        Affects text colors, popup styles, backgrounds, and page images.
        """
        if self.theme_setting == 0:

            # Color theme settings.
            self.color_text_coordinate = (33, 33, 33)
            self.color_text_timer = (33, 33, 33)
            self.color_popup_background = (188, 173, 119)
            self.color_popup_border = (33, 33, 33)
            self.color_popup_button = (33, 33, 33)
            self.color_popup_button_border = (33, 33, 33)
            self.color_popup_text = (188, 173, 119)
            self.color_popup_text_button = (33, 33, 33)
            self.color_text_side_box = (33, 33, 33)
            self.color_text_word = (33, 33, 33)
            self.color_text_cards = (33, 33, 33)
            self.color_text_selected_card = (240, 153, 31)
            self.color_text_round = (33, 33, 33)
            self.color_card_overlay = (33, 33, 33)
            self.color_point_block = (188, 173, 119)
            self.color_option_button = (188, 173, 119)

            if hasattr(self, 'notification'):
                self.notification.update_colors(
                    background_color=(188, 173, 119),
                    border_color=(33, 33, 33), text_color=(33, 33, 33)
                )

            # Page settings.
            self.image_welcome_page = self.image_welcome_page_0
            self.image_rules_page = self.image_rules_page_0
            self.image_options_page = self.image_options_page_0
            self.image_credits_page = self.image_credits_page_0
            self.image_current_background = self.image_background_0
            self.image_current_background_mute = self.image_background_mute_0
            self.image_player_first_page = self.image_player_first_0
            self.image_computer_first_page = self.image_computer_first_0
            self.image_game_paused_page = self.image_game_paused_page_0
            self.image_rules_main_page = self.image_rules_main_page_0
            self.image_victory_page = self.image_victory_page_0
            self.image_defeat_page = self.image_defeat_page_0
            self.image_remove_page = self.image_remove_page_0
            self.image_remove_mode_page = self.image_remove_page_mode_0

            # Audio settings.
            if self.sound_enabled:
                pygame.mixer.music.load(self.background_music_0)
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.3)

        elif self.theme_setting == 1:

            # Color settings
            self.color_text_coordinate = (0, 49, 82)
            self.color_text_timer = (228, 222, 215)
            self.color_popup_background = (228, 222, 215)
            self.color_popup_border = (0, 49, 82)
            self.color_popup_button = (0, 49, 82)
            self.color_popup_button_border = (0, 49, 82)
            self.color_popup_text = (228, 222, 215)
            self.color_popup_text_button = (0, 49, 82)
            self.color_text_side_box = (228, 222, 215)
            self.color_text_word = (228, 222, 215)
            self.color_text_cards = (0, 49, 82)
            self.color_text_selected_card = (240, 153, 31)
            self.color_text_round = (228, 222, 215)
            self.color_card_overlay = (0, 49, 82)
            self.color_point_block = (0, 49, 82)
            self.color_option_button = (0, 49, 82)

            if hasattr(self, 'notification'):
                self.notification.update_colors(
                    background_color=(228, 222, 215),
                    border_color=(0, 49, 82),
                    text_color=(0, 49, 82)
                )

            # Page settings.
            self.image_welcome_page = self.image_welcome_page_1
            self.image_rules_page = self.image_rules_page_1
            self.image_options_page = self.image_options_page_1
            self.image_credits_page = self.image_credits_page_1
            self.image_current_background = self.image_background_1
            self.image_current_background_mute = self.image_background_mute_1
            self.image_player_first_page = self.image_player_first_1
            self.image_computer_first_page = self.image_computer_first_1
            self.image_game_paused_page = self.image_game_paused_page_1
            self.image_rules_main_page = self.image_rules_main_page_1
            self.image_victory_page = self.image_victory_page_1
            self.image_defeat_page = self.image_defeat_page_1
            self.image_remove_page = self.image_remove_page_1
            self.image_remove_mode_page = self.image_remove_page_mode_1

            # Audio settings.
            if self.sound_enabled:
                pygame.mixer.music.load(self.background_music_1)
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.3)

    def draw_timer(self):
        """
        Draw the game timer.

        Displays remaining time on screen in "00:XX" format.
        """
        timer_text = self.font_timer.render(
            f"00:{self.timer_seconds:02d}", True, self.color_text_timer
        )
        self.screen.blit(timer_text, (self.timer_x, self.timer_y))

    def draw_points(self):
        """
        Draw the points blocks.

        Display current points using blue blocks arranged horizontally, maximum 8 blocks.
        Display from left to right, points reduction removes blocks from left to right.
        """
        for i in range(self.point_maximum):

            # Calculate block position
            x = self.point_block_x + i * (
                    self.point_block_length + self.point_block_spacing
            )
            rect = pygame.Rect(
                x, self.point_block_y,
                self.point_block_length, self.point_block_height
            )

            # Draw blocks.
            if i >= (self.point_maximum - (self.points - 1)):
                pygame.draw.rect(self.screen, self.color_point_block, rect)

    def draw_side_status(self):
        """
        Draw the current side status text box.

        Renders and displays the current player's turn status at the top of the screen.
        """
        text = self.font_default.render(
            self.side_text_box, True, self.color_text_side_box
        )
        self.screen.blit(
            text, (self.side_text_box_pos[0] - text.get_width() // 2,
                   self.side_text_box_pos[1])
        )

    def draw_word(self):
        """
        Draw the current word letters in the game.

        Renders each letter of the current word in the designated positions
        with proper centering and spacing.
        """
        for i, pos in enumerate(self.word_card_positions):
            letter_text = self.font_word.render(
                self.word_cards[i], True, self.color_text_word
            )
            text_x = pos[0] + 47 - letter_text.get_width() // 2
            text_y = pos[1] + 47 - letter_text.get_height() // 2
            self.screen.blit(letter_text, (text_x, text_y))

    def draw_cards(self):
        """
        Draw the card letters in a centered layout.

        Dynamically positions and renders available card letters:
            - Centers remaining cards based on total available space.
            - Excludes previously used cards from display.
            - Updates click areas for each visible card.
            - Maintains consistent spacing between cards.

        Card positions are calculated using:
            - Total screen width.
            - Number of unused cards.
            - Card width and spacing.
            - Historical card usage data.
        """
        for i, pos in enumerate(self.card_positions[:self.game_settings.MAX_CARDS]):

            # Only draw unused cards.
            if i not in self.used_card_positions:
                letter_text = self.font_cards.render(
                    self.player_cards[i], True, self.color_text_cards
                )
                text_x = pos[0] + 25 - letter_text.get_width() // 2
                text_y = pos[1] + 25 - letter_text.get_height() // 2
                self.screen.blit(letter_text, (text_x, text_y))

    def draw_selected_card(self):
        font = self.font_cards
        start_y = 443
        for i, letter in enumerate(self.selected_card):
            if isinstance(letter, tuple):
                position, letter = letter
                text_x = (
                        self.card_positions[position][0] + 25 - font.size(letter)[0] // 2
                )
            else:
                text_x = self.screen_width - 150 + i * 20

            letter_text = font.render(
                str(letter), True, self.color_text_selected_card
            )
            self.screen.blit(letter_text, (text_x, start_y))

    def draw_card_overlay(self):
        for i, pos in enumerate(self.card_positions[:self.game_settings.MAX_CARDS]):
            if i in self.used_card_positions:
                rect = pygame.Rect(pos[0], pos[1] - 10, 49, 70)
                pygame.draw.rect(self.screen, self.color_card_overlay, rect)

    def draw_coordinate_display(self):
        """
        Draw mouse coordinate display.

        Shows the current X and Y coordinates of the mouse cursor
        in the top-left corner of the screen.
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        text = self.font_default.render(
            f"X: {mouse_x}, Y: {mouse_y}", True, self.color_text_coordinate
        )
        text_rect = text.get_rect()
        text_rect.topleft = (650, 0)
        self.screen.blit(text, text_rect)

    def draw_popup(self):
        """
        Draw the side change popup.

        Creates a semi-transparent overlay and displays a popup message
        when the active player changes, with an OK button to dismiss.
        """
        s = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))
        self.screen.blit(s, (0, 0))

        pygame.draw.rect(
            self.screen, self.color_popup_background, self.popup_rect
        )
        pygame.draw.rect(
            self.screen, self.color_popup_border, self.popup_rect, 5
        )
        popup_text_render = self.font_default.render(
            self.popup_side_changer_text, True, self.color_popup_text_button
        )
        self.screen.blit(
            popup_text_render,
            (
                self.popup_rect.centerx - popup_text_render.get_width() // 2,
                self.popup_rect.centery - 40)
        )
        pygame.draw.rect(
            self.screen, self.color_popup_button, self.popup_button_rect
        )
        pygame.draw.rect(
            self.screen, self.color_popup_button_border, self.popup_button_rect, 2
        )
        button_text_render = self.font_default.render(
            self.popup_side_changer_text_button, True, self.color_popup_text
        )
        self.screen.blit(
            button_text_render,
        (
            self.popup_button_rect.centerx - button_text_render.get_width() // 2,
            self.popup_button_rect.centery - button_text_render.get_height() // 2
            )
        )

    def draw_popup_remove(self):
        """
        Draw the remove mode popup.

        Same content as above.
        """
        s = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))
        self.screen.blit(s, (0, 0))

        pygame.draw.rect(
            self.screen, self.color_popup_background, self.popup_remove_rect
        )
        pygame.draw.rect(
            self.screen, self.color_popup_border, self.popup_remove_rect, 5
        )

        popup_text_render = self.font_default.render(
            self.popup_remove_text, True, self.color_popup_text_button
        )
        self.screen.blit(
            popup_text_render,
            (
                self.popup_remove_rect.centerx - popup_text_render.get_width() // 2,
                self.popup_remove_rect.centery - 40
            )
        )

        pygame.draw.rect(
            self.screen, self.color_popup_button, self.popup_remove_yes_button_rect
        )
        pygame.draw.rect(
            self.screen, self.color_popup_button_border,
            self.popup_remove_yes_button_rect, 2
        )

        yes_text_render = self.font_default.render(
            self.popup_remove_text_yes, True, self.color_popup_text
        )
        self.screen.blit(
            yes_text_render,
            (
                self.popup_remove_yes_button_rect.centerx - yes_text_render.get_width() // 2,
                self.popup_remove_yes_button_rect.centery - yes_text_render.get_height() // 2
            )
        )

        pygame.draw.rect(
            self.screen, self.color_popup_button, self.popup_remove_no_button_rect
        )
        pygame.draw.rect(
            self.screen, self.color_popup_button_border,
            self.popup_remove_no_button_rect, 2
        )

        no_text_render = self.font_default.render(
            self.popup_remove_text_no, True, self.color_popup_text
        )
        self.screen.blit(
            no_text_render,
            (
                self.popup_remove_no_button_rect.centerx - no_text_render.get_width() // 2,
                self.popup_remove_no_button_rect.centery - no_text_render.get_height() // 2
            )
        )

    def draw_popup_bot_difficulty(self):
        """
        Draw the bot difficulty selection popup.

        Displays a popup with three difficulty options: EASY, MEDIUM, HARD.
        """
        s = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))
        self.screen.blit(s, (0, 0))

        pygame.draw.rect(
            self.screen, self.color_popup_background, self.popup_bot_difficulty_rect
        )
        pygame.draw.rect(
            self.screen, self.color_popup_border, self.popup_bot_difficulty_rect, 5
        )

        popup_text_render = self.font_default.render(
            "GAME DIFFICULTY SELECTION", True, self.color_popup_text_button
        )
        self.screen.blit(
            popup_text_render,
            (
                self.popup_bot_difficulty_rect.centerx - popup_text_render.get_width() // 2,
                self.popup_bot_difficulty_rect.centery - 40
            )
        )

        for button, text in [
            (self.popup_bot_difficulty_easy_button_rect, "EASY"),
            (self.popup_bot_difficulty_medium_button_rect, "MEDIUM"),
            (self.popup_bot_difficulty_hard_button_rect, "HARD")
        ]:
            pygame.draw.rect(self.screen, self.color_popup_button, button)
            pygame.draw.rect(
                self.screen, self.color_popup_button_border, button, 2
            )
            button_text = self.font_default.render(
                text, True, self.color_popup_text
            )
            text_rect = button_text.get_rect(center=button.center)
            self.screen.blit(button_text, text_rect)

    def handle_bot_turn(self):
        if self.side_status == 1 and not self.game_paused:
            current_word = "".join(self.word_cards).lower()
            print(f"[handle_bot_turn] Current Word: {str(current_word).upper()}")

            bot_output = self.bot.play_turn(current_word, self.timer_seconds)

            match bot_output:
                case self.bot.Output.THINKING:
                    print(f"[handle_bot_turn] Bot Output: {bot_output}")
                    print(f"[handle_bot_turn] Cards (Computer): {self.bot.cards}")
                    print(f"[handle_bot_turn] Will Computer answer: {self.bot.current_turn_will_answer_or_not}")
                    print(f"[handle_bot_turn] Next Word: {self.bot.current_turn_answer}")
                    print(f"[handle_bot_turn] Answer Time: {self.bot.current_turn_answer_time}")
                    print(f"[handle_bot_turn] Ran Initial Code: {self.bot.ran_current_turn_code}\n")
                    return

                case _:
                    computer_answer, computer_used_card = bot_output
                    self.word_cards = list(computer_answer.upper())
                    print(f"[handle_bot_turn] {bot_output} answered")
                    print(f"[handle_bot_turn] Computer Used Card:", computer_used_card)

                    if computer_answer and computer_used_card:
                        if computer_used_card in self.bot.cards:
                            self.bot.cards.remove(computer_used_card)
                            print(f"[handle_bot_turn] Card {computer_used_card} removed from Computer's Cards")
                            print(f"[handle_bot_turn] Computer Cards (after removed Used Card): {self.bot.cards}")
                        self.deck.append(computer_used_card)
                        print(f"[handle_bot_turn] Card {computer_used_card} returned to Deck")

                    self.timer_seconds = 0

                    if self.computer_points == 3:
                        self.bot.discard_card()
                        print(f"[handle_bot_turn] Computer discarded a Card")

                    return

    def handle_button_click(self, mouse_x, mouse_y):
        """
        Handle all button click events.

        Parameters:
            mouse_x (int): X coordinate of mouse click.
            mouse_y (int): Y coordinate of mouse click.

        Returns:
            bool: False if quit button is clicked, True otherwise.

        Processes clicks on:
            - Welcome page and story pages.
            - Back button.
            - Rules button.
            - Quit button.
            - Game_Paused button.
            - Confirm button.
            - Sound toggle button.
            - Remove button (developing).
        """
        if (self.x_min_theme_0_button <= mouse_x <= self.x_max_theme_0_button and
                self.y_min_theme_0_button <= mouse_y <= self.y_max_theme_0_button):
            if (pygame.mouse.get_pressed()[0] and self.show_options_page and
                    self.theme_setting == 1):
                self.button_sound.play()
                print(f"[handle_button_click] Button (Theme-0) was clicked")
                self.theme_setting = 0
                self.update_theme()

            elif (pygame.mouse.get_pressed()[0] and self.show_options_page and
                  self.theme_setting == 0):
                self.button_sound.play()
                pass

        if (self.x_min_theme_1_button <= mouse_x <= self.x_max_theme_1_button and
                self.y_min_theme_1_button <= mouse_y <= self.y_max_theme_1_button):
            if (pygame.mouse.get_pressed()[0] and self.show_options_page and
                    self.theme_setting == 0):
                self.button_sound.play()
                self.theme_setting = 1
                self.update_theme()
                print(f"[handle_button_click] Button (Theme-1) was clicked")

            elif (pygame.mouse.get_pressed()[0] and self.show_options_page and
                  self.theme_setting == 1):
                self.button_sound.play()
                pass

        # Click sound button.
        if self.x_min_click_sound_button <= mouse_x <= self.x_max_click_sound_button and self.y_min_click_sound_button <= mouse_y <= self.y_max_click_sound_button:
            if pygame.mouse.get_pressed()[0] and self.show_options_page:
                self.button_sound.play()
                self.options_click_sound = 1 - self.options_click_sound
                if self.options_click_sound == 1:
                    self.button_sound.set_volume(1.0)

                elif self.options_click_sound == 0:
                    self.button_sound.set_volume(0.0)

                print(f"[handle_button_click] Button (Button-click sound) was clicked")

        # Background_Music_Button
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

                print(f"[handle_button_click] Button (Background Music) was clicked")

        # Quit_Button
        if self.x_min_quit_button <= mouse_x <= self.x_max_quit_button and self.y_min_quit_button <= mouse_y <= self.y_max_quit_button and not (self.show_welcome_page or self.show_rules_page or self.show_options_page or self.show_credits_page or self.show_computer_first_page or self.show_player_first_page or self.show_remove_page or self.show_remove_page_mode or self.show_victory_page or self.show_defeat_page or self.show_rules_main_page):
            if pygame.mouse.get_pressed()[0]:
                self.button_sound.play()
                print(f"[handle_button_click] Button (Quit) was clicked")
                return False

        # Confirm_Button
        if self.x_min_confirm_button <= mouse_x <= self.x_max_confirm_button and self.y_min_confirm_button <= mouse_y <= self.y_max_confirm_button:
            if pygame.mouse.get_pressed()[0] and self.side_status == 0 and not (self.show_welcome_page or self.show_rules_page or self.show_options_page or self.show_credits_page or self.show_computer_first_page or self.show_player_first_page):
                self.button_sound.play()
                self.timer_seconds = 0

            elif pygame.mouse.get_pressed()[0] and self.show_game_paused_page:
                self.button_sound.play()
                print(f"[handle_button_click] Button (Restart) was clicked")
                python = sys.executable
                script = os.path.abspath(__file__)
                os.execv(python, [python, script])

        # Sound_Button
        if self.x_min_sound_button <= mouse_x <= self.x_max_sound_button and self.y_min_sound_button <= mouse_y <= self.y_max_sound_button and not (self.show_welcome_page or self.show_rules_page or self.show_options_page or self.show_credits_page or self.show_computer_first_page or self.show_player_first_page or self.show_rules_main_page):
            if pygame.mouse.get_pressed()[0]:
                self.button_sound.play()
                if self.sound_enabled:
                    pygame.mixer.music.set_volume(0.0)
                    self.sound_enabled = False
                    if self.theme_setting == 0:
                        self.image_current_background = self.image_background_mute_0

                    elif self.theme_setting == 1:
                        self.image_current_background = self.image_background_mute_1
                else:
                    pygame.mixer.music.set_volume(0.3)

                    self.sound_enabled = True
                    if self.theme_setting == 0:
                        self.image_current_background = self.image_background_0
                    elif self.theme_setting == 1:
                        self.image_current_background = self.image_background_1
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
            self.game_paused = True
            pygame.time.set_timer(self.timer_event, 0)
            print(f"[check_victory_condition] Game status: Victory")
            return True
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
            self.game_paused = True
            pygame.time.set_timer(self.timer_event, 0)
            print(f"[check_failure_condition] Game status: Defeat")
            return True
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
                        self.selected_card = [(i, self.player_cards[i])]
                        self.show_popup_remove = True
                        return True
            return False

        if self.side_status != 0 or self.game_paused:
            return

        for i, (x, y, width, height) in enumerate(self.card_click_areas):
            if x <= mouse_x <= x + width and y <= mouse_y <= y + height:
                if i not in self.used_card_positions:
                    selected_card = self.player_cards[i]
                    self.selected_card = [(i, selected_card)]
                    print(f"[handle_card_click] Selected Card: {selected_card}")
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
                        card_position, previous_card = self.selected_card[0]
                        current_card = self.word_cards[i]

                        if i in self.replaced_positions:
                            print(f"[handle_word_click] Position {i} has already been replaced and cannot be replaced again")
                            return False

                        # Check if the letters are the same as those in the original word
                        if previous_card.lower() == self.previous_word_cards[i].lower():
                            print(f"[handle_word_click] Cannot replace same card：{previous_card}")
                            self.notification.show_message_box("CANNOT SWAP SAME CARD")
                            return False

                        if current_card == previous_card:
                            print(f"[handle_word_click] Cannot replace same card: {previous_card} ")
                            self.notification.show_message_box("CANNOT SWAP SAME CARD")
                            self.selected_card = []
                            return True

                        # Handle_Previous_Swap
                        elif self.last_swapped_position is not None:
                            # Same_Position_Swap
                            if self.last_swapped_position == i:
                                if self.used_card_positions:
                                    last_card_position = self.used_card_positions.pop()
                                    print(f"[handle_word_click] Restored Previous Card at Position {last_card_position}")

                            # Different_Position_Swap
                            else:
                                self.word_cards[self.last_swapped_position] = self.original_cards[
                                    self.last_swapped_position]
                                if self.used_card_positions:
                                    last_card_position = self.used_card_positions.pop()
                                    print(f"[handle_word_click] Restored Card at Position {last_card_position}")
                                print(f"[handle_word_click] Restored Position {self.last_swapped_position} to {self.original_cards[self.last_swapped_position]}")

                        # Store_original_cards
                        elif not self.original_cards:
                            self.original_cards = self.word_cards.copy()

                        # Update_Current_Word
                        self.word_cards[i] = previous_card
                        print(f"[handle_word_click] Card Swap confirmation: {current_card} -> {previous_card}")
                        print(f"[handle_word_click] Current Word: {''.join(self.word_cards)}")

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
        current_word_str = ''.join(self.word_cards).lower()
        if self.logic.check_exists(current_word_str):
            if self.side_status == 0:
                self.player_answer_status = 1
                self.notification.show_message_box("VALID WORD")
                replaced_card = None
                for i, card in enumerate(self.word_cards):
                    if card != self.previous_word_cards[i]:
                        replaced_card = card
                        print(f"[check_word_validity] Player's Used Card: {card}")
                        self.deck.append(card.lower())
                        print(f"[check_word_validity] {card} returned to deck")
                self.previous_word_cards = self.word_cards.copy()
                self.previous_used_card_positions = self.used_card_positions.copy()
                print(f"[check_word_validity] Answer checked (Player): {self.player_answer_status}")

            elif self.side_status == 1:
                if self.bot.current_turn_will_answer_or_not:
                    if not self.bot.current_turn_answer == None:
                        self.computer_answer_status = 1
                        print(f"[check_word_validity] Answer checked (Computer answered and not NONE): {self.computer_answer_status}")
                        self.notification.show_message_box("VALID WORD")

                    else:
                        self.computer_answer_status = 0
                        print(f"[check_word_validity] Answer checked (Computer answered but NONE): {self.computer_answer_status}")
                        new_card = self.deck.pop()
                        self.bot.add_card(new_card)
                        print(f"[handle_bot_turn] Computer got a penalty card: {new_card}")
                        self.notification.show_message_box("NO WORD CHANGED")

                else:
                    self.computer_answer_status = 0
                    print(f"[check_word_validity] Answer checked (Computer did not answer): {self.computer_answer_status}")
                    new_card = self.deck.pop()
                    self.bot.add_card(new_card)
                    print(f"[handle_bot_turn] Computer got a penalty card: {new_card}")
                    self.notification.show_message_box("NO WORD CHANGED")

        else:
            if self.side_status == 0:
                self.player_answer_status = 0
                self.notification.show_message_box("INVALID WORD")
                self.word_cards = self.previous_word_cards.copy()
                self.used_card_positions = self.previous_used_card_positions.copy()
                print(f"[check_word_validity] Answer Checked (Player): {self.player_answer_status}")

            elif self.side_status == 1:
                self.computer_answer_status = 0
                print(f"[check_word_validity] Answer checked (Computer): {self.computer_answer_status}")

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
                print(f"[handle_timer_event] Current Word:", self.word_cards)
                print(f"[handle_timer_event] Previous Word:", self.previous_word_cards)
                if not self.show_remove_page and not self.show_remove_page_mode:
                    if self.word_cards == self.previous_word_cards:
                        print(f"[handle_timer_event] No Word changed")
                        print(f"[handle_timer_event] Answer Checked (Player did not change Word): {self.player_answer_status}")
                        self.notification.show_message_box("NO WORD CHANGED")
                        self.player_answer_status = 0
                        self.add_penalty_card()
                        self.update_side_text()
                        self.update_popup_text()
                        pass

                    else:
                        print(f"[handle_timer_event] Word changed")
                        self.check_word_validity()
                        print(f"[handle_timer_event] Word Validity checked")
                        self.update_side_text()
                        if self.player_answer_status == 1:
                            self.points += 1
                            print(f"[handle_timer_event] Points (Player) added one")
                            print(f"[handle_timer_event] Points (Player): {self.points}")

                        elif self.player_answer_status == 0:
                            self.add_penalty_card()
                        self.update_popup_text()
                        print(f"[handle_timer_event] Popup Text (All) Updated.")

            elif self.side_status == 1:
                self.check_word_validity()
                self.update_popup_text()
                print(f"[handle_timer_event] Popup Text (All) Updated.")
                self.update_side_text()
                if self.computer_answer_status == 1:
                    self.computer_points += 1
                    print(f"[handle_timer_event] Points (Computer) added one")
                    print(f"[handle_timer_event] Points (Computer): {self.computer_points}")
                self.bot.end_turn()
            print(f"[handle_timer_event] Side Status (Player-0 Computer-1): {self.side_status}")
            print(f"[handle_timer_event] Player's answer status (Invalid-0 Valid-1): {self.player_answer_status}")
            print(f"[handle_timer_event] Computer's answer status (Invalid-0 Valid-1): {self.computer_answer_status}")
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
                print(f"[handle_timer_event] --- Remove Mode Enables ---")
                print(f"[handle_timer_event] Remove Mode: Enable")

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
            if self.popup_button_rect.collidepoint(pos):
                self.button_sound.play()
                self.organize_cards()
                self.update_side_text()

                #Shuffle the deck
                print(f"[handle_popup_click] Deck (before shuffled): {self.deck}")
                self.deck = self.logic.fisher_shuffle(self.deck)
                print(f"[handle_popup_click] Deck (after shuffled): {self.deck}")

                #Sort player cards
                valid_cards = []
                valid_positions = []
                for i in range(len(self.player_cards)):
                    if self.player_cards[i] and i not in self.used_card_positions:
                        valid_cards.append(self.player_cards[i])
                        valid_positions.append(i)
                self.logic.quicksort(valid_cards)
                for i, pos in enumerate(valid_positions):
                    self.player_cards[pos] = valid_cards[i]
                print(f"[handle_popup_click] Player's cards have been sorted: {valid_cards}")

                self.show_popup = False
                self.game_paused = False
                self.show_remove_page = False
                self.show_remove_page_mode = False
                self.round_counter_popup_click_count += 1
                self.round = math.floor(self.round_counter_popup_click_count / 2)

                if '*' in self.word_cards:
                    self.star_card_active = True

                # If the star card is activated, generate new word
                if self.star_card_active:
                    self.word = self.logic.word_generator().upper()
                    self.word_cards = list(self.word)
                    self.previous_word_cards = self.word_cards.copy()
                    self.star_card_active = False
                    print(f"[handle_popup_click] New word generated ('*' Card): {self.word}")

                self.replaced_positions.clear()
                if self.side_status == 0:
                    print(f"[handle_popup_click] --- Computer's Turn Ends ---\n")
                    print(f"\n[handle_popup_click] --- Player's Turn Starts ---")
                    print(f"[handle_popup_click] Current Round {self.round_counter_popup_click_count / 2}")
                    print(f"[handle_popup_click] Current Points: {self.points}")

                else:
                    print(f"[handle_popup_click] --- Player's Turn Ends ---\n")
                    print(f"[handle_popup_click] --- Computer's Turn Starts ---")
                
                pygame.time.set_timer(self.timer_event, 1000)

        elif self.show_popup_remove:
            mouse_x, mouse_y = pos
            if self.popup_remove_yes_button_rect.collidepoint(mouse_x, mouse_y):
                if pygame.mouse.get_pressed()[0]:
                    self.button_sound.play()
                    self.side_status = 0
                    print(f"[handle_popup_click] Removal Successful\n[handle_popup_click] Remove Mode: Disable")
                    print(f"[handle_popup_click] --- Remove Mode Disables ---")
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

            elif self.popup_remove_no_button_rect.collidepoint(mouse_x, mouse_y):
                if pygame.mouse.get_pressed()[0]:
                    self.button_sound.play()
                    print(f"[handle_popup_click] Removal canceled")
                    self.show_popup_remove = False
                    pygame.time.set_timer(self.timer_event, 0)
                    return True

        elif self.show_popup_bot_difficulty:
            mouse_x, mouse_y = pos
            if self.popup_bot_difficulty_easy_button_rect.collidepoint(mouse_x, mouse_y):
                self.button_sound.play()
                self.bot = Bot(Bot.Difficulty.EASY, self.bot.cards)
                self.show_popup_bot_difficulty = False
                print(f"[handle_popup_click] Computer Difficulty EASY")

            elif self.popup_bot_difficulty_medium_button_rect.collidepoint(mouse_x, mouse_y):
                self.button_sound.play()
                self.bot = Bot(Bot.Difficulty.MEDIUM, self.bot.cards)
                self.show_popup_bot_difficulty = False
                print(f"[handle_popup_click] Computer Difficulty MEDIUM")

            elif self.popup_bot_difficulty_hard_button_rect.collidepoint(mouse_x, mouse_y):
                self.button_sound.play()
                self.bot = Bot(Bot.Difficulty.HARD, self.bot.cards)
                self.show_popup_bot_difficulty = False
                print(f"[handle_popup_click] Computer Difficulty HARD")
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
                    pygame.quit()
                    sys.exit()

                #Card Click event
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
                                self.show_player_first_page = True
                                #self.notification.show_message_box("THE COIN IS HEAD")
                                self.show_computer_first_page = False
                                valid_cards = []
                                valid_positions = []
                                for i in range(len(self.player_cards)):
                                    if self.player_cards[i] and i not in self.used_card_positions:
                                        valid_cards.append(self.player_cards[i])
                                        valid_positions.append(i)
                                self.logic.quicksort(valid_cards)
                                for i, pos in enumerate(valid_positions):
                                    self.player_cards[pos] = valid_cards[i]
                                print(f"[handle_events] Player's cards have been sorted: {valid_cards}")

                            elif self.side_status == 1:
                                self.show_player_first_page = False
                                self.show_computer_first_page = True
                                #self.notification.show_message_box("THE COIN IS TAIL")

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
                elif (self.show_computer_first_page or self.show_player_first_page) and not self.show_popup_bot_difficulty:
                    self.button_sound.play()
                    self.show_computer_first_page = False
                    self.show_player_first_page = False
                    if self.side_status == 0:
                        print(f"[handle_events] --- Player's Turn Starts ---")
                    elif self.side_status == 1:
                        print(f"[handle_events] --- Computer's Turn Starts ---")
                    pygame.time.set_timer(self.timer_event, 1000)

                elif not (self.show_welcome_page or self.show_rules_page or self.show_options_page or self.show_credits_page) and self.x_min_game_paused_page <= mouse_x <= self.x_max_game_paused_page and self.y_min_game_paused_page <= mouse_y <= self.y_max_game_paused_page:
                    if not self.show_game_paused_page and not (
                            self.show_computer_first_page and self.show_player_first_page) and not self.show_rules_main_page:
                        self.button_sound.play()
                        self.game_paused = True
                        self.show_game_paused_page = True
                        print(f"[handle_events] Game Paused")
                        pygame.time.set_timer(self.timer_event, 0)

                    elif self.show_rules_main_page and not self.show_game_paused_page:
                        self.button_sound.play()
                        self.show_rules_main_page = False
                        pygame.time.set_timer(self.timer_event, 1000)

                    elif self.show_game_paused_page:
                        self.button_sound.play()
                        self.game_paused = False
                        self.show_game_paused_page = False
                        print(f"[handle_events] Game Unpaused")
                        pygame.time.set_timer(self.timer_event, 1000)

                elif self.show_game_paused_page and self.x_min_rules_main_button <= mouse_x <= self.x_max_rules_main_button and self.y_min_rules_main_button <= mouse_y <= self.y_max_rules_main_button:
                    self.button_sound.play()
                    self.show_rules_main_page = True
                    self.show_game_paused_page = False
                    self.marker_game_paused_page_enable = 1
                    pygame.time.set_timer(self.timer_event, 0)

                elif not (self.show_welcome_page or self.show_rules_page or self.show_options_page or self.show_credits_page):
                    if self.x_min_rules_main_button <= mouse_x <= self.x_max_rules_main_button and self.y_min_rules_main_button <= mouse_y <= self.y_max_rules_main_button and not self.show_rules_page:
                        self.button_sound.play()
                        self.show_rules_main_page = True
                        self.show_game_paused_page = False
                        pygame.time.set_timer(self.timer_event, 0)

                    elif self.show_rules_main_page:
                        if self.marker_game_paused_page_enable == 1:
                            self.button_sound.play()
                            self.show_rules_main_page = False
                            self.show_game_paused_page = True
                            self.marker_game_paused_page_enable = 0
                            pygame.time.set_timer(self.timer_event, 0)

                        else:
                            self.button_sound.play()
                            self.show_rules_main_page = False
                            pygame.time.set_timer(self.timer_event, 1000)

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
        round_text = self.font_round.render(str(self.round), True, self.color_text_round)
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
            self.screen.blit(self.image_current_background, (0, 0))

        elif not self.sound_enabled:
            self.screen.blit(self.image_current_background_mute, (0, 0))
        self.draw_timer()
        self.draw_side_status()

        #self.draw_coordinate_display()
        if not self.show_popup:
            self.draw_word()
            self.draw_cards()
            if self.side_status == 0:
                self.draw_selected_card()

        
        self.draw_round_counter()
        self.draw_card_overlay()
        self.draw_points()
        self.notification.update_message_box()

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

        if self.show_player_first_page:
            self.screen.blit(self.image_player_first_page, (0, 0))

        if self.show_computer_first_page:
            self.screen.blit(self.image_computer_first_page, (0, 0))

        if self.show_options_page:
            self.screen.blit(self.image_options_page, (0, 0))
            if self.options_click_sound == 1:
                self.marker_click_sound_enable = 1
                pygame.draw.rect(self.screen, self.color_option_button, self.options_box1_rect)

            else:
                self.marker_click_sound_enable = 0

            if self.options_background_music == 1:
                self.marker_background_music_enable = 1
                pygame.draw.rect(self.screen, self.color_option_button, self.options_box2_rect)

            else:
                self.marker_background_music_enable = 0

        if self.show_remove_page_mode:
            self.screen.blit(self.image_remove_mode_page, (0, 0))

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

        self.notification.draw_message_box(self.screen, self.font_default)

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