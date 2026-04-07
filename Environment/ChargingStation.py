class ChargingStation: 
    "Represents the robot's charging station."

    def __init__(self, stationPos: tuple[int, int], isOccupied: bool, chargeRate: float) -> None:
        self.station_pos = stationPos
        self._isOccupied = isOccupied
        self._chargeRate = chargeRate

    def getChargeRate(self) -> float:
        return self._chargeRate

    def isOccupied(self) -> bool:
        return self._isOccupied

    def charge(self, CleaningModule) -> int:
        return 0 #TO-DO : implement logic for charging the robot's battery based on charge rate and time spent at station

    def atStation(self) -> bool:
        return True #TO-DO : Make this work
    #Test I only want to change this