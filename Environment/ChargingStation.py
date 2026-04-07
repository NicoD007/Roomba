from RobotInternals.Battery import Battery


class ChargingStation: 
    "Represents the robot's charging station."

    def __init__(self, stationPos: tuple[int, int], chargeRate: float = 5.0, isOccupied: bool = False) -> None:
        self.stationPos = stationPos
        self._chargeRate = chargeRate
        self._isOccupied = isOccupied

    def getChargeRate(self) -> float:
        return self._chargeRate

    def charge(self, battery: Battery, duration: float) -> int:
        if not self._isOccupied:
            return battery.checkBattery()

        if duration <= 0:
            return battery.checkBattery()

        current_level = battery.checkBattery()
        charged_level = min(100, int(round(current_level + (self._chargeRate * duration))))
        battery._battery_percentage = charged_level
        return charged_level

    def atStation(self, position: tuple[int, int]) -> bool:
        return position == self.stationPos