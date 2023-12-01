import random
import copy

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
BLUE = (0, 0, 180)
RED = (180, 0, 0)
GREEN = (0, 180, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (128, 0, 128)


# screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Tile:
    def __init__(self, value, color):
        self.value = value
        self.color = color

# Classes
class Pool:
    def __init__(self):  # Ideally the pool starts with a pool with all 150 tiles
        self.tiles = []
        self.init_pool()

    def init_pool(self):
        tile_colors = [RED, BLUE, GREEN, BLACK, PURPLE]  # modified to incorporate RGB combinations
        self.tiles = [Tile(i % 15 + 1, t) for i in range(30) for t in tile_colors]
        random.shuffle(self.tiles)

    def remaining_tiles(self):
        return len(self.tiles)

    def initial_tiles(
            self):  # what I think is to remove rack frm here, then the rack will call this method to add tiles
        # I see it can potentially create problems..
        # why 14 tiles not 16
        send_tiles = [self.tiles.pop(random.randrange(len(self.tiles))) for _ in range(14)]
        send_tiles = send_tiles + [None] * (40 - len(send_tiles))
        return send_tiles

    def draw_2_tiles(self):
        selected_tiles = [self.tiles.pop(random.randrange(len(self.tiles))) for _ in range(2)]
        tile1 = selected_tiles[0]
        tile2 = selected_tiles[1]

        return [tile1, tile2]


class Rack:
    def __init__(self, tiles):
        self.tiles = tiles

    def initial_tiles(self, pool):
        # This take tiles that were expelled by the pool
        # The pool will intialized as an instance of class Pool
        self.tiles.extend(pool.initial_tiles())
        return (self.tiles)

    def sort_tiles(self):
        odd_tiles = [tile for tile in self.tiles if tile.value % 2 != 0]
        even_tiles = [tile for tile in self.tiles if tile.value % 2 == 0]
        # return odd_tiles, even_tiles
        # before putting them together, lets sort them by value and color
        odd_tiles = sorted(odd_tiles, key=lambda x: (x.value, x.color))
        even_tiles = sorted(even_tiles, key=lambda x: (x.value, x.color))
        return odd_tiles + even_tiles  # i think they should be joined,!!

    # def move_tile(self, tile_number):  # is this the tile that is going to be played?
    #     for i, tile in enumerate(self.tiles):
    #         if tile.number == tile_number:
    #             moved_tile = self.tiles.pop(i)
    #             return moved_tile
    #     return None
    def remove_tile(self, position):
        self.tiles[position] = None

    def add_tile(self, tile, position):
        self.tiles[position] = tile


#     # def remove_picked_tiles(self):
#     #     for _ in range(picked_tiles):
#     #         self.tiles.pop()
#     #     return self.tiles
# # Crate an instance of Pool object to be used by players

class Player:
    def __init__(self, name, tiles):
        self.rack = Rack(tiles)
        self.name = name

    def initial_tiles(self, pool):
        return self.rack.initial_tiles(pool)

    def sort_tiles(self):
        self.rack.sort_tiles()

    def remove_tile(self, position):
        self.rack.remove_tile(position)

    def add_tile(self, tile, position):
        self.rack.add_tile(tile, position)

    def get_tiles(self):
        return self.rack.tiles


# bukayo = Player('Bukayo Saka')
##  This needs a game board
class ValidMoves:
    def __init__(self, board):
        self.board = board

    # validate player moves
    def is_run(self):
        if 3 <= len(self.player.run) <= 5:
            if all(j.value % 2 == 0 for _, j in enumerate(self.player.run)):
                if all(self.player.run[i + 1].value - self.player.run[i].value == 2 for i, _ in
                       enumerate(self.player.run[:-1])):
                    return True
                else:
                    return False

    def is_group(self):
        if 3 <= len(self.player.run) <= 5:
            if all(i == j for i, j in zip(self.player.run, self.player.run)):
                if all(self.player.run[i + 1].color != self.player.run[i] for i, j in enumerate(self.player.run[:-1])):
                    pass
                ## to be completed


class GameBoard:
    # rect (left/x, top/y, width, height)
    def __init__(self):
        self.board = []  # initialise the game board as an empty list.
        self.rows, self.columns = 9, 20
        for i in range(self.rows):
            new_row = []
            for j in range(self.columns):
                new_row.append(None)
            self.board.append(new_row)

    def validate_board(self, game_board, current_player):
        # game_board is the current state of the gameboard - a 9 by 20 matrix of tile objects passed in from frontend.
        # current_player is the player whose turn it is. we need to check if they have played 30 points or not

        # this function returns a list [boolean, list]
        # the boolean let's us know if the board is valid or not
        # the list contains each position of the tiles on the board that form invalid game play.

        invalid_positions = []
        status = True
        tile_pos = {}
        i, j = 0, 0

        for each_row in game_board:  # outer loop, checks each row
            set = []  # store our runs and groups
            for element in each_row:  # checks each space/element in that row
                if element != None:
                    set.append(element)  # add that tile to our set
                    tile_pos[element] = str(i) + "," + str(j)

                if element == None:  # if the current element in the row is an empty space
                    if set:  # if set is not empty by the time we run into an empty space
                        is_valid = is_valid_move(current_player, set)  # check if it is a valid group or run
                        if is_valid == False:  # if the move is not valid, add the positions of all invalid tiles to invalid positions
                            status = False
                            for tile in set:
                                invalid_positions.append(tile_pos[tile])
                            set = []  # clear set for the next sets.
                        else:
                            set = []  # if the move was valid, set only clear set.
                j += 1  # update the column position as we move through the row.

            if set:  # if the set is not empty after we reach the end of the row
                is_valid = is_valid_move(current_player, set)  # check if it is a valid group or run
                if is_valid == False:  # if the move is not valid, add the positions of all invalid tiles to invalid positions
                    status = False
                    for tile in set:
                        invalid_positions.append(tile_pos[tile])
                    set = []  # clear set for the next sets.
                else:
                    set = []  # if the move was valid, set should be reset
            i += 1  # update the row position as we move through the board

        if status:  # if thr board is valid, update the gameboard
            self.board = copy.deepcopy(game_board)

        return [status, invalid_positions]

    def get_copy(self):
        return copy.deepcopy(self.board)


def is_valid_move(current_player, list_of_tiles):
    # Checking if it is a run even/odd
    if 3 <= len(list_of_tiles) <= 5:
        all_odd_or_even = all(t.value % 2 == 0 for t in list_of_tiles) or all(t.value % 2 != 0 for t in list_of_tiles)
        diff_2 = all(list_of_tiles[i + 1].value - list_of_tiles[i].value == 2 for i in range(len(list_of_tiles) - 1))
        same_color = all(list_of_tiles[i + 1].color == list_of_tiles[i].color for i in range(len(list_of_tiles) - 1))
        # Checking if the list meet all conditions to be a run
        run = all_odd_or_even and diff_2 and same_color
        if run:
            if current_player.is_greater_30 == False:
                valid = is_more_than_30(list_of_tiles)
                if valid:
                    current_player.is_greater_30 = True
                return valid
            else:
                return run
        else:  # Check whether it is a group
            same_value = all(
                list_of_tiles[i + 1].value == list_of_tiles[i].value for i in range(len(list_of_tiles) - 1))
            different_color = len(set([t.color for t in list_of_tiles])) == len(list_of_tiles)
            group = same_value and different_color
            if current_player.is_greater_30 == False:
                valid = is_more_than_30(list_of_tiles)
                if valid:
                    current_player.is_greater_30 = True
                return valid
            else:
                return group
    else:
        return False

    # If it is the players turn for the first attempt to play, the board is valid if total value for sets or runs or both
    # only if sum is >30
    # This fucnction must be implemented jointly implemented with `is_valid_move` that is, both conditions must be met
    # for a player to countinue playing, if not the player has to draw card from the pool
    # This is a simple function that returns a bool `True` if greater than thirty
    # Eventually when the both `is_valid_move` and `is_more_than_30` return True, the player attribute is_greater_30 is set to True
    # The player is then allowed to play


def is_more_than_30(list_of_tiles):
    if sum(list_of_tiles) > 30:
        return True
    else:
        return False
