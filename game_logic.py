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
        self.position = [None,None]

    def __str__(self):
        return f"Value: {self.value}, Color = {self.color}"

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
        self.turn = False # when 
        self.is_greater_30 = False
    
    def __str__(self):
        return f"Name: {self.name} Turn: {self.turn}"

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


class AIPlayer(Player): # still working on it, Praise make changes
    def __init__(self,rack,name,turn,is_greater_30):
        super().__init__(rack,name,turn,is_greater_30)
    
    def scan_board(self,game_board):
        # gameboard is an instance of class gameboard
        for row in game_board:
            # get positions of the separators, for now I will use a  `space` as placeholder, rect is a rectangle that represents a tile
            sep_position = [i for i,rect in enumerate(row) if rect is None]
            # break the rows into sublists, which are valid sets(groups) and runs
            sets_and_runs = [row[i:j] for i,j in zip([0]+sep_position,sep_position+None)]
            # remove the blank spaces to remain with valid sublist of sets and runs
            self.board_sets_and_runs = [[rect for rect in set_or_run if rect is not None] for set_or_run in sets_and_runs]
        return self.board_sets_and_runs ## here is a list of sublists 
    
    def scan_rack(self): # scans the rack and play tiles
        # check all tiles in the rack and append the tile to the end or the beginning of a set or run
        # we need to obtain the first and last tiles in group/run from the gameboard, then comapare with what the player has
        # This will require to break is_valid_move to identify groups and runs separately
        for sublist in self.board_sets_and_runs:
            if is_group(sublist):
                # Check if there is any tile of same value with different color from what is on game board
                # Took the first one since they are all of the same value
                board_tile_value = sublist[0].value
                board_tile_colors = [tile.color for tile in sublist]
        # check if there is any tile of `value` in rack anf of different color from those on game board
                for i,tile in enumerate(self.rack):
                    if tile.value == board_tile_value and tile.color not in board_tile_colors:
                        pick_tile = self.rack.pop(i)
                    sublist.append(pick_tile)
        # Checking runs and appending
            if is_run(sublist):
                board_tile_values = [tile.value for tile in sublist]
                board_tile_color = sublist[0].color
                # checking at the beginning and end of runs, play as        
                for i,tile in enumerate(self.rack):
                    if tile.color == board_tile_color:
                        if tile.value+2 == board_tile_values[0]:
                            pick_tile = self.rack.pop(i)
                            sublist.insert(0,pick_tile)
                        if tile.value-2 == board_tile_values[-1]:
                            pick_tile = self.rack.pop(i)
                            sublist.append(pick_tile)
                         # This will need to be drawn on screen 
            else:
                self.pick_tiles()
                # the player turn ends
                # One added to rack other returned


# bukayo = Player('Bukayo Saka')

