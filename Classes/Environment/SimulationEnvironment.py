import sys
import os
import pygame

# Add parent directory to path so we can import from Core and Environment
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ChargingStation import ChargingStation
from RoomMap import RoomMap
from Core.CleaningModule import CleaningModule
from Obstacles import Obstacles


class SimulationEnvironment:
    def __init__(
        self,
        window_width: int = 800,
        window_height: int = 600,
        fps: int = 30,
        title: str = "Simulation Environment",
        charging_station: ChargingStation | None = None,
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
        self._room_map = room_map
        self._sprites = pygame.sprite.Group()
        self._cleaning_module = None

    def initialize(self) -> bool:
        pygame.init()
        self._window = pygame.display.set_mode(
            (self._window_width, self._window_height)
        )
        pygame.display.set_caption(self._title)
        self._clock = pygame.time.Clock()
        self._running = True
        
        # Initialize room map if not provided
        if self._room_map is None:
            self._room_map = RoomMap(roomId=1, width=64, height=42, objects=[], numOfRooms=6)
            self._room_map.generate()
        
        # Initialize cleaning module in top-left corner
        self._cleaning_module = CleaningModule(50, 50, 50)
        self._sprites.add(self._cleaning_module)
        
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

    def draw_room_map(self) -> None:
        if self._window is None or self._room_map is None:
            return
        
        # Get the blueprint from room map
        blueprint = getattr(self._room_map, '_blueprint', None)
        if blueprint is None:
            return
            
        # Calculate cell size to fit the map in the window
        cell_width = self._window_width // len(blueprint[0]) if blueprint[0] else 20
        cell_height = self._window_height // len(blueprint) if blueprint else 20
        cell_size = min(cell_width, cell_height)
        
        # Draw each cell
        for y, row in enumerate(blueprint):
            for x, cell in enumerate(row):
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                if cell == 1:  # Room floor
                    pygame.draw.rect(self._window, (100, 100, 100), rect)
                    pygame.draw.rect(self._window, (150, 150, 150), rect, 1)  # Border
                elif cell == 2:  # Object/obstacle
                    pygame.draw.rect(self._window, (200, 50, 50), rect)  # Red for obstacles
                    pygame.draw.rect(self._window, (255, 100, 100), rect, 1)
                elif cell == 0:  #wall
                    pygame.draw.rect(self._window, (20, 20, 20), rect)  # Gray for walls
                    pygame.draw.rect(self._window, (50, 50, 50), rect, 1)
                elif cell == 3:  #cleaned tile
                    pygame.draw.rect(self._window, (255, 182, 193), rect)  # pink
                    pygame.draw.rect(self._window, (50, 50, 50), rect, 1)
                elif cell == 4:  #cleaning module                                                       #place roomba sprite on top of it
                    pygame.draw.rect(self._window, (146, 41, 82), rect)  # por por a
                    pygame.draw.rect(self._window, (150, 150, 150), rect, 1)
                elif cell == 5:  #charging station
                    pygame.draw.rect(self._window, (245, 217, 10), rect)  # yollowww
                    pygame.draw.rect(self._window, (50, 50, 150), rect, 1)


    def update(self) -> float:
        if self._window is None or self._clock is None:
            return 0.0

        pygame.display.flip()
        delta_ms = self._clock.tick(self._fps)
        return delta_ms / 1000.0

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
            # Draw room map
            self.draw_room_map()
            # Draw all sprites
            if self._window is not None:
                self._sprites.draw(self._window)
            dt = self.update() #dt will be used for charging per second and for drain

           

        self.stop()


if __name__ == "__main__":
    env = SimulationEnvironment(window_width=900, window_height=650, fps=60)
    env.run_demo()
