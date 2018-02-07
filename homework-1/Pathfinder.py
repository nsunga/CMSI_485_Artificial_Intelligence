'''
The Pathfinder class is responsible for finding a solution (i.e., a
sequence of actions) that takes the agent from the initial state to the
optimal goal state.

This task is done in the Pathfinder.solve method, as parameterized
by a maze pathfinding problem, and is aided by the SearchTreeNode DS.
'''

from MazeProblem import MazeProblem
from SearchTreeNode import SearchTreeNode
import heapq
import unittest

class Pathfinder:

    @staticmethod
    def solve(problem):
        # TODO: Implement A* graph search!
        priority_queue = []
        visited_states = []
        root = SearchTreeNode(problem.initial, None, None, 0,
                            problem.heuristic(problem.initial))
        temp_node = root
        visited_states.append(temp_node.state)
        while not problem.goalTest(temp_node.state):
            children_list = problem.transitions(temp_node.state)

            for every_tuple in children_list:
                temp_node.children.append(SearchTreeNode(every_tuple[2],
                                        every_tuple[0], temp_node,
                                        every_tuple[1] + temp_node.totalCost,
                                        problem.heuristic(every_tuple[2])))

            for child in temp_node.children:
                heapq.heappush(priority_queue, child)

            temp_node = heapq.heappop(priority_queue)

            if temp_node.state not in visited_states:
                visited_states.append(temp_node.state)
            else:
                while temp_node.state in visited_states:
                    if len(priority_queue) == 0: return None
                    temp_node = heapq.heappop(priority_queue)

                visited_states.append(temp_node.state)

        path = []
        while temp_node.state != root.state:
            path.append(temp_node.action)
            temp_node = temp_node.parent

        path.reverse()
        return path

class PathfinderTests(unittest.TestCase):
    def test_maze1(self):
        maze = ["XXXXX", "X..GX", "X...X", "X*..X", "XXXXX"]
        problem = MazeProblem(maze)
        soln = Pathfinder.solve(problem)
        solnTest = problem.solnTest(soln)
        print(soln)
        self.assertTrue(solnTest[1])
        self.assertEqual(solnTest[0], 4)

    def test_maze2(self):
        maze = ["XXXXX", "XG..X", "XX..X", "X*..X", "XXXXX"]
        problem = MazeProblem(maze)
        soln = Pathfinder.solve(problem)
        solnTest = problem.solnTest(soln)
        print(soln)
        self.assertTrue(solnTest[1])
        self.assertEqual(solnTest[0], 4)

    def test_maze3(self):
        maze = ["XXXXX", "X..GX", "X.MMX", "X*..X", "XXXXX"]
        problem = MazeProblem(maze)
        soln = Pathfinder.solve(problem)
        solnTest = problem.solnTest(soln)
        print(soln)
        self.assertTrue(solnTest[1])
        self.assertEqual(solnTest[0], 4)

    def test_maze4(self):
        maze = ["XXXXXX", "X....X", "X*.XXX", "X..XGX", "XXXXXX"]
        problem = MazeProblem(maze)
        soln = Pathfinder.solve(problem)
        print(soln)
        self.assertFalse(soln)

    def test_maze5(self):
        maze = ["XXXXXX", "X....X", "X*.XXX", "X...GX", "XXXXXX"]
        problem = MazeProblem(maze)
        soln = Pathfinder.solve(problem)
        solnTest = problem.solnTest(soln)
        print(soln)
        self.assertTrue(solnTest[1])
        self.assertEqual(solnTest[0], 4)

    def test_maze6(self):
        maze = ["XXXXX", "X.MGX", "X.MMX", "X*..X", "XXXXX"]
        problem = MazeProblem(maze)
        soln = Pathfinder.solve(problem)
        solnTest = problem.solnTest(soln)
        print(soln)
        self.assertTrue(solnTest[1])
        self.assertEqual(solnTest[0], 6)

    def test_maze7(self):
        maze = ["XXXXX", "X.MGX", "X.MMX", "X*MMX", "XXXXX"]
        problem = MazeProblem(maze)
        soln = Pathfinder.solve(problem)
        solnTest = problem.solnTest(soln)
        print(soln)
        self.assertTrue(solnTest[1])
        self.assertEqual(solnTest[0], 6)

    def test_maze8(self):
        maze = ["XXXXXX", "X*...X", "X...XX", "XXXXGX", "XXXXXX"]
        problem = MazeProblem(maze)
        soln = Pathfinder.solve(problem)
        print(soln)
        self.assertFalse(soln)

if __name__ == '__main__':
    unittest.main()
