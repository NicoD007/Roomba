#Hello
import sys
import os

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("Classes"))

from Classes.Environment.SimulationEnvironment import SimulationEnvironment
from Classes.Environment.RoomMap import RoomMap

def main() -> None:
    

    
    window_width = 900
    window_height = 650
   
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
