"""
Clone of 2048 game.
"""
# http://www.codeskulptor.org/#user41_P4CeSAZ17Y_28.py

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: [1, 0],
           DOWN: [-1, 0],
           LEFT: [0, 1],
           RIGHT: [0, -1]}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    
    shifted = []
    result = []
    skip_next = False
    
    # shift all non-zero values to left
    for num in line:
        if num != 0:
            shifted.append(num)
    while len(shifted) < len(line):
        shifted.append(0)
    
    # merge adjacent equal values from left to right
    for num in range(0,len(shifted) - 1):
        if skip_next:
            skip_next = False
        else:
            if shifted[num] == shifted[num + 1]:
                result.append(shifted[num] * 2)
                skip_next = True
            else:
                result.append(shifted[num])
    
    if shifted[-1] != 0 and skip_next == False:
        result.append(shifted[-1])
    
    while len(result) < len(line):
        result.append(0)
        
    return result

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, height, width):
        
        self.grid_height = height
        self.grid_width = width
        self.grid_values = []
        
        # create initial list of tiles for each direction
        self.start_pos = {UP: [[0, num] for num in range(self.get_grid_width())],
                         DOWN: [[self.get_grid_height() - 1, num] for num in range(self.get_grid_width())],
                         RIGHT: [[num, self.get_grid_width() - 1] for num in range(self.get_grid_height())],
                         LEFT: [[num, 0] for num in range(self.get_grid_height())]}
        
        # REMOVE for GUI version
        self.reset()
        
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        
        self.grid_values = [[0 for col in range(self.get_grid_width())]
                           for row in range(self.get_grid_height())]
        self.new_tile()
        self.new_tile()
        
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        result = ""
        print(self.grid_values)
        for row in range(self.get_grid_height()):
            for col in range(self.get_grid_width()):
                result += str(self.get_tile(row, col)) + " "                     
        return result

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        init_list = self.start_pos[direction]
        temp_list = []
        moved = False   
    
        if direction == UP or direction == DOWN:
            num_steps = self.get_grid_height()
        elif direction == RIGHT or direction == LEFT:
            num_steps = self.get_grid_width()
        
        for start_cell in init_list:
            temp_list = []
            merged_list = []
            for step in range(0,num_steps):
                row = start_cell[0] + step * OFFSETS[direction][0]
                col = start_cell[1] + step * OFFSETS[direction][1]
                temp_list.append(self.get_tile(row,col))

            # merge tiles
            merged_list = merge(temp_list)
            if merged_list != temp_list:
                moved = True
            for step in range(num_steps):
                row = start_cell[0] + step * OFFSETS[direction][0]
                col = start_cell[1] + step * OFFSETS[direction][1]
                self.set_tile(row, col, merged_list[step])

        if moved:
            self.new_tile()
        
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """     
        iterate = True
        while iterate:
            rand_row = random.choice(range(self.get_grid_height()))
            rand_col = random.choice(range(self.get_grid_width()))
            if self.get_tile(rand_row,rand_col) == 0:
                iterate = False
                
        rand = random.random()
        if rand < 0.1:
            value = 4
        else:
            value = 2
            
        self.set_tile(rand_row, rand_col, value)

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self.grid_values[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self.grid_values[row][col]

#test_game = TwentyFortyEight(4,4)
#poc_2048_gui.run_gui(test_game)



