import random

class RoomMap:
    def __init__(self, roomId: int, width: int, height: int, objects: list, position: tuple, blueprint: list[list[int]]) -> None:
        self._width = width
        self._height = height
        self._room_id = roomId
        self._objects = objects
        self._position = position
        self._blueprint = blueprint

    def generate(self) -> None:
        self._map = [[0 for _ in range(32)] for _ in range(32)]
        self._rooms = []  # Store rooms as [(start_x, start_y, end_x, end_y, room_id), ...]
        
        # Generate initial room between (0, 0) and (self._height//2, self._width//2)
        room1_x = random.randint(0, self._width//2)
        room1_y = random.randint(0, self._height//2)
        
        # Store room coordinates with room ID
        room_id = 0
        self._rooms.append((0, 0, room1_x, room1_y, room_id))
        
        # Fill initial room with 1s
        for x in range(0, room1_x + 1):
            for y in range(0, room1_y + 1):
                self._map[y][x] = 1
        
        # Generate additional rooms connected to existing rooms
        num_additional_rooms = 3  # Adjust this number as needed
        for i in range(num_additional_rooms):
            # Pick a random existing room
            random_room = random.choice(self._rooms)
            room_start_x, room_start_y, room_end_x, room_end_y, _ = random_room
            
            # Pick a random tile from that room
            tile_from_room_x = random.randint(room_start_x, room_end_x)
            tile_from_room_y = random.randint(room_start_y, room_end_y)
            
            # Pick a random tile in the full grid
            random_tile_x = random.randint(0, 31)
            random_tile_y = random.randint(0, 31)
            
            # Store new room coordinates with room ID
            room_id += 1
            new_room_start_x = min(tile_from_room_x, random_tile_x)
            new_room_start_y = min(tile_from_room_y, random_tile_y)
            new_room_end_x = max(tile_from_room_x, random_tile_x)
            new_room_end_y = max(tile_from_room_y, random_tile_y)
            self._rooms.append((new_room_start_x, new_room_start_y, new_room_end_x, new_room_end_y, room_id))
            
            # Fill the area between them with 1s
            for x in range(new_room_start_x, new_room_end_x + 1):
                for y in range(new_room_start_y, new_room_end_y + 1):
                    self._map[y][x] = 1

    def getRoomId(self) -> int:
        return self._room_id
    def addObject(self, objects: list) -> None:
        pass #TO-DO : implement logic for adding an object to the room map
    def removeObject(self, objects: list) -> None:
        pass #TO-DO : implement logic for removing an object from the room map
    def pushMap(self,module_map) -> None:
        pass #TO-DO : implement logic for pushing the room map to modulemap
        #hiiiiiiii