from pygame import Surface, MOUSEBUTTONDOWN, MOUSEBUTTONUP, draw, mouse
from pygame import event
from pygame import QUIT
from pygame import init
from pygame import display
from pygame import time
from game_components import build_tile, GameRects, rack_length, screen_width, \
    screen_height, num_of_rows, num_of_columns, playing_board_width
from game_components import tile_height
from pygame import font
from game_logic import Tile
import pygame
from game_play import GamePlay
from game_events import GameEvents

# initialization of game loading pages.
pygame.init()


#create game window
SCREEN_WIDTH =1100
SCREEN_HEIGHT = 800

#define colors
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
purple =(125, 0, 125)
wine =(240, 0, 50)
blue = (0, 0, 255)
pink =(238,162,173)
UoNblue =(25,12,112)
beige =(255,211,155)

#define rectangle
x = 200
y = 450


#define fonts
font =pygame.font.Font('Milk And Honey.ttf', 100)
regularFont = pygame.font.Font('Sweet Vusstain.ttf', 65)

#screens and captions
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("First display page")


#sounds and effects.
sound= pygame.mixer.Sound('Dave-Ft-Burna-Boy-Location.mp3')


#define fonts
font =pygame.font.Font('Milk And Honey.ttf', 100)
regularFont = pygame.font.Font('Sweet Vusstain.ttf', 65)
loading_font =pygame.font.Font(None, 36)

#define clock
clock = pygame.time.Clock()
fps = 60

IMAGE = pygame.image.load('UoNLogo.png')
IMAGE = pygame.transform.scale_by(IMAGE, 0.4)

#create a text surface object
text =font.render("Rummikub", True, red)

#create rectangular object for text
textRect = text.get_rect()

