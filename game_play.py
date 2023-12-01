from game_logic import Pool, Player, GameBoard


class GamePlay:
    def __init__(self):
        self.comp_tile_visible = False
        self.pool = Pool()
        self.comp_player = Player("Comp", self.pool.initial_tiles())
        self.player = Player("User", self.pool.initial_tiles())
        self.game_board = GameBoard()
        self.game_state = self.game_board.get_copy()
        # position used for selecting tiles from board or rack e.g[0,1] = [row, col]
        self.selected_position = None

    def toggle_comp_tile_visible(self):
        self.comp_tile_visible = not self.comp_tile_visible

    def update_game_state(self, tile, row, col):
        self.game_state[row][col] = tile

    def remove_game_state_tile(self, row, col):
        self.game_state[row][col] = None

    def submit_game_state(self):
        self.game_board.validate_board(self.game_state, self.player)

    def move_tile_on_board(self, initial_row, initial_col, target_row, target_col):
        self.game_state[target_row][target_col] = self.game_state[initial_row][initial_col]
        self.game_state[initial_row][initial_col] = None
