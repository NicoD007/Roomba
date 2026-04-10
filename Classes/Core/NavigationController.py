from Classes.Core.ModuleMap import ModuleMap
from Classes.Core.PathPlanner import PathPlanner


# constants for the cell nature
WALL = 0
UNCLEANED = 1
OBSTACLE = 2
CLEANED = 3
ROBOT = 4
CHARGER = 5


class NavigationController:
    def __init__(self, moduleMap, pathPlanner):
        self.moduleMap = ModuleMap
        self.pathPlanner = PathPlanner


        self.startLocation = None
        self.currentPosition = (0,0)
        self.targetLocation = None


        self.path = []
        self.pathIndex = 0


        self.chargingMode = False


    # -------------------------------
    # INIT
    # -------------------------------
    def startNav(self, startLocation):
        self.startLocation = startLocation
        self.currentPosition = startLocation


        self.targetLocation = self.choose_target()


        if self.targetLocation:
            self.requestPath(self.targetLocation)
            return True
        return False


    # -------------------------------
    # PATH REQUEST
    # -------------------------------
    def requestPath(self, target):
        if target is None:
            self.path = []
            return


        self.targetLocation = target
        self.path = self.pathPlanner.generatePath(self.currentPosition, target)
        self.pathIndex = 0


    # -------------------------------
    # UPDATE POSITION
    # -------------------------------
    def updatePosition(self, new_position):
        # mark current tile as cleaned if not at start or charger
        if self.currentPosition == self.startLocation:
            x, y = self.currentPosition
            self.moduleMap.map[x][y] = CHARGER #leave charging station alone
        else:
            x, y = self.currentPosition
            self.moduleMap.map[x][y] = CLEANED #place clean tile
       
        self.currentPosition = new_position


        x, y = new_position
        self.moduleMap.map[x][y] = ROBOT  # move


    # -------------------------------
    # HANDLE OBSTACLE
    # -------------------------------
    def handle_obstacle(self, pos):     #isnt it belong in sensor and cleaning module?
        x, y = pos


        if self.moduleMap.map[x][y] not in [WALL, OBSTACLE]:    
            self.moduleMap.map[x][y] = OBSTACLE            


            # Replan ONLY if obstacle affects remaining path
            if self.path and pos in self.path[self.pathIndex:]:
                self.requestPath(self.targetLocation)


    # -------------------------------
    # TARGET SELECTION
    # -------------------------------
    def choose_target(self):            #isnt it belong in cleaning module?
        cx, cy = self.currentPosition
       
        best = None
        best_dist = float('inf')


        for x in range(len(self.moduleMap.map)):
            for y in range(len(self.moduleMap.map[0])):
                if self.moduleMap.map[x][y] == 1:
                    dist = abs(cx - x) + abs(cy - y)


                    if dist < best_dist:
                        best_dist = dist
                        best = (x, y)


        return best


    # -------------------------------
    # CHARGING
    # -------------------------------
    def find_charger(self):
        for x in range(len(self.moduleMap.map)):
            for y in range(len(self.moduleMap.map[0])):
                if self.moduleMap.map[x][y] == CHARGER:
                    return (x, y)
        return None


    def go_to_charge(self):
        charger = self.find_charger()
        if charger:
            self.chargingMode = True
            self.requestPath(charger)


    def stop_charging_mode(self):
        self.chargingMode = False


    # -------------------------------
    # PATH MANAGEMENT
    # -------------------------------
    def ensure_path(self):
        if self.chargingMode:
            return


        if not self.path or self.pathIndex >= len(self.path):
            self.targetLocation = self.choose_target()


            if self.targetLocation:
                self.requestPath(self.targetLocation)


    # -------------------------------
    # MAIN STEP
    # -------------------------------
    def get_next_move(self):
        self.ensure_path()


        if not self.path or self.pathIndex >= len(self.path):
            return None


        next_tile = self.path[self.pathIndex]


        x, y = next_tile


        if self.moduleMap.map[x][y] in [WALL, OBSTACLE]:
            self.requestPath(self.targetLocation)
            return None


        self.updatePosition(next_tile)
        self.pathIndex += 1
        return next_tile


    # -------------------------------
    # STATUS
    # -------------------------------
    def is_done_cleaning(self):
        return not any(UNCLEANED in row for row in self.moduleMap.map)