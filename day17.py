#!/usr/local/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.setrecursionlimit(3000)

# some initial values
maxy = 0
miny = 10000
maxx = 0
minx = 10000

# updates minimum and maximum values
def update(minimum, maximum, x):
    minimum = min(minimum, x)
    maximum = max(maximum, x)
    return minimum, maximum

# list of clay tiles
clays = []

with open("17.txt") as f:
    for line in f.readlines():

        splitted = line.split('=')
        first = splitted[0]
        first_number, second = splitted[1].split(', ')
        second_start, second_end = splitted[2].split('..')
        second_start, second_end = int(second_start), int(second_end)

        if first == 'x':
            x = int(first_number)
            minx, maxx = update(minx, maxx, x)
            miny, maxy = update(miny, maxy, second_start)
            miny, maxy = update(miny, maxy, second_end)
            for y in range(second_start, second_end+1):

                clays.append((y,x))

        if first == 'y':
            y = int(first_number)
            miny, maxy = update(miny, maxy, y)
            minx, maxx = update(minx, maxx, second_start)
            minx, maxx = update(minx, maxx, second_end)
            for x in range(second_start, second_end+1):
                clays.append((y,x))

# uses some unneccesary space below minx and miny
ground = np.empty((maxy+2, maxx+2),dtype='str')

for x in range(minx-1, maxx+2):
    for y in range(miny-1, maxy+2):
        ground[y,x] = '.'

for clay in clays:
    ground[clay] = '#'

def plot_ground():
    vg = ground[miny-1:maxy+2,minx-1:maxx+2]
    plt.imshow((vg == '#') + 4* (vg == '|') + 3* (vg == '~'))
    plt.show()


# lets the water flow down
def flow_down(y, x):
    if y > maxy:
        # bottom found!!
        return True
    else:
        if ground[y, x] == '#': # or ground[y,x] == '~':
            # bottom not found here
            return False
        else:
            # let water flow down
            ground[y, x] = '|'
            if flow_down(y+1, x):
                # bottom found somewhere deeper
                return True
            else:
                # let water flow left and right
                a = flow_side(y, x, -1)
                b = flow_side(y, x, 1)
                # fill with '~' if walls on both sides
                if not(a or b):
                    xtmp = x
                    while ground[y,xtmp] != '#':
                        ground[y,xtmp] = '~'
                        xtmp -= 1
                    xtmp = x
                    while ground[y,xtmp] != '#':
                        ground[y,xtmp] = '~'
                        xtmp += 1
                # return bottom in either direction
                return a or b

def flow_side(y, x, delta):
    x += delta
    if ground[y, x] == '#':
        # a wall (or other water) was hitted
        return False
    if ground[y, x] == '|':
        # if water already flowing here, it will reach somewhere
        return True
    else:
        ground[y, x] = '|'
        if ground[y+1,x] == '.':
            # let water flow down
            down = flow_down(y+1,x)
            if down:
                return True
                # or else flow to the side again
        return flow_side(y, x, delta)

# start filling from the spring at x = 500, y = 0
flow_down(1, 500)

# calculate the number of water tiles (miny according to rules...)
print("Part 1: Number of water tiles:", np.sum(ground[miny:] == '|')
                                        + np.sum(ground == '~'))
print("Part 2: Number of still water tiles:",  np.sum(ground == '~'))

# plot the ground!
plot_ground()
