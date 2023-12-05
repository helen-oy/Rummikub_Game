from game_logic import Pool, Player, GameBoard, AIPlayer


class GamePlay:
    def __init__(self):
        self.comp_tile_visible = False
        self.pool = Pool()
        self.comp_player = AIPlayer("Comp", self.pool.initial_tiles())
        self.player = Player("User", self.pool.initial_tiles())
        self.game_board = GameBoard()
        self.game_state = self.game_board.get_copy()
        self.drawn_tiles_from_pool = []
        self.remaining_tiles_in_pool = self.pool.remaining_tiles()

        # position used for selecting tiles from board or rack e.g[0,1] = [row, col]
        self.selected_position = None

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

    #select two tiles from pool
    def draw_tile_from_pool(self):
        self.drawn_tiles_from_pool = self.pool.draw_2_tiles()

    def reset_draw(self):
        self.remaining_tiles_in_pool = self.pool.remaining_tiles()
        self.drawn_tiles_from_pool = []












def move_tile_on_board(self, initial_row, initial_col, target_row, target_col):
    self.game_state[target_row][target_col] = self.game_state[initial_row][initial_col]
    self.game_state[initial_row][initial_col] = None

