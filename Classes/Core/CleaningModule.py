import pygame
from typing import Optional, Tuple
from RobotInternals.Sensor import Sensor
from Core.ModuleMap import ModuleMap
from RobotInternals.Battery import Battery
from Environment.RoomMap import RoomMap

# changes will be made: shanges cleaning module size from pixel to tiles
# remove  xpixelLocation: int, ypixelLocation: int, sizepixel: int = 50
class CleaningModule(pygame.sprite.Sprite):
    def __init__(self,tileSize: int, xTileLocation: int = 0, yTileLocation: int = 0) -> None:
        super().__init__()

        self.moduleID: int = None
        self.currentLocation: Tuple[int, int] = (xTileLocation, yTileLocation)
        self.speed: int = 0
        self.direction: str = ""
        self.isActive: bool = False
        self.unFinishedCleaning: bool = False
        self._sensor = Sensor(1)
        self._battery = Battery(joules=100, batteryPercentage=30)

        self.size = tileSize
        self.image = self._draw_roomba(tileSize)
        self.rect = self.image.get_rect(center=(tileSize//2, tileSize//2))

    def _draw_roomba(self, size: int) -> pygame.Surface:
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        cx, cy = size // 2, size // 2
        radius = size // 2 - 2

        # Body
        pygame.draw.circle(surface, (60, 60, 60), (cx, cy), radius)

        # Inner ring
        pygame.draw.circle(surface, (80, 80, 80), (cx, cy), int(radius * 0.75), 1)

        # Bumper arc (front = top)
        bumper_rect = pygame.Rect(cx - int(radius * 0.85), cy - int(radius * 0.85),
                                  int(radius * 1.7), int(radius * 1.7))
        pygame.draw.arc(surface, (120, 120, 120), bumper_rect,
                        pygame.math.Vector2(0, -1).angle_to(pygame.math.Vector2(1, 0)) * 3.14159 / 180,
                        3.14159, 4)

        # Center button
        btn_r = max(size // 8, 4)
        pygame.draw.circle(surface, (40, 40, 40), (cx, cy), btn_r)
        pygame.draw.circle(surface, (100, 100, 100), (cx, cy), btn_r, 1)

        # Sensor eyes
        eye_offset = size // 7
        eye_r = max(size // 14, 2)
        for ex in [cx - eye_offset, cx + eye_offset]:
            ey = cy - size // 6
            pygame.draw.circle(surface, (30, 30, 30), (ex, ey), eye_r)
            pygame.draw.circle(surface, (200, 200, 200), (ex - 1, ey - 1), max(eye_r // 2, 1))

        # Side brushes
        brush_color = (90, 90, 90)
        brush_len = size // 6
        for side in [-1, 1]:
            bx = cx + side * (radius - 2)
            by = cy + size // 8
            for angle_offset in [-15, 0, 15]:
                import math
                angle = math.radians(90 + angle_offset)
                ex2 = int(bx + side * brush_len * math.cos(angle))
                ey2 = int(by + brush_len * math.sin(angle))
                pygame.draw.line(surface, brush_color, (bx, by), (ex2, ey2), 1)

        # Outline
        pygame.draw.circle(surface, (100, 100, 100), (cx, cy), radius, 1)

        return surface

    def setPosition(self, x: int, y: int) -> None:
        self.currentLocation = (x, y)

    def startCleaning(self) -> bool:
        self.isActive = True
        return self.isActive

    def stop(self) -> bool:
        self.isActive = False
        return not self.isActive

    def scan(self) -> list:
        
        S = Sensor(1)
        grid = getattr(RoomMap, 'blueprint')
        location = self.currentLocation
        

        return S.Scan(location, grid)

    def getBatteryLevel(self) -> float:
        return float(self._battery.getLevel())

    def noActionTimer(self) -> None:
        pass

    def readBattery(self) -> int:
        return self._battery.checkBattery()

    def setBatteryLevel(self, batteryPercentage: int) -> None:
        self._battery.setBattery(batteryPercentage)

    def requestCharging(self) -> bool:
        return self.readBattery() < 20

    def shutDown(self) -> bool:
        return self.stop()

    def moveTo(self, target: Tuple[int, int]) -> None:
        if target is None:
            return
        self.setPosition(target[0], target[1])
        self.updateSpritePosition(self.tileSize)

    def updateSpritePosition(self, cell_size: int):
        tile_x, tile_y = self.currentLocation

        pixel_x = tile_x * cell_size + cell_size // 2
        pixel_y = tile_y * cell_size + cell_size // 2

        self.rect.center = (pixel_x, pixel_y)

    def temp(self) -> None:
        #used to see if something compiles, ignore
        self.scan()

        pass