import matplotlib.pyplot as plt
import matplotlib.lines as lines
import numpy as np
from challenge_arena import challenge_arena


#First, set up the arena:

ysize = 18
xsize = 30
nptsx = xsize * 4
nptsy = ysize * 4
ymin = -9
xmin = -15
arena = challenge_arena(ysize, xsize, nptsy, nptsx, ymin, xmin)
#This sets up a 72 x 120  array (72 down, 120 across) and fills it with 1's representing interior walls.

#Let's Visualize this:
xmax = xmin + xsize
ymax = ymin + ysize
plt.fill([xmin, xmin, xmin-0.1, xmin - 0.1],[ymin, ymax, ymax, ymin],'b') # outer wall left
plt.fill([xmax, xmax, xmax+0.1, xmax + 0.1],[ymin, ymax, ymax, ymin],'b') # outer wall right
plt.fill([xmin, xmax, xmax, xmin], [ymin - 0.1, ymin - 0.1, ymin, ymin],'b')# outer wall lower
plt.fill([xmin, xmax, xmax, xmin], [ymax + 0.1, ymax + 0.1, ymax, ymax],'b')# outer wall upper


#now loop through the arena.  
dx = xsize / nptsx
dy = ysize / nptsy

for m in range(0,nptsy):
    for n in range(0,nptsx):
        if arena.arena_array[m,n] == 1:
            xpoint = n*dx + xmin
            ypoint = m * dy + ymin
            print(xpoint,ypoint)
            plt.fill([xpoint, xpoint+dx, xpoint+dx, xpoint],[ypoint, ypoint, ypoint+dy, ypoint+dy],'r')

plt.show()