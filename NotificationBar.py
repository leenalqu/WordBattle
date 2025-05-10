# Coded by Jiaxi Huang (5670238)
# Libraries Used: pygame, sys
# Data Structures: Tuples, Rectangles, Classes
# Programming Techniques: Object-Oriented Programming(OOP)


# Import libraries
import pygame
import sys


class NotificationBar:
    """
    A notification system that displays temporary message boxes on the screen.
    
    This class creates animated notification boxes that slide down from the top of the screen,
    display for a set duration, and then fade out. 
    It's designed to provide feedback to the user during gameplay without disrupting the main interface.
    
    Attributes:
        screen_width (int): Width of the game screen in pixels.
        screen_height (int): Height of the game screen in pixels.
        width_message_box (int): Width of the notification box.
        height_message_box (int): Height of the notification box.
        x_message_box (int): X-coordinate of the notification box.
        y_message_box (int): Current Y-coordinate of the notification box.
        y_target_message_box (int): Target Y-coordinate for the animation.
        surface (pygame.Surface): Surface for rendering the notification.
        transparency_level (int): Current alpha value for fade effects (0-255).
        show_time (int): Timestamp when the notification was shown.
        is_showing (bool): Whether the notification is currently visible.
        message (str): Text content of the notification.
        color_message_box_background (tuple): RGB color for the box background.
        color_message_box_border (tuple): RGB color for the box border.
        color_message_box_text (tuple): RGB color for the text.
    """
    def __init__(self, screen_width=800, screen_height=600, x=None, y=None):
        """
        Initialize the NotificationBar with default settings.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.width_message_box = 291
        self.height_message_box = 80
        self.x_message_box = 258
        self.y_message_box = -60 #Original Y-coordinate of the notification box
        self.y_target_message_box = 0 # Target Y-coordinate for the animation
        self.surface = pygame.Surface((self.width_message_box, self.height_message_box), pygame.SRCALPHA) # Create a surface with alpha channel
        self.transparency_level = 255
        self.show_time = 0
        self.is_showing = False 
        self.message = ""
        self.color_message_box_background = (188, 173, 119)
        self.color_message_box_border = (33, 33, 33)
        self.color_message_box_text = (33, 33, 33)
        self.update_colors(self.color_message_box_background, self.color_message_box_border, self.color_message_box_text)  

    def update_colors(self, background_color, border_color, text_color):
        """
        Update the color scheme of the notification box.
        
        Parameters:
            background_color (tuple): RGB color tuple for the notification background.
            border_color (tuple): RGB color tuple for the notification border.
            text_color (tuple): RGB color tuple for the notification text.
        """
        self.color_message_box_background = background_color
        self.color_message_box_border = border_color
        self.color_message_box_text = text_color
    
    def show_message_box(self, message):
        """
        Display a notification with the specified message.
        
        Sets the notification to visible state, resets its position to start the slide-down animation, and initializes the transparency for fade effects.
        
        Parameters:
            message (str): The text message to display in the notification box.
        """
        self.message = message # Set the message to display
        self.is_showing = True
        self.show_time = pygame.time.get_ticks() # Get the current time in milliseconds
        self.transparency_level = 255
        self.y_message_box = -60
        
    def update_message_box(self):
        """
        Update the notification box animation state.
        Handles the sliding animation by incrementally moving the box to its target position.
        Manages the fade-out effect after a set display duration.
        """
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
        """
        Render the notification box on the specified screen.

        Parameters:
            screen (pygame.Surface): The surface to draw the notification on.
            font (pygame.font.Font): The font to use for rendering the message text.
        """
        if not self.is_showing:
            return
        self.surface.fill((0, 0, 0, 0)) 
        # Draw the notification box with background, border, and text
        pygame.draw.rect(self.surface, (*self.color_message_box_background, self.transparency_level), (0, 0, self.width_message_box, self.height_message_box))
        border_width = 5  
        pygame.draw.rect(self.surface, (*self.color_message_box_border, self.transparency_level), (0, 0, self.width_message_box, self.height_message_box), border_width)
        text = font.render(self.message, True, self.color_message_box_text) 
        text.set_alpha(self.transparency_level)
        text_rect = text.get_rect(center=(self.width_message_box//2, self.height_message_box//2+1))
        self.surface.blit(text, text_rect)
        screen.blit(self.surface, (self.x_message_box, self.y_message_box))

def run_notification_demo():
    """
    A demo function with game background to test the NotificationBar.
    """
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    background_image = pygame.image.load("data/image/background_0.png")
    font = pygame.font.Font("data/font/AaHuanMengKongJianXiangSuTi-2.ttf", 24)
    notification = NotificationBar(screen_width=screen_width, screen_height=screen_height)
    clock = pygame.time.Clock() # Create a clock object to control the time
    button_rect = pygame.Rect(0, 0, screen_width, screen_height)    
    button_color = (0, 0, 0)
    button_text = font.render("DISPLAY", True, (255, 255, 255))
    button_text_rect = button_text.get_rect(center=button_rect.center)
    
    while True: # Main game loop
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