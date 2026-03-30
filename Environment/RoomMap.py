class RoomMap:
    def __init__(self, roomId: int, width: int, height: int, objects: list, position: tuple, blueprint: list[list[int]]) -> None:
        self._width = width
        self._height = height
        self._room_id = roomId
        self._objects = objects
        self._position = position
        self._blueprint = blueprint
    def generate(self) -> None:
        pass #TO-DO : implement logic for generating the room mapm map based on the given parameters
    def getRoomId(self) -> int:
        return self._room_id
    def addObject(self, objects: list) -> None:
        pass #TO-DO : implement logic for adding an object to the room map
    def removeObject(self, objects: list) -> None:
        pass #TO-DO : implement logic for removing an object from the room map
    def pushMap(self,module_map) -> None:
        pass #TO-DO : implement logic for pushing the room map to modulemap