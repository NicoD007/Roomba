class Obstacles:
    "Represents an obstacle in the environment."

    def __init__(self, size: float, posX: int, posY: int, isMovable: bool) -> None:
        self._size = size
        self._pos_x = posX
        self._pos_y = posY
        self._is_movable = isMovable

    def getPosition(self) -> tuple:
        return (self._pos_x, self._pos_y) 

    def getSize(self) -> float:
        return self._size 

    def move(self, posX: int, posY: int) -> None:
        pass #TO-DO : implement logic for moving the obstacle if it is movable, and updating its position accordingly