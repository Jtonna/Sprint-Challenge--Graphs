from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

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
traversalPath = []

backwardsDirections = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

reversePath = [None]

rooms = {}

roomsdict = {}

rooms[0] = player.current_room.getExits()

roomsdict[0] = player.current_room.getExits()

while len(rooms) < len(roomGraph)-1:
    print(f"rooms length:{len(rooms)} < room graph len:{len(roomGraph)} -1 ")
    if player.current_room.id not in rooms:
        print(f"    room:{player.current_room.id} is not in rooms dict.")
        rooms[player.current_room.id] = player.current_room.getExits()
        roomsdict[player.current_room.id] = player.current_room.getExits()
        lastDirection = reversePath[-1]
        roomsdict[player.current_room.id].remove(lastDirection)
        print(f"        Just removed {lastDirection} from the roomsdict")

    while len(roomsdict[player.current_room.id]) < 1:
        print(f"the room's id:{len(roomsdict[player.current_room.id])} is < 1")
        reverse = reversePath.pop()
        traversalPath.append(reverse)
        player.travel(reverse)
        print(f"    Just popped from the reverse path & appended the traversal path: {reverse}\n    Making the player travel the path now")


    exit_dir = roomsdict[player.current_room.id].pop(0)
    traversalPath.append(exit_dir)
    reversePath.append(backwardsDirections[exit_dir])
    player.travel(exit_dir)

    if len(roomGraph) - len(rooms) ==1:
        print(f"room graph length:{len(roomGraph)} - room len:{len(room)} is 1. \ngetting exits for the current room")
        rooms[player.current_room.id] = player.current_room.getExits()
        print(f"{player.current_room.getExits()}")



# TRAVERSAL TEST
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
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