class GameBoard:
    def __init__(self):
        self.board = []  # initialise the game board as an empty list.
        self.rows, self.columns = 9, 20
        for i in range(self.rows):
            new_row = []
            for j in range(self.columns): # each row is full of Nones to denote empty spaces
                new_row.append(None)
            self.board.append(new_row)

    def validate_board(self, game_board, current_player):
        # game_board is the current state of the gameboard - a 9 by 20 matrix of tile objects passed in from frontend.
        # current_player is the player whose turn it is. 
        # we need to check if they have played at least 30 points on their first move
        # we also need to set their turn to false once they play a valid move.

        # this function returns a list [boolean, list]
        # the boolean let's us know if the board is valid or not
        # the list contains each position of the tiles on the board that form invalid game play.

        invalid_positions = [] # list of invalid positions
        status = True # represents the status of the gameboard. We initialise it to true but set it to false once gameboard is found to be invalid.
        tile_pos = {} # a dictionary to help us link each tile to its position of the board so we can return those positions later
        i, j = 0, 0 # i, j represent coordinates on the board. they are updated as we loop through the board and used to determine tile positions on the board.

        for each_row in game_board:  # outer loop, checks each row in the game board. Increment i at the end of this loop.
            set = []  # create an empty list to store groups and runs we find on the board (using None - empty space - as delimiter)
            for element in each_row:  # inner loop, checks each space/element in that row. Increment j at the end of this loop.
                if element != None: # If the element is not an empty space (so if it is a tile object)
                    set.append(element)  # add that tile to our set
                    tile_pos[element] = str(i) + "," + str(j) # store the tile's position on the board in a dictionary using the tile as key and it's position as value.

                if element == None:  # if the current element in the row is an empty space
                    if set:  # check if set is not empty by the time we run into an empty space. If it isn't then we have a set we need to validate.
                        is_valid = is_valid_move(set, current_player)  # check if the set is a valid group or run
                        if is_valid == False:  # if the move is not valid, add the positions of all invalid tiles to invalid positions
                            status = False # set the status of our gameboard to false.
                            for tile in set:
                                invalid_positions.append(tile_pos[tile])
                            set = []  # clear set for the next sets.
                        else:
                            set = []  # if the move was valid, only clear set.
                j += 1  # update the column position as we move through the row.

            if set:  # if the set is not empty after we reach the end of the row
                is_valid = is_valid_move(set, current_player)  # check if it is a valid group or run
                if is_valid == False:  # if the move is not valid, add the positions of all invalid tiles to invalid positions
                    status = False
                    for tile in set:
                        invalid_positions.append(tile_pos[tile])
                    set = []  # clear set for the next sets.
                else:
                    set = []  # if the move was valid, set should be reset
            i += 1  # update the row position as we move through the board

        if status:  # if status is true after we have looped through the board, then the board is valid. So we update the gameboard and end the player's turn
            self.board = copy.deepcopy(game_board)
            current_player.turn = False

        return [status, invalid_positions] # return the board status and invalid positions. this will be [True, []] when board is valid.

    def get_copy(self):
        return copy.deepcopy(self.board)


def is_run(list_of_tiles):
        # Checking if it is a run even/odd
    if 3<=len(list_of_tiles)<=8:
        all_odd_or_even = all(t.value % 2==0 for t in list_of_tiles) or all(t.value % 2!=0 for t in list_of_tiles) 
        diff_2 = all(list_of_tiles[i+1].value-list_of_tiles[i].value==2 for i in range(len(list_of_tiles)-1))
        same_color = all(list_of_tiles[i+1].color==list_of_tiles[i].color for i in range(len(list_of_tiles)-1))
        # Checking if the list meet all conditions to be a run
        run = all_odd_or_even and diff_2 and same_color
        return run
    else:
        return False
    
def is_group(list_of_tiles):
    if 3<=len(list_of_tiles)<=5:
        same_value = all(list_of_tiles[i+1].value==list_of_tiles[i].value for i in range(len(list_of_tiles)-1))
        different_color = len(set([t.color for t in list_of_tiles]))==len(list_of_tiles)
        group = same_value and different_color
        return group                 
    else:
        return False
    
def is_more_than_30(list_of_tiles): # once one player has more than 30 and continues playing how will this work
    if sum([tile.value for tile in list_of_tiles])>=30:
        return True
    else:
        return False

def is_valid_move(list_of_tiles,player):
    if player.is_greater_30 == False:
        passed = is_more_than_30(list_of_tiles)
        if passed:
            player.is_greater_30 = True
            return is_group(list_of_tiles) or is_run(list_of_tiles)
        else:
            return passed
    else:
        return is_group(list_of_tiles) or is_run(list_of_tiles)

# list_of_players contains all the players in the game in order of their decided turns
def change_turns(list_of_players, Current_Player,Next_Player): 
	if Current_Player.turn == False: # If it is no longer the current player's turn
		index = list_of_players.index(Current_Player) # get the position of the current player in list of players
		Next_Player.turn = True # set the next player's turn to true
		Current_Player = Next_Player # update the current player
		if index < len(list_of_players) - 1: # as long as we have not reached the end of our list of players
			new_index = list_of_players.index(Current_Player) + 1 # the next player is the player beside our updated current player
		else:
			new_index = 0 # else if we have reached the end of the list, cycle back to the first player
		Next_Player = list_of_players[new_index] # update the next player
	return Current_Player, Next_Player # return the current and next player so that their values can be set outside the function

