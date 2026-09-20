import search
import util

class robotNavigation(search.SearchProblem):

    """
    Robot Navigation with Obstacles — SearchProblem formulation.

    Find a path from a start cell to a goal cell on a 2D grid while avoiding
    obstacles. Works with any width/height, start, goal, and obstacle layout.

    Constructor args:
        width, height       — grid size
        start_pos, goal_pos — (x, y) Cartesian coordinates
        obstacles           — list of (x, y) obstacle cells
        needs_heuristic     — if True, A* uses Euclidean distance (default False)

    Formulation:
        1. State representation
           A state is a free grid cell (x, y). Obstacles and out-of-bounds
           cells are not valid states.

        2. Initial state
           The starting position start_pos (marked S on the grid).

        3. Goal state
           The goal position goal_pos (marked G). A state is a goal iff
           state == goal_pos.

        4. Possible actions
           Four moves: 'up', 'down', 'left', 'right'
           (dy=+1, dy=-1, dx=-1, dx=+1 respectively).

        5. Successor function
           For each action, the successor is (x+dx, y+dy) if that cell is
           inside the grid and not an obstacle. Returns triples
           (successor_state, action, step_cost).

        6. Action cost
           Every legal move has cost 1. Path cost is the number of moves.

        7. Heuristic (for A* Search)
           Euclidean distance from the current cell to the goal:
           h(state) = sqrt((x - goal_x)^2 + (y - goal_y)^2).
           Admissible for unit-cost 4-directional movement. Returns 0 when
           needs_heuristic is False (Dijkstra-style behaviour).

    Grid legend (see printCurrentState):
        S = start, G = goal, # = obstacle, . = free cell
    """

    def __init__(self, width, height, start_pos, goal_pos, obstacles, needs_heuristic = False):
        self.width = width 
        self.height = height
        self.start_pos = start_pos # tuple containing start coordinate (x,y)
        self.goal_pos = goal_pos # tuple containing goal coordinate (x,y)
        self.obstacles = obstacles # list of tuples containing obstacle coordinates
        self.needs_heuristic = needs_heuristic

    def getStartState(self):
        return self.start_pos

    def isGoalState(self, state):
        return state == self.goal_pos

    def getSuccessors(self, state):
        successors = []
        current_position = state # current (x,y)
        moves = {
            'up' : (0, 1), # move name : (dx, dy)
            'down': (0, -1,),
            'right': (1, 0),
            'left': (-1, 0)
        }

        for action, (dx, dy) in moves.items():
            next_state = (current_position[0] + dx, current_position[1] + dy)
            if 0 <= next_state[0] < self.width and 0 <= next_state[1] < self.height and next_state not in self.obstacles:
                step_cost = 1
                successors.append((next_state, action, step_cost))

        return successors

    def getCostOfActions(self, actions):
        total_cost = 0
        current_state = self.start_pos

        for action in actions:
            successors = self.getSuccessors(current_state)
            action_is_legal = False
            for next_state, valid_action, step_cost in successors:
                if action == valid_action:
                    total_cost += step_cost
                    current_state = next_state
                    action_is_legal = True
                    break
            if not action_is_legal:
                return -1

        return total_cost
        


    def getHeuristic(self, state):
        # returns the Euclidean Distance from current state to the goal state if needs_heuristic == True
        if not self.needs_heuristic:
            return 0
        # squareroot((x2-x1)^2 + (y2-y1)^2)
        return util.euclideanDistance(state, self.goal_pos)


# The function below is just to help me visualize the states

    def printCurrentState(self):
        # Outer loop starts at height-1, the step is -1, and it stops when the loop reaches -1
        # Trying to use the standard Cartesian coordinate system
        for y in range(self.height-1, -1, -1):
            for x in range(0, self.width):
                if (x, y) in self.obstacles:
                    print("#", end="") # using end="" we can remove the newline symbol and print on the same line
                elif (x, y) == self.start_pos:
                    print("S", end="")
                elif (x, y) == self.goal_pos:
                    print("G", end="")
                else:
                    print(".", end="")
            # Move to the next row using empty print
            print()

