import random
import copy

# Constants

FPS = 60
BLUE = (0, 0, 180)
RED = (180, 0, 0)
GREEN = (0, 180, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (128, 0, 128)




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

    def initial_tiles(self):  # what I think is to remove rack frm here, then the rack will call this method to add tiles
        # I see it can potentially create problems..
        # why 14 tiles not 16
        send_tiles = [self.tiles.pop(random.randrange(len(self.tiles))) for _ in range(14)]
        send_tiles = send_tiles + [None] * (40 - len(send_tiles))
        return send_tiles

    def draw_2_tiles(self):
        selected_tiles = [self.tiles.pop(random.randrange(len(self.tiles))) for _ in range(2)]
        tile1 = selected_tiles[0]
        tile2 = selected_tiles[1]
        return tile1, tile2


    def update_pool(self, tile):
        return self.tiles.append(tile)



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
        self.toss = None
    
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
        tile.position[1] = position

    def get_tiles(self):
        return self.rack.tiles
    
    def player_toss(self,pool):
        self.toss = random.choice(pool.tiles)
        return self.toss.value


class AIPlayer(Player): # still working on it, Praise make changes
    def __init__(self,name,tiles):
        super().__init__(name,tiles)

    # the get_rack_moves function is not called directly. Instead the make_moves_rack functon should be called.
    # the make_moves_rack function calls get_rack_moves to get the sets and runs the player can play. 
    # once it knows what the player can play, it scans the board to determine where they can play it.
    # it returns two lists. [[current tile positions in the rack], [new tile positions on the board]]
    # Esentially it returns where the tiles are and where they should be. The first tile position corresponds with the first board position, the second tile position with the second board position and so on. Output format can be changed as needed.
    # To avoid placing tiles from the rack beside tiles on the board (as this function is not trying to extend existing sets but play new ones), the function looks for a little more space than necessary.
    # This function assumes that tiles have a position attribute which is updated as they move around (more importantly, anytime they return to the rack). It uses this attribute to return current tile position in the rack.

    def get_rack_moves(self, which_player): # this function takes in the player the AI should make moves for (on the computers turn, it will take in computer. When player clicks "Play for me" it will take in player).
        from itertools import permutations # so we can easily generate arrangements of tiles in the rack and find possible moves
    
        min_size = 3 # the minimum size of a possible move. 
        max_size = 3 # the maximum size of a possible move.
        depth = 9 # how far the computer should go in its quest to find valid possible moves. At a depth of 5, the computer (if that many exist) would find the 5 highest scoring moves.

        all_sets = [scan_rack_odds(which_player), scan_rack_evens(which_player),scan_rack_group(which_player)]
        # rack = copy.deepcopy(which_player.rack.tiles)  # Deep copy to avoid modifying the original rack. The computer removes tiles from this rack to know what the next highest scoring move will be after it has played the first.
        rack = all_sets[0]
        moves_to_play = [] # a list of moves to play on the board. Computer returns this list when it is done searching.

        def find_highest_move(rack, depth, all_sets, moves_to_play): # we will generate all possible moves (not the most optimal approach), find the valid ones, and find the highest scoring valid move

            combos = [] # list to store all possible arrangements of tiles in the rack
            valid_combos = [] # list to store the combinations that are valid

            for combo_size in range(min_size, max_size + 1): # a combo should be between 3 and 8
                permutations_of_combo_size = [list(permutation) for permutation in permutations(rack, combo_size)] # a list of all possible arrangements of tiles within the currently specified combo_size
                combos.extend(permutations_of_combo_size) # add each move set individually from the list of possible moves

            for possible_move in combos: # filter out the valid moves
                if is_valid_move(possible_move, which_player): # for each possible move, check if it is valid
                    valid_combos.append(possible_move) # add it to our list of valid combos

            if not valid_combos or depth == 0:
                return  # If there are no more valid movesvor we have reached our specified depth, end recursion

            highest_combo = max(valid_combos, key=lambda combo: sum(tile.value for tile in combo)) # from the list of valid combos, return the one with the highest sum of tile values
            moves_to_play.append(highest_combo) # add the highest combo as the first move in moves to play.

            new_rack = [tile for tile in rack if tile not in highest_combo] # Remove tiles that make up the highest move from the rack so that rack is different on next iteration
            #new_same = [tile for tile in all_sets[2] if tile not in highest_combo]
            #all_sets[2] = new_same

            if depth == 6:
                print("update new rack to use evens")
                new_rack = all_sets[1]
            elif depth == 3:
                print("update new rack to use same")
                new_rack = all_sets[2]

            find_highest_move(new_rack, depth - 1, all_sets, moves_to_play) # Call the function within itself but with the updated rack

        find_highest_move(rack, depth, all_sets, moves_to_play) # Start the recursion herre

        return moves_to_play # return the list of all moves to play.
    
    def make_moves_rack(self, which_player, game_board): # this function returns where the tiles we want to play are in the rack, and where we want to place them on the board.
        moves_to_play = self.get_rack_moves(which_player) # get all the groups and runs that can be formed from the tiles in player rack
        needed_spaces = [(len(move) + 2) for move in moves_to_play] # get the space we need to play our moves. plus 2 to allow space between moves already on the gameboard

        position_in_rack = [] # list to store the positions of the tiles in the rack
        position_in_board = [] # list to store the where we want to place our tiles on the board.

        if is_empty(game_board): # if the gameboard is empty, we can place tiles anywhere.
            i, j = 0, 0
            for move in moves_to_play:
                for tile in move:
                    position_in_rack.append(tile.position[1])
                    position_in_board.append([i,j])
                    j += 1
                i += 1
                j = 0
            return [position_in_rack, position_in_board]
        
        for row_index, each_row in enumerate(game_board): # outer loop, checks each row and saves the row index
            empty_spaces = [] # store the positions of our empty spaces
            for column_index, element in enumerate(each_row): # checks each element in that row and saves the column index
                if element == None: # if the element is an empty space
                    empty_spaces.append([row_index, column_index]) # add its position to our list of empty spaces 

                if element != None or (len(empty_spaces) in needed_spaces): # if we run into a tile object or we have as much empty spaces as needed to play our move
                    if empty_spaces: # if we have a bunch of empty spaces by the time we run into a tile (check for the tile half of the previous condition)
                        for move in moves_to_play: # go through our list of moves. 
                            if len(move) == len(empty_spaces) - 2: # if we find a move that we have enough space for.
                                needed_spaces.remove(len(empty_spaces)) # remove that space from our list of empty spaces so we know it has been used up on the next iteration
                                for tile in move:
                                    position_in_rack.append(tile.position[1]) # add the position in rack to our list
                                for i in range(1, len(empty_spaces) - 1):
                                    position_in_board.append(empty_spaces[i]) # add the position of the empty spaces in our list, starting from 1 for extra spacing between tiles on the board.

                                empty_spaces = [] # reset our list of empty spaces
                                moves_to_play.remove(move) # remove the move from ourlist of moves so that we know it has been handled on the next iteration

                                break # break out of the loop since the move has been addressed and we are looking for space all over again. Also we are not iterating over moves_to_play as we are modifying it
                    empty_spaces = [] # if the empty_spaces we found so far (by the time we ran into a tile) isn't long enough for any of our moves, reset it as well.
                
            # if empty_spaces: # if we have a bunch of empty spaces by the time we reach the end of our row (this might be redundant, I'm not sure)
            #     for move in moves_to_play:
            #         if len(move) == len(empty_spaces) - 2:
            #             needed_spaces.remove(len(empty_spaces))
            #             for tile in move:
            #                 position_in_rack.append(tile.position[1])
            #             for i in range(1, len(empty_spaces) - 1):
            #                 position_in_board.append(empty_spaces[i])
            #
            #                 empty_spaces = []
            #                 moves_to_play.remove(move)
            #
            #                 break
            empty_spaces = []
        print("find move says rack to board is", len(position_in_rack), len(position_in_board))
        return [position_in_rack, position_in_board]
    
    def format_board(self,game_board): 
        board_sets_runs = []
        board_positions = {}
        for i, row in enumerate(game_board):
            temp = []
            for j, item in enumerate(row):
                if item is not None:
                    temp.append(item)
                    board_positions[item] = [i, j]
                elif temp:
                    board_sets_runs.append(temp)
                    temp = []
            if temp:
                board_sets_runs.append(temp)
        return board_sets_runs, board_positions


    def extend_board(self, which_player, game_board):

        board_cleaned, board_positions = self.format_board(game_board)
        tile_pos_in_rack = []
        tile_pos_for_board = []

        rack = copy.deepcopy(which_player.rack.tiles)

        # Game board is taken as a list of lists where sublists are runs or sets
        runs_board = []
        for i, sublist in enumerate(board_cleaned):
            if is_run(sublist):
                runs_board.append(sublist)

        # # get colors of runs
        colors = []
        for i, sublist in enumerate(runs_board):
            for t in sublist:
                colors.append(t.color)
        colors = list(set(colors))
        # print('colors',colors)

        found_run = False  # flag to check if a match was found
        for rack_tile in rack:
            if rack_tile is not None and rack_tile.color in colors:
                for board_run in runs_board:
                    if rack_tile.value-board_run[0].value == -2 and rack_tile.color == board_run[0].color:
                        i, j = board_positions[board_run[0]]
                        if j >= 4:
                            if game_board[i][j-1] is None and game_board[i][j-2] is None:
                                if rack_tile.position[1] not in tile_pos_in_rack:
                                    tile_pos_in_rack.append(rack_tile.position[1])
                                    tile_pos_for_board.append([i, j-1])
                                    found_run = True  # set flag to True (technically only true if there is enough space on the board to play the move)
                        elif 4 > j > 0:
                            if game_board[i][j-1] is None:
                                if rack_tile.position[1] not in tile_pos_in_rack:
                                    tile_pos_in_rack.append(rack_tile.position[1])
                                    tile_pos_for_board.append([i, j-1])
                                    found_run = True

                    if rack_tile.value-board_run[-1].value==2 and rack_tile.color==board_run[-1].color:
                        i,j = board_positions[board_run[-1]]
                        if 15 < j < 19:
                            tile_pos_in_rack.append(rack_tile.position[1])
                            tile_pos_for_board.append([i, j+1])
                            found_run = True  # set flag to True
                        elif j <= 15:
                            if game_board[i][j + 1] is None and game_board[i][j + 2] is None:
                                tile_pos_in_rack.append(rack_tile.position[1])
                                tile_pos_for_board.append([i, j + 1])
                                found_run = True  # set flag to True

        for position in tile_pos_in_rack:
            rack[position] = None

        groups_board = []
        for sublist in board_cleaned:
            if is_group(sublist):
                groups_board.append(sublist)

            # get values contained in groups_board:
        values = []
        colors = []
        for i, sublist in enumerate(groups_board):
            for t in sublist:
                values.append(t.value)
                colors.append(t.color)

        found_match = False
        for rack_tile in rack:
            if rack_tile is not None and rack_tile.value in values:
                for sublist in groups_board:
                    if rack_tile.value==sublist[0].value and rack_tile.color not in [c.color for c in sublist]:
                        i, j = board_positions[sublist[0]]
                        if j >= 4:
                            if game_board[i][j-1] is None and game_board[i][j-2] is None:
                                if rack_tile.position[1] not in tile_pos_in_rack:
                                    tile_pos_in_rack.append(rack_tile.position[1])
                                    tile_pos_for_board.append([i, j-1])
                                    found_match = True
                            #else:
                                #needed_spaces = len(sublist) + 2
                        elif 4 > j > 0:
                            if game_board[i][j - 1] is None:
                                if rack_tile.position[1] not in tile_pos_in_rack:
                                    tile_pos_in_rack.append(rack_tile.position[1])
                                    tile_pos_for_board.append([i, j - 1])
                                    found_match = True

        return [tile_pos_in_rack, tile_pos_for_board]

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

        if is_empty(game_board):
            return [False, invalid_positions]

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
            # current_player.turn = False

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
# def change_turns(list_of_players, Current_Player,Next_Player):
# 	if Current_Player.turn == False: # If it is no longer the current player's turn
# 		index = list_of_players.index(Current_Player) # get the position of the current player in list of players
# 		Next_Player.turn = True # set the next player's turn to true
# 		Current_Player = Next_Player # update the current player
# 		if index < len(list_of_players) - 1: # as long as we have not reached the end of our list of players
# 			new_index = list_of_players.index(Current_Player) + 1 # the next player is the player beside our updated current player
# 		else:
# 			new_index = 0 # else if we have reached the end of the list, cycle back to the first player
# 		Next_Player = list_of_players[new_index] # update the next player
# 	return Current_Player, Next_Player # return the current and next player so that their values can be set outside the function

def toggle_players(player_1, player_2): #simple function to toggle player turns. Use this instead of change turns since game is not multiplayer
    player_1.turn = not player_1.turn
    player_2.turn = not player_2.turn
def is_empty(game_board):
    return all(all(x == game_board[0][0] for x in row) for row in game_board) # if every element in a row is same as the first element and every row is the same as the first row

def scan_rack_group(player):
    same_tiles = []
    for i, tile in enumerate(player.rack.tiles):
        if tile is not None:
            for other_tile in player.rack.tiles:
                if other_tile is not None:
                    if other_tile != tile and other_tile.value == tile.value:
                        same_tiles.append(tile)
                        break
    return same_tiles

def scan_rack_odds(player):
    odd_tiles = [t for t in player.rack.tiles if t is not None and t.value%2!=0]
    return odd_tiles

def scan_rack_evens(player):
    even_tiles = [t for t in player.rack.tiles if t is not None and t.value%2==0]
    return even_tiles

def who_plays_first(player,pool):
    random_pick = random.choice(pool)


# tile1 = Tile(2, BLUE)
# tile2 = Tile(4, BLUE)
# tile3 = Tile(6, BLUE)
#
# tile4 = Tile(5, RED)
# tile5 = Tile(5, BLUE)
# tile6 = Tile(5, BLACK)
# tile7 = Tile(5, GREEN)
#
# tile11 = Tile(3, BLUE)
# tile12 = Tile(3, RED)
# tile13 = Tile(3, BLACK)
#
# tile14 = Tile(7, RED)
# tile15 = Tile(8, BLUE)
# tile16 = Tile(8, BLACK)
# tile17 = Tile(7, GREEN)
#
# tile18 = Tile(9, RED)
# tile20 = Tile(9, BLUE)
# tile19 = Tile(9, GREEN)
#
# tile24 = Tile(11, RED)
# tile25 = Tile(10, BLUE)
# tile26 = Tile(10, BLACK)
# tile27 = Tile(11, GREEN)
#
# tile21 = Tile(13, BLUE)
# tile22 = Tile(12, BLUE)
# tile23 = Tile(13, RED)
#
# tile28 = Tile(15, RED)
# tile29 = Tile(14, BLUE)
# tile30 = Tile(14, BLACK)
# tile31 = Tile(15, GREEN)
#
# tile32 = Tile(1, GREEN)
#
# tile33 = Tile(2, RED)
# tile34 = Tile(6, BLUE)
# tile35 = Tile(6, BLACK)
# tile36 = Tile(7, BLACK)
#
# tile37 = Tile(8, GREEN)
# tile38 = Tile(10, GREEN)
# tile39 = Tile(8, RED)
#
# tile40 = Tile(6, RED)
# tile41 = Tile(11, BLUE)
# tile42 = Tile(6, BLACK)
# tile43 = Tile(11, GREEN)
#
# player_1 = AIPlayer("Peanuts", [tile7, tile12, tile13, tile14, tile15, tile16, tile17, tile18, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, tile19, tile20, tile21, tile26, tile22, tile23]) #, tile24, tile25, tile26, tile11, tile27, tile28, tile29, tile30]) #, tile31, tile32, tile33, tile34, tile35, tile36, tile37, tile38, tile39, tile40, tile41, tile42, tile43])
# for i in range(len(player_1.rack.tiles)):
#     if player_1.rack.tiles[i] is not None:
#         player_1.rack.tiles[i].position = [0,i]
# player_1.is_greater_30 = True
#
# board = []  # initialise the game board as an empty list.
# rows, columns = 9, 20
# for i in range(rows):
#     new_row = []
#     for j in range(columns): # each row is full of Nones to denote empty spaces
#         new_row.append(None)
#     board.append(new_row)
#
# tile8 = Tile(1, BLUE)
# tile9 = Tile(1, BLACK)
# tile10 = Tile(1, RED)
#
# board[0][2] = tile8
# board[0][3] = tile9
# board[0][4] = tile10
#
# board[3][3] = tile4
# board[3][4] = tile5
# board[3][5] = tile6
#
# board[5][0] = tile1
# board[5][1] = tile2
# board[5][2] = tile3
#
# #for row in board:
#     #print(row)
#
# #evens = scan_rack_evens(player_1)
# #for tile in evens:
# #     print(tile)
#
# #odds = scan_rack_odds(player_1)
# #for tile in odds:
# #    print(tile)
#
# #same = scan_rack_group(player_1)
# #for tile in same:
# #   print(tile)
#
# # print("player tiles are: ")
# # for tile in player_1.rack.tiles:
# #     print(tile)
#
# print(player_1.make_moves_rack(player_1, board))
# print(player_1.extend_board(player_1, board))
# #print(player_1.extend_board_groups(board))
# #print(player_1.extend_board_runs(board))
#
# # for set in player_1.get_rack_moves(player_1):
# #     print("New set is")
# #     for tile in set:
# #         print(tile)
# #     print()