import sys
import os

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("Classes"))

from Classes.Environment.SimulationEnvironment import SimulationEnvironment


def main() -> None:
    env = SimulationEnvironment(window_width=900, window_height=650, fps=60)
    print("Starting simulation. Press S to publish 'start'. Press ESC to quit.")

    if not env.initialize():
        print("Failed to initialize simulation environment")
        return

    while env.handle_events():
        env.clear((20, 20, 20))
        env.draw_room_map()
        if env._window is not None:
            env._sprites.draw(env._window)
        env.update()

    env.stop()


if __name__ == "__main__":
    main()
