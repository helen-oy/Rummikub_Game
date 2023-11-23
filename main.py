from game_logic import *
from game_constants import *

def run_game():
    # Initialize Pygame
    pygame.init()

    # Initialize Pygame window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Rummikub")
    
    # Display main menu. Enter Game flow once player hits 'play' option

    # -------------------- GAME FLOW ---------------------------#
    # create a list to store the order of players based on the value of their tiles drawn at the start of the game.
    # Human player and AI player draw cards from pool to decide who goes first.
    # Append players to list of players in order of who drew the highest card.
    # create global variables, Current player and Nextplayer. Initialise these variables to the first and second players in our list.
    # Set the turn of the current player to true.

    # Initialise the gameboard
    # Initialise the player's rack (give each player 14 cards)

    # Main game loop
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # Uncomment the code below to toggle player turns once the required function arguments have been implemented outside the while loop.
        # Current_Player, Next_Player = game_logic.change_turns(list_of_players, Current_Player, Next_Player)

        # The current player has to make a move
            # If the current player decides not to make a move on the board (because they can't or simply won't)
                # They draw two tiles from the pool and choose one
                # Their turn ends so set Current_Player.turn to false.
    
            # else if the current player makes a move on the board
                # The gameboard validates the move
                    # If the gameboard validation returns true, 
                        # update the gameboard since the play was valid
                        # Check if the current player's rack is empty
                            # If the rack is empty, 
                                # The game is over and the current player won.
                                # Tally up the points.
                                # Display the victory message. 
                            #else
                                # Their turn ends so set Current_Player.turn to false. Game continues.
                    #else
                        # return the tiles back to the current player. Gameboard is not updated since play was invalid.
                        # Current Player draws two tiles from the pool and chooses one.
                        # Their turn ends so set Current_Player.turn to false
    
    
    pygame.time.Clock().tick(FPS)

run_game()
# Quit Pygame
pygame.quit()
sys.exit()