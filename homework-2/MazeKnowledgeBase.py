'''
MazeKnowledgeBase.py

Specifies a simple, Conjunctive Normal Form Propositional
Logic Knowledge Base for use in Grid Maze pathfinding problems
with side-information.
'''
from MazeClause import MazeClause
import unittest
import itertools

class MazeKnowledgeBase:

    def __init__ (self):
        self.clauses = set()

    # [!] Assumes that a clause is never added that causes the
    # KB to become inconsistent
    def tell (self, clause):
        self.clauses.add(clause)
        # for every_clause in self.clauses:
        #     print("some clause: ", every_clause, '\n')

    # [!] Queries are always MazeClauses
    def ask (self, query):
        # TODO: Implement resolution inference here!
        # This is currently implemented incorrectly; see
        # spec for details!
        negated_sentence = set()

        for every_prop in query.props:
            negated_sentence.add((every_prop, not query.getProp(every_prop)))

        not_alpha = MazeClause(negated_sentence)
        kb_with_not_alpha = MazeKnowledgeBase()

        for every_clause in self.clauses:
            kb_with_not_alpha.tell(every_clause)

        kb_with_not_alpha.tell(not_alpha)

        every_combination = list(itertools.combinations(kb_with_not_alpha.clauses, 2))
        new = set()
        is_subset = False
        while True:
            is_subset = False
            for every_tuple in every_combination:
                # print("resolve[0]: ", every_tuple[0])
                # print("resolve[1]: ", every_tuple[1])
                resolvents = MazeClause.resolve(every_tuple[0], every_tuple[1])
                if MazeClause([]) in resolvents:
                    return True

                for every_thing in resolvents:
                    new.add(every_thing)

            # for mc_in_new in new:
            #     print("considering this mc: ", mc_in_new)
            #     if mc_in_new in kb_with_not_alpha.clauses:
            #         is_subset = True
            #         print("was subset")
            #     else:
            #         print("checking...")
            #         is_subset = False
            #         # break

            if set(new) < set(kb_with_not_alpha.clauses):
                is_subset = True
                print("was subset")

            if is_subset:
                return False

            for mc_in_new in new:
                # print("adding: ", mc_in_new)
                kb_with_not_alpha.tell(mc_in_new)
            new.clear()
            every_combination = list(itertools.combinations(kb_with_not_alpha.clauses, 2))

class MazeKnowledgeBaseTests(unittest.TestCase):
    # def test_mazekb1(self):
    #     kb = MazeKnowledgeBase()
    #     kb.tell(MazeClause([(("X", (1, 1)), True)]))
    #     self.assertTrue(kb.ask(MazeClause([(("X", (1, 1)), True)])))
    #
    # def test_mazekb2(self):
    #     kb = MazeKnowledgeBase()
    #     kb.tell(MazeClause([(("X", (1, 1)), False)]))
    #     kb.tell(MazeClause([(("X", (1, 1)), True), (("Y", (1, 1)), True)]))
    #     # for every_maze_clause in kb.clauses:
    #     #     print("KB: ", every_maze_clause)
    #     self.assertTrue(kb.ask(MazeClause([(("Y", (1, 1)), True)])))
    #
    # def test_mazekb3(self):
    #     kb = MazeKnowledgeBase()
    #     kb.tell(MazeClause([(("X", (1, 1)), False), (("Y", (1, 1)), True)]))
    #     kb.tell(MazeClause([(("Y", (1, 1)), False), (("Z", (1, 1)), True)]))
    #     kb.tell(MazeClause([(("W", (1, 1)), True), (("Z", (1, 1)), False)]))
    #     kb.tell(MazeClause([(("X", (1, 1)), True)]))
    #     self.assertTrue(kb.ask(MazeClause([(("W", (1, 1)), True)])))
    #     self.assertFalse(kb.ask(MazeClause([(("Y", (1, 1)), False)])))
    #
    # def test_mazekb4(self):
    #     kb = MazeKnowledgeBase()
    #     kb.tell(MazeClause([(("X", (1, 1)), False), (("Y", (1, 1)), True), (("W", (1, 1)), True)]))
    #     kb.tell(MazeClause([(("W", (1, 1)), False), (("Z", (1, 1)), False), (("S", (1, 1)), True)]))
    #     kb.tell(MazeClause([(("S", (1, 1)), False), (("T", (1, 1)), False)]))
    #     kb.tell(MazeClause([(("X", (1, 1)), True), (("T", (1, 1)), True)]))
    #     kb.tell(MazeClause([(("W", (1, 1)), True)]))
    #     kb.tell(MazeClause([(("T", (1, 1)), True)]))
    #     self.assertTrue(kb.ask(MazeClause([(("Z", (1, 1)), False)])))
    #
    def test_mazekb5(self):
        kb = MazeKnowledgeBase()
        kb.tell(MazeClause([(("X", (1, 1)), False), (("Y", (1, 1)), True), (("W", (1, 1)), True)]))
        kb.tell(MazeClause([(("W", (1, 1)), False), (("Z", (1, 1)), False), (("S", (1, 1)), True)]))
        kb.tell(MazeClause([(("S", (1, 1)), False), (("T", (1, 1)), False)]))
        kb.tell(MazeClause([(("X", (1, 1)), True), (("T", (1, 1)), True)]))
        kb.tell(MazeClause([(("W", (1, 1)), True)]))
        kb.tell(MazeClause([(("T", (1, 1)), True)]))
        self.assertTrue(kb.ask(MazeClause([(("Z", (1, 1)), True), (("W", (1, 1)), True)])))

    # def test_mazekb6(self):
    #     kb = MazeKnowledgeBase()
    #     kb.tell(MazeClause([(("X", (1, 1)), False), (("Y", (1, 1)), False), (("Z", (1, 1)), False)]))
    #     kb.tell(MazeClause([(("X", (1, 1)), True)]))
    #     self.assertFalse(kb.ask(MazeClause([(("Z", (1, 1)), False)])))
    #     kb.tell(MazeClause([(("Y", (1, 1)), True)]))
    #     self.assertTrue(kb.ask(MazeClause([(("Z", (1, 1)), False)])))


if __name__ == "__main__":
    unittest.main()
