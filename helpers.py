# Util classes from utils file
from utils import Stack
from utils import Queue

# This BFS will take the player back to the nearest room that has an unexplored exit
def uncharted_path(currentPath, room_id, player):
    # Create an empty set to store visited nodes
    visited = set()
    # Create an empty Queue and enqueue A PATH TO the starting vertex
    q = Queue()
    path = [room_id]
    q.enqueue(path)
    # While the queue is not empty...
    while q.size() > 0:
        # Dequeue the first PATH
        p = q.dequeue()
        # GRAB THE VERTEX FROM THE START OF THE PATH
        v = p[0]
        # IF VERTEX == TARGET ('?'), SET PATH THEN BREAK
        if v == '?':
            path = p[1:]
            break
        # If that vertex has not been visited...
        if v not in visited:
            # Mark it as visited
            visited.add(v)
            # Then add A PATH TO all of its neighbors to the back of the queue
            for neighbors in currentPath[v]:
                node = currentPath[v][neighbors]
                new_path = p.copy()
                new_path.insert(0, node)
                q.enqueue(new_path)
    # this list will contain the directions that the player needs to move back
    movements = []
    
    # While loop runs trying to create a path of movements
    while len(path) > 1:
        # remove the last room and store as a variable
        current = path.pop(-1)
        # find the direction that will take you to the prior room and add it to a movements list
        for route in currentPath[current]:
            if currentPath[current][route] == path[-1]:
                movements.append(route)
    
    # for every element in movements, move in that direction until you reach the spot
    for move in movements:
        player.travel(move)

    # return the movements to be appended to traversalPath
    return movements

# This function is only for getting the opposite compass pointer to update our question marks for the room we just came from
def inverse_point(point):
    if point == 'n':
        direc = 's'
    elif point == 's':
        direc = 'n'
    elif point == 'e':
        direc = 'w'
    elif point == 'w':
        direc = 'e'
    return direc