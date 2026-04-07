class Sensor:
    "Represents the robot's sensor."

    def __init__(self, sensorRadius: int) -> None:
        self._sensor_radius = sensorRadius

        # TO-DO: logic for how the sensor detects obstacles and dirt, 
        # and how it interacts with the module map

    def detectObstacles(self, RoomMap) -> bool:
        return False

    def detectDirt(self, RoomMap) -> bool:
        return False
   