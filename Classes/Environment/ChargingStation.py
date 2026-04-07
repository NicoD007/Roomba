from Core.CleaningModule import CleaningModule


class ChargingStation:
    "Represents the robot's charging station."

    def __init__(self, stationPos: tuple[int, int], chargeRate: float = 5.0) -> None:
        self.stationPos = stationPos
        self._chargeRate = chargeRate

    def getChargeRate(self) -> float:
        return self._chargeRate

    def charge(self, cleaningModule: CleaningModule, duration: float = 1.0) -> int:
        if duration <= 0:
            return cleaningModule.readBattery()

        current_level = cleaningModule.readBattery()
        charged_level = min(100, int(round(current_level + (self._chargeRate * duration))))
        cleaningModule.setBatteryLevel(charged_level)
        return charged_level

    def atStation(self, position: tuple[int, int]) -> bool:
        return position == self.stationPos
