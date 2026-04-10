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
    
    window_width = 900
    window_height = 650
    blueprint = getattr(room_map, '_blueprint', None)
    if blueprint:
        rows = len(blueprint)
        cols = len(blueprint[0]) if blueprint[0] else 0
        max_dim = max(rows, cols)
        cell_size = min(window_width // max_dim, window_height // max_dim)
        window_width = cell_size * max_dim
        window_height = cell_size * max_dim
    else:
        cell_size = 30  # fallback
    
    module_map = room_map.pushMap(room_map._blueprint)
    path_planner = PathPlanner([], module_map)
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
