import sys

sys.path.insert(0, "Classes")

from Environment.SimulationEnvironment import SimulationEnvironment


def main() -> None:
    env = SimulationEnvironment(window_width=900, window_height=650, fps=60)
    print("Starting simulation. Press S to publish 'start'. Press ESC to quit.")
    env.run_demo()


if __name__ == "__main__":
    main()
