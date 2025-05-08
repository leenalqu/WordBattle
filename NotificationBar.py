import pygame
import sys
import time


class NotificationBar:
    """
    # Import Librart
    from NotificationBar import NotificationBar

    # Create a notification bar instance
    notification = NotificationBar(screen_width=your_screen_width, screen_height=your_screen_height)
    notification.update_message_box()

    # Use the notification bar in main game loop
    notification.draw_message_box(screen, font)

    # Show a notification message in the game
    notification.show_message_box("CANNOT REPLACE SAME CARD")
    """
    def __init__(self, screen_width=800, screen_height=600, x=None, y=None):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.width_message_box = 291
        self.height_message_box = 80
        self.x_message_box = 258
        self.y_message_box = -60
        self.y_target_message_box = 0
        self.surface = pygame.Surface((self.width_message_box, self.height_message_box), pygame.SRCALPHA)
        self.transparency_level = 255
        self.show_time = 0
        self.is_showing = False
        self.message = ""
        self.color_message_box_background = (188, 173, 119)
        self.color_message_box_border = (33, 33, 33)
        self.color_message_box_text = (33, 33, 33)
        self.update_colors(self.color_message_box_background, self.color_message_box_border, self.color_message_box_text)

    def update_colors(self, background_color, border_color, text_color):
        self.color_message_box_background = background_color
        self.color_message_box_border = border_color
        self.color_message_box_text = text_color

    def show_message_box(self, message):
        self.message = message
        self.is_showing = True
        self.show_time = pygame.time.get_ticks()
        self.transparency_level = 255
        self.y_message_box = -60
        
    def update_message_box(self):
        if not self.is_showing:
            return

        current_time = pygame.time.get_ticks()
        if self.y_message_box < self.y_target_message_box:
            self.y_message_box += 4

        if current_time - self.show_time > 2200:
            self.transparency_level -= 5
            if self.transparency_level <= 0:
                self.is_showing = False
                
    def draw_message_box(self, screen, font):
        if not self.is_showing:
            return

        self.surface.fill((0, 0, 0, 0))
        pygame.draw.rect(self.surface, (*self.color_message_box_background, self.transparency_level), (0, 0, self.width_message_box, self.height_message_box))
        border_width = 5
        pygame.draw.rect(self.surface, (*self.color_message_box_border, self.transparency_level), (0, 0, self.width_message_box, self.height_message_box), border_width)
        text = font.render(self.message, True, self.color_message_box_text)
        text.set_alpha(self.transparency_level)
        text_rect = text.get_rect(center=(self.width_message_box//2, self.height_message_box//2+1))
        self.surface.blit(text, text_rect)
        screen.blit(self.surface, (self.x_message_box, self.y_message_box))

def run_notification_demo():
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    background_image = pygame.image.load("data/image/background_0.png")
    font = pygame.font.Font("data/font/AaHuanMengKongJianXiangSuTi-2.ttf", 24)
    notification = NotificationBar(screen_width=screen_width, screen_height=screen_height)
    clock = pygame.time.Clock()
    button_rect = pygame.Rect(0, 0, screen_width, screen_height)
    button_color = (0, 0, 0)
    button_text = font.render("DISPLAY", True, (255, 255, 255))
    button_text_rect = button_text.get_rect(center=button_rect.center)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    notification.show_message_box("MESSAGE BOX DISPLAY")
                    
        notification.update_message_box()
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, button_color, button_rect)
        screen.blit(button_text, button_text_rect)
        screen.blit(background_image, (0, 0))
        notification.draw_message_box(screen, font)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    run_notification_demo()