
# should i move numOfRooms into __init__ ?
# roomlist into diagram
#remove posicion
# change objects to obsticleList
# remove roomid  
# add furnished map to diagram and code


import random

class RoomMap:
    def __init__(self, roomId: int, width: int = 32, height: int = 32, objects: list = None, position: tuple = None, blueprint: list[list[int]] = None) -> None:
        self._width = width
        self._height = height
        self._room_id = roomId # i think i will remove this, it doesent really make sense.
        self._objects = objects
        self._position = position
        self._blueprint = blueprint
        self._rooms = []  # [(start_x, start_y, end_x, end_y, room_id), ...]


    def generate(self) -> None:
        self._map = [[0 for _ in range(self._width)] for _ in range(self._height)]
        room_id = 0
        numOfRooms = 3  # Adjust this number as needed

        # get first room coordinates
        room1_x = random.randint(0, self._width//2)
        room1_y = random.randint(0, self._height//2)
        self._rooms.append((0, 0, room1_x, room1_y, room_id))
        
        # Fill first room with 1s
        for x in range(0, room1_x + 1):
            for y in range(0, room1_y + 1):
                self._map[y][x] = 1
        
        # create the remaining rooms
        for i in range(numOfRooms):

            # Picking a starting point from an existing room
            random_room = random.choice(self._rooms)
            room_start_x, room_start_y, room_end_x, room_end_y, _ = random_room            
            tile_from_room_x = random.randint(room_start_x, room_end_x)
            tile_from_room_y = random.randint(room_start_y, room_end_y)
            
            # Picking an endpoint from the full grid
            random_tile_x = random.randint(0, 31)
            random_tile_y = random.randint(0, 31)
            
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
        
        self._blueprint = self._map
        #adding objects to the map
        for room in self._rooms:
            start_x, start_y, end_x, end_y, room_id = room
            for _ in range(random.randint(0, 5)):  # Random number of objects per room
                obj_x = random.randint(start_x, end_x)
                obj_y = random.randint(start_y, end_y)
                self._map[obj_y][obj_x] = 2  
                self._objects.append((obj_x, obj_y))  # Store object position
                


    def getRoomId(self) -> int:
        return self._room_id
    def addObject(self, objects: list) -> None:
        pass #TO-DO : implement logic for adding an object to the room map
    def removeObject(self, objects: list) -> None:
        pass #TO-DO : implement logic for removing an object from the room map
    def pushMap(self,module_map) -> None:
        pass #TO-DO : implement logic for pushing the room map to modulemap
        #hiiiiiiii