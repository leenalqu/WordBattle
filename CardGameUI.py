#Coded by Jiaxi Huang (5670238)

#Import libraries
import pygame
import sys

#Initialize Pygame
pygame.init()

#Config_Settings
show_popup = False
game_paused = False
show_welcome_page = True
show_game_paused_page = False
show_homepage = False

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

#Config_Welcome_Page
image_welcome_page = pygame.image.load("data/image/welcome_page.png")
image_welcome_page = pygame.transform.scale(image_welcome_page, (screen_width, screen_height))

#Config_Pause_Page
image_game_paused_page = pygame.image.load("data/image/game_paused_page.png")
image_game_paused_page = pygame.transform.scale(image_game_paused_page, (screen_width, screen_height))

#Config_HomePage
image_homepage = pygame.image.load("data/image/homepage.png")
image_homepage = pygame.transform.scale(image_homepage, (screen_width, screen_height))

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

#Coodinate Checker

#Homepage_Button
x_min_homepage, y_min_homepage = 146, 563
x_max_homepage, y_max_homepage = 176, 593

#Game_Paused_Button
x_min_game_paused_page, y_min_game_paused_page = 181, 563
x_max_game_paused_page, y_max_game_paused_page = 211, 593

#Game_Continued_Button
x_min_game_continued_page, y_min_game_continued_page = 216, 563
x_max_game_continued_page, y_max_game_continued_page = 246, 593

#Quit_Button
x_min_quit, y_min_quit = 251, 563
x_max_quit, y_max_quit = 281, 593

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

        #Detect the coordinate range of mouse clicks
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            #Homepage_Button
            if x_min_homepage <= mouse_x <= x_max_homepage and y_min_homepage <= mouse_y <= y_max_homepage:
                show_homepage = True
            #Quit_Button
            if x_min_quit <= mouse_x <= x_max_quit and y_min_quit <= mouse_y <= y_max_quit:
                print("Quit")
                running = False
            #Game_Paused_Button
            if x_min_game_paused_page <= mouse_x <= x_max_game_paused_page and y_min_game_paused_page <= mouse_y <= y_max_game_paused_page:
                show_game_paused_page = True
                game_paused = True
            #Game_Continued_Button
            if x_min_game_continued_page <= mouse_x <= x_max_game_continued_page and y_min_game_continued_page <= mouse_y <= y_max_game_continued_page:
                show_game_paused_page = False
                show_homepage = False
                game_paused = False

        #Welcome_Page_Interaction
        elif show_welcome_page:
            if event.type == pygame.MOUSEBUTTONDOWN:
                show_welcome_page = False

            elif event.type == pygame.MOUSEBUTTONDOWN and show_welcome_page:
                show_welcome_page = False
                game_paused = False

        #HomePage_Interaction
        elif show_homepage:
            if event.type == pygame.MOUSEBUTTONDOWN and x_min_game_continued_page <= mouse_x <= x_max_game_continued_page and y_min_game_continued_page <= mouse_y <= y_max_game_continued_page:
                show_homepage = False
                game_paused = False

        #Game_Paused_Page_Interaction
        elif show_game_paused_page:
            if event.type == pygame.MOUSEBUTTONDOWN and x_min_game_continued_page <= mouse_x <= x_max_game_continued_page and y_min_game_continued_page <= mouse_y <= y_max_game_continued_page:
                show_game_paused_page = False
                game_paused = False

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

    if show_welcome_page:
        screen.blit(image_welcome_page, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                show_welcome_page = False
        pygame.display.flip()
        continue

    if show_game_paused_page:
        screen.blit(image_game_paused_page, (0, 0))

    if show_homepage:
        screen.blit(image_homepage, (0, 0))

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