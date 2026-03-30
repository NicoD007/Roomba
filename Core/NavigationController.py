class NavigationController:
    "Handles movement and navigation execution."

    def __init__(self, targetLocation: tuple[int, int], startLocation: tuple[int, int], PathPlanner, pathIndex: int) -> None:
        self._target_location = targetLocation
        self._start_location = startLocation
        self._PathPlanner = PathPlanner
        self._path_index = pathIndex

    def moveTo(self, target: tuple[int, int]) -> None:
        pass

    def requestPath(self, target: tuple[int, int]) -> None:
        pass

    def followPath(self) -> None:
        pass

    def updatePosition(self, new_position: tuple[int, int]) -> None:
        pass

    def startNav(self) -> bool:
        return True

    def getNextMove(self) -> tuple[int, int]:
        return (0, 0)