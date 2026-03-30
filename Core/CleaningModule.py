class CleaningModule:
    "Represents the robot's main cleaning module."

    def __init__(self, moduleId: int, posX: int, posY: int, currentLocation: tuple[int, int], speed: int, direction: str, isActive: bool) -> None:
        self._module_id = moduleId
        self._pos_x = posX
        self._pos_y = posY
        self._current_location = currentLocation
        self._speed = speed
        self._direction = direction
        self._is_active = isActive

    def unfinishedCleaning(self) -> bool: #TO-DO : implement all of this
        return False

    def startCleaning(self) -> bool:
        return False

    def stop(self) -> bool:
        return True 

    def scan(self) -> None:
        pass

    def setPosition(self, x: int, y: int) -> None:
        pass

    def getBatteryLevel(self) -> float:
        return 0.0

    def noActionTimer(self) -> None:
        pass

    def readBattery(self) -> int:
        return 0

    def requestCharging(self) -> bool:
        return False