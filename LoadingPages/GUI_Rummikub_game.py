
# MAIN
# references
# fonts from dafont.com
# https://www.pygame.org/
# https://youtu.be/_D-_OmR36Pk?si=L24aue5dqPrN-_5D
# https://youtu.be/3Yhhzflmxfs?si=X11-bAG-pGzgwOnM
# https://replit.com/@Rabbid76/PyGame-TextInput#main.py
# https://www.geeksforgeeks.org/how-to-create-a-text-input-box-with-pygame/
import pygame, sys, threading, time, math
import os
from pygame.locals import *
from button import Button
from soundbutton import Button2
from main_game import main_game
pygame.init()
pygame.mixer.init()
# create game window
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 800
# define colors
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
purple = (125, 0, 125)
wine = (240, 0, 50)
blue = (0, 0, 255)
pink = (238, 162, 173)
UoNblue = (25, 12, 112)
beige = (255, 211, 155)
maroon = (128, 0, 0)
# define rectangle
x = 200
y = 450
# sounds and effects.
SOUNDON = pygame.image.load("soundon.png")
HOVERING_SOUNDOFF = pygame.image.load("soundoff.png")
# sound button
SOUNDON_BUTTON = Button2(SOUNDON, 60, 713)
HOVERING_SOUNDOFF_BUTTON = Button2(HOVERING_SOUNDOFF, 60, 713)
# define fonts
font = pygame.font.Font('Milk And Honey.ttf', 100)
regularFont = pygame.font.Font('Sweet Vusstain.ttf', 65)
# screens and captions
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("First display page")
# sounds and effects.
# sound= pygame.mixer.Sound('Dave-Ft-Burna-Boy-Location.mp3')

# define fonts
font = pygame.font.Font('Milk And Honey.ttf', 100)
regularFont = pygame.font.Font('Sweet Vusstain.ttf', 65)
loading_font = pygame.font.Font(None, 36)
# define clock
clock = pygame.time.Clock()
fps = 60
IMAGE = pygame.image.load('UoNLogo.png')
IMAGE = pygame.transform.scale_by(IMAGE, 0.4)
# create a text surface object
text = font.render("Rummikub", True, red)
# create rectangular object for text
textRect = text.get_rect()
# set the center of the rectangular object
textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
# Resume text to show start of game after loading:
finished = regularFont.render("Start Game", True, "purple")
finished_rect = finished.get_rect(center=(550, 400))
# create rectangle for username
input_rect = pygame.Rect(200, 200, 140, 32)

def get_font(size):
    return pygame.font.Font('Sweet Vusstain.ttf', size)

base_font = pygame.font.Font(None, 32)
username = " "
# create rectangle for username
input_rect = pygame.Rect(200, 200, 140, 32)
# gets active input box
color_active = pygame.Color('lightskyblue3')
# color of input box.
color_passive = pygame.Color('chartreuse4')
color_passive = pygame.Color('chartreuse4')
color = color_passive
active = False

# if event.type == pygame.MOUSEBUTTONDOWN:
#             if input_rect.collidepoint(event.pos):
#                 active = True
#             else:
#                 active = False
#         if event.type == pygame.KEYDOWN:
#             # Check for backspace
#             if event.key == pygame.K_BACKSPACE:
#                 #text input from 0 to -1 i.e. end.
#                 username = username[:-1]
#             # Unicode standard is used for string
#             # formation
#             else:
#                 username += event.unicode

#         # set background color of screen
#         screen.fill((255, 255, 255))
#         if active:
#             color = color_active
#         else:
#             color = color_passive

#         pygame.draw.rect(screen, color, input_rect)
#         username_surface = base_font.render(username, True, (255, 255, 255))
#         # render at position stated in arguments
#         screen.blit(username_surface, (input_rect.x+5, input_rect.y+5))
#         # set width of textfield so that text cannot get
#         # outside of user's text input
#         input_rect.w = max(100, username_surface.get_width()+10)

