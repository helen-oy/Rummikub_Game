import game_play
from game_play import GamePlay
from game_components import GameRects
import random




class GameEvents:
    def __init__(self, game_play: GamePlay, game_surfaces: GameRects):
        self.game_play = game_play
        self.game_surfaces = game_surfaces
        self.selected_rack_tile_index = None
        self.selected_game_board_tile_positions = None # [row,col]
        self.show = True

    def handle_events(self, pos):
        if self.game_surfaces.is_colliding_with_player_rack(pos):
            self.handle_user_player_rack_events(pos)

        elif self.game_surfaces.is_colliding_with_game_board(pos):
            self.handle_game_board_events(pos)

        elif self.game_surfaces.show_button[1].collidepoint(pos):
            self.game_play.toggle_comp_tile_visible()
            self.game_surfaces.update_comp_tiles_surfaces()

        elif self.game_surfaces.draw_tiles_button[1].collidepoint(pos):
            if len(self.game_play.drawn_tiles_from_pool) == 0:
                drawn_tiles = self.game_play.draw_tile_from_pool()
                self.game_surfaces.update_drawn_pool_tiles()

        elif self.game_surfaces.is_colliding_with_drawn_tile(pos):
            self.handle_pool_event(pos)
            self.game_play.reset_draw()
            self.game_surfaces.update_drawn_pool_tiles()
            self.game_surfaces.update_remaining_tiles()

        elif self.game_surfaces.submit_button[1].collidepoint(pos):
            validation = self.game_play.submit_game_state()
            if validation[0]:
                print("true")
            else:
                print("false")

        elif self.game_surfaces.play_for_me[1].collidepoint(pos):
            self.handle_computer_moves(self.game_play.player)

    def handle_computer_moves(self, which_player): # The computer makes moves for which_player. which_player could be itself or the human player.
        user_player = self.game_play.player
        computer_player = self.game_play.comp_player # get the computer player because the algorithm to make moves is a method of its class
        tiles_to_use = which_player.get_tiles() # the tiles we will be making use of gotten from whomever the computer is playing for
        tile_surfaces = self.game_surfaces.comp_tiles_surfaces if isinstance(which_player, game_play.AIPlayer) else self.game_surfaces.player_tiles_surfaces # game surface is computer's if which player is computer else it is user's
        game_board = self.game_play.game_state # get the gameboard.

        rack_moves = computer_player.make_moves_rack(which_player, game_board) # get the moves to play from rack

        tile_positions = rack_moves[0] # these are the indexes in the rack of the tiles we want to play
        board_positions = rack_moves[1] # these are the positions on the board where we want to place our tiles

        no_moves_played = 0 # this keeps track of whether a move has been placed or not.

        if len(tile_positions) > 0: # if there are moves on the rack

            for k in range(len(tile_positions)): # we loop for the length of indexes in our rack of tiles we want to play.
                self.selected_rack_tile_index = tile_positions[k] # the index of the tile in our rack updates going from the first element in our list of indexes when k = 0
                i, j = board_positions[k] # for each tile found at the given index in our rack, where we want to play it on the board corresponds with board positions at k
                self.game_play.update_game_state(tiles_to_use[self.selected_rack_tile_index], i, j) # update the game state with the tile found at the given index and place it  in the specified board position
                if isinstance(which_player, game_play.AIPlayer): # if whichplayer is the ai player update the ai player's rack
                    self.game_play.comp_player.remove_tile(self.selected_rack_tile_index)
                    self.game_surfaces.update_comp_tiles_surfaces()
                else: # if which player is not the AI player, then udate the human player's rack instead
                    self.game_play.player.remove_tile(self.selected_rack_tile_index)
                    self.game_surfaces.update_player_tiles_surfaces()
                self.game_surfaces.update_game_state_tiles_surfaces() # update our visual gameboard, i guess
                self.selected_rack_tile_index = None

            # submit move here
            self.game_play.submit_game_state() # submit the move we just played
        else:
            no_moves_played += 1 # if there were no rack moves, take note so we can know if computer did not play anything at all and so needs to pick

        board_extensions = computer_player.extend_board(which_player, game_board) # repeat the same logic but for board extensions

        tile_positions = board_extensions[0]
        board_positions = board_extensions[1]

        if len(tile_positions) > 0:  # if there are moves on the rack

            for k in range(len(tile_positions)):
                self.selected_rack_tile_index = tile_positions[k]
                i, j = board_positions[k]
                self.game_play.update_game_state(tiles_to_use[self.selected_rack_tile_index], i, j)
                if isinstance(which_player, game_play.AIPlayer):
                    self.game_play.comp_player.remove_tile(self.selected_rack_tile_index)
                    self.game_surfaces.update_comp_tiles_surfaces()
                else:
                    self.game_play.player.remove_tile(self.selected_rack_tile_index)
                    self.game_surfaces.update_player_tiles_surfaces()
                self.game_surfaces.update_game_state_tiles_surfaces()
                self.selected_rack_tile_index = None

            # submit move here
            self.game_play.submit_game_state()
        else:
            no_moves_played += 1

        if no_moves_played < 2:
            self.game_play.toggle_players(computer_player, user_player) # if moves were played end turn
        elif no_moves_played == 2: # if no moves were played pick from the pool
            if len(self.game_play.pool.tiles) > 1:
                random_tile = random.choice(self.game_play.pool.tiles)
                self.game_play.pool.tiles.remove(random_tile)
                for i, tile in enumerate(which_player.get_tiles()):
                    if tile is None:
                        if isinstance(which_player, game_play.AIPlayer):
                            self.game_play.comp_player.add_tile(random_tile, i)
                            self.game_surfaces.update_comp_tiles_surfaces()
                        else:
                            self.game_play.player.add_tile(random_tile, i)
                            self.game_surfaces.update_player_tiles_surfaces()
                        break
                self.game_play.toggle_players(computer_player, user_player) # after picking from pool, end turn
            else:
                print("pool is empty") # test purposes
    def handle_user_player_rack_events(self, pos):
        user_tiles = self.game_play.player.get_tiles()
        user_tile_surfaces = self.game_surfaces.player_tiles_surfaces
        for i, tile in enumerate(user_tile_surfaces):
            if tile[1].collidepoint(pos) and user_tiles[i] is not None:
                self.selected_rack_tile_index = i

            elif tile[1].collidepoint(pos) and self.selected_rack_tile_index is not None:
                if user_tiles[i] is None:
                    self.game_play.player.add_tile(user_tiles[self.selected_rack_tile_index], i)
                    self.game_play.player.remove_tile(self.selected_rack_tile_index)
                    self.game_surfaces.update_player_tiles_surfaces()
                    self.selected_rack_tile_index = None

    #           BOARD -> RACK TODO

    def handle_game_board_events(self, pos):
        user_tiles = self.game_play.player.get_tiles()
        game_board_surfaces = self.game_surfaces.game_board_tile_surfaces

        for i in range(len(game_board_surfaces)):
            for j in range(len(game_board_surfaces[i])):
                if game_board_surfaces[i][j][1].collidepoint(pos):
                    if self.selected_rack_tile_index is not None and self.game_play.game_state[i][j] is None:
                        self.game_play.update_game_state(user_tiles[self.selected_rack_tile_index], i, j)
                        self.game_play.player.remove_tile(self.selected_rack_tile_index)
                        self.game_surfaces.update_player_tiles_surfaces()
                        self.game_surfaces.update_game_state_tiles_surfaces()
                        self.selected_rack_tile_index = None
                        self.selected_game_board_tile_positions = None

                    elif self.selected_game_board_tile_positions is not None and self.game_play.game_state[i][j] is None:
                        selected_x,selected_y = self.selected_game_board_tile_positions
                        self.game_play.update_game_state(self.game_play.game_state[selected_x][selected_y], i, j)
                        self.game_play.remove_game_state_tile(selected_x, selected_y)
                        self.game_surfaces.update_player_tiles_surfaces()
                        self.game_surfaces.update_game_state_tiles_surfaces()
                        self.selected_game_board_tile_positions = None

                    elif self.game_play.game_state[i][j] is not None:
                        self.selected_game_board_tile_positions = [i, j]
                        self.selected_rack_tile_index = None


    def handle_pool_event(self, pos):
        selected_index = None
        for i, tile in enumerate(self.game_surfaces.drawn_pool_tiles_surfaces):
            print("here", tile)
            if tile[1].collidepoint(pos):
                for j, tile in enumerate(self.game_play.player.get_tiles()):
                    if tile is None:
                        self.game_play.player.add_tile(self.game_play.drawn_tiles_from_pool[i], j)
                        self.game_surfaces.update_player_tiles_surfaces()
                        selected_index = i

                        if selected_index == 0:
                            self.game_play.pool.update_pool(self.game_play.drawn_tiles_from_pool[1])
                            break
                        else:
                            self.game_play.pool.update_pool(self.game_play.drawn_tiles_from_pool[0])
                            break




