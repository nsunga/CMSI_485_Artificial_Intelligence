'''
MazeClause.py

Specifies a Propositional Logic Clause formatted specifically
for Grid Maze Pathfinding problems. Clauses are a disjunction of
GridPropositions (2-tuples of (symbol, location)) mapped to
their negated status in the sentence.
'''
import unittest

class MazeClause:

    def __init__ (self, props):
        self.props = {}
        self.valid = False

        for key, value in props:
            if key in self.props:
                if self.props[key] != value:
                    self.valid = True
                    self.props = {}
                    break
            else:
                self.props[key] = value

        # print("props: ", self.props)
        # if len(self.props) == 1:
        #     for key, value in props:
        #         if self.props[key] == True:
        #             self.valid = True

    def getProp (self, prop):
        return self.props[prop] if prop in self.props else None

    def isValid (self):
        return self.valid

    def isEmpty (self):
        return True if len(self.props) == 0 and self.valid == False else False

    def __eq__ (self, other):
        return self.props == other.props and self.valid == other.valid

    def __hash__ (self):
        # Hashes an immutable set of the stored props for ease of
        # lookup in a set
        return hash(frozenset(self.props.items()))

    def __str__ (self):
        return str(self.props)

    # Hint: Specify a __str__ method for ease of debugging (this
    # will allow you to "print" a MazeClause directly to inspect
    # its composite literals)
    # def __str__ (self):
    #     return ""

    @staticmethod
    def resolve (c1, c2):
        results = set()
        removed_once = False

        if c1.isValid() or c2.isValid():
            return results(MazeClause([]))

        for key in c1.props:
            results.add((key, c1.getProp(key)))

        for key in c2.props:
            c1_value = c1.getProp(key)
            c2_value = c2.getProp(key)

            if removed_once and c1_value != c2_value:
                results.add((key, c2_value))
                is_valid_mc = MazeClause(results)
                if is_valid_mc.isValid():
                    results.clear()
                    return results

            if c1_value is not None and c1_value == c2_value:
                results.add((key, c2_value))
                is_valid_mc = MazeClause(results)
                if is_valid_mc.isValid():
                    results.clear()
                    return results
            elif c1_value is None:
                results.add((key, c2_value))
                is_valid_mc = MazeClause(results)
                if is_valid_mc.isValid():
                    results.clear()
                    return results
            elif not removed_once:
                removed_once = True
                results.remove((key, c1_value))

        if MazeClause(results) == c1 or MazeClause(results) == c2:
            results.clear()
            return results

        inferred_result = set()
        inferred_result.add(MazeClause(results))
        # print("results: ", results)
        # print("inferred_result: ", inferred_result)
        return inferred_result


class MazeClauseTests(unittest.TestCase):
    # def test_mazeprops1(self):
    #     mc = MazeClause([(("X", (1, 1)), True), (("X", (2, 1)), True), (("Y", (1, 2)), False)])
    #     self.assertTrue(mc.getProp(("X", (1, 1))))
    #     self.assertTrue(mc.getProp(("X", (2, 1))))
    #     self.assertFalse(mc.getProp(("Y", (1, 2))))
    #     self.assertTrue(mc.getProp(("X", (2, 2))) is None)
    #     self.assertFalse(mc.isEmpty())
    #
    # def test_mazeprops2(self):
    #     mc = MazeClause([(("X", (1, 1)), True), (("X", (1, 1)), True)])
    #     self.assertTrue(mc.getProp(("X", (1, 1))))
    #     self.assertFalse(mc.isEmpty())
    #
    # def test_mazeprops3(self):
    #     mc = MazeClause([(("X", (1, 1)), True), (("Y", (2, 1)), True), (("X", (1, 1)), False)])
    #     self.assertTrue(mc.isValid())
    #     self.assertTrue(mc.getProp(("X", (1, 1))) is None)
    #     self.assertFalse(mc.isEmpty())
    #
    # def test_mazeprops4(self):
    #     mc = MazeClause([])
    #     self.assertFalse(mc.isValid())
    #     self.assertTrue(mc.isEmpty())
    #
    # def test_mazeprops5(self):
    #     mc1 = MazeClause([(("X", (1, 1)), True)])
    #     mc2 = MazeClause([(("X", (1, 1)), True)])
    #     res = MazeClause.resolve(mc1, mc2)
    #     self.assertEqual(len(res), 0)
    #
    # def test_mazeprops6(self):
    #     mc1 = MazeClause([(("X", (1, 1)), True)])
    #     mc2 = MazeClause([(("X", (1, 1)), False)])
    #     mc1.getProp(("X", (1, 1)))
    #     res = MazeClause.resolve(mc1, mc2)
    #     self.assertEqual(len(res), 1)
    #     self.assertTrue(MazeClause([]) in res)
    #
    # def test_mazeprops7(self):
    #     mc1 = MazeClause([(("X", (1, 1)), True), (("Y", (1, 1)), True)])
    #     mc2 = MazeClause([(("X", (1, 1)), False), (("Y", (2, 2)), True)])
    #     res = MazeClause.resolve(mc1, mc2)
    #     self.assertEqual(len(res), 1)
    #     self.assertTrue(MazeClause([(("Y", (1, 1)), True), (("Y", (2, 2)), True)]) in res)
    #
    # def test_mazeprops8(self):
    #     mc1 = MazeClause([(("X", (1, 1)), True), (("Y", (1, 1)), False)])
    #     mc2 = MazeClause([(("X", (1, 1)), False), (("Y", (1, 1)), True)])
    #     res = MazeClause.resolve(mc1, mc2)
    #     self.assertEqual(len(res), 0)
    #
    # def test_mazeprops9(self):
    #     mc1 = MazeClause([(("X", (1, 1)), True), (("Y", (1, 1)), False), (("Z", (1, 1)), True)])
    #     mc2 = MazeClause([(("X", (1, 1)), False), (("Y", (1, 1)), True), (("W", (1, 1)), False)])
    #     res = MazeClause.resolve(mc1, mc2)
    #     self.assertEqual(len(res), 0)

    def test_mazeprops10(self):
        mc1 = MazeClause([(("X", (1, 1)), True), (("Y", (1, 1)), False), (("Z", (1, 1)), True)])
        mc2 = MazeClause([(("X", (1, 1)), False), (("Y", (1, 1)), False), (("W", (1, 1)), False)])
        res = MazeClause.resolve(mc1, mc2)
        print("res: ", res)
        self.assertEqual(len(res), 1)
        self.assertTrue(MazeClause([(("Y", (1, 1)), False), (("Z", (1, 1)), True), (("W", (1, 1)), False)]) in res)
    # ~X ^ X Resolve -> self.props empty, self.valid is false
if __name__ == "__main__":
    unittest.main()
