
#Instructions for Reserved Interface：
    #1. For is_one_letter_dif in GameFunction.py, I have created a code in the UI that only allows the replacement of one word, which may have the possibility of duplication or conflict
        #1.1 My code allows:
            #1.1.1 Only different letters can be replaced
            #1.1.2 Before replacing letters, the selected letter will be checked to see if it is the same as the letter in the target position.
            #1.1.3 If it is the same letter, the selection will be canceled and a prompt message will be output.
    #2. For check_exists in GameFunction.py, I have reserved a variable called 'current word' to display the words after each round ends
        #2.1 In terminal output, the output format is: "Round X ended. Current word: XXX"
    #3. For word_generater in GameFunction.py, self.current_word_letters provides a list to store the Current_Word, which can be connected to the GameFunction.py.
    #4. For card in GameFunction.py, self.card_letter_1 to self.card_letter_15 are created to store the letters of the cards.

#The Function I am still developing:
    #1. Prepare to connect bot_function-py.
    #2. Points function and card removal function (Done).
    #3. Card centering and dynamic quantity of cards (Done).
    #4. Star Card.

#Things need attention:
    #1. My UI interaction is based on detecting whether there are clicks within a specified coordinate range.
    #2. The order of element drawing should not be changed without testing fully.

#Import libraries
import pygame
import sys
import os