#set the center of the rectangular object 
textRect.center =(SCREEN_WIDTH//2,SCREEN_HEIGHT//2-50)


#Resume text to show start of game after loading:
finished = regularFont.render("Start Game", True, "purple")
finished_rect = finished.get_rect(center=(550, 400))


def get_font(size):
    return pygame.font.Font('Sweet Vusstain.ttf', size)


def run_game():
    
    #render text
    pygame.display.set_caption("initialize game")
    
    screen.fill((0, 0, 230))
    
    IMAGE = pygame.image.load('UoNLogo.png')
    IMAGE = pygame.transform.scale_by(IMAGE, 0.4)
    
    text =font.render("Rummikub", True, red) 
    textRect = text.get_rect()
    textRect.center =(SCREEN_WIDTH//2,SCREEN_HEIGHT//2-50)
    
    screen.blit(IMAGE,(0,0))
    screen.blit(text, textRect)
    
    #Loading bar
    pygame.draw.rect(screen, pygame.Color('yellow'), (250, 450, 100, 10), border_radius =5)
    pygame.draw.rect(screen, pygame.Color('yellow'), (250, 450,loading_progress, 10), border_radius =5)
    
    
    #loading text
    loading_text = loading_font.render("Loading ...", True, wine)
    loading_rect = loading_text.get_rect(center = (SCREEN_WIDTH//2, 435))
    screen.blit(loading_text, loading_rect)
    
#Play Screen    
def play(): 
    pygame.display.set_caption("Play")
    
    while True:
        
        play_mouse_pos = pygame.mouse.get_pos()
        
        screen.fill(beige)
        
        play_text =get_font(50).render("PLAY NOW", True, UoNblue)
        play_rect =play_text.get_rect(center =(550, 400))
        screen.blit(play_text, play_rect)
        
        play_back = Button(image =None, pos=(1035, 30), text_input ="BACK", font =get_font(50), base_color = UoNblue, hovering_color = wine)
        
        screen.blit(IMAGE,(0,0))
        
        play_back.changeColor(play_mouse_pos)
        play_back.update(screen)
        
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
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
        
        options_text =get_font(50).render("User Instructions", True, UoNblue)
        options_rect =options_text.get_rect(center =(550, 200))
        screen.blit(options_text, options_rect)
        details = ("1. Arrange your tiles into sets of runs or groups of the same number to build melds \n" 
                   "    on the table.\n"
                   "2. Each player must start their turn by drawing a tile, and then they can choose to\n"
                   "    manipulate existing melds or create new ones.\n"
                   "3. The first player to successfully empty their rack by playing all their tiles and shout \n   ""Rummikub"" wins the game, while unplayed tiles from opponents' racks \n"
                   "    contribute to their score.")
        
        naturalFont = pygame.font.SysFont('Arial', 25)
        
        instructions_text = naturalFont.render(details, True, UoNblue)
        instructions_rect = instructions_text.get_rect(midleft =(40,350))

        # Split the text into lines and render each line separately
        lines = details.split('\n')
        for i, line in enumerate(lines):
            line_text = naturalFont.render(line, True, UoNblue)
            line_rect = line_text.get_rect(midleft=(40, 300 + i * 40))  # Adjust the vertical spacing as needed
            screen.blit(line_text, line_rect)
        
    
        
        options_back = Button(image =None, pos=(1035, 30), text_input ="BACK", font =get_font(50), base_color = UoNblue, hovering_color = wine)
        
        screen.blit(IMAGE,(0,0))
        
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

        
    
    #Main menu screen
def main_menu():
    pygame.display.set_caption("Menu")
                           
    while True:
        
        menu_mouse_pos = pygame.mouse.get_pos()
        
        screen.fill((0, 0, 230))
        
        menu_text = get_font(50).render("MAIN MENU", True,(240, 0, 50))
        menu_rect = menu_text.get_rect(center=(550, 100))
        
        play_button = Button(image =pygame.image.load("rectPLAY.png"), pos =(550,250), text_input ="PLAY", font = get_font(50), base_color = (240, 0, 50), hovering_color= "white")
        options_button  = Button(image =pygame.image.load("rectOPTIONS.png"), pos =(550,400), text_input ="OPTIONS", font =get_font(50), base_color = (240, 0, 50), hovering_color= "white")
        quit_button = Button(image =pygame.image.load("rectQUIT.png"), pos =(550,550), text_input ="QUIT", font =get_font(50), base_color = (240, 0, 50), hovering_color= "white")
        
        screen.blit(IMAGE,(0,0))
        
        
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



init()
screen = display.set_mode((screen_width, screen_height))
clock = time.Clock()
game_font = font.SysFont('arial', 30, bold=True)

game_play = GamePlay()
game_surfaces = GameRects(game_play, game_font)
game_events = GameEvents(game_play, game_surfaces)

# FIX THIS
pick_tile = game_play.pool.draw_2_tiles()
remaining_tiles = game_play.pool.remaining_tiles()

running = True
while running:

    # Creating user and player rack surfaces rects
    user_player_rack = game_surfaces.player_rack_position
    comp_player_rack = game_surfaces.comp_rack_position

    screen.blit(user_player_rack[0], user_player_rack[1])
    screen.blit(comp_player_rack[0], comp_player_rack[1])

    game_background = game_surfaces.game_background_surface
    screen.blit(game_background, (0, 0))

    show_button = game_surfaces.show_button
    screen.blit(show_button[0], show_button[1])

    user_player = game_play.player
    computer_player = game_play.comp_player

    user_tiles = user_player.get_tiles()
    computer_tiles = computer_player.get_tiles()

    # Creating circle for pool
    pool_surface = draw.circle(screen, (0, 0, 0), ((screen_width - playing_board_width) / 4, screen_height / 2), 30)

    game_state = game_play.game_state

    # Creating tile in racks
    comp_rack_surfaces = game_surfaces.comp_tiles_surfaces
    player_rack_surfaces = game_surfaces.player_tiles_surfaces

    for i in range(rack_length):
        comp_rack_tile = comp_rack_surfaces[i]
        screen.blit(source=comp_rack_tile[0], dest=comp_rack_tile[1])

        player_rack_tile = player_rack_surfaces[i]
        screen.blit(source=player_rack_tile[0], dest=player_rack_tile[1])

    # Creating grid rects in playing board
    playing_board_tiles_surfaces = game_surfaces.game_board_tile_surfaces
    for i in range(num_of_rows):
        for j in range(num_of_columns):
            playing_grid = playing_board_tiles_surfaces[i][j]
            screen.blit(source=playing_grid[0], dest=playing_grid[1])

    # Tile drawing from pool for user player
    if game_play.comp_tile_visible:
        temp_tiles = []
        for i in range(len(computer_tiles)):
            temp_tiles.append(Tile(0, (255, 255, 255)))
    else:
        temp_tiles = computer_tiles
    # class for player which creates 140 tile, some of them are empty, it have 14 cells

    # # Creating Tiles on gameboard
    # matrix_tile_rect = []
    # for i in range(num_of_rows):
    #     tile_rect = []
    #     for j in range(num_of_columns):
    #         if game_state[i][j] != None:
    #             tile_surface = build_tile(game_state[i][j], game_font)
    #             x_position = playing_board_x + 1 + (j * (tile_width + tile_spacing))
    #             y_position = playing_board_y + 1 + (i * (tile_height + tile_spacing))
    #             tile_rect1 = tile_surface.get_rect().move(x_position, y_position)
    #             screen.blit(tile_surface, (x_position, y_position))
    #             tile_rect.append(tile_rect1)
    #         else:
    #             tile_rect.append(None)
    #     matrix_tile_rect.append(tile_rect)

    # Rendring remaining tile on pool circle
    font = pygame.font.SysFont('arial', 20)
    img = font.render(str(remaining_tiles), True, (255, 255, 0))
    img_rect = img.get_rect()
    img_rect.center = ((screen_width - playing_board_width) / 4, screen_height / 2)
    screen.blit(img, img_rect)

    for e in event.get():
        if e.type == QUIT:
            running = False

        if e.type == MOUSEBUTTONUP:
            pos = mouse.get_pos()

            game_events.handle_events(pos)

    # show pick tile
    for i in range(2):
        tile_surface = build_tile(pick_tile[i], game_font)
        screen.blit(tile_surface, (pool_surface.x + 5, (i * tile_height) + pool_surface.y + 63))

    display.update()
