class NavigationController:
    def __init__(self, grid, pathPlanner):
        self.grid = grid
        self.pathPlanner = pathPlanner

        self.startLocation = None
        self.currentPosition = None
        self.targetLocation = None

        self.path = []
        self.pathIndex = 0

        self.chargingMode = False

    # -------------------------------
    # INIT
    # -------------------------------
    def startNav(self, start):
        self.startLocation = start
        self.currentPosition = start

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
        self.path = self.pathPlanner.plan(self.currentPosition, target)
        self.pathIndex = 0

    # -------------------------------
    # UPDATE POSITION
    # -------------------------------
    def updatePosition(self, new_position):
        self.currentPosition = new_position

        x, y = new_position

        if self.grid[x][y] == 1:
            self.grid[x][y] = 4  # cleaned

    # -------------------------------
    # HANDLE OBSTACLE
    # -------------------------------
    def handle_obstacle(self, pos):
        x, y = pos

        if self.grid[x][y] not in [0, 2]:
            self.grid[x][y] = 2

            # Replan ONLY if obstacle affects remaining path
            if pos in self.path[self.pathIndex:]:
                self.requestPath(self.targetLocation)

    # -------------------------------
    # TARGET SELECTION
    # -------------------------------
    def choose_target(self):
        cx, cy = self.currentPosition

        best = None
        best_dist = float('inf')

        for x in range(len(self.grid)):
            for y in range(len(self.grid[0])):
                if self.grid[x][y] == 1:
                    dist = abs(cx - x) + abs(cy - y)
                    if dist < best_dist:
                        best_dist = dist
                        best = (x, y)

        return best

    # -------------------------------
    # CHARGING
    # -------------------------------
    def find_charger(self):
        for x in range(len(self.grid)):
            for y in range(len(self.grid[0])):
                if self.grid[x][y] == 5:
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

        if self.grid[x][y] in [0, 2]:
            self.requestPath(self.targetLocation)
            return None

        self.pathIndex += 1
        return next_tile

    # -------------------------------
    # STATUS
    # -------------------------------
    def is_done_cleaning(self):
        return not any(1 in row for row in self.grid)