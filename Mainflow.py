#Hello
import sys
import os

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("Classes"))

from Classes.Environment.SimulationEnvironment import SimulationEnvironment
from Classes.Environment.RoomMap import RoomMap
from Classes.Core.CleaningModule import CleaningModule
from Classes.Environment.ChargingStation import ChargingStation
from Classes.Core.NavigationController import NavigationController
from Classes.Core.PathPlanner import PathPlanner
from Classes.Core.ModuleMap import ModuleMap
from Classes.RobotInternals.Sensor import Sensor

def main() -> None:
    
    room_map = RoomMap(width=22, height=25, numOfRooms=4)
    room_map.generate()

    module_map = room_map.pushMap(room_map._objectlessBlueprint)

    path_planner = PathPlanner([], module_map)
    navigation = NavigationController(module_map, path_planner)

    cleaningmodule = CleaningModule(30,0,0)
    navigation.startNav((0, 0))

    window_width = 800
    window_height = 600

    env = SimulationEnvironment(
        window_width = window_width,
        window_height = window_height,
        fps = 30,     #change this back to 10 when submitting
        navigation = navigation,
        sensor=Sensor(1),
        Roommap = room_map,
        Modulemap = module_map
        )
   

    # Run the simulation
    env.run_NOT_demo()

if __name__ == "__main__":
    main()
