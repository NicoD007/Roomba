
# should i move numOfRooms into __init__ ?
# roomlist into diagram
#remove posicion
# change objects to obsticleList
# remove roomid  
# add furnished map to diagram and code


import random
from Obstacles import Obstacles

class RoomMap:
    def __init__(self, roomId: int, width: int = 32, height: int = 32, objects: list = None, position: tuple = None, blueprint: list[list[int]] = None, numOfRooms: int = 6) -> None:
        self._width = width
        self._height = height
        self._room_id = roomId # i think i will remove this, it doesent really make sense.
        self._objects = objects
        self._position = position
        self._blueprint = blueprint
        self._rooms = []  # [(start_x, start_y, end_x, end_y, room_id), ...]
        self._numOfRooms = numOfRooms


    def generate(self) -> None:
        self._map = [[0 for _ in range(self._width)] for _ in range(self._height)]
        room_id = 0
        numOfRooms = self._numOfRooms
        # get first room coordinates
        room1_x = random.randint(0, 5+ self._width//2)
        room1_y = random.randint(0, 5+ self._height//2)
        self._rooms.append((0, 0, room1_x, room1_y, room_id))
        
        # Fill first room with 1s
        for x in range(0, room1_x + 1):
            for y in range(0, room1_y + 1):
                self._map[y][x] = 1
        
        # create the remaining rooms
        for i in range(numOfRooms):

            # Picking a starting point from an existing room (with increasing bias towards later rooms)
            weights = list(range(1, len(self._rooms) + 1))  # Higher weights for later rooms
            random_room = random.choices(self._rooms, weights=weights)[0]
            room_start_x, room_start_y, room_end_x, room_end_y, _ = random_room            
            tile_from_room_x = random.randint(room_start_x, room_end_x)
            tile_from_room_y = random.randint(room_start_y, room_end_y)
            '''
            # Picking an endpoint from the full grid (with increasing bias towards the right and bottom)
            W = 0
            H = 0
            for j in range(i//2):
                W = max(random.randint(0,self._width-1),W)
                H = max(random.randint(0,self._height-1),H)
            '''
            # Picking an endpoint from the full grid (without bias)
            W = self._width-1
            H = self._height-1
            random_tile_x = random.randint(0,W)
            random_tile_y = random.randint(0,H)
            
            # Store new room coordinates
            room_id += 1
            new_room_start_x = min(tile_from_room_x, random_tile_x)
            new_room_start_y = min(tile_from_room_y, random_tile_y)
            new_room_end_x = max(tile_from_room_x, random_tile_x)
            new_room_end_y = max(tile_from_room_y, random_tile_y)
            self._rooms.append((new_room_start_x, new_room_start_y, new_room_end_x, new_room_end_y, room_id))
            
            # Fill room thith 1s
            for x in range(new_room_start_x, new_room_end_x + 1):
                for y in range(new_room_start_y, new_room_end_y + 1):
                    self._map[y][x] = 1

        #trimming unused rows and columns
        
        # Trim unused rows and columns
        # Trim rows from bottom
        while self._map and sum(self._map[-1]) == 0:
            self._map.pop()
        # Trim columns from right
        while self._map and all(row[-1] == 0 for row in self._map):
            for row in self._map:
                row.pop()
        # Update dimensions
        self._height = len(self._map)
        self._width = len(self._map[0]) if self._map else 0

        self._blueprint = self._map
        # Create obstacles
        for room in self._rooms:
            start_x, start_y, end_x, end_y, room_id = room
            for _ in range(random.randint(0, 5)):  # Random number of objects per room
                obj_x = random.randint(start_x, end_x)
                obj_y = random.randint(start_y, end_y)
                # Create an Obstacle instance and add to objects list
                size = random.randint(1, 3)
                
                # Check if it fits
                while size >= 1:
                    check_x = obj_x + size - 1
                    check_y = obj_y + size - 1
                    
                    # Verify position is within bounds and on a room tile
                    if check_x < len(self._map[0]) and check_y < len(self._map) and self._map[check_y][check_x] == 1:
                        break  # Valid placement found
                    
                    size -= 1
                
               
                obstacle = Obstacles(size=size, posX=obj_x, posY=obj_y, isMovable=random.choice([True, False]))
                self._objects.append(obstacle)

        # Draw obstacles on the map
        for obstacle in self._objects:
            pattern = obstacle.getShape()
            obj_x, obj_y = obstacle.getPosition()
            # Draw the pattern onto the map
            for py in range(len(pattern)):
                for px in range(len(pattern[0])):
                    if pattern[py][px] == 2:
                        map_y = obj_y + py
                        map_x = obj_x + px
                        if 0 <= map_y < len(self._map) and 0 <= map_x < len(self._map[0]):
                            self._map[map_y][map_x] = 2
                


    def getRoomId(self) -> int:
        return self._room_id
    def addObject(self, objects: list) -> None:
        pass #TO-DO : implement logic for adding an object to the room map
    def removeObject(self, objects: list) -> None:
        pass #TO-DO : implement logic for removing an object from the room map
    def pushMap(self,module_map) -> None:
        pass #TO-DO : implement logic for pushing the room map to modulemap
        #hiiiiiiii