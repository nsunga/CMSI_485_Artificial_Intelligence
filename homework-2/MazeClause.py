'''
AUTHOR: NICK SUNGA
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

    @staticmethod
    def resolve (c1, c2):
        results = set()
        removed_once = False
        complimentary_keys = set()

        if c1.isValid() or c2.isValid():
            return results(MazeClause([]))

        for key in c2.props:
            c1_value = c1.getProp(key)
            c2_value = c2.getProp(key)

            if c1_value is not None and c1_value != c2_value:
                complimentary_keys.add(key)

        for key in c1.props:
            c1_value = c1.getProp(key)
            c2_value = c2.getProp(key)

            if c2_value is not None and c2_value != c1_value:
                complimentary_keys.add(key)

        for key in c1.props:
            if key not in complimentary_keys:
                results.add((key, c1.getProp(key)))

        for key in c2.props:
            if key not in complimentary_keys:
                results.add((key, c2.getProp(key)))

        results_mc = MazeClause(results)

        # adding something true makes no difference
        if results_mc.isValid():
            results.clear()
            return results

        # adding the same clause makes no difference
        if results_mc == c1 or results_mc == c2:
            results.clear()
            return results

        # two clauses, length one, that are compliments: give empty set
        if len(results) == 0 and len(complimentary_keys) == 1:
            results.add(MazeClause([]))
            return results

        # can only eliminate one literal at a time -> union becomes true
        if len(complimentary_keys) > 1:
            results.clear()
            return results

        resolved_clause = set()
        resolved_clause.add(results_mc)
        return resolved_clause

class MazeClauseTests(unittest.TestCase):
    def test_mazeprops1(self):
        mc = MazeClause([(("X", (1, 1)), True), (("X", (2, 1)), True), (("Y", (1, 2)), False)])
        self.assertTrue(mc.getProp(("X", (1, 1))))
        self.assertTrue(mc.getProp(("X", (2, 1))))
        self.assertFalse(mc.getProp(("Y", (1, 2))))
        self.assertTrue(mc.getProp(("X", (2, 2))) is None)
        self.assertFalse(mc.isEmpty())

    def test_mazeprops2(self):
        mc = MazeClause([(("X", (1, 1)), True), (("X", (1, 1)), True)])
        self.assertTrue(mc.getProp(("X", (1, 1))))
        self.assertFalse(mc.isEmpty())

    def test_mazeprops3(self):
        mc = MazeClause([(("X", (1, 1)), True), (("Y", (2, 1)), True), (("X", (1, 1)), False)])
        self.assertTrue(mc.isValid())
        self.assertTrue(mc.getProp(("X", (1, 1))) is None)
        self.assertFalse(mc.isEmpty())

    def test_mazeprops4(self):
        mc = MazeClause([])
        self.assertFalse(mc.isValid())
        self.assertTrue(mc.isEmpty())

    def test_mazeprops5(self):
        mc1 = MazeClause([(("X", (1, 1)), True)])
        mc2 = MazeClause([(("X", (1, 1)), True)])
        res = MazeClause.resolve(mc1, mc2)
        self.assertEqual(len(res), 0)

    def test_mazeprops6(self):
        mc1 = MazeClause([(("X", (1, 1)), True)])
        mc2 = MazeClause([(("X", (1, 1)), False)])
        mc1.getProp(("X", (1, 1)))
        res = MazeClause.resolve(mc1, mc2)
        self.assertEqual(len(res), 1)
        self.assertTrue(MazeClause([]) in res)

    def test_mazeprops7(self):
        mc1 = MazeClause([(("X", (1, 1)), True), (("Y", (1, 1)), True)])
        mc2 = MazeClause([(("X", (1, 1)), False), (("Y", (2, 2)), True)])
        res = MazeClause.resolve(mc1, mc2)
        self.assertEqual(len(res), 1)
        self.assertTrue(MazeClause([(("Y", (1, 1)), True), (("Y", (2, 2)), True)]) in res)

    def test_mazeprops8(self):
        mc1 = MazeClause([(("X", (1, 1)), True), (("Y", (1, 1)), False)])
        mc2 = MazeClause([(("X", (1, 1)), False), (("Y", (1, 1)), True)])
        res = MazeClause.resolve(mc1, mc2)
        self.assertEqual(len(res), 0)

    def test_mazeprops9(self):
        mc1 = MazeClause([(("X", (1, 1)), True), (("Y", (1, 1)), False), (("Z", (1, 1)), True)])
        mc2 = MazeClause([(("X", (1, 1)), False), (("Y", (1, 1)), True), (("W", (1, 1)), False)])
        res = MazeClause.resolve(mc1, mc2)
        self.assertEqual(len(res), 0)

    def test_mazeprops10(self):
        mc1 = MazeClause([(("X", (1, 1)), True), (("Y", (1, 1)), False), (("Z", (1, 1)), True)])
        mc2 = MazeClause([(("X", (1, 1)), False), (("Y", (1, 1)), False), (("W", (1, 1)), False)])
        res = MazeClause.resolve(mc1, mc2)
        self.assertEqual(len(res), 1)
        self.assertTrue(MazeClause([(("Y", (1, 1)), False), (("Z", (1, 1)), True), (("W", (1, 1)), False)]) in res)
    # ~X ^ X Resolve -> self.props empty, self.valid is false
if __name__ == "__main__":
    unittest.main()
