import pygame
import sys
import random

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
    def 
