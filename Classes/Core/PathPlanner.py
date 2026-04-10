from Classes.Core.ModuleMap import ModuleMap


# constants for the cell nature
WALL = 0
UNCLEANED = 1
OBSTACLE = 2
CLEANED = 3
ROBOT = 4
CHARGER = 5


class PathPlanner:
    "This class handles the path planning logic for the roomba using a greedy approach."


    def __init__(self, currentPath, moduleMap=None) -> None:
        self._current_path = currentPath or []


        # Keep a ModuleMap reference so PathPlanner can explicitly requestMap().
        if moduleMap is not None:
            self._module_map = moduleMap
        else:
            self._module_map = ModuleMap([], [])


        self._map = self._module_map.requestMap()


        self._visit_count = {}  # prevent loops


    # -------------------------------
    # MAP REQUEST (diagram flow)
    # -------------------------------
    def requestMap(self):
        self._map = self._module_map.requestMap()
        return self._map


    # -------------------------------
    # PUBLIC: PATH TO CHARGER
    # -------------------------------
    def findPathToChargingstation(self, start: tuple[int, int]):
        self.requestMap()
        charger = self._find_charger()


        if charger:
            self._current_path = self.generatePath(start, charger)


        return self._current_path


    # -------------------------------
    # RECALCULATE PATH
    # -------------------------------
    def recalculatePath(self) -> None:
        if not self._current_path:
            return


        # Recalculate from current position to last target
        start = self._current_path[0]
        target = self._current_path[-1]


        self._current_path = self.generatePath(start, target)


    # -------------------------------
    # CORE: GENERATE PATH (VERY SIMPLE GREEDY APPROACH)
    # -------------------------------
    def generatePath(self, start: tuple[int, int], target: tuple[int, int]) -> list[tuple[int, int]]:
        path = []
        current = start


        visited_local = set()


        max_steps = len(self._map) * len(self._map[0])  # safety limit


        for _ in range(max_steps):


            if current == target:
                break


            next_move = self._get_best_neighbor(current, target)


            if next_move is None:
                break  # stuck


            if next_move in visited_local:
                break  # loop detected


            path.append(next_move)
            visited_local.add(next_move)


            # track visits globally (anti-loop behavior)
            self._visit_count[next_move] = self._visit_count.get(next_move, 0) + 1


            current = next_move


        return path


    # -------------------------------
    # UPDATE MAP (called externally)
    # -------------------------------
    def updateMap(self, new_map=None) -> None:
        if new_map is not None:
            self._map = new_map
            if hasattr(self._module_map, "map"):
                self._module_map.map = new_map




    # -------------------------------
    # INTERNAL: FIND CHARGER
    # -------------------------------
    def _find_charger(self):
        for x in range(len(self._map)):
            for y in range(len(self._map[0])):
                if self._map[x][y] == CHARGER:
                    return (x, y)
        return None


    # -------------------------------
    # INTERNAL: BEST NEIGHBOR (CORE LOGIC)
    # -------------------------------
    def _get_best_neighbor(self, pos, target):
        neighbors = self._get_neighbors(pos)


        best = None
        best_score = float('-inf')


        for n in neighbors:
            if not self._is_walkable(n):
                continue


            score = self._evaluate_cell(n, target)


            if score > best_score:
                best_score = score
                best = n


        return best


    # -------------------------------
    # CELL EVALUATION (WEIGHTS)
    # -------------------------------
    def _evaluate_cell(self, pos, target):
        x, y = pos
        cell = self._map[x][y]


        # Base score
        if cell == UNCLEANED:        
            score = 10
        elif cell == CLEANED:    
            score = 1
        elif cell == CHARGER:      
            score = 5
        else:
            return float('-inf')


        # Prefer getting closer to target
        dist = abs(pos[0] - target[0]) + abs(pos[1] - target[1])
        score += max(0, 10 - dist)  # closer = better


        # Penalize revisits (prevents loops)
        visits = self._visit_count.get(pos, 0)
        score -= visits * 5 # each visit reduces score


        return score


    # -------------------------------
    # WALKABLE CHECK
    # -------------------------------
    def _is_walkable(self, pos):
        x, y = pos


        if x < 0 or y < 0:
            return False
        if x >= len(self._map) or y >= len(self._map[0]):
            return False


        return self._map[x][y] not in [WALL, OBSTACLE]


    # -------------------------------
    # Surrounding cells
    # -------------------------------
    def _get_neighbors(self, pos):
        x, y = pos
        return [
            (x+1, y),
            (x-1, y),
            (x, y+1),
            (x, y-1),
        ]
