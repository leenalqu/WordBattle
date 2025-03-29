#Coded by Jiaxi Huang (5670238)

#Import libraries
import pygame
import sys

#Initialize Pygame
pygame.init()

#Config_Settings
show_popup = False
game_paused = False

#Config_Screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Debug Mode")

#Config_Coordinate_Box
text_color_coordinate = (0, 49, 82)

#Config_Background
background = pygame.image.load("data/image/background.png")
background = pygame.transform.scale(background, (screen_width, screen_height))

#Config_Font
font_size_default = 24
font_size_timer = 88
font_default = pygame.font.Font("data/font/AaHuanMengKongJianXiangSuTi-2.ttf", font_size_default)
font_timer = pygame.font.Font("data/font/AaHuanMengKongJianXiangSuTi-2.ttf", font_size_timer)

#Config_Timer
timer_event = pygame.USEREVENT + 1
timer_duration = 15
timer_seconds = timer_duration
timer_x = 301
timer_y = 282
text_color_timer = (228, 222, 215)
pygame.time.set_timer(timer_event, 1000)
popup_rect = pygame.Rect(screen_width // 2 - 150, screen_height // 2 - 75, 300, 150)
button_rect = pygame.Rect(screen_width // 2 - 50, screen_height // 2 + 25, 100, 30)

#Config_Popup
popup_side_changer_width = 350
popup_side_changer_height = 150
popup_side_changer_width_button = 100
popup_side_changer_height_button = 30
popup_side_changer_pos_x = screen_width // 2 - popup_side_changer_width // 2
popup_side_changer_pos_y = screen_width // 2 - popup_side_changer_height // 2
popup_side_changer_pos_x_button = screen_width // 2 - popup_side_changer_width_button // 2
popup_side_changer_pos_y_button = screen_width // 2 + 25
popup_side_changer_color_background = (228, 222, 215)
popup_side_changer_color_border = (228, 222, 215)
popup_side_changer_color_button = (0, 49, 82)
popup_side_changer_color_button_border = (0, 49, 82)
popup_side_changer_color_text = (228, 222, 215)
popup_side_changer_color_text_button = (0, 49, 82)
popup_side_changer_text = "Side has changed"
popup_side_changer_text_button = "OK"

#Config_Side_Status
side_status = 0
if side_status == 0:
    side_text_box = "YOUR TURN"
elif side_status == 1:
    side_text_box = "COMPUTER'S TURN"
side_text_box_pos = (screen_width // 2, 5)
side_text_box_color = (0, 49, 82)

#Function Section
def draw_timer():
    global timer_seconds, side_status
    timer_text = font_timer.render(f"00:{timer_seconds:02d}", True, text_color_timer)
    screen.blit(timer_text, (timer_x, timer_y))

def draw_side_text_box():
    #Draw Title
    text = font_default.render(side_text_box, True, side_text_box_color)
    screen.blit(text, (side_text_box_pos[0] - text.get_width() // 2, side_text_box_pos[1]))

#Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #Ban Mousewheel
        elif event.type == pygame.MOUSEWHEEL:
            continue
        #Pause Game when Popup
        elif event.type == timer_event:
            if timer_seconds > 0 and not game_paused:
                timer_seconds -= 1
            else:
                side_status = 1 - side_status
                timer_seconds = timer_duration
                if side_status == 0:
                    side_text_box = "YOUR TURN"
                else:
                    side_text_box = "COMPUTER'S TURN"
                show_popup = True
                game_paused = True
                pygame.time.set_timer(timer_event, 0)
        #Continue Game when no Popup
        elif event.type == pygame.MOUSEBUTTONDOWN and show_popup:
            if button_rect.collidepoint(event.pos):
                show_popup = False
                game_paused = False
                pygame.time.set_timer(timer_event, 1000)

    #Obtain Mouse Coordinate
    mouse_x, mouse_y = pygame.mouse.get_pos()
    text = font_default.render(f"X: {mouse_x}, Y: {mouse_y}", True, text_color_coordinate)
    text_rect = text.get_rect()
    text_rect.topleft = (10, 5)

    #Draw Sections
    screen.blit(background, (0, 0))
    draw_timer()
    draw_side_text_box()
    screen.blit(text, text_rect)

    if not game_paused:
        draw_side_text_box()
        draw_timer()

    if show_popup:
        s = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))
        screen.blit(s, (0, 0))
        pygame.draw.rect(screen, popup_side_changer_color_background, popup_rect)
        pygame.draw.rect(screen, popup_side_changer_color_border, popup_rect, 2)
        popup_text_render = font_default.render(popup_side_changer_text, True, popup_side_changer_color_text_button)
        screen.blit(popup_text_render, (popup_rect.centerx - popup_text_render.get_width() // 2, popup_rect.centery - 40))
        pygame.draw.rect(screen, popup_side_changer_color_button, button_rect)
        pygame.draw.rect(screen,popup_side_changer_color_button_border, button_rect, 2)
        button_text_render = font_default.render(popup_side_changer_text_button, True, popup_side_changer_color_text)
        screen.blit(button_text_render, (button_rect.centerx - button_text_render.get_width() // 2, button_rect.centery - button_text_render.get_height() // 2))

    #Refresh Screen
    pygame.display.flip()

#Quit Pygame
pygame.quit()
sys.exit()