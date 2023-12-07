import copy
import random

from game_logic import Pool, Player, GameBoard, AIPlayer, toggle_players

time_limit = 15


class GamePlay:
    def __init__(self):
        self.comp_tile_visible = False
        self.pool = Pool()
        self.comp_player = AIPlayer("Comp", self.pool.initial_tiles())
        self.player = Player("User", self.pool.initial_tiles())
        self.previous_state = self.player.rack_deep_copy()
        self.game_board = GameBoard()
        self.game_state = self.game_board.get_copy()
        self.drawn_tiles_from_pool = []
        self.remaining_tiles_in_pool = self.pool.remaining_tiles()
        self.invalid_position = []
        self.selected_rack_tile_index = None
        self.selected_game_board_tile_positions = None
        self.comp_random_time = 0
        self.running = True


        # position used for selecting tiles from board or rack e.g[0,1] = [row, col]
        self.selected_position = None
        self.timer = time_limit

    def assign_rack_positions(self):
        for i, tile in enumerate(self.player.rack.tiles):
            if tile is not None:
                tile.position[1] = i

        for i, tile in enumerate(self.comp_player.rack.tiles):
            if tile is not None:
                tile.position[1] = i

    def toggle_comp_tile_visible(self):
        self.comp_tile_visible = not self.comp_tile_visible

    def update_game_state(self, tile, row, col):
        self.game_state[row][col] = tile

    def remove_game_state_tile(self, row, col):
        self.game_state[row][col] = None

    def submit_game_state(self):
        validation = self.game_board.validate_board(self.game_state, self.player)
        return validation

    # select two tiles from pool
    def draw_tile_from_pool(self):
        self.drawn_tiles_from_pool = self.pool.draw_2_tiles()

    def reset_draw(self):
        self.remaining_tiles_in_pool = self.pool.remaining_tiles()
        self.drawn_tiles_from_pool = []

    def toggle_players(self):
        toggle_players(self.comp_player, self.player)
        if self.comp_player.turn:
            # adding few seconds random delay
            self.comp_random_time = random.randint(8, 10)
        else:
            self.starting_setup_for_user_turn()

        self.selected_position = None
        self.selected_game_board_tile_positions = None
        self.invalid_position = []
        self.update_timer()
        # self.previous_state = self.player.rack_deep_copy()

        print("RANDOM", self.comp_random_time, "User= ", self.player.turn, "AI= ", self.comp_player.turn)

    def delay_com_turn(self):
        if self.comp_random_time > 0:
            self.comp_random_time -= 1

    def copy_player_initial_state(self):
        self.player.rack.tiles = copy.deepcopy(self.previous_state)

    def updated_selected_tile_index(self, index):
        self.selected_rack_tile_index = index

    def updated_selected_tile_index_board(self, row, column):
        if row is None:
            self.selected_game_board_tile_positions = None
        else:
            self.selected_game_board_tile_positions = [row, column]

    def add_drawn_tile_to_rack_from_pool(self, selected_pool_tile_index):
        for target_index, player_tile in enumerate(self.player.get_tiles()):
            if player_tile is None:
                self.player.add_tile(self.drawn_tiles_from_pool[selected_pool_tile_index], target_index)

                if selected_pool_tile_index == 0:
                    self.pool.update_pool(self.drawn_tiles_from_pool[1])
                    break
                else:
                    self.pool.update_pool(self.drawn_tiles_from_pool[0])
                    break

    def add_1_tile_to_rack(self, tile):
        for target_index, player_tile in enumerate(self.player.get_tiles()):
            if player_tile is None:
                self.player.add_tile(tile, target_index)
                break

    def move_tile_on_board(self, initial_row, initial_col, target_row, target_col):
        self.game_state[target_row][target_col] = self.game_state[initial_row][initial_col]
        self.game_state[initial_row][initial_col] = None

    def starting_setup_for_user_turn(self):
        self.copy_player_initial_state()
        self.game_state = self.game_board.get_copy()

    def finalising_user_turn(self, validated):
        if not validated:
            self.game_state = self.game_board.get_copy()

    def user_timeout(self):
        self.copy_player_initial_state()
        self.add_1_tile_to_rack(self.pool.draw_1_tile())
        self.game_state = self.game_board.get_copy()

    def update_timer(self):
        if self.timer > 0:
            self.timer = self.timer - 1
        else:
            self.timer = time_limit

    def reset_timer(self):
        self.timer = 0
