import pygame
import sys
import random
import game_constants

tile_height = game_constants.tile_height
tile_width = game_constants.tile_width

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
    
    # during gameplay
    def add_tile_to_rack(self,pool):
        # A player randomly pick two cards, select one return one
        selected_tiles = random.sample(pool.tiles,2)
        for tile in selected_tiles:
            tile.show() # show tiles that a player can select, show method to be in class Tile
            # if selected, kept in rack 
            # otherwise return to pool

        # selected_tile 
        # for picked tile in picked tiles, the player chooses one
        # pop the selected tile from pool
        # not sure how to implement for human player

    
    def pick_tile_from_rack(self,tile): # does this require a parameter? unsure: idea human player clicks/or drags the tile, it captures the tile
        index = self.rack.index(tile) if tile in self.rack else None
        picked_tile = self.rack.pop(index)
        return picked_tile
    
    # def play_tile(self):
    #     return self.pick_tile_from_rack()
        # board.append(tile) append tile to the board if it forms a valid set or run
        ## add the picked tile to game board to form a set or run

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

class GameBoard:
    #rect (left/x, top/y, width, height)
    def __init__(self):
        self.board = [] # initialise the game board as an empty list.
        for i in range(8): # outer loop for the 8 rows
            new_row = []
            for j in range(22): # inner loop for the columns
                row.append(pygame.Rect(i * 30, j * 30), tile_width, tile_height) # agree with Iram how much gameboard tiles should be spaced apart.
            self.board.append(new_row)

    def validate_board(self, tiles_in_play): # function takes in a list of all the tiles that have been drawn
        # each time a tile is drawn, the visual representation and data must be linked using a dictionary.
        # In the dictionary, the key will be the rect objecct that represents the tile while the value will be the tile object
        # when two tiles are drawn from pool and one is returned, the returned tile must be removed from the dictionary and their rect object deleted
        # if dictionary is used for link, then each time a tile is drawn it must also be added to a list called colliders
        # If tiles are drawn using sprite, they can be given an id that links them to tile object.
        # if use sprite, tiles_in_play is list of sprites. sprite.id will lxike back to tile. sprite.rect, its rect. This is not bad tbh
  
        for each_row in self.board: # outer loop, checks each row
            set = [] # store our runs and groups
            for each_space in each_row: # checks each space in that row
                occupied = False # lets us know if a space is occupied or not
                # looks at the list of tiles currently in the game and checks if any is colliding with the gameboard space
                for tile in tiles_in_play: 
                    if tile.rect.colliderect(each_space): #alternatively, we can check if their positions match
                        occupied = True # the space is indeed occupied
                        # set.append(tile_dict(tile))# use the dictionary to add the tile represented by the object in collision with the gameboard
                        break # exit this loop since only one tile can be in a spot
                        
                if not occupied: # if the space is empty
                    if set: # if set is not empty by the time we run into an empty space
                        is_valid = self.is_valid_move(set) # check if it is a valid group or run
                        if is_valid == False: # if the move is not valid, validate_board should return false
                            return False
                        else:
                            set = [] # if the move was valid, set should be reset
            if set: # if the set is not empty after we reach the end of the row
                is_valid = self.is_valid_move(set) # check if it is a valid group or run
                    if is_valid == False: # if the move is not valid, validate_board should return false
                        return False
                    else:
                        set = [] # if the move was valid, set should be reset
                

def is_valid_move(list_of_tiles):
        # Checking if it is a run even/odd
    if 3<=len(list_of_tiles)<=5:
        all_odd_or_even = all(t.value % 2==0 for t in list_of_tiles) or all(t.value % 2!=0 for t in list_of_tiles) 
        diff_2 = all(list_of_tiles[i+1].value-list_of_tiles[i].value==2 for i in range(len(list_of_tiles)-1))
        same_color = all(list_of_tiles[i+1].color==list_of_tiles[i].color for i in range(len(list_of_tiles)-1))

        return all_odd_or_even and diff_2 and same_color
    # to be continued
    
	