class CardGameUI:
    """
    Card Game User Interface Class

    This class manages the game's graphical interface, event handling, and game states.
    Contains all visual elements, audio controls, and interaction logic.

    Attributes:
        screen_width (int): Game window width
        screen_height (int): Game window height
        show_popup (bool): Whether to show popup
        game_paused (bool): Whether game is paused
        current_round (int): Current round number
        side_status (int): Current active player (0 for player, 1 for computer)
    """

    def __init__(self):
        #Initialize Pygame
        pygame.init()
        pygame.mixer.init()

        #Config_Settings
        self.show_popup = False
        self.game_paused = False
        self.show_welcome_page = True
        self.show_game_paused_page = False
        self.show_rules_page = False

        #Config_Screen
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Debug Mode")

        #Config_Coordinate_Box
        self.text_color_coordinate = (0, 49, 82)

        #Config_Background
        self.background = pygame.image.load("data/image/background.png")
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        self.background_mute = pygame.image.load("data/image/background_mute.png")
        self.background_mute = pygame.transform.scale(self.background_mute, (self.screen_width, self.screen_height))
        self.current_background = self.background

        #Config_Welcome_Page
        self.image_welcome_page = pygame.image.load("data/image/welcome_page.png")
        self.image_welcome_page = pygame.transform.scale(self.image_welcome_page,
                                                         (self.screen_width, self.screen_height))

        #Config_Story_Pages
        self.current_story_page = 0
        self.story_images = []
        for i in range(6):
            image = pygame.image.load(f"data/image/story_{i}.png")
            image = pygame.transform.scale(image, (self.screen_width, self.screen_height))
            self.story_images.append(image)

        #Config_Pause_Page
        self.image_game_paused_page = pygame.image.load("data/image/game_paused_page.png")
        self.image_game_paused_page = pygame.transform.scale(self.image_game_paused_page,
                                                             (self.screen_width, self.screen_height))

        #Config_Rules_Page
        self.image_rules_page = pygame.image.load("data/image/rules_page.png")
        self.image_rules_page = pygame.transform.scale(self.image_rules_page, (self.screen_width, self.screen_height))

        #Config_Win_Lose_Page
        self.image_win_page = pygame.image.load("data/image/win_page.png")
        self.image_win_page = pygame.transform.scale(self.image_win_page, (self.screen_width, self.screen_height))
        self.image_lose_page = pygame.image.load("data/image/lose_page.png")
        self.image_lose_page = pygame.transform.scale(self.image_lose_page, (self.screen_width, self.screen_height))

        #Config_Remove_Page
        self.image_remove_page = pygame.image.load("data/image/remove_page.png")
        self.image_remove_page = pygame.transform.scale(self.image_remove_page, (self.screen_width, self.screen_height))

        #Config_Font
        self.font_size_default = 24
        self.font_size_timer = 88
        self.font_size_round = 34
        self.card_font_size = 52
        self.font_default = pygame.font.Font("data/font/AaHuanMengKongJianXiangSuTi-2.ttf", self.font_size_default)
        self.font_timer = pygame.font.Font("data/font/AaHuanMengKongJianXiangSuTi-2.ttf", self.font_size_timer)
        self.font_round = pygame.font.Font("data/font/AaHuanMengKongJianXiangSuTi-2.ttf", self.font_size_round)
        self.card_font = pygame.font.Font("data/font/AaHuanMengKongJianXiangSuTi-2.ttf", self.card_font_size)

        #Config_Timer
        self.timer_event = pygame.USEREVENT + 1
        self.timer_duration = 15
        self.timer_seconds = self.timer_duration
        self.timer_x = 301
        self.timer_y = 248
        self.text_color_timer = (228, 222, 215)
        pygame.time.set_timer(self.timer_event, 1000)

        #Config_Popup
        self.popup_side_changer_width = 350
        self.popup_side_changer_height = 150
        self.popup_side_changer_width_button = 100
        self.popup_side_changer_height_button = 30
        self.popup_side_changer_pos_x = self.screen_width // 2 - self.popup_side_changer_width // 2
        self.popup_side_changer_pos_y = self.screen_width // 2 - self.popup_side_changer_height // 2
        self.popup_side_changer_pos_x_button = self.screen_width // 2 - self.popup_side_changer_width_button // 2
        self.popup_side_changer_pos_y_button = self.screen_width // 2 + 25
        self.popup_side_changer_color_background = (228, 222, 215)
        self.popup_side_changer_color_border = (228, 222, 215)
        self.popup_side_changer_color_button = (0, 49, 82)
        self.popup_side_changer_color_button_border = (0, 49, 82)
        self.popup_side_changer_color_text = (228, 222, 215)
        self.popup_side_changer_color_text_button = (0, 49, 82)
        self.popup_side_changer_text = "Side has changed"
        self.popup_side_changer_text_button = "OK"
        self.popup_rect = pygame.Rect(self.screen_width // 2 - 150, self.screen_height // 2 - 75, 300, 150)
        self.button_rect = pygame.Rect(self.screen_width // 2 - 50, self.screen_height // 2 + 25, 100, 30)

        #Config_Rmover_Popup
        self.popup_remove_width = 350
        self.popup_remove_height = 150
        self.popup_remove_width_button = 100
        self.popup_remove_height_button = 30
        self.popup_remove_pos_x = self.screen_width // 2 - self.popup_remove_width // 2
        self.popup_remove_pos_y = self.screen_width // 2 - self.popup_remove_height // 2
        self.popup_remove_pos_x_button = self.screen_width // 2 - self.popup_remove_width_button // 2
        self.popup_remove_pos_y_button = self.screen_width // 2 + 25
        self.popup_remove_color_background = (228, 222, 215)
        self.popup_remove_color_border = (228, 222, 215)
        self.popup_remove_color_button = (0, 49, 82)
        self.popup_remove_color_button_border = (0, 49, 82)
        self.popup_remove_color_text = (228, 222, 215)
        self.popup_remove_color_text_button = (0, 49, 82)
        self.popup_remove_text = "Already used"
        self.popup_remove_text_button = "OK"
        self.remove_popup_rect = pygame.Rect(self.screen_width // 2 - 150, self.screen_height // 2 - 75, 300, 150)
        self.remove_button_rect = pygame.Rect(self.screen_width // 2 - 50, self.screen_height // 2 + 25, 100, 30)

        #Config_Side_Status
        self.side_status = 0
        self.update_side_text()
        self.side_text_box_pos = (self.screen_width // 2, 5)
        self.side_text_box_color = (228, 222, 215)

        #Config_Current_Word
        self.current_word_font_size = 88
        self.current_word_font = pygame.font.Font("data/font/AaHuanMengKongJianXiangSuTi-2.ttf",
                                                  self.current_word_font_size)
        self.current_word_letters = ['C', 'A', 'T']
        self.current_word_text_color = (228, 222, 215)
        self.current_word_positions = []
        current_word_start_x = 256
        current_word_width = 95
        current_word_spacing = 5
        current_word_y = 110
        self.current_word_click_areas = []
        self.selected_current_word_letters = []
        for i in range(3):
            self.current_word_positions.append(
                (current_word_start_x + i * (current_word_width + current_word_spacing), current_word_y))
        for i in range(3):
            x = current_word_start_x + i * (current_word_width + current_word_spacing)
            y = current_word_y
            self.current_word_click_areas.append((x, y, current_word_width, current_word_width))

        #Config_Card_Letters
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
        self.card_text_color = (228, 222, 215)
        self.card_positions = []
        card_start_x = 28
        card_width = 49
        card_spacing = 1
        card_y = 449
        for i in range(15):
            self.card_positions.append((card_start_x + i * (card_width + card_spacing), card_y))

        #Config_Card_Clickers
        self.card_click_areas = []
        for i in range(15):
            x = card_start_x + i * (card_width + card_spacing)
            y = card_y
            self.card_click_areas.append((x, y, card_width, card_width))

        #Config_Selected_Letters
        self.selected_letters = []
        self.last_swapped_position = None
        self.original_letters = []
        self.used_card_positions = []

        #Config_Used_Cards_History
        self.used_cards_history = {}

        #Config_Sound
        pygame.mixer.music.load("data/sound/background_music.wav")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        self.button_sound = pygame.mixer.Sound("data/sound/button_sound.wav")
        self.sound_enabled = True

        #Config_Points
        self.points = 8
        self.max_points = 8
        self.point_block_size = 19
        self.point_block_spacing = 2
        self.point_block_color = (0, 49, 82)
        self.point_block_y = 569
        self.point_block_start_x = 244

        #Config_Round_Counter
        self.current_round = 1
        self.round_text_pos = (119, 559)
        self.round_text_color = (228, 222, 215)

        #Game_Paused_Button
        self.x_min_game_paused_page, self.y_min_game_paused_page = 472, 563
        self.x_max_game_paused_page, self.y_max_game_paused_page = 502, 593

        #Quit_Button
        self.x_min_quit, self.y_min_quit = 508, 563
        self.x_max_quit, self.y_max_quit = 538, 593

        #Sound_Button
        self.x_min_sound_button, self.y_min_sound_button = 436, 563
        self.x_max_sound_button, self.y_max_sound_button = 466, 593

        #Confirm_Button
        self.x_min_confirm_button, self.y_min_confirm_button = 666, 563
        self.x_max_confirm_button, self.y_max_confirm_button = 794, 593

        #Rules_Button
        self.x_min_rules_button, self.y_min_rules_button = 547, 563
        self.x_max_rules_button, self.y_max_rules_button = 660, 593

        #Back_Button
        self.x_min_back_button, self.y_min_back_button = 547, 563
        self.x_max_back_button, self.y_max_back_button = 660, 593

        #Remove_Button
        self.x_min_remove_button, self.y_min_remove_button = 547, 563
        self.x_max_remove_button, self.y_max_remove_button = 660, 593
        self.remove_mode = False
        self.last_clicked_card = None
        self.last_click_time = 0
        self.remove_click_count = 0
        self.remove_used_this_round = False
        self.show_remove_popup = False
        self.last_click_time = 0
        self.remove_click_count = 0
        self.remove_used_this_round = False

    def update_side_text(self):
        """
        Update the display text for current active player

        Updates to show "YOUR TURN" or "COMPUTER'S TURN" based on side_status value
        """
        #Update_Side_Text_Box
        if self.side_status == 0:
            self.side_text_box = "YOUR TURN"
        elif self.side_status == 1:
            self.side_text_box = "COMPUTER'S TURN"

    def draw_timer(self):
        """
        Draw game timer

        Displays remaining time on screen in "00:XX" format
        """
        #Draw_Timer_Text
        timer_text = self.font_timer.render(f"00:{self.timer_seconds:02d}", True, self.text_color_timer)
        self.screen.blit(timer_text, (self.timer_x, self.timer_y))

    def draw_points(self):
        """
        Draw points blocks

        Display current points using blue blocks arranged horizontally, maximum 8 blocks
        Display from left to right, points reduction removes blocks from left to right
        """
        #Draw_Points_Blocks
        for i in range(self.max_points):
            #Calculate_Block_Position
            x = self.point_block_start_x + i * (self.point_block_size + self.point_block_spacing)
            rect = pygame.Rect(x, self.point_block_y, self.point_block_size, self.point_block_size)
            #Draw_Active_Blocks
            if i >= (self.max_points - self.points):
                pygame.draw.rect(self.screen, self.point_block_color, rect)

    def draw_side_text_box(self):
        """
        Draw the current side status text box

        Renders and displays the current player's turn status at the top of the screen
        """
        #Draw_Title
        text = self.font_default.render(self.side_text_box, True, self.side_text_box_color)
        self.screen.blit(text, (self.side_text_box_pos[0] - text.get_width() // 2, self.side_text_box_pos[1]))

    def draw_current_word_letters(self):
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

    def draw_card_letters(self):
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
        card_width = 49
        card_spacing = 1
        card_y = 449
        total_positions = 15

        #Get all historically used cards
        all_used_cards = set()
        for used_cards in self.used_cards_history.values():
            all_used_cards.update(used_cards)

        #Get currently available cards (excluding historically used cards)
        unused_cards = [i for i in range(self.visible_card_count) if
                        i not in all_used_cards and i not in self.used_card_positions]
        total_unused = len(unused_cards)

        #Calculate the number of empty card position
        total_empty = total_positions - total_unused
        empty_start = total_empty // 2
        if total_unused % 2 == 0:
            empty_start = (total_empty - 1) // 2

        #Traverse all card positions
        for i in range(total_positions):
            x = 28 + i * (card_width + card_spacing)

            #Determine whether the card should be displayed at the current location
            card_index = i - empty_start
            if 0 <= card_index < total_unused:
                card_idx = unused_cards[card_index]
                #Update the click area to a new location
                self.card_click_areas[card_idx] = (x, card_y, card_width, card_width)
                #Draw card letters
                letter_text = self.card_font.render(self.card_letters[card_idx], True, self.card_text_color)
                text_x = x + 25 - letter_text.get_width() // 2
                text_y = card_y + 25 - letter_text.get_height() // 2
                self.screen.blit(letter_text, (text_x, text_y))

    def draw_coordinate_display(self):
        """
        Draw mouse coordinate display

        Shows the current X and Y coordinates of the mouse cursor
        in the top-left corner of the screen
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        text = self.font_default.render(f"X: {mouse_x}, Y: {mouse_y}", True, self.text_color_coordinate)
        text_rect = text.get_rect()
        text_rect.topleft = (10, 5)
        self.screen.blit(text, text_rect)

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
            current_word = ''.join(self.current_word_letters)
            print(f"Round {self.current_round} ended. Current word: {current_word}")

            #Save the cards used in this round to the self.used_cards_history
            if self.used_card_positions:
                self.used_cards_history[self.current_round] = self.used_card_positions.copy()

            #Check remaining cards
            all_used_cards = set()
            for used_cards in self.used_cards_history.values():
                all_used_cards.update(used_cards)
            unused_cards = [i for i in range(self.visible_card_count)
                            if i not in all_used_cards and i not in self.used_card_positions]
            if len(unused_cards) == 0:
                print("Win")
                self.screen.blit(self.image_win_page, (0, 0))
                pygame.display.flip()
            if len(unused_cards) >= 16:
                print("Lose")
                self.screen.blit(self.image_lose_page, (0, 0))
                pygame.display.flip()

                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            pygame.quit()
                            python = sys.executable
                            os.execl(python, python, *sys.argv)
                        elif event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

            #Reset the usage record of the current round (keep the historical cards)
            self.used_card_positions = []
            self.last_swapped_position = None
            self.original_letters = []
            self.selected_letters = []
            self.remove_used_this_round = False
            #Update the sides
            self.side_status = 1 - self.side_status
            if self.side_status == 0:
                self.current_round += 1

            #Reset Timer
            self.timer_seconds = self.timer_duration
            self.update_side_text()
            self.show_popup = True
            self.game_paused = True
            pygame.time.set_timer(self.timer_event, 0)

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
        pygame.draw.rect(self.screen, self.popup_side_changer_color_border, self.popup_rect, 2)
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

    def draw_remove_popup(self):
        """
        Draw the remove mode popup

        Same content as above
        """
        s = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))
        self.screen.blit(s, (0, 0))
        pygame.draw.rect(self.screen, self.popup_remove_color_background, self.popup_rect)
        pygame.draw.rect(self.screen, self.popup_remove_color_border, self.popup_rect, 2)
        popup_text_render = self.font_default.render(self.popup_remove_text, True, self.popup_remove_color_text_button)
        self.screen.blit(popup_text_render,
                         (self.popup_rect.centerx - popup_text_render.get_width() // 2, self.popup_rect.centery - 40))
        pygame.draw.rect(self.screen, self.popup_remove_color_button, self.button_rect)
        pygame.draw.rect(self.screen, self.popup_remove_color_button_border, self.button_rect, 2)
        button_text_render = self.font_default.render(self.popup_remove_text_button, True, self.popup_remove_color_text)
        self.screen.blit(button_text_render, (self.button_rect.centerx - button_text_render.get_width() // 2,
                                              self.button_rect.centery - button_text_render.get_height() // 2))

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
        #Disable all buttons on the welcome page and story pages
        if self.show_welcome_page or self.current_story_page >= 0:
            return True

        #Back_Button
        if self.show_rules_page:
            if self.x_min_back_button <= mouse_x <= self.x_max_back_button and self.y_min_back_button <= mouse_y <= self.y_max_back_button:
                if pygame.mouse.get_pressed()[0]:
                    self.button_sound.play()
                    self.show_rules_page = False
                    self.game_paused = False
                    pygame.time.set_timer(self.timer_event, 1000)

        #Rules_Button
        if self.x_min_rules_button <= mouse_x <= self.x_max_rules_button and self.y_min_rules_button <= mouse_y <= self.y_max_rules_button:
            if pygame.mouse.get_pressed()[0]:
                self.button_sound.play()
                if self.show_game_paused_page and not self.show_rules_page:
                    self.show_rules_page = True
                    self.show_game_paused_page = False

        #Quit_Button
        if self.x_min_quit <= mouse_x <= self.x_max_quit and self.y_min_quit <= mouse_y <= self.y_max_quit:
            if pygame.mouse.get_pressed()[0]:
                self.button_sound.play()
                print("Quit")
                return False

        #Game_Paused_Button
        if self.x_min_game_paused_page <= mouse_x <= self.x_max_game_paused_page and self.y_min_game_paused_page <= mouse_y <= self.y_max_game_paused_page:
            if pygame.mouse.get_pressed()[0]:
                self.button_sound.play()
                if self.show_game_paused_page:
                    self.show_game_paused_page = False
                    self.game_paused = False
                    pygame.time.set_timer(self.timer_event, 1000)
                else:
                    self.show_game_paused_page = True
                    self.game_paused = True
                    pygame.time.set_timer(self.timer_event, 0)

        #Confirm_Button
        if self.x_min_confirm_button <= mouse_x <= self.x_max_confirm_button and self.y_min_confirm_button <= mouse_y <= self.y_max_confirm_button:
            if pygame.mouse.get_pressed()[0] and self.side_status == 0:
                self.button_sound.play()
                self.timer_seconds = 0

        #Sound_Button
        if self.x_min_sound_button <= mouse_x <= self.x_max_sound_button and self.y_min_sound_button <= mouse_y <= self.y_max_sound_button:
            if pygame.mouse.get_pressed()[0]:
                self.button_sound.play()
                if self.sound_enabled:
                    pygame.mixer.music.set_volume(0)
                    self.sound_enabled = False
                    self.current_background = self.background_mute
                else:
                    pygame.mixer.music.set_volume(0.3)
                    self.sound_enabled = True
                    self.current_background = self.background
                self.button_sound.play()

        #Remove_Button
        if (
                self.x_min_remove_button <= mouse_x <= self.x_max_remove_button and self.y_min_remove_button <= mouse_y <= self.y_max_remove_button):
            if pygame.mouse.get_pressed()[0] and not self.show_game_paused_page and not self.show_rules_page:
                if self.side_status == 0:
                    if self.remove_used_this_round:
                        self.show_remove_popup = True
                        return True
                    self.button_sound.play()
                    if self.remove_mode:
                        self.remove_mode = False
                    else:
                        self.remove_mode = True
                else:
                    self.popup_remove_text = "Player's turn only"
                    self.show_remove_popup = True
                return True

        return True

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
        if self.side_status != 0 or self.game_paused:
            return

        #Get all historically used cards
        all_used_cards = set()
        for used_cards in self.used_cards_history.values():
            all_used_cards.update(used_cards)

        #Get currently available cards (excluding historically used cards)
        unused_cards = [i for i in range(self.visible_card_count)
                        if i not in all_used_cards and i not in self.used_card_positions]
        total_unused = len(unused_cards)

        #Calculate the number of empty card position and starting position
        total_empty = 15 - total_unused
        empty_start = total_empty // 2
        if total_unused % 2 == 0:
            empty_start = (total_empty - 1) // 2

        #Calculate the actual card position and click area
        card_width = 49
        card_spacing = 1
        card_y = 449

        #Traverse the actual displayed card positions
        for i in range(total_unused):
            x = 28 + (i + empty_start) * (card_width + card_spacing)
            if x <= mouse_x <= x + card_width and card_y <= mouse_y <= card_y + card_width:
                if i < len(unused_cards):
                    card_idx = unused_cards[i]
                    if card_idx not in self.used_card_positions:
                        selected_letter = self.card_letters[card_idx]
                        if self.remove_mode:
                            #Check if points are sufficient
                            if self.points < 2:
                                print("Insufficient points to remove card")
                                return True
                            current_time = pygame.time.get_ticks()
                            if self.last_clicked_card != card_idx or current_time - self.last_click_time > 1000:
                                self.remove_click_count = 1
                                self.last_clicked_card = card_idx
                            else:
                                self.remove_click_count += 1
                                if self.remove_click_count >= 3:
                                    print(f"Card removed: {selected_letter}")
                                    self.used_card_positions.append(card_idx)
                                    #Consume 2 points
                                    self.points -= 2
                                    self.remove_click_count = 0
                                    self.last_clicked_card = None
                                    self.remove_mode = False
                                    #Mark remove mode as used for this round
                                    self.remove_used_this_round = True
                                else:
                                    print(f"Click count: {self.remove_click_count}")
                            self.last_click_time = current_time
                            return True
                        self.selected_letters = [(card_idx, selected_letter)]
                        print(f"Selected Letter: {selected_letter}")
                        return True
        return False

    def handle_current_word_click(self, mouse_x, mouse_y):
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

                    #Same_Letter_Checker
                    if card_letter == current_letter:
                        print(f"Cannot swap same letter: {card_letter}")
                        self.selected_letters = []
                        return True

                    #Handle_Previous_Swap
                    if self.last_swapped_position is not None:
                        #Same_Position_Swap
                        if self.last_swapped_position == i:
                            if self.used_card_positions:
                                last_card_position = self.used_card_positions.pop()
                        #Different_Position_Swap
                        else:
                            self.current_word_letters[self.last_swapped_position] = self.original_letters[
                                self.last_swapped_position]
                            if self.used_card_positions:
                                last_card_position = self.used_card_positions.pop()

                    #Store_Original_Letters
                    if not self.original_letters:
                        self.original_letters = self.current_word_letters.copy()

                    #Update_Current_Word
                    self.current_word_letters[i] = card_letter
                    print(f"Swapped letters: {current_letter} -> {card_letter}")

                    #Update_Swap_Status
                    self.last_swapped_position = i
                    self.used_card_positions.append(card_position)
                    self.selected_letters = []
                return True
        return False

    def handle_popup_click(self, pos):
        """
        Handle clicks on popups
        """
        if self.show_remove_popup:
            if self.remove_button_rect.collidepoint(pos):
                self.button_sound.play()
                self.show_remove_popup = False
                return

        if self.show_popup:
            if self.button_rect.collidepoint(pos):
                self.button_sound.play()
                self.show_popup = False
                self.game_paused = False
                pygame.time.set_timer(self.timer_event, 1000)

    def handle_events(self):
        """
        Main event handler for the game

        Returns:
            bool: False if game should quit, True otherwise

        Processes all game events including:
            - Quit events
            - Mouse wheel events
            - Mouse clicks
            - Timer events
            - Others (Developing)
        """
        for event in pygame.event.get():
            #Quit_Event
            if event.type == pygame.QUIT:
                return False
            #Mouse_Wheel_Event
            elif event.type == pygame.MOUSEWHEEL:
                continue
            #Mouse_Click_Event
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if not self.handle_button_click(mouse_x, mouse_y):
                    return False
                #Welcome_Page_Click
                if self.show_welcome_page:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.button_sound.play()
                        self.show_welcome_page = False
                        self.current_story_page = 0
                        pygame.time.set_timer(self.timer_event, 0)
                #Story_Page_Click
                elif self.current_story_page >= 0:
                    #Left_Click_Next_Page
                    if event.button == 1:
                        self.button_sound.play()
                        if self.current_story_page == 5:
                            self.current_story_page = -1
                            self.game_paused = False
                            pygame.time.set_timer(self.timer_event, 1000)
                        else:
                            self.current_story_page += 1
                    #Right_Click_Previous_Page
                    elif event.button == 3:
                        self.button_sound.play()
                        if self.current_story_page > 0:
                            self.current_story_page -= 1
                #Popup_Click
                elif self.show_popup or self.show_remove_popup:
                    self.handle_popup_click(event.pos)
                #Game_Card_Click
                else:
                    self.handle_card_click(mouse_x, mouse_y)
                    self.handle_current_word_click(mouse_x, mouse_y)
            #Timer_Event
            elif event.type == self.timer_event:
                self.handle_timer_event()
        return True

    #Draw_Round_Counter
    def draw_round_counter(self):
        """
        Draw the current round number

        Renders the current round number at the designated position
        using the round font and color
        """
        round_text = self.font_round.render(str(self.current_round), True, self.round_text_color)
        self.screen.blit(round_text, self.round_text_pos)

    #Draw_Game_Screen
    def draw(self):
        """
        Main drawing function

        Handles all game rendering including:
            - Background
            - Game elements (timer, text, cards)
            - Welcome page
            - Story pages
            - Pause menu
            - Popups
            - Rules page
            - Others (Developing)
        """
        #Draw_Background
        self.screen.blit(self.current_background, (0, 0))
        self.draw_side_text_box()
        self.draw_coordinate_display()
        self.draw_current_word_letters()
        self.draw_card_letters()
        self.draw_points()
        self.draw_round_counter()

        #Draw_Timer_After_Overlay
        self.draw_timer()

        #Draw_Game_Status
        if not self.game_paused:
            self.draw_side_text_box()
            self.draw_timer()

        #Draw_Welcome_Page
        if self.show_welcome_page:
            self.screen.blit(self.image_welcome_page, (0, 0))
            pygame.display.flip()
            return

        #Draw_Story_Page
        elif self.current_story_page >= 0:
            self.screen.blit(self.story_images[self.current_story_page], (0, 0))
            pygame.display.flip()
            return

        #Draw_Game_Pages
        if self.show_game_paused_page:
            self.screen.blit(self.image_game_paused_page, (0, 0))
        if self.show_popup:
            self.draw_popup()
        if self.show_rules_page:
            self.screen.blit(self.image_rules_page, (0, 0))

        #Draw Remove Mode Page
        if self.remove_mode:
            self.screen.blit(self.image_remove_page, (0, 0))

        #Draw Remove Popup
        if self.show_remove_popup:
            self.draw_remove_popup()

        #Update_Screen
        pygame.display.flip()

    def run(self):
        """
        Main game loop

        Initializes and runs the game, handling events and updating display
        until the game is closed
        """
        running = True
        while running:
            running = self.handle_events()
            self.draw()
        #Quit Pygame
        pygame.mixer.music.stop()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = CardGameUI()
    game.run()

