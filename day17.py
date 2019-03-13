#!/usr/local/bin/python3
import numpy as np
import matplotlib.pyplot as plt

# some initial values
maxy = 0
miny = 10000
maxx = 0
minx = 10000

def updateX(minx, maxx, x):
    if x > maxx:
        maxx = x
    elif x < minx:
        minx = x
    return minx, maxx

def updateY(miny, maxy, y):
    if y > maxy:
        maxy = y
    elif y < miny:
        miny = y
    return miny, maxy

clays = []

with open("17ex.txt") as f:
    for line in f.readlines():

        splitted = line.split('=')
        first = splitted[0]
        num1, sec = splitted[1].split(', ')
        secs, sece = splitted[2].split('..')

        if first == 'x':
            x = int(num1)
            minx, maxx = updateX(minx, maxx, x)
            for y in range(int(secs), int(sece)+1):
                miny, maxy = updateY(miny, maxy, y)
                clays.append((y,x))

        if first == 'y':
            y =int(num1)
            miny, maxy = updateY(miny, maxy, y)

            for x in range(int(secs), int(sece)+1):
                minx, maxx = updateX(minx, maxx, x)
                clays.append((y,x))


#print(clays)
#print(maxx, minx)
#print(maxy, miny)


#ground = np.empty((maxx-miny+1, maxy-miny+1),dtype='str')
ground = np.empty((maxy+1, maxx+1),dtype='str')

for x in range(minx, maxx+1):
    for y in range(miny, maxy+1):
        ground[y,x] = '.'

for clay in clays:
    ground[clay] = '#'

def print_ground():
    #np.set_printoptions(threshold=np.inf)
    visground = ground[miny:maxy+1,minx:maxx+1]

    # print terrain...
    for line in visground:
        print(''.join(line))




def fill_down(y, x):
    while ground[y, x] == '.':
        ground[y, x] = '|'
        y += 1

    fill_left(y-1,x-1)
    fill_right(y-1,x+1)

def fill_left(y, x):
    while ground[y, x] == '.':
        ground[y, x] = '|'
        x -= 1

def fill_right(y, x):
    while ground[y, x] == '.':
        ground[y, x] = '|'
        x += 1

fill_down(1, 500)

print_ground()





#plt.imshow(ground == '#')
#plt.show()
