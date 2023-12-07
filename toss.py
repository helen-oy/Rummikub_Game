import random
from game_logic import *

def who_plays_first(players:list,pool):
    for i in range(len(players)-1):
        toss_values = []
        if players[i].player_toss(pool) > players[i+1].player_toss(pool):
            players[i].turn = True
            # print('FIRST',players[i])
            return players[i]  
        elif players[i].player_toss(pool) < players[i+1].player_toss(pool):
            players[i+1].turn = True
            # print('SECOND',players[i+1])
            return players[i+1]
        else:
            p = random.choice(players)
            p.turn = True