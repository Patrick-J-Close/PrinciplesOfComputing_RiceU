# http://www.codeskulptor.org/#user42_kBZ6DnFDUa_7.py

"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7

"""
Queue class
"""

class Queue:
    """
    A simple implementation of a FIFO queue.
    """

    def __init__(self):
        """ 
        Initialize the queue.
        """
        self._items = []

    def __len__(self):
        """
        Return the number of items in the queue.
        """
        return len(self._items)
    
    def __iter__(self):
        """
        Create an iterator for the queue.
        """
        for item in self._items:
            yield item

    def __str__(self):
        """
        Return a string representation of the queue.
        """
        return str(self._items)

    def enqueue(self, item):
        """
        Add item to the queue.
        """        
        self._items.append(item)

    def dequeue(self):
        """
        Remove and return the least recently inserted item.
        """
        return self._items.pop(0)

    def clear(self):
        """
        Remove all items from the queue.
        """
        self._items = []
        

class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for cell in self._zombie_list:
            yield cell

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for cell in self._human_list:
            yield cell
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        # create visited grid as empty with equal size
        visited = poc_grid.Grid(self.get_grid_height(), self.get_grid_width())
        
        # create distance field list with h * w value for each entry
        distance_field = [[ self.get_grid_height() * self.get_grid_width() \
                           for dummy_col in range(self.get_grid_width())] \
                          for dummy_row in range(self.get_grid_height())]
                           
        # create boundary queue as a copy of entity list
        boundary = poc_queue.Queue()
                                                 
        if entity_type == 7:
            for zombie in self.zombies():
                boundary.enqueue(zombie)
                visited.set_full(zombie[0], zombie[1])
                distance_field[zombie[0]][zombie[1]] = 0
        elif entity_type == 6:
            for human in self.humans():
                boundary.enqueue(human)
                visited.set_full(human[0], human[1])
                distance_field[human[0]][human[1]] = 0
        
        while len(boundary) != 0:
            cell = boundary.dequeue()
            neighbors = self.four_neighbors(cell[0], cell[1])
            
            for neighbor in neighbors:
                # check not obstacle
                if self.is_empty(neighbor[0], neighbor[1]):
                    if visited.is_empty(neighbor[0], neighbor[1]):
                        visited.set_full(neighbor[0], neighbor[1])
                        boundary.enqueue(neighbor)
                        neighbor_dist = distance_field[neighbor[0]][neighbor[1]]
                        current_cell_dist = distance_field[cell[0]][cell[1]] + 1
                        distance_field[neighbor[0]][neighbor[1]] = \
                        min(neighbor_dist, current_cell_dist)
        return distance_field
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        visited = poc_grid.Grid(self.get_grid_height(), self.get_grid_width())
        obstacles = len(zombie_distance_field) * len(zombie_distance_field[0])
        temp_list = []
        
        for human in self.humans():
            best_moves = {}
            neighbors = visited.eight_neighbors(human[0], human[1])
            best_moves[zombie_distance_field[human[0]][human[1]]] = human
            for neighbor in neighbors:
                if zombie_distance_field[neighbor[0]][neighbor[1]] > \
                zombie_distance_field[human[0]][human[1]] and zombie_distance_field[neighbor[0]][neighbor[1]] != obstacles:
                    best_moves[zombie_distance_field[neighbor[0]][neighbor[1]]] = neighbor
            temp_list.append(best_moves[max(best_moves)])
        self._human_list = temp_list
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        visited = poc_grid.Grid(self.get_grid_height(), self.get_grid_width())
        temp_list = []
        
        for zombie in self.zombies():
            best_moves = {}
            neighbors = visited.four_neighbors(zombie[0], zombie[1])
            best_moves[human_distance_field[zombie[0]][zombie[1]]] = zombie
            for neighbor in neighbors:
                if human_distance_field[neighbor[0]][neighbor[1]] < \
                human_distance_field[zombie[0]][zombie[1]]:
                    best_moves[human_distance_field[neighbor[0]][neighbor[1]]] = neighbor
            temp_list.append(best_moves[min(best_moves)])
        self._zombie_list = temp_list                             
                               
            

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Apocalypse(30, 40))

### TEST CODE ###
#test = Apocalypse(10,12)
#test.set_full(5,5)
#test.set_full(3,4)
#print test
#test.clear()
#print test

#test.add_zombie(2,2)
#test.add_zombie(3,3)
#print test._zombie_list
#print test.num_zombies()
#for num in test.zombies():
#    print num