# def user_input():
#     username = " "
#     input_active =True
#     run = True
#     while run:
#         clock.tick(60)
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run = False
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 input_active = True
#                 username = " "
#             elif event.type == pygame.KEYDOWN and input_active:
#                 if event.key == pygame.K_RETURN:
#                     input_active = False
#                 elif event.key == pygame.K_BACKSPACE:
#                     username =  username[:-1]
#                 else:
#                     username += event.unicode
#             # screen.fill(0)
#             username_surf =font.render(username, True, blue)
#             screen.blit(username_surf, username_surf.get_rect(center=(550,300)))
#             pygame.display.flip()
def run_game():
    # render text
    pygame.display.set_caption("initialize game")
    screen.fill(maroon)
    IMAGE = pygame.image.load('UoNLogo.png')
    IMAGE = pygame.transform.scale_by(IMAGE, 0.4)
    SOUNDON = pygame.image.load("soundon.png")
    HOVERING_SOUNDOFF = pygame.image.load("soundoff.png")
    # sound buttons
    SOUNDON_BUTTON = Button2(SOUNDON, 60, 713)
    HOVERING_SOUNDOFF_BUTTON = Button2(HOVERING_SOUNDOFF, 60, 713)
    # sound effect
    SOUNDON_SFX = pygame.mixer.Sound("backgroundmusic.mp3")
    HOVERING_SOUNDOFF_SFX = pygame.mixer.Sound("ping-sound 1.mp3")
    text = font.render("Rummikub", True, beige)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
    screen.blit(IMAGE, (0, 0))
    # screen.blit(SOUNDON,(0,630))
    # screen.blit(SOUNDOFF,(0,713))
    screen.blit(text, textRect)
    # Loading bar
    pygame.draw.rect(screen, pygame.Color('yellow'), (250, 450, 100, 10), border_radius=5)
    pygame.draw.rect(screen, pygame.Color('yellow'), (250, 450, loading_progress, 10), border_radius=5)
    # loading text
    loading_text = loading_font.render("Loading ...", True, UoNblue)
    loading_rect = loading_text.get_rect(center=(SCREEN_WIDTH // 2, 435))
    screen.blit(loading_text, loading_rect)
    playsound = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if SOUNDON_BUTTON.checkForInput(pygame.mouse.get_pos()):
                playsound = not playsound
                if playsound:
                    SOUNDON_SFX.play()
                else:
                    SOUNDON_SFX.stop()
    SOUNDON_BUTTON.update(screen)
    # HOVERING_SOUNDOFF_BUTTON.update(screen)
    if SOUNDON_BUTTON.checkForInput(pygame.mouse.get_pos()):
        SOUNDON_BUTTON.image = HOVERING_SOUNDOFF
    else:
        SOUNDON_BUTTON.image = SOUNDON
    if HOVERING_SOUNDOFF_BUTTON.checkForInput(pygame.mouse.get_pos()):
        HOVERING_SOUNDOFF_BUTTON.HOVERING_SOUNDOFF = SOUNDON
    else:
        HOVERING_SOUNDOFF_BUTTON.image = HOVERING_SOUNDOFF
    pygame.display.update()

# save username to be called other times
def save_username(username):
    with open("username.txt", "w") as file:
        file.write(username)

def load_username():
    if os.path.exists("username.txt"):
        with open("username.txt", "r") as file:
            return file.read().strip()
    return ""

# Play Screen
def play():
    pygame.display.set_caption("Play")
    active = False
    username = "user"
    while True:
        play_mouse_pos = pygame.mouse.get_pos()
        screen.fill(maroon)
        # # "PLAY NOW" text
        # play_text =get_font(50).render("PLAY NOW", True, UoNblue)
        # play_rect =play_text.get_rect(center =(550, 400))
        # screen.blit(play_text, play_rect)
        # "BACK" button
        play_back = Button(image=None, pos=(1035, 30), text_input="BACK", font=get_font(50), base_color=UoNblue,
                           hovering_color=wine)
        play_back.changeColor(play_mouse_pos)
        play_back.update(screen)
        play_now_mouse_pos = pygame.mouse.get_pos()
        # "BACK" button
        play_now = Button(image=None, pos=(550, 400), text_input="PLAY NOW", font=get_font(50), base_color=UoNblue,
                          hovering_color=wine)
        play_now.changeColor(play_now_mouse_pos)
        play_now.update(screen)
        # UonN IMAGE
        screen.blit(IMAGE, (0, 0))
        # username input box
        # create rectangle for username
        input_rect = pygame.Rect(550, 300, 140, 32)
        # gets active input box
        color_active = pygame.Color('lightskyblue3')
        # color of input box.
        color_passive = pygame.Color('bisque1')
        color = color_active if active else color_passive
        pygame.draw.rect(screen, color, input_rect, 2)
        # "Enter Username:" text
        enter_username_text = base_font.render("Enter Username:", True, (255, 255, 255))
        screen.blit(enter_username_text, (input_rect.x - 200, input_rect.y + 5))
        # username text
        username_surface = base_font.render(username, True, (0, 0, 0))
        screen.blit(username_surface, (input_rect.x + 20, input_rect.y + 5))
        # width of textfield so that text cannot get outside of user's text input
        input_rect.w = max(100, username_surface.get_width() + 10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if play_back.checkInput(play_mouse_pos):
                    main_menu()
                if play_now.checkInput(play_now_mouse_pos):
                    # name = read name from where they have typed
                    # if name is not empty
                    save_username(username)
                    main_game()
                # else
                # save_username(username)
                if input_rect.collidepoint(event.pos):
                    active = not active
            if event.type == pygame.KEYDOWN:
                if active:
                    # Check for backspace
                    if event.key == pygame.K_BACKSPACE:
                        # text input from 0 to -1 i.e. end.
                        username = username[:-1]
                        # Unicode standard string formation
                    else:
                        username += event.unicode
        pygame.display.update()

def options():
    pygame.display.set_caption("Play")
    while True:
        options_mouse_pos = pygame.mouse.get_pos()
        screen.fill(pink)
        options_text = get_font(50).render("User Instructions", True, UoNblue)
        options_rect = options_text.get_rect(center=(550, 200))
        screen.blit(options_text, options_rect)
        details = ("1. Arrange your tiles into sets of runs or groups of the same number to build melds \n"
                   "    on the table.\n"
                   "2. Each player must start their turn by drawing a tile, and then they can choose to\n"
                   "    manipulate existing melds or create new ones.\n"
                   "3. The first player to successfully empty their rack by playing all their tiles and shout \n   ""Rummikub"" wins the game, while unplayed tiles from opponents' racks \n"
                   "    contribute to their score.")
        naturalFont = pygame.font.SysFont('Arial', 25)
        instructions_text = naturalFont.render(details, True, UoNblue)
        instructions_rect = instructions_text.get_rect(midleft=(40, 350))
        # Split the text into lines and render each line separately
        lines = details.split('\n')
        for i, line in enumerate(lines):
            line_text = naturalFont.render(line, True, UoNblue)
            line_rect = line_text.get_rect(midleft=(40, 300 + i * 40))  # Adjust the vertical spacing as needed
            screen.blit(line_text, line_rect)
        options_back = Button(image=None, pos=(1035, 30), text_input="BACK", font=get_font(50), base_color=UoNblue,
                              hovering_color=wine)
        screen.blit(IMAGE, (0, 0))
        options_back.changeColor(options_mouse_pos)
        options_back.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if options_back.checkInput(options_mouse_pos):
                    main_menu()
        pygame.display.update()

# def play_now():
#     while True:

# # "PLAY NOW" text
# play_text =get_font(50).render("PLAY NOW", True, UoNblue)
# play_rect =play_text.get_rect(center =(550, 400))
# screen.blit(play_text, play_rect)
# "BACK" button
# play_now_back = Button(image =None, pos=(1035, 30), text_input ="BACK", font =get_font(50), base_color = UoNblue, hovering_color = wine)
# play_now_back.changeColor(play_now_mouse_pos)
# play_now_back.update(screen)

# Main menu screen
def main_menu():
    pygame.display.set_caption("Menu")
    while True:
        menu_mouse_pos = pygame.mouse.get_pos()
        screen.fill((0, 0, 230))
        menu_text = get_font(50).render("MAIN MENU", True, (240, 0, 50))
        menu_rect = menu_text.get_rect(center=(550, 100))
        play_button = Button(image=pygame.image.load("rectPLAY.png"), pos=(550, 250), text_input="PLAY",
                             font=get_font(50), base_color=(240, 0, 50), hovering_color="white")
        options_button = Button(image=pygame.image.load("rectOPTIONS.png"), pos=(550, 400), text_input="OPTIONS",
                                font=get_font(50), base_color=(240, 0, 50), hovering_color="white")
        quit_button = Button(image=pygame.image.load("rectQUIT.png"), pos=(550, 550), text_input="QUIT",
                             font=get_font(50), base_color=(240, 0, 50), hovering_color="white")
        screen.blit(IMAGE, (0, 0))
        screen.blit(menu_text, menu_rect)
        for button in [play_button, options_button, quit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(screen)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkInput(menu_mouse_pos):
                    play()
                if options_button.checkInput(menu_mouse_pos):
                    options()
                if quit_button.checkInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

# Main game loop
clock = pygame.time.Clock()
loading_progress = 0
loading_speed = 10
start_time = time.time()
current_screen = "loading"
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if event.type == pygame.MOUSEMOTION:
        pygame.display.set_caption(str(event.pos))
    if current_screen == "loading":
        run_game()
        loading_progress += loading_speed
        if loading_progress >= 600:
            loading_progress = 600
            if time.time() - start_time > 5:
                current_screen = "menu"
    elif current_screen == "menu":
        main_menu()
    pygame.display.flip()
    clock.tick(fps)

