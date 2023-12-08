
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

def gameover(winner):
    pygame.display.set_caption("Gameover")

    while True:

        gameover_mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(maroon)

        IMAGE = pygame.image.load('UoNLogo.png')
        IMAGE = pygame.transform.scale_by(IMAGE, 0.4)

        screen.blit(IMAGE,(0,0))


        # BACK BUTTON
        gameover_back = Button(image =None, pos=(1035, 30), text_input ="BACK", font =get_font(50), base_color = UoNblue, hovering_color = wine)
        gameover_back.changeColor(gameover_mouse_pos)
        gameover_back.update(screen)

        # quit button
        gameover_quit= Button(image =pygame.image.load("rectQUIT.png"), pos =(550,550), text_input ="QUIT", font =get_font(50), base_color = (240, 0, 50), hovering_color= "white")
        gameover_quit.changeColor(gameover_mouse_pos)
        gameover_quit.update(screen)

        gameover_mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                    if gameover_back.checkInput(gameover_mouse_pos):
                        from GUI_Rummikub_game import main_menu
                        main_menu()
                    if gameover_quit.checkInput(gameover_mouse_pos):
                                pygame.quit()
                                sys.exit()


        # Display congratulations and Gameover  message based on the winner

        if  winner == "computer_player":
            gameover_text = font.render("GAME OVER !!!", True, UoNblue)
            congrats_text = get_font(60).render("You lost! \n"
                                                "Computer player won!\n", True, (255,211,155) )
        elif winner == "user player":
            username == load_username()
            gameover_text = font.render("GAME OVER !!!", True, UoNblue)
            congrats_text = get_font(60).render(f"Congratulations! \n"
                                                f"{username} won!\n", True, (255,211,155) )
        else:
            gameover_text = font.render("GAME OVER !!!",True, UoNblue)
            congrats_text = get_font(60).render("It's a draw! Do you want to play again? Return to main menu", True, (255,211,155) )

        gameover_rect = gameover_text.get_rect(center=(550,300))
        screen.blit(gameover_text, gameover_rect)

        congrats_rect = congrats_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(congrats_text, congrats_rect)

        pygame.display.update()

