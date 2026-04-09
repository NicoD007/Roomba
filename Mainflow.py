import sys
import os

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("Classes"))

from Classes.Environment.SimulationEnvironment import SimulationEnvironment


def main() -> None:
    env = SimulationEnvironment()
    if not env.initialize():
        print("Failed to initialize simulation environment")
        return

    if env._room_map is None:
        print("Failed to create room map")
        return

    room_map = env._room_map
    room_map.generate()

    print("Room generated")

    while env.handle_events():
        env.clear((20, 20, 20))
        env.draw_room_map()
        if env._window is not None:
            env._sprites.draw(env._window)
        env.update()

    env.stop()

    


if __name__ == "__main__":
    main()
