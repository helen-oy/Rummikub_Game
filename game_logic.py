import pygame
import sys
import random
import copy
from game_constants import *

class Tile:
    def __init__(self, value, color):
        self.value = value
        self.color = color
        self.width, self.height = TILE_WIDTH, TILE_HEIGHT
        # self.image = pygame.image.load('tile.png')


class Pool:
    def __init__(self): # initialize pool to generate tiles
        self.tiles = []
        self.init_pool()
 
    def init_pool(self):
        tile_colors = [RED,BLUE,GREEN,BLACK,PURPLE] 
        self.tiles = [Tile(i % 15 + 1, t) for i in range(30) for t in tile_colors] # create 2 sets of tile colors numbered 1-15
        random.shuffle(self.tiles)  # shuffle all 150 tiles
 
    def remaining_tiles(self): # count of tiles remaining in pool
        return len(self.tiles)
 
    def initial_tiles(self): # initial tiles to playes rack
        send_tiles = [self.tiles.pop(random.randrange(len(self.tiles))) for _ in range(14)]
        return send_tiles
 


class Rack:
    def __init__(self): # initialize rack as an empty list
        self.tiles = []
 
    def add_tile(self, tile): # choose 2 tiles return one
        self.tiles.append(tile)
    
    def initial_tiles(self,pool): 
        # This take tiles that were expelled by the pool    
        # The pool will intialized as an instance of class Pool
        self.tiles.append(pool.initial_tiles()) 
 
    def sort_tiles(self):
        odd_tiles = [tile for tile in self.tiles if tile.number % 2 != 0]
        even_tiles = [tile for tile in self.tiles if tile.number % 2 == 0]
        # return odd_tiles, even_tiles 
        # before putting them together, lets sort them by value and color
        odd_tiles = sorted(odd_tiles,key=lambda x: (x.value,x.color))
        even_tiles = sorted(even_tiles,key=lambda x: (x.value,x.color))
        return odd_tiles + even_tiles # i think they should be joined,!!
	


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


class Player:
    def __init__(self,name):
        self.rack = []
        self.name = name
        self.turn = False # when 

    
    def initial_tiles(self,rack): 
        # Add tiles to players rack
        self.rack.append(rack.initial_tiles())
    
    def play_tile(self,tile): # does this require a parameter? unsure: idea human player clicks/or drags the tile, it captures the tile
        index = self.rack.index(tile) if tile in self.rack else None
        picked_tile = self.rack.pop(index)
        return picked_tile
    
    # get total value of tiles in the rack: to compute total points when the game ends
    def get_total_value(self):
        value = 0
        for tile in self.rack.tiles:
            value += tile.value
        return value
    
    # 
    def pick_tiles(self, pool): 
        selected_tiles = [pool.tiles.pop(random.randrange(len(pool.tiles))) for _ in range(2)]
        tile1 = selected_tiles[0]
        tile2 = selected_tiles[1]
        return selected_tiles
        # show selected tiles on the screen
    # Detect mouse collision, both tiles will wait MOUSEBOTTONDOWN event, the clicked tile, added to rack
    #   self.rack.add_tiles(selected_tiles[0 or 1])
    # send the other tile back to the pool
    # After this action, set players turn to False
 
        
    
		

	
    #     return self.pick_tile_from_rack()
        # board.append(tile) append tile to the board if it forms a valid set or run
        ## add the picked tile to game board to form a set or run

class GameBoard:
    #rect (left/x, top/y, width, height)
    def __init__(self):
        self.board = [] # initialise the game board as an empty list. 
        self.rows, self.columns = 9, 20
        for i in range(self.rows):
            new_row = []
            for j in range(self.columns):
                new_row.append(None)
            self.board.append(new_row)

    def validate_board(self, game_board): 
        # game_board is the current state of the gameboard - a 9 by 20 matrix of tile objects passed in from frontend.

        # this function returns a list [boolean, list]
        # the boolean let's us know if the board is valid or not
        # the list contains each position of the tiles on the board that form invalid game play.

        invalid_positions = []
        status = True
        tile_pos = {}
        i, j = 0,0
        
        for each_row in game_board: # outer loop, checks each row 
            set = [] # store our runs and groups
            for element in each_row: # checks each space/element in that row
                if element != None:
                    set.append(element) # add that tile to our set
                    tile_pos[element] = str(i) + "," + str(j)
                            
                if element == None: # if the current element in the row is an empty space
                    if set: # if set is not empty by the time we run into an empty space
                        is_valid = self.is_valid_move(set) # check if it is a valid group or run
                        if is_valid == False: # if the move is not valid, add the positions of all invalid tiles to invalid positions
                            status = False
                            for tile in set:
                                invalid_positions.append(tile_pos[tile])
                            set = [] # clear set for the next sets.
                        else:
                            set = [] # if the move was valid, set only clear set.
                j += 1 # update the column position as we move through the row.
                
            if set: # if the set is not empty after we reach the end of the row
                is_valid = self.is_valid_move(set) # check if it is a valid group or run
                if is_valid == False: # if the move is not valid, add the positions of all invalid tiles to invalid positions
                    status = False
                    for tile in set:
                        invalid_positions.append(tile_pos[tile])
                    set = [] # clear set for the next sets.
                else:
                    set = [] # if the move was valid, set should be reset
            i += 1 # update the row position as we move through the board
            
        if status: # if thr board is valid, update the gameboard
            self.board = copy.deepcopy(game_board)
            
        return [status, invalid_positions]

    def get_copy(self):
        return copy.deepcopy(self.board)
        

def is_valid_move(list_of_tiles):
        # Checking if it is a run even/odd
    if 3<=len(list_of_tiles)<=5:
        all_odd_or_even = all(t.value % 2==0 for t in list_of_tiles) or all(t.value % 2!=0 for t in list_of_tiles) 
        diff_2 = all(list_of_tiles[i+1].value-list_of_tiles[i].value==2 for i in range(len(list_of_tiles)-1))
        same_color = all(list_of_tiles[i+1].color==list_of_tiles[i].color for i in range(len(list_of_tiles)-1))
        # Checking if the list meet all conditions to be a run
        run = all_odd_or_even and diff_2 and same_color
        if run:
            return run
        else: # Check whether it is a group
            same_value = all(list_of_tiles[i+1].value==list_of_tiles[i].value for i in range(len(list_of_tiles)-1))
            different_color = len(set([t.color for t in list_of_tiles]))==len(list_of_tiles)
            group = same_value and different_color
            return group                 
    else:
        return False