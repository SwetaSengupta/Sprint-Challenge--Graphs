
from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Util classes from utils file
from utils import Stack, Queue

# Helper functions from helpers file
from helpers import inverse_point, uncharted_path


# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
# Once this is full, the loop will stop and we will have completed the spec
visited = {}

# This is the Main loop running while visited is less than # of rooms
while len(visited) < len(room_graph):
    # Get current room and it's exits
    room_id = player.current_room.id
    room_exits = player.current_room.get_exits()

    # If current room is not in visited, add it
    if room_id not in visited:
        visited[room_id] = { points: '?' for points in room_exits }
    
    # Get current room's exits
    uncharted = [point for point in visited[room_id] if visited[room_id][point] == '?']
    
    # If uncharted is not an empty list, explore an unknown room
    if len(uncharted) > 0:
        # make a random index to go to the next unexplored room
        next_room_index = random.randint(0, len(uncharted)-1)
        next_point = uncharted[next_room_index]

        # move to the uncharted room
        player.travel(next_point)
        
        # Add this travel destination to your main path
        traversal_path.append(next_point)
        
        # Now we know what the next room is, set it for the previous room's direction index
        next_room_id = player.current_room.id
        visited[room_id][next_point] = next_room_id
        
        # If next room is not in visited, add it
        if next_room_id not in visited:
            next_room_exits = player.current_room.get_exits()
            visited[next_room_id] = { points: '?' for points in next_room_exits }
        
        # Now we know the room where we came from is the opposite direction of the current room
        rev_point = inverse_point(next_point)
        visited[next_room_id][rev_point] = room_id

    # else find your way back to the nearest unexplored room using BFS
    else:
        traversal_path += uncharted_path(visited, room_id, player)




# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")





