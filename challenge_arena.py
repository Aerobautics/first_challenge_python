import matplotlib.pyplot as plt
import matplotlib.lines as lines
from math import sqrt
import numpy as np

# To set up an array that represents the first challenge:
# in python, do the following:
# >>> from challenge_arena import challenge_arena
# >>> arena = challenge_arena(18, 30, 4*18, 4*30, -9, -15)

# The 18 and 30 represent the size of the arena in challenge 1.  (maybe 18x30 meters?)
# The 4*18, etc. represents how finely to divide the arena (0.25 meters per division)
# The -9 and -15 make the arena go from -9...9 and -15...15 in real space.

#To see the empty arena, after creating the arena above, enter the following:
# >>> print(arena.arena_array)

#There is another array called self.searched, that can be populated as the arena is searched.

#I haven't implimented a good visualization yet.

class challenge_arena():
    def __init__(self, size_y, size_x, npoints_y, npoints_x, min_y, min_x):
        # The arena....
        self.nx = npoints_x
        self.ny = npoints_y
        self.sizex = size_x
        self.sizey = size_y
        
        #min points: useful for converting real coords to squares.
        self.minx = min_x 
        self.miny = min_y
        self.arena_array = np.zeros((self.ny, self.nx))
        #has the array been searched?
        self.set_walls()
        self.searched = self.arena_array * 2
        
       
    
    def set_walls(self):
        #Only showing inner walls.  Outer walls are edge of the array.
        #Innter walls:
        #I can't figure these out.  
        #Roughly this:
        #print(self.arena_array.shape)
        wall_1_start = self.convert_to_grid(0,-10)
        
        wall_1_end = self.convert_to_grid(0,10)
        #print(wall_1_start, wall_1_end)
        
        for m in range(wall_1_start[0], wall_1_end[0]+1):
            #print(wall_1_start[1], wall_1_end[1]+1)
            for n in range(wall_1_start[1], wall_1_end[1]+1):
                #print(m,n)
                self.arena_array[n,m] =1
                #print("Setting: ",  n,m, self.arena_array.shape)
        
        wall_2_start = self.convert_to_grid(-5,-10)
        wall_2_end = self.convert_to_grid(5,-10);
        for m in range(wall_2_start[0], wall_2_end[0]+1):
            for n in range(wall_2_start[1], wall_2_end[1]+1):
                #print("Setting: ", n,m, self.arena_array.shape)
                self.arena_array[n,m] =1
        
        wall_3_start = self.convert_to_grid(-5,10)
        wall_3_end = self.convert_to_grid(5,10);
        for m in range(wall_3_start[0], wall_3_end[0]+1):
            for n in range(wall_3_start[1], wall_3_end[1]+1):
                #print("Setting: ", n,m, self.arena_array.shape)
                self.arena_array[n,m] =1
        
    def convert_to_grid(self,ypos, xpos):
        #This routine is neccessary to convert back to grid coords.
        gridx = int((xpos-self.minx) / (self.sizex)* self.nx)
        gridy = int((ypos- self.miny) / (self.sizey) * self.ny)
        grid = [gridx, gridy]
        return grid
    