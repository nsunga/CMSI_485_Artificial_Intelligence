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
        root = SearchTreeNode(problem.initial, None, None, 0, 0)
        temp_node = root
        #print("INSIDE: SOLVE")
        while not problem.goalTest(temp_node.state):
        #    print("iterate")
            children_list = problem.transitions(temp_node.state)
            for children in children_list:
                heapq.heappush(priority_queue, SearchTreeNode(children[2], children[0], temp_node, children[1], problem.heuristic(children[2])))
            temp_node = heapq.heappop(priority_queue)

        path = []
        #print("inside path")
        while temp_node != root:
            path.append(temp_node.action)
            temp_node = temp_node.parent
        #print("IS GOAL: ", problem.goalTest(temp_node))
        path.reverse()
        #print("PATH: ", path)
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


if __name__ == '__main__':
    unittest.main()
