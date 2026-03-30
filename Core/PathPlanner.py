class PathPlanner:
    "Represents the path planning logic for the robot."

    def __init__(self, currentPath, mapData) -> None:
        self._current_path = currentPath
        self._map = mapData

    def findPathToChargingstation(self, start: tuple[int, int]):
        pass

    def recalculatePath(self) -> None:
        pass

    def generatePath(self, start: tuple[int, int], target: tuple[int, int]) -> list[tuple[int, int]]:
        return []

    def updateMap(self) -> None:
        pass

    def readMap(self) -> None:
        pass