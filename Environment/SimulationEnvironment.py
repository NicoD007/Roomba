class SimulationEnvironment:
    def __init__ (self, window: object, windowWidth: int, windowHeight: int, fps: int, title: str, ChargingStation) -> None:
        self._window = window
        self._window_width = windowWidth
        self._window_height = windowHeight
        self._fps = fps
        self._title = title
        self._charging_station = ChargingStation

    def initialize(self) -> bool:
        return False #TO-DO : implement logic for initializing the simulation environment, such as setting up the window and any necessary libraries
    def stop(self) -> bool:
        return False #TO-DO : implement logic for stopping the simulation environment and cleaning up any resources
    def setFps(self, fps: int) -> None:
        self._fps = fps