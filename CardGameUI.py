#Coded by Jiaxi Huang (5670238)

#Import libraries
import pygame
import sys

class CardGameUI:
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
        self.image_welcome_page = pygame.transform.scale(self.image_welcome_page, (self.screen_width, self.screen_height))

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

        #Config_Font
        self.font_size_default = 24
        self.font_size_timer = 88
        self.font_size_round = 34
        self.font_default = pygame.font.Font("data/font/AaHuanMengKongJianXiangSuTi-2.ttf", self.font_size_default)
        self.font_timer = pygame.font.Font("data/font/AaHuanMengKongJianXiangSuTi-2.ttf", self.font_size_timer)
        self.font_round = pygame.font.Font("data/font/AaHuanMengKongJianXiangSuTi-2.ttf", self.font_size_round)

        #Config_Timer
        self.timer_event = pygame.USEREVENT + 1
        self.timer_duration = 15
        self.timer_seconds = self.timer_duration
        self.timer_x = 301
        self.timer_y = 248
        self.text_color_timer = (228, 222, 215)
        pygame.time.set_timer(self.timer_event, 1000)
        self.popup_rect = pygame.Rect(self.screen_width // 2 - 150, self.screen_height // 2 - 75, 300, 150)
        self.button_rect = pygame.Rect(self.screen_width // 2 - 50, self.screen_height // 2 + 25, 100, 30)

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

        #Config_Side_Status
        self.side_status = 0
        self.update_side_text()
        self.side_text_box_pos = (self.screen_width // 2, 5)
        self.side_text_box_color = (228, 222, 215)

        #Config_Current_Word
        self.current_word_font_size = 88
        self.current_word_font = pygame.font.Font("data/font/AaHuanMengKongJianXiangSuTi-2.ttf", self.current_word_font_size)
        self.current_word_letter_1 = 'C'
        self.current_word_letter_2 = 'A'
        self.current_word_letter_3 = 'T'
        self.current_word_letters = [self.current_word_letter_1, self.current_word_letter_2, self.current_word_letter_3]
        self.current_word_text_color = (228, 222, 215)
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

        #Config_Card_Letters
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
        self.card_text_color = (228, 222, 215)
        self.selected_letter_color = (240, 153, 31)
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

        #Config_Sound
        pygame.mixer.music.load("data/sound/background_music.wav")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        self.button_sound = pygame.mixer.Sound("data/sound/button_sound.wav")
        self.sound_enabled = True

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

    def update_side_text(self):
        if self.side_status == 0:
            self.side_text_box = "YOUR TURN"
        elif self.side_status == 1:
            self.side_text_box = "WORDIUS'S TURN"

    def draw_timer(self):
        timer_text = self.font_timer.render(f"00:{self.timer_seconds:02d}", True, self.text_color_timer)
        self.screen.blit(timer_text, (self.timer_x, self.timer_y))

    def draw_side_text_box(self):
        #Draw Title
        text = self.font_default.render(self.side_text_box, True, self.side_text_box_color)
        self.screen.blit(text, (self.side_text_box_pos[0] - text.get_width() // 2, self.side_text_box_pos[1]))

    def draw_current_word_letters(self):
        for i, pos in enumerate(self.current_word_positions):
            letter_text = self.current_word_font.render(self.current_word_letters[i], True,
                                                        self.current_word_text_color)
            text_x = pos[0] + 47 - letter_text.get_width() // 2
            text_y = pos[1] + 47 - letter_text.get_height() // 2
            self.screen.blit(letter_text, (text_x, text_y))

    def draw_card_letters(self):
        for i, pos in enumerate(self.card_positions[:self.visible_card_count]):
            #Only draw unused cards
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

    def draw_coordinate_display(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        text = self.font_default.render(f"X: {mouse_x}, Y: {mouse_y}", True, self.text_color_coordinate)
        text_rect = text.get_rect()
        text_rect.topleft = (10, 5)
        self.screen.blit(text, text_rect)

    def draw_popup(self):
        s = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))
        self.screen.blit(s, (0, 0))
        pygame.draw.rect(self.screen, self.popup_side_changer_color_background, self.popup_rect)
        pygame.draw.rect(self.screen, self.popup_side_changer_color_border, self.popup_rect, 2)
        popup_text_render = self.font_default.render(self.popup_side_changer_text, True,  self.popup_side_changer_color_text_button)
        self.screen.blit(popup_text_render, (self.popup_rect.centerx - popup_text_render.get_width() // 2, self.popup_rect.centery - 40))
        pygame.draw.rect(self.screen, self.popup_side_changer_color_button, self.button_rect)
        pygame.draw.rect(self.screen, self.popup_side_changer_color_button_border, self.button_rect, 2)
        button_text_render = self.font_default.render(self.popup_side_changer_text_button, True, self.popup_side_changer_color_text)
        self.screen.blit(button_text_render, (self.button_rect.centerx - button_text_render.get_width() // 2,  self.button_rect.centery - button_text_render.get_height() // 2))

    def handle_button_click(self, mouse_x, mouse_y):
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

        return True

    #Handle_Card_Click
    def handle_card_click(self, mouse_x, mouse_y):
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

    #Handle_Current_Word_Click
    def handle_current_word_click(self, mouse_x, mouse_y):
        if self.side_status != 0 or self.game_paused:
            return
        for i, (x, y, width, height) in enumerate(self.current_word_click_areas):
            if x <= mouse_x <= x + width and y <= mouse_y <= y + height:
                if self.selected_letters:
                    card_position, card_letter = self.selected_letters[0]
                    current_letter = self.current_word_letters[i]

                    #Handle_Previous_Swap
                    if self.last_swapped_position is not None:
                        #Same_Position_Swap
                        if self.last_swapped_position == i:
                            if self.used_card_positions:
                                last_card_position = self.used_card_positions.pop()
                                print(f"Restored previous card at position {last_card_position}")
                        #Different_Position_Swap
                        else:
                            self.current_word_letters[self.last_swapped_position] = self.original_letters[
                                self.last_swapped_position]
                            if self.used_card_positions:
                                last_card_position = self.used_card_positions.pop()
                                print(f"Restored card at position {last_card_position}")
                            print(f"Restored position {self.last_swapped_position} to {self.original_letters[self.last_swapped_position]}")

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

    def handle_timer_event(self):
        if self.timer_seconds > 0 and not self.game_paused:
            self.timer_seconds -= 1
        else:
            self.side_status = 1 - self.side_status
            if self.side_status == 0:
                self.current_round += 1
            self.timer_seconds = self.timer_duration
            self.update_side_text()
            self.show_popup = True
            self.game_paused = True
            pygame.time.set_timer(self.timer_event, 0)

    def handle_popup_click(self, pos):
        if self.button_rect.collidepoint(pos):
            self.show_popup = False
            self.game_paused = False
            pygame.time.set_timer(self.timer_event, 1000)

    def handle_events(self):
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
                elif self.show_popup:
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
        round_text = self.font_round.render(str(self.current_round), True, self.round_text_color)
        self.screen.blit(round_text, self.round_text_pos)

    #Draw_Game_Screen
    def draw(self):
        #Draw_Background
        self.screen.blit(self.current_background, (0, 0))
        self.draw_timer()
        self.draw_side_text_box()
        self.draw_coordinate_display()
        self.draw_current_word_letters()
        self.draw_card_letters()
        self.draw_selected_letters()

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

        #Update_Screen
        pygame.display.flip()

    def run(self):
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