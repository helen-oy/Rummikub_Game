from typing import List

import pygame.image
from pygame import Surface, Rect
from pygame import font

from game_play import GamePlay

screen_width = 1100
screen_height = 800

num_of_rows = 9
num_of_columns = 20

rack_num_rows = 2
rack_num_col = 20

rack_length = rack_num_rows * rack_num_col

game_board_center_x = screen_width * 0.5
game_board_center_y = screen_height * 0.5

playing_board_width = 0.8 * screen_width
playing_board_height = 0.60 * screen_height
tile_spacing = 2
tile_width = (playing_board_width / num_of_columns) - tile_spacing
tile_height = (playing_board_height / num_of_rows) - tile_spacing
screen_center_x = screen_width * 0.5
screen_center_y = screen_height * 0.5
show = False

circle_diameter = 65

path = ".././"
background = path+"board.png"
game_background = path+"background.jpg"
button = path+"b_4.png"
draw_button = path+"draw.png"
circle = path + "circle.png"
tile_image = path + "tile.png"
tile_error = path + "tile_error.png"
tile_selected = path + "tile_selected.png"



class GameRects:

    def __init__(self, game_play: GamePlay, game_font):
        self.game_play = game_play
        self.game_font = game_font

        self.comp_rack_position = GameRects.create_rack_positions(0.1)
        self.player_rack_position = GameRects.create_rack_positions(0.9)
        self.game_board_position = GameRects.create_board_surface()

        # Computer tiles - (surface, rect)
        self.comp_tiles_surfaces = []
        self.update_comp_tiles_surfaces()

        # Player tiles - (surface, rect)
        self.player_tiles_surfaces = []
        self.update_player_tiles_surfaces()

        # game board tiles- matrix of (surface, rects)
        self.game_board_tile_surfaces = []
        self.update_game_state_tiles_surfaces()

        # Creating show button for computer
        self.show_button = GameRects.show_tile_button_surface()

        # creating submit button
        self.submit_button = GameRects.submit_button()

        # Creating play for me button
        self.play_for_me = GameRects.play_for_me()

        # Creating draw tile button
        self.draw_tiles_button = GameRects.draw_tiles_button()

        # building tile drawn from pool

        self.drawn_pool_tiles_surfaces = []

        # Display remaining_tiles_number in pool
        self.remaining_tile_surface = GameRects.remaining_tile_button(self.game_play.remaining_tiles_in_pool, game_font)

        # Game board tiles - (surface, rect)
        # self.game_board_tile_surfaces = GameRects.create_board_surfaces(self.game_board_position.x,
        #                                                                 self.game_board_position.y,
        #                                                                 game_play.game_state,
        #                                                                 game_font)
        # self.pool_tile_rects = []


        # Creates game background
        self.game_background_surface = GameRects.create_game_background_surface()

        self.dict = {}
        # self.dict = GameRects.get_board_rect_dict(game_font,self.game_board_position.x, self.game_board_position.y, show_number=False )

    def update_game_state_tiles_surfaces(self):
        self.game_board_tile_surfaces = GameRects.create_board_surfaces(self.game_board_position.x,
                                                                        self.game_board_position.y,
                                                                        self.game_play.game_state,
                                                                        self.game_font, self.game_play.invalid_position, self.game_play.selected_game_board_tile_positions)

    def update_player_tiles_surfaces(self):
        self.player_tiles_surfaces: List[(Surface, Rect)] = GameRects.create_rack_surfaces(
            self.game_play.player.get_tiles(), self.game_font,
            self.player_rack_position[1].x, self.player_rack_position[1].y,
            selected_tile_rack_index=self.game_play.selected_rack_tile_index)

    def update_comp_tiles_surfaces(self):
        self.comp_tiles_surfaces: List[(Surface, Rect)] = GameRects.create_rack_surfaces(
            self.game_play.comp_player.get_tiles(),
            self.game_font,
            self.comp_rack_position[1].x, self.comp_rack_position[1].y,
            show_number=self.game_play.comp_tile_visible)

    def is_colliding_with_comp_rack(self, pos):
        if self.comp_rack_position[1].collidepoint(pos[0], pos[1]):
            return True
        else:
            return False

    def is_colliding_with_player_rack(self, pos):
        if self.player_rack_position[1].collidepoint(pos[0], pos[1]):
            return True
        else:
            return False

    def is_colliding_with_game_board(self, pos):
        if self.game_board_position.collidepoint(pos[0], pos[1]):
            return True
        else:
            return False

    def is_colliding_with_drawn_tile(self, pos):
        for i, tile in enumerate(self.drawn_pool_tiles_surfaces):
            print(tile)
            if tile[1].collidepoint(pos):
                return True

    def event_on_player_rack(self, pos):
        # for i, tile in enumerate(player_rack_surfaces):
        #     if tile[1].collidepoint(pos[0], pos[1]) and user_tiles[i] is not None:
        #         print("Selected tile")
        #         selected_tile_rack = self.game_play.g
        #         user_tile_index_number = i
        pass

    def get_comp_tiles_in_grid(self):
        pass

    def update_drawn_pool_tiles(self):
        self.drawn_pool_tiles_surfaces = GameRects.create_tile_drawn_from_pool(self.game_play.drawn_tiles_from_pool,
                                                                               self.game_font)

    def update_remaining_tiles(self):
        self.remaining_tile_surface = GameRects.remaining_tile_button(self.game_play.remaining_tiles_in_pool,self.game_font)

    def get_time(self):
        return GameRects.time_surface(self.game_play.timer, self.game_font)

    @classmethod
    def create_tile_drawn_from_pool(cls, tiles, game_font):
        surface = []
        for i, tile in enumerate(tiles):
            print(tile)
            tile_surface = build_tile(tile, game_font, True)
            tile_surface_rect = tile_surface.get_rect()
            tile_surface_rect.topleft = (screen_width * 0.03, screen_height * 0.70 + (i * tile_height))
            surface.append((tile_surface, tile_surface_rect))

        return surface

    @classmethod
    def create_rack_surfaces(cls, tiles, game_font, rack_x, rack_y, show_number=True, selected_tile_rack_index=None):
        surfaces = []
        length = len(tiles)
        tiles.extend([None] * (40 - length))
        for i in range(rack_length):
            selected_tile_rack = False
            if selected_tile_rack_index == i:
                selected_tile_rack = True
            col = i % num_of_columns
            row = 0
            if i > 19:
                row = 1
            tile_surface = build_tile(tiles[row * rack_num_col + col], game_font, show_number=show_number,
                                      selected_tile_rack=selected_tile_rack)
            x_pos = rack_x + (col * tile_width) + 1 + (col * 2)
            y_pos = rack_y + (row * tile_height) + 7 + (row * 2)
            rect = tile_surface.get_rect()
            rect.topleft = (x_pos, y_pos)
            surfaces.append((tile_surface, rect))
        return surfaces

    @classmethod
    def create_rack_positions(cls, y_position):
        rack_surface = Surface((0.8 * screen_width, 0.15 * screen_height))
        rack_surface_rect = rack_surface.get_rect()
        rack_surface_rect.center = (screen_width * 0.5, screen_height * y_position)
        return rack_surface, rack_surface_rect

    @classmethod
    def create_board_surfaces(cls, playing_board_x, playing_board_y, game_state, game_font, invalid_position, selected_tile_board_indices):
        rect = []
        print("true", invalid_position, "iram")
        for i in range(num_of_rows):
            grid_rect = []
            for j in range(num_of_columns):
                show_error_tile = False
                selected_tile_board = False
                if f"{i},{j}" in invalid_position:
                    show_error_tile = True
                if selected_tile_board_indices is not None and selected_tile_board_indices == [i,j]:
                    selected_tile_board = True



                tile = game_state[i][j]
                tile_surface = build_tile(tile, game_font, show_error=show_error_tile, selected_tile_rack_borad = selected_tile_board )
                # tile_surface.fill((150, 75, 0))
                # alpha = 50
                x_position = playing_board_x + 1 + (j * (tile_width + tile_spacing))
                y_position = playing_board_y + 1 + (i * (tile_height + tile_spacing))
                position = tile_surface.get_rect()
                position.topleft = (x_position, y_position)
                grid_rect.append((tile_surface, position))
            rect.append(grid_rect)
        return rect

    @classmethod
    def create_board_surface(cls):
        playing_board_surface = pygame.image.load(background)
        playing_board_rect = playing_board_surface.get_rect()
        playing_board_rect.center = (game_board_center_x, game_board_center_y)
        # screen.blit(playing_board_surface, playing_board_rect)
        # return playing_board_surface, playing_board_rect
        return playing_board_rect

    @classmethod
    def create_game_background_surface(cls):
        playing_board_surface = pygame.image.load(game_background)
        return playing_board_surface

    @classmethod
    def show_tile_button_surface(cls):
        show_tile = Surface((35, 35))
        show_tile.fill((0, 0, 0))
        game_font_size_8 = font.SysFont('arial', 8, bold=True)
        text = game_font_size_8.render("Show tile", True, (255, 0, 255))
        text_rect = text.get_rect()
        text_rect.topleft = (0, 35 * 0.2)
        show_tile_rect = show_tile.get_rect()
        show_tile_rect.topleft = (screen_width * 0.93, screen_height * 0.07)
        show_tile.blit(text, text_rect)
        return show_tile, show_tile_rect

    @classmethod
    def submit_button(cls):
        submit_surface = Surface((35, 35))
        submit_surface.fill((0, 0, 0))
        submit_button_rect = submit_surface.get_rect()
        submit_button_rect.topleft = (screen_width * 0.93, screen_height * 0.92)
        game_font_size_10 = font.SysFont('arial', 10, bold=True)
        text = game_font_size_10.render("submit", True, (255, 0, 255))
        text_rect = text.get_rect()
        text_rect.topleft = (0, 35 * 0.2)
        submit_surface.blit(text, text_rect)

        return submit_surface, submit_button_rect

    @classmethod
    def play_for_me(cls):
        play_me_surface = Surface((35, 35))
        play_me_surface.fill((0, 0, 0))
        play_me_rect = play_me_surface.get_rect()
        play_me_rect.topleft = (screen_width * 0.93, screen_height * 0.85)
        game_font_size_10 = font.SysFont('arial', 10, bold=True)
        text = game_font_size_10.render("Auto Play", True, (255, 0, 255))
        text_rect = text.get_rect()
        text_rect.topleft = (0, 35 * 0.2)
        play_me_surface.blit(text, text_rect)
        return play_me_surface, play_me_rect

    @classmethod
    def draw_tiles_button(cls):
        draw_tile_surface = pygame.image.load(draw_button)

        # draw_tile_surface = Surface((40, 40))
        # draw_tile_surface.fill((0, 0, 0))
        draw_tile_surface_rect = draw_tile_surface.get_rect()
        draw_tile_surface_rect.topleft = (screen_width * 0.03, screen_height * 0.55)
        # game_font_size_10 = font.SysFont('arial', 10, bold=True)
        # text = game_font_size_10.render("Draw Tile", True, (255, 0, 255))
        # text_rect = text.get_rect()
        # text_rect.topleft = (0, 35 * 0.2)
        # draw_tile_surface.blit(text, text_rect)
        return draw_tile_surface, draw_tile_surface_rect

    @classmethod
    def remaining_tile_button(cls, remaining_tile, font):
        img = font.render(str(remaining_tile), True, (255, 255, 0))
        img_rect = img.get_rect()
        img_rect.center = ((screen_width - playing_board_width) / 4, screen_height / 2)
        return img, img_rect

    @classmethod
    def time_surface(cls, time, game_font):
        time_surface = pygame.image.load(circle)
        time_rect = time_surface.get_rect()
        time_rect.center = (screen_width * 0.95, screen_height / 2)
        text = game_font.render(str(time), True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (circle_diameter * 0.5, circle_diameter * 0.5)
        time_surface.blit(text, text_rect)

        return time_surface, time_rect



def build_tile(tile, font, show_number=True, show_error=False, selected_tile_rack=False, selected_tile_rack_borad = False):
    tile_surface = Surface((42, 50), pygame.SRCALPHA)
    tile_surface = tile_surface.convert_alpha()
    tile_surface.fill((0, 0, 0, 100))
    if tile is not None:
        tile_surface = pygame.image.load(tile_image)
        if show_error:
            tile_surface = pygame.image.load(tile_error)
        if selected_tile_rack:
            tile_surface = pygame.image.load(tile_selected)
        if selected_tile_rack_borad:
            tile_surface = pygame.image.load(tile_selected)


        tile_surface = pygame.transform.scale(tile_surface, (42, 50))
        number = str(tile.value)
        if not show_number:
            number = ""

        text_surface = font.render(number, True, tile.color)
        text_rect = text_surface.get_rect()
        text_rect.center = (42 * 0.5, 50 * 0.4)
        # tile_surface.fill((255, 180, 255))
        tile_surface.blit(text_surface, text_rect)
    return tile_surface
