
#remove update dirt from diagrams
#change cleanedCell to cleanedCells
#remove grid from diagram and code, not sure of its porpuse

class ModuleMap: #Didn't implement arrows yet sorry          #what are arrows? 
    "Represents the robot's internal map."

    def __init__(self, grid, cleanedCells, mapData) -> None:
        self._grid = grid
        self._cleaned_cell = cleanedCells
        self.map = mapData

    def updateObstacles(self, obstacleLocation) -> None:
        x, y = obstacleLocation
        self.map[x][y] = 4

    def updateCell(self, Location, value) -> None:
        x, y = Location
        self.map[x][y] = value

    def mapComplete(self) -> bool:
        return not any(1 in row for row in self.map)