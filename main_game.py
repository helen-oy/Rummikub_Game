import pygame
from pygame import MOUSEBUTTONUP, mouse
from pygame import QUIT
from pygame import display
from pygame import event
from pygame import init
from pygame import time

from game_components import GameRects, rack_length, screen_width, \
    screen_height, num_of_rows, num_of_columns
from game_events import GameEvents, every_second_timer_tick_event
from game_logic import Tile
from game_play import GamePlay

init()

def main_game():
    screen = display.set_mode((screen_width, screen_height))

    game_font = pygame.font.SysFont('arial', 30, bold=True)
    game_play = GamePlay()
    game_surfaces = GameRects(game_play, game_font)
    game_events = GameEvents(game_play, game_surfaces)

    user_player = game_play.player
    computer_player = game_play.comp_player

    user_player.turn = True  # testing purposes. Implement toss here
    # computer_player.is_greater_30 = True  # testing purposes
    # user_player.is_greater_30 = True  # testing purposes

    time.set_timer(every_second_timer_tick_event, 1000)

    while game_play.running:

        # Creating user and player rack surfaces rects
        user_player_rack = game_surfaces.player_rack_position
        comp_player_rack = game_surfaces.comp_rack_position

        screen.blit(user_player_rack[0], user_player_rack[1])
        screen.blit(comp_player_rack[0], comp_player_rack[1])

        game_background = game_surfaces.game_background_surface
        screen.blit(game_background, (0, 0))

        game_play.assign_rack_positions()

        user_tiles = user_player.get_tiles()
        computer_tiles = computer_player.get_tiles()

        game_state = game_play.game_state

        # Creating tile in racks
        comp_rack_surfaces = game_surfaces.comp_tiles_surfaces
        player_rack_surfaces = game_surfaces.player_tiles_surfaces

        show_button = game_surfaces.show_button
        screen.blit(show_button[0], (show_button[1]))

        submit_button = game_surfaces.submit_button
        screen.blit(submit_button[0], submit_button[1])

        play_for_me = game_surfaces.play_for_me
        screen.blit(play_for_me[0], play_for_me[1])

        draw_tiles_button = game_surfaces.draw_tiles_button
        screen.blit(draw_tiles_button[0], draw_tiles_button[1])

        draw_tile_build = game_surfaces.drawn_pool_tiles_surfaces
        for tile in draw_tile_build:
            screen.blit(tile[0], tile[1])

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
        remaining_tiles_surface = game_surfaces.remaining_tile_surface
        screen.blit(remaining_tiles_surface[0], remaining_tiles_surface[1])

        time_surface = game_surfaces.get_time()
        screen.blit(time_surface[0], time_surface[1])

        if game_play.player.turn == True:
            user_icon = game_surfaces.user_icon_surface()
            screen.blit(user_icon[0], user_icon[1])

        if game_play.comp_player.turn == True:
            comp_icon = game_surfaces.comuter_icon()
            screen.blit(comp_icon[0], comp_icon[1])

        quit_icon = game_surfaces.quit_surface()
        screen.blit(quit_icon[0], quit_icon[1])

        if game_play.show_error_prompt == True:
            error_prompt = game_surfaces.error_prompt_surface()
            screen.blit(error_prompt[0], error_prompt[1])

        # Rendring remaining tile on pool circle
        for e in event.get():
            if e.type == QUIT:
                game_play.running = False

            if e.type == MOUSEBUTTONUP:
                pos = mouse.get_pos()
                game_events.handle_events(pos)

            if e.type == every_second_timer_tick_event:
                game_events.handle_countdown_event()

        # text = game_font.render(str(game_play.comp_random_time), True, (255, 255, 255))
        # screen.blit(text, (0, 0))


        display.update()


main_game()
