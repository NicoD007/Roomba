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
    
    


    # start Roomba
    start_pos = (cleaningmodule.x, cleaningmodule.y)
    NavigationController.startNav(start_pos)

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
