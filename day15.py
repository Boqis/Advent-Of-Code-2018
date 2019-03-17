#!/usr/local/bin/python3
import numpy as np

import time

TYPE = 0
HP = 1

data = []
with open('15h.txt') as f:
    for line in f.readlines():
        data.append([i for i in line])

data = np.array(data)

# print data to console
def print_data(mat):
    for line in mat:
        print(''.join(line), end='')

# prints playing field
def print_field():
    field = cave.copy()
    for pos in players.keys():
        player = players[pos]
        field[pos] = player[TYPE]
    print_data(field)

# finds targets other than team
def find_targets(team):
    targets = []
    for pos in players.keys():
        player = players[pos]
        if player[0] != team:
            targets.append(pos)
    return targets

# finds squares adjacent to squares at targets (excluding blocked)
def find_adjacent(targets, blocked):
    adjacent = []
    for target in targets:
        for dr, dc in [(-1,0),(0,-1),(0,1),(1,0)]: # up, left, right, down
            new = (target[0]+dr, target[1]+dc)
            if cave[new] == '.' and new not in blocked:
                adjacent.append(new)
    return adjacent

# constructs search graph
def get_graph():
    graph = neighbours.copy()
    for player in players.keys():
        graph[player] = []
    return graph

# top to bottom, then left to right
def reading_order(x):
    return x[0]*100+x[1]

# search for goals (bfs)
def search(start, goals):
    nexts = set()
    visited = set()
    parents = dict()
    nexts.add(start)
    parents[start] = None

    # search until path found or all possiblities tested
    # returns found goal, path length
    while len(nexts) > 0:
        parent = nexts.pop()
        # check if goal
        if parent in goals:
            steps = 0
            node = parent
            while parents[parent] != None:
                parent = parents[parent]
                steps += 1
            return parent, steps
        else:
            # expant node
            graph = get_graph()
            for child in graph[parent]:
                if child not in visited:
                    if child not in nexts:
                        parents[child] = parent
                        nexts.add(child)
            visited.add(parent)
    # no path found
    return (-1,-1), 1e10

# let player at pos attack neighbours if in range
# returns attack succesful
def attack(pos):
    player = players[pos]
    team = player[TYPE]
    neighbours = find_adjacent([pos], dict())
    lowest_hp = 300
    target = (-1,-1)
    for neighbour in neighbours:
        if neighbour in players.keys():
            possible_enemy = players[neighbour]
            if possible_enemy[TYPE] != team:
                if possible_enemy[HP] < lowest_hp:
                    target = neighbour
                    lowest_hp = possible_enemy[HP]
    if target != (-1,-1):
        enemy = players[target]
        new_hp = enemy[HP] - 3
        if new_hp <= 0:
            del players[target]
            alive[enemy[TYPE]] -= 1
        else:
            players[target] = (enemy[TYPE],new_hp)
        return True
    return False



# players states
players = dict() # players[pos] = (type, hp)
alive = dict()
alive['E'] = 0
alive['G'] = 0

# calculate the cave (play field without players) and the players
cave = data.copy()
for row in range(len(data)):
    for col in range(len(data[0])):
        type = data[row,col]
        if type == 'E' or type == 'G':
            cave[row,col] = '.'
            players[(row,col)] = (type, 200) # 200 hp
            alive[type] += 1

# create cave neighbour-dict
neighbours = {}
for row in range(len(cave)):
    for col in range(len(cave[0])):
        if cave[row,col] == '.':
            neighbours[(row,col)] = find_adjacent([(row,col)], dict())

# plays the game until one team wins
def play():
    round = 0
    while alive['E'] > 0 and alive['G'] > 0:
        print('Round:', round)
        player_order = list(players.keys())
        player_order.sort(key = lambda x: reading_order(x))
        for i, pos in enumerate(player_order):
            if pos in players.keys(): # might have been killed
                player = players[pos]
                targets = find_targets(player[0])
                goals = find_adjacent(targets, players)
                # if no enemy in range, first move, then attack
                if not attack(pos):
                    possible_first_steps = find_adjacent([pos], players)
                    shortest_path_length = 1e9
                    next_step = (-1,-1)
                    for first_step in possible_first_steps:
                        # sorted by reading order
                        goal, path_length = search(first_step, goals)
                        if path_length < shortest_path_length:
                            shortest_path_length = path_length
                            next_step = first_step
                            shortest_goal = goal
                        elif path_length == shortest_path_length:
                            if reading_order(goal) < reading_order(shortest_goal):
                                next_step = first_step
                                shortest_goal = goal

                    if next_step != (-1,-1):
                        players[next_step] = players[pos]
                        del players[pos]
                        attack(next_step)

            if alive['E'] == 0 or alive['G'] == 0:
                if i == len(player_order)-1:
                    return round + 1
                else:
                    return round

        round += 1
        print_field()
        #time.sleep(1)

rounds = play()
print_field()

hp_sum = 0
for pos in players.keys():
    player = players[pos]
    hp_sum += player[HP]

print(hp_sum)
print(rounds)

print(players)
print('Outcome:', rounds * hp_sum)

## TODO: när plocka ut round??


# 15d  37 * 982 = 36334

# 15f  35 * 793 = 27755
# 15g  54 * 536 = 28944
# 15h  20 * 937 = 18740


# 2418
# 155

# = 374790 not correct....
# = 377 208 not correct (space??)
# = 377208 too high...
