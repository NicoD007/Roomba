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


def main() -> None:
    
    
    # push room map to module map
    module_map = ModuleMap(cleanedCells=set(), mapData=room_map._map)

    # inform the path planner of the module map so it can requestMap() when needed
    path_planner = PathPlanner([], module_map)
    # inform the navigation controller of the module map and path planner so it can requestPath() when needed
    navigation = NavigationController(module_map, path_planner)

    # start Roomba
    start_pos = (cleaningmodule.x, cleaningmodule.y)
    navigation.startNav(start_pos)

    # Create simulation environment with the components
    env = SimulationEnvironment(
        window_width=window_width,
        window_height=window_height,
        fps=60,
    )

    

    # Run the simulation
    env.run_demo()



if __name__ == "__main__":
    main()
