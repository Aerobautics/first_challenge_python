import matplotlib.pyplot as plt
import matplotlib.lines as lines
import numpy as np
from challenge_arena import challenge_arena
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection
from time import sleep
from math import sqrt, atan2, sin, cos



def mover(arena, drone_pos,waypoint):
    #Head to drone waypoint
    move_dist = 0.3
    dy = waypoint[1]-drone_pos[1]
    dx = waypoint[0] - drone_pos[0]
#    print("Current: %.2f,%.2f" % drone_pos )
#    print("Heading to: %d,%d" % waypoint )
    
    
    angle = atan2(dy,dx)
    newx = drone_pos[0] + move_dist  * cos(angle)
    
    newy = drone_pos[1] + move_dist  * sin(angle)
#    print(" ")

    new_pos = (newx, newy)
    return new_pos
                              
                              


#First, set up the arena:

ysize = 18
xsize = 30
nptsx = xsize * 4
nptsy = ysize * 4
ymin = -11
xmin = -15
arena = challenge_arena(ysize, xsize, nptsy, nptsx, ymin, xmin)
#This sets up a 72 x 120  array (72 down, 120 across) and fills it with 1's representing interior walls.

#Let's Visualize this:
xmax = xmin + xsize
ymax = ymin + ysize

fig, ax = plt.subplots()

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
            #print(xpoint,ypoint)
            plt.fill([xpoint, xpoint+dx, xpoint+dx, xpoint],[ypoint, ypoint, ypoint+dy, ypoint+dy],'r')

patches = []
            
#Now make the drone appear and do stuff...            
drone_x = 10
drone_y = -9
drone_pos = (drone_x, drone_y)
#
circ = Circle(drone_pos, 0.5,color='#EB70AA',edgecolor=None)
patches.append(circ)
p = PatchCollection(patches, alpha=0.4)

ax.add_patch(circ)


plt.draw()
sleep(0.2)
#Now, make some waypoints:

#Waypoints assuming vision is about 0.5 radius
waypoints = [(14,-10.5),(9.3,-10.5),(9.1,-0.5),(-9.0,-0.5), (-9.0,-2), (8,-2),(8 ,-3.5),(-9,-3.5), (-9,-5),(8,-5),(8,-10.5), (6.5,-10.5),(6.5, -6.5),(5,-6.5),(5,-10.5),(3.5,-10.5),(3.5,-6.5),(2,-6.5),(2,-10.5),(0.5,-10.5),(0.5,-6.5),(-1,-6.5),(-1,-10.5),(-2.5,-10.5),(-2.5,-6.5), (-4,-6.5),(-4,-10.5),(-5.5,-10.5),(-5.5,-6.5),(-7,-6.5),(-7,-10.5),(-8.5,-6.5),(-8.5,-10.5),(-14.5,-10.5), (-14.5,6),(14.5,6), (14.5,-9),(13,-9),(13,4.5), (-13,4.5),(-13,-9),(-11,-9),(-11,4.5),(-9,4.5),(-9,1),(9,1),(9,2.5),(-8,2.5),(-8,3.5),(8,3.5),(11,3.5),(11,-9.5),(12,-9.5),(12,4)]

for x in waypoints: 
    print("Heading to: %.2f,%.3f" % x )
#    print(x[0])
#    print(drone_pos[0])
        
#    print(x[0] - drone_pos[0])
    dist = sqrt((x[0] - drone_pos[0])**2+(x[1] - drone_pos[1])**2)
    while dist > 0.2:
        old_pos = drone_pos
        drone_pos = mover(arena, drone_pos, x)
        circ = Circle(drone_pos, 0.5,color='#EB70AA',edgecolor=None)
        patches.append(circ)
        p = PatchCollection(patches, alpha=0.4)
        ax.add_patch(circ)
        plt.plot([old_pos[0],drone_pos[0]], [old_pos[1],drone_pos[1]], 'b')
        plt.draw()
        dist = sqrt((x[0] - drone_pos[0])**2+(x[1] - drone_pos[1])**2)

print("DONE!!!")
plt.show()