import sys
import pygame

from ChargingStation import ChargingStation
from Obstacles import Obstacles
from RoomMap import RoomMap


class SimulationEnvironment:
    def __init__(
        self,
        window_width: int = 800,
        window_height: int = 600,
        fps: int = 30,
        title: str = "Simulation Environment",
        charging_station: ChargingStation | None = None,
        obstacles: list[Obstacles] | None = None,
        room_map: RoomMap | None = None,
    ) -> None:
        self._window = None
        self._window_width = window_width
        self._window_height = window_height
        self._fps = fps
        self._title = title
        self._clock = None
        self._running = False
        self._charging_station = charging_station
        self._obstacles = obstacles or []
        self._room_map = room_map

    def initialize(self) -> bool:
        pygame.init()
        self._window = pygame.display.set_mode(
            (self._window_width, self._window_height)
        )
        pygame.display.set_caption(self._title)
        self._clock = pygame.time.Clock()
        self._running = True
        return True

    def stop(self) -> bool:
        self._running = False
        pygame.quit()
        return True

    def set_fps(self, fps: int) -> None:
        self._fps = fps

    def clear(self, color=(30, 30, 30)) -> None:
        if self._window is not None:
            self._window.fill(color)

    def update(self) -> None:
        if self._window is None:
            return

        pygame.display.flip()
        self._clock.tick(self._fps)

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._running = False
        return self._running

    def run_demo(self) -> None:
        if not self.initialize():
            print("Failed to initialize simulation environment")
            return

        while self._running:
            self.handle_events()
            self.clear((20, 20, 20))
            # Blank scene for now; no objects rendered.
            self.update()

        self.stop()


if __name__ == "__main__":
    env = SimulationEnvironment(window_width=900, window_height=650, fps=60)
    env.run_demo()
