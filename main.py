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
