import sys
import os

from Classes.RobotInternals.Sensor import Sensor

# Add Classes directory to sys.path for absolute imports
classes_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if classes_path not in sys.path:
    sys.path.insert(0, classes_path)

import pygame

from Environment.ChargingStation import ChargingStation
from Environment.RoomMap import RoomMap
from Core.CleaningModule import CleaningModule
from Communication.MQTTClient import MQTTClient
from Core.NavigationController import NavigationController
from RobotInternals.Sensor import Sensor
from Core.ModuleMap import ModuleMap

# constants for the cell nature
WALL = 0
UNCLEANED = 1
OBSTACLE = 2
CLEANED = 3
ROBOT = 4
CHARGER = 5

class SimulationEnvironment:
    def __init__(
        self,
        window_width: int = 800,
        window_height: int = 600,
        fps: int = 30,
        title: str = "Simulation Environment",
        charging_station: ChargingStation | None = None,
        cleaning_module: CleaningModule | None = None,
        navigation: NavigationController | None = None,
        sensor: Sensor | None = None,
        Roommap : RoomMap | None = None,
        Modulemap : ModuleMap = ModuleMap([], [])
    ) -> None:
        self._window = None
        self._window_width = window_width
        self._window_height = window_height
        self._fps = fps
        self._title = title
        self._clock = None
        self._running = False
        self._room_map = Roommap
        self._module_map = Modulemap
        self._cleaning_module = CleaningModule(30,0,0) #initialize cleaning module with default values
        self._sprites = pygame.sprite.Group()
        self._mqtt_client = None
        self._mqtt_connected = False
        self.navigation = navigation
        self.sensor = sensor

    def initialize(self) -> bool:
        pygame.init()
        self._window = pygame.display.set_mode(
            (self._window_width, self._window_height)
        )
        pygame.display.set_caption(self._title)
        self._clock = pygame.time.Clock()
        self._running = True
        # Calculate tile size based on the room map's maximum dimension
        blueprint = getattr(self._room_map, '_blueprint', None)
        if blueprint:
            rows = len(blueprint)
            cols = len(blueprint[0]) if blueprint[0] else 0
            max_dim = max(rows, cols)
            cell_width = self._window_width // max_dim if max_dim else 20
            cell_height = self._window_height // max_dim if max_dim else 20
            self._cell_size = min(cell_width, cell_height)
        else:
            self._cell_size = 30  # fallback
        '''add cleaning module size here somehow'''
        
        setattr(CleaningModule, 'tileSize', self._cell_size)

        # Add cleaning module to sprites if provided
        if self._cleaning_module is not None:
            self._sprites.add(self._cleaning_module)

        return True

    def step(self):
        if not self.navigation:
            return
        
        # ask for the next move from navigation controller
        next_pos = self.navigation.get_next_move()

        if next_pos is None:
            return
        
        if self._cleaning_module.currentLocation == (0,0):
            self._module_map.updateCell(self._cleaning_module.currentLocation, CHARGER)  # Mark as robot's current position
        else:
            self._module_map.updateCell(self._cleaning_module.currentLocation, CLEANED)  # Mark as robot's current position
        
        # Move the ROOMBA
        self._cleaning_module.moveTo(next_pos)

        # Update robot position in the map
        self._module_map.updateCell(self._cleaning_module.currentLocation, ROBOT)  # Mark as robot's current position
        

        # Sensor handling
        if self.sensor:
            obstacles = self.sensor.Scan(next_pos, getattr(self._module_map, 'map'))

            for obs in obstacles:
                self.navigation.handle_obstacle(obs)
        
    def connect_mqtt(self) -> bool:
        if self._cleaning_module is None:
            self._mqtt_connected = False
            return False

        self._mqtt_client = MQTTClient(self._cleaning_module)
        self._mqtt_connected = self._mqtt_client.connect()
        return self._mqtt_connected
        if self._cleaning_module is None:
            self._mqtt_connected = False
            return False

        self._mqtt_client = MQTTClient(self._cleaning_module)
        self._mqtt_connected = self._mqtt_client.connect()
        return self._mqtt_connected

    def publish_start_command(self) -> bool:
        if self._mqtt_client is None or not self._mqtt_connected:
            if self._cleaning_module is not None:
                self._cleaning_module.startCleaning()
                print("Fallback start: cleaning started locally.")
                return True
            return False

        published = self._mqtt_client.publish_command("start")
        if not published and self._cleaning_module is not None:
            self._cleaning_module.startCleaning()
            print("Fallback start: cleaning started locally.")
            return True
        return published

    def stop(self) -> bool:
        if self._mqtt_client is not None:
            self._mqtt_client.disconnect()
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
        if not blueprint:
            return
            
        # Calculate cell size to fit the map in the window
        cell_width = self._window_width // len(blueprint)
        cell_height = self._window_height // len(blueprint[0]) if blueprint[0] else 20
        cell_size = min(cell_width, cell_height)
        
        # Draw each cell
        for x, column in enumerate(blueprint):
            for y, cell in enumerate(column):
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
                elif event.key == pygame.K_s:
                    if self.publish_start_command():
                        print("Published: start")
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
            self.step()
            
            # Draw all sprites
            if self._window is not None:
                self._sprites.draw(self._window)
            dt = self.update() #dt will be used for charging per second and for drain

           

        self.stop()
