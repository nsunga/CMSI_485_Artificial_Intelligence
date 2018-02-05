'''
Homework 1 MazeProblem Formalization:
MazeProblems represent 2D pathfinding problems, as programmatically
formalized via:

=== Mazes ===
Represented as a list of strings in which:
  X = impassable wall
  * = the initial state
  . = open cells (movement cost of 1)
  M = mud tiles (movement cost of 3)
  G = goal states (movement cost of 1)
All valid mazes have:
  - Exactly 1 initial state
  - At least 1 goal state
  - A border of walls (plus possibly other walls)
[!] Note: for HW1, a valid maze may *not* have a solution!
(We'll ignore invalid maze states as possible inputs, for simplicity)

Maze elements are indexed starting at (0, 0) [top left of maze]. E.g.,
["XXXXX", "X..GX", "X.M.X", "X*..X", "XXXXX"] is interpretable as:
  01234
0 XXXXX
1 X..GX
2 X.M.X
3 X*..X
4 XXXXX

=== States ===
Representing the position of the agent, as tuples in which:
(x, y) = (col, row)
(0, 0) is located at the top left corner; Right is +x, and Down is +y

=== Actions ===
Representing the allowable Up, Down, Left, and Right movement capabilities
of the agent in the 2D Maze; we'll simply use string representations:
"U", "D", "L", "R"

=== Transitions ===
Given some state s, the transitions will be represented as a list of tuples
of the format:
[(action1, cost_of_action1, result(action1, s)), ...]
For example, if an agent is at state (1, 1), and can only move right and down
into clear tiles (.), then the transitions for that s = (1, 1) would be:
[("R", 1, (2, 1)), ("D", 1, (1, 2))]
'''
class MazeProblem:
    # Static costMap for maze components and the cost to move onto them
    # Any component not listed assumed to have a cost of 1
    costMap = {"M": 3}

    # MazeProblem Constructor:
    # Constructs a new pathfinding problem from a maze, described above
    def __init__(self, maze):
        self.maze = maze
        self.initial = None
        self.goals = []

        for r in list(enumerate(maze)):
            for c in list(enumerate(r[1])):
                state = (c[0], r[0])
                if c[1] is "*":
                    self.initial = state
                if c[1] is "G":
                    self.goals.append(state)
        print("\n")
        print("\n".join(self.maze))
        print("INITIAL PT:", self.initial)
        print("GOAL PTS:", self.goals)
        print("DOING INITIAL PT TRANSITIONS:", self.transitions(self.initial))
        print("MANHATTAN DISTANCE OF INITIAL:", self.heuristic(self.initial))
        # print("GOAL PTS:", self.maze[3][1])


    # goalTest is parameterized by a state, and
    # returns True if the given state is a goal, False otherwise
    def goalTest(self, state):
        if state in self.goals:
            return True
        return False

    # Implements the Manhattan Distance Heuristic, which (given a state)
    # provides the cell-distance to the nearest goal state
    def heuristic(self, state):
        # TODO: STILL GOTTA DO IT, or i think its done..
        distances = []
        for cell in self.goals:
            distances.append(abs(state[0] - cell[0]) + abs(state[1] - cell[1]))

        return min(distances)

    # transitions returns a list of tuples in the format:
    # [(action1, cost_of_action1, result(action1, s), ...]
    # corresponding to allowable actions of the given state, as well
    # as the next state the action leads to
    def transitions(self, state):
        # TODO: Implement as intended
        transitions_list = []
        maze_col = state[0]
        maze_row = state[1]
        move_right = maze_col + 1
        move_left = maze_col - 1
        move_up = maze_row - 1
        move_down = maze_row + 1

        if move_right < len(self.maze[maze_row]):
            if self.maze[maze_row][move_right] != 'X':
                transitions_list.append( ("R", self.cost((move_right, maze_row)), (move_right, maze_row)) )
        if move_left >= 0:
            if self.maze[maze_row][move_left] != 'X':
                transitions_list.append( ("L", self.cost((move_left, maze_row)), (move_left, maze_row)) )
        if move_up >= 0:
            if self.maze[move_up][maze_col] != 'X':
                transitions_list.append( ("U", self.cost((maze_col, move_up)), (maze_col, move_up)) )
        if move_down < len(self.maze):
            if self.maze[move_down][maze_col] != 'X':
                transitions_list.append( ("D", self.cost((maze_col, move_down)), (maze_col, move_down)) )

        return transitions_list

    # cost returns the cost of moving onto the given state, and employs
    # the MazeProblem's costMap
    def cost(self, state):
        cm = MazeProblem.costMap
        cell = self.maze[state[1]][state[0]]
        return cm[cell] if cell in cm else 1

    # solnTest will return a tuple of the format (cost, isSoln) where:
    # cost = the total cost of the solution,
    # isSoln = true if the given sequence of actions of the format:
    # [a1, a2, ...] successfully navigates to a goal state from the initial state
    # If NOT a solution, return a cost of -1
    def solnTest(self, soln):
        trans = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0)}
        s = self.initial
        tc = 0
        for m in soln:
            s = (s[0] + trans[m][0], s[1] + trans[m][1])
            tc += self.cost(s)
            if self.maze[s[1]][s[0]] == "X":
                return (-1, False)
        return (tc, self.goalTest(s))
