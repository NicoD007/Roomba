class Battery:
    "Represents the robot's battery."

    def __init__(self, joules: int, batteryPercentage: int) -> None:
        self._joules = joules
        self._battery_percentage = batteryPercentage

    def checkBattery(self) -> int:
        "Return the current battery percentage."
        return self._battery_percentage

    def beep(self) -> None:
        "Trigger a warning if battery is critically low."
        if self._battery_percentage < 5: # TO-DO: implement an actual 
            # warning for this method
            pass