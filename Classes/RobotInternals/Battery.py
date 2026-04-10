class Battery:
    "Represents the robot's battery and charging behavior."

    LOW_THRESHOLD = 20
    FULL_LEVEL = 100

    def __init__(self, joules: int, batteryPercentage: int) -> None:
        self._joules = joules
        self._batteryPercentage = max(0, min(self.FULL_LEVEL, batteryPercentage))
        self._drainAccumulator = 0.0

    def getLevel(self) -> int:
        return self._batteryPercentage

    def setLevel(self, percentage: int) -> None:
        self._batteryPercentage = max(0, min(self.FULL_LEVEL, percentage))

    def isLow(self, threshold: int = LOW_THRESHOLD) -> bool:
        return self._batteryPercentage <= threshold

    def isFull(self) -> bool:
        return self._batteryPercentage >= self.FULL_LEVEL

    def drain(self, duration: float, rate_per_second: float = 1.0) -> int:
        self._drainAccumulator += duration * rate_per_second
        if self._drainAccumulator < 1.0:
            return self._batteryPercentage

        drain_amount = int(self._drainAccumulator)
        self._drainAccumulator -= drain_amount
        self.setLevel(self._batteryPercentage - drain_amount)
        return self._batteryPercentage

    def charge(self, duration: float, charge_rate: float = 5.0) -> int:
        if duration <= 0 or self.isFull():
            return self._batteryPercentage

        new_level = int(round(self._batteryPercentage + (charge_rate * duration)))
        self.setLevel(new_level)
        return self._batteryPercentage
