import pygame
import sys
import random

def change_turns(list_of_players, Current_Player,Next_Player):
	if Current_Player.turn == False:
		index = list_of_players.index(Current_Player)
		Next_Player.turn = True
		Current_Player = Next_Player
		if index < len(list_of_players) - 1:
			new_index = list_of_players.index(Current_Player) + 1
		else:
			new_index = 0
		Next_Player = list_of_players[new_index]
	return Current_Player, Next_Player