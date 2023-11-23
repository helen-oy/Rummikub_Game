# Lets create our Rummikub Game:
import pygame
import sys
import random

# import game_objects
# Initialize Pygame
pygame.init()


# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
BLUE = (0, 0, 180)
RED = (180, 0, 0)
GREEN = (0,180,0)
YELLOW = (250,250,0)
WHITE = (255,255,255)
PURPLE = (128,0,128)

tile_colors = [RED,BLUE,GREEN,YELLOW,PURPLE]
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Classes
class Tile:
    def __init__(self, value, color):
        self.value = value
        self.color = color
        self.width, self.height = 50, 70
        self.image = pygame.image.load('tile.png')

    def draw(self, x, y):
        screen.blit(self.image, (x, y))
        # pygame.draw.rect(screen, self.color, (x, y, self.width, self.height))
        font = pygame.font.Font(None, 36)
        text = font.render(str(self.value), True, self.color)
        screen.blit(text, (x+3, y+3))
    def show(self):
        pass
    # Create tiles with values 1-15 and F

# The racks holds tiles for each player
class Rack:
    def __init__(self):
        # start with an empty rack
        self.tiles = []

    def draw(self, x, y):
        font = pygame.font.Font(None, 36)
        text = font.render(str(self.value), True, BLUE)
        screen.blit(text, (x, y))

   
    
    # get total value of tiles in the rack
    def get_total_value(self):
        value = 0
        for tile in self.tiles:
            value += tile.value
        return value
    
class Pool:
    def __init__(self):
        self.tiles = [Tile(i + 1, t) for t in tile_colors for i in range(15)]

    # def remove_picked_tiles(self):
    #     for _ in range(picked_tiles):
    #         self.tiles.pop()
    #     return self.tiles
# Crate an instance of Pool object to be used by players

pool = Pool()
# define class sets which holds runs and groups 
class Sets:
    def __init__(self,tiles):
        self.tiles = tiles

    def create(self):
        pass

class Group(Sets):
    def __init__(self):
        super().__init__()

    def create_group(self):
        pass

class Runs(Sets):
    def __init__(self):
        super().__init__()
        self.valid_runs = []

    def create_runs(self,n, m):
        """
        This creates a list of all possible runs: 
        `n` is an integer representing minimum length of runs
        `m` is the maximum length of runs
        """
        valid_runs_even = []
        valid_runs_odd = []
    
        numlist = [i + 1 for i in range(15)]
        even = [i for i in numlist if i % 2 == 0]
        odd = [i for i in numlist if i % 2 != 0]

    
        for i in range(n, m + 1):
            valid_runs_even.extend([even[j:j + i] for j in range(len(even) - i + 1)])
            valid_runs_odd.extend([odd[j:j + i] for j in range(len(odd) - i + 1)])
        
        self.valid_runs = valid_runs_even + valid_runs_odd
        
        return self.valid_runs

# valid_runs = Runs().create_runs()



class Player:
    def __init__(self,name):
        self.rack = Rack()
        self.name = name

    def pick_tiles_from_pool(self):
        # for beginning the game
        first_two = random.sample(Pool().tiles,2) #leaves pool unchanged
        score = 0
        for tile in first_two:
            score += tile.value
        return score 
    
    # during gameplay
    def add_tile_to_rack(self,selected_tiles):
        selected_tiles = random.sample(Pool().tiles,2)
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
    
    def play_tile(self,tile):
        self.rack.remove(tile)
        # board.append(tile) append tile to the board
        pass
        ## add the picked tile to game board to form a set or run


    def create_run(self): 
        self.run = []
        self.run.append(self.pick_tile_from_rack(tile))
        # check if the run is valid

        
    def create_group(self):
        pass

bukayo = Player('Bukayo Saka')
# 
class ValidMoves:
    def __init__(self,player):
        self.player = player

    # validate player moves 
    def validate_run(self):
        if 3<=len(self.player.run)<=5:
            if all(j.value % 2==0 for _,j in enumerate(self.player.run)):
                if all(self.player.run[i+1].value-self.player.run[i].value==2 for i,_ in enumerate(self.player.run[:-1])):
                    return True
                else:
                    print("Error: This is not a valid move")
                    return False
                    

    def validate_group(self):
        if 3<=len(self.player.run)<=5:
            if all(i==j for i,j in zip(self.player.run,self.player.run)):
                if all(self.player.run[i+1].color!=self.player.run[i] for i,j in enumerate(self.player.run[:-1])):
                    pass
                ## to be completed






# Initialize Pygame window

pygame.display.set_caption("Rummikub")

# Create tiles



# Shuffle tiles
# random.shuffle(tiles)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw tiles
    screen.fill(WHITE)
    x, y = 50, 50
    for tile in Pool().tiles:
        print(tile.value,tile.color)
        tile.draw(x, y)
        x += 70  # Spacing between tiles

    pygame.display.flip()
    pygame.time.Clock().tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
