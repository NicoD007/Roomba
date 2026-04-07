class ModuleMap: #Didn't implement arrows yet sorry
    "Represents the robot's internal map."

    def __init__(self, grid, cleanedCell, mapData) -> None:
        self._grid = grid
        self._cleaned_cell = cleanedCell
        self.map = mapData

    def updateObstacles(self) -> None:
        pass

    def updateDirt(self) -> None:
        pass

    def updateCell(self) -> None:
        pass

    def mapComplete(self) -> bool:
        return True #TO-DO : implement logic to determine if the map is complete, meaning all cells have been cleaned and all obstacles have been mapped