
#remove update dirt from diagrams
#change cleanedCell to cleanedCells
#remove grid from diagram and code, not sure of its porpuse
#request map added to code and diagram

class ModuleMap: #Didn't implement arrows yet sorry          #what are arrows? 
    "Represents the robot's internal map."

    def __init__(self, cleanedCells, mapData) -> None:
        self._cleaned_cell = cleanedCells
        self.map = mapData

    def updateMap(self, obstacleLocation) -> None:
        x, y = obstacleLocation
        self.map[x][y] = 4

    def updateCell(self, Location, value) -> None:
        x, y = Location
        self.map[x][y] = value

    def mapComplete(self) -> bool:
        return not any(1 in row for row in self.map)
    
    def requestMap(self):
        return self.map