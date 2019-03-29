#!/usr/local/bin/python3

def printforest():
    for i in range(rows):
        print(forest[i*rows:i*rows+cols])

def get_neighbours(pos):
    neighbours = ''
    ds = [(-1,0),(1,0),(0,-1),(0,1),(1,1),(-1,1),(1,-1),(-1,-1)]
    for d in ds:
        r, c = pos[0] + d[0], pos[1] + d[1]
        neighbours += forest[r*rows+c]
    return neighbours

def insert(source_str, char, pos):
    return source_str[:pos] + char + source_str[pos+1:]

with open('18.txt') as f:
    data = f.readlines()

rows = len(data) + 2 # padding
cols = len(data[0]) - 1 + 2 # remove newline char
forest = " " * cols # padding to create valid neighbours for the edges

for line in data:
    forest += " " + line[:-1] + " " # remove newline char (-1)
forest += " " * cols

printforest()

previous_states = dict()

has_jumped = False

i = 0
while i < 1e9:
    # check if previously seen for part 2
    if not has_jumped:
        if forest in previous_states.keys():
            has_jumped = True
            step = i - previous_states[forest]
            i = i%step + (1e9 // step) * step
        else:
            previous_states[forest] = i
    i += 1

    # update forest
    new_forest = forest;
    for r in range(1,rows-1):
        for c in range(1,cols-1):
            neighbours = get_neighbours((r,c))
            n_trees = neighbours.count('|')
            n_lumberyards = neighbours.count('#')
            acre = forest[r*rows+c]
            if acre == '.' and n_trees >= 3:
                new_forest = insert(new_forest, '|', r*rows+c)
            elif acre == '|' and n_lumberyards >= 3:
                new_forest = insert(new_forest, '#', r*rows+c)
            elif acre == '#' and not (n_lumberyards >= 1 and n_trees >= 1):
                new_forest = insert(new_forest, '.', r*rows+c)

    forest = new_forest

    # part 1
    if i == 10:
        part1 = forest.count('|')*forest.count('#')

    printforest()

print('Total resource value (Part 1):', part1)
print('Total resource value (Part 2):', forest.count('|')*forest.count('#'))
