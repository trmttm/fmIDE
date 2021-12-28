import unittest


class MyTestCase(unittest.TestCase):
    def test_topological_order(self):
        from src.Utilities.Graphs.graph_theory_dfs import Graph
        graph = Graph()
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        graph.add_edge(2, 4)
        topological_order = graph.get_topological_order()
        self.assertEqual(topological_order, (1, 2, 4, 3))


if __name__ == '__main__':
    unittest.main()
