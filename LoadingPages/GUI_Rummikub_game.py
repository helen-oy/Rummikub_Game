#!/usr/bin/env python
# coding: utf-8

# In[1]:


# pip install pygame


# In[1]:


# MAIN
# references
# fonts from dafont.com
# https://www.pygame.org/
# https://youtu.be/_D-_OmR36Pk?si=L24aue5dqPrN-_5D

import pygame, sys, threading, time, math
from pygame.locals import *
from button import Button
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

# define rectangle
x = 200
y = 450

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


def get_font(size):
    return pygame.font.Font('Sweet Vusstain.ttf', size)


def run_game():
    # render text
    pygame.display.set_caption("initialize game")

    screen.fill((0, 0, 230))

    IMAGE = pygame.image.load('UoNLogo.png')
    IMAGE = pygame.transform.scale_by(IMAGE, 0.4)

    text = font.render("Rummikub", True, red)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)

    screen.blit(IMAGE, (0, 0))
    screen.blit(text, textRect)

    # Loading bar
    pygame.draw.rect(screen, pygame.Color('yellow'), (250, 450, 100, 10), border_radius=5)
    pygame.draw.rect(screen, pygame.Color('yellow'), (250, 450, loading_progress, 10), border_radius=5)

    # loading text
    loading_text = loading_font.render("Loading ...", True, wine)
    loading_rect = loading_text.get_rect(center=(SCREEN_WIDTH // 2, 435))
    screen.blit(loading_text, loading_rect)


# Play Screen
def play():
    pygame.display.set_caption("Play")

    while True:

        play_mouse_pos = pygame.mouse.get_pos()

        screen.fill(beige)

        play_text = get_font(50).render("PLAY NOW", True, UoNblue)
        play_rect = play_text.get_rect(center=(550, 400))
        screen.blit(play_text, play_rect)

        play_back = Button(image=None, pos=(1035, 30), text_input="BACK", font=get_font(50), base_color=UoNblue,
                           hovering_color=wine)

        screen.blit(IMAGE, (0, 0))

        play_back.changeColor(play_mouse_pos)
        play_back.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if play_back.checkInput(play_mouse_pos):
                    main_menu()

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

    # Main menu screen


def main_menu():
    pygame.display.set_caption("Menu")

    # while True:

    menu_mouse_pos = pygame.mouse.get_pos()

    screen.fill((0, 0, 230))

    menu_text = get_font(50).render("MAIN MENU", True, (240, 0, 50))
    menu_rect = menu_text.get_rect(center=(550, 100))

    play_button = Button(image=pygame.image.load("rectPLAY.png"), pos=(550, 250), text_input="PLAY", font=get_font(50),
                         base_color=(240, 0, 50), hovering_color="white")
    options_button = Button(image=pygame.image.load("rectOPTIONS.png"), pos=(550, 400), text_input="OPTIONS",
                            font=get_font(50), base_color=(240, 0, 50), hovering_color="white")
    quit_button = Button(image=pygame.image.load("rectQUIT.png"), pos=(550, 550), text_input="QUIT", font=get_font(50),
                         base_color=(240, 0, 50), hovering_color="white")

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
                main_game()
            if options_button.checkInput(menu_mouse_pos):
                options()
            if quit_button.checkInput(menu_mouse_pos):
                pygame.quit()
                sys.exit()



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

        if event.type == pygame.KEYDOWN:
            if event.type == pygame.K_SPACE:
                pass
                # sound.play()

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

# In[ ]:


# In[ ]:


# In[ ]:


# In[ ]:
