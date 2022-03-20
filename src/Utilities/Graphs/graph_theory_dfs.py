from typing import Any
from typing import Dict

from Utilities.Graphs.johnson_algorithm import simple_cycles


class Graph:
    def __init__(self):
        self._graph: Dict[Any, list] = {}

    def add_edge(self, vertex_from, vertex_to):
        if vertex_from in self._graph:
            self._graph[vertex_from].append(vertex_to)
        else:
            self._graph[vertex_from] = [vertex_to]

        if vertex_to not in self._graph:
            self._graph[vertex_to] = []

    def get_strongly_connected_components(self) -> tuple:
        visited = self._create_default_visited_set()
        stack_by_finished_time = []

        for vertex in self._graph.keys():
            if visited[vertex] is False:
                self._stack_by_finished_time(vertex, visited, stack_by_finished_time)

        reversed_graph = self._get_reversed_graph()
        visited = self._create_default_visited_set()
        strongly_connected_components = ()
        while stack_by_finished_time:
            current_vertex = stack_by_finished_time.pop()
            if visited[current_vertex] is False:
                scc = [current_vertex]
                reversed_graph._recursively_add_scc_element(current_vertex, visited, scc)
                strongly_connected_components += (tuple(scc),)

        return strongly_connected_components

    def _create_default_visited_set(self) -> dict:
        visited = {}
        for vertex in self._graph.keys():
            visited[vertex] = False
        return visited

    def _stack_by_finished_time(self, current_vertex, visited: dict, stack: list):
        visited[current_vertex] = True
        for vertex in self._graph[current_vertex]:
            if visited[vertex] is False:
                self._stack_by_finished_time(vertex, visited, stack)
        stack.append(current_vertex)

    def _get_reversed_graph(self) -> 'Graph':
        reversed_graph = Graph()

        for vertex_from in self._graph.keys():
            for vertex_to in self._graph[vertex_from]:
                reversed_graph.add_edge(vertex_to, vertex_from)  # reversed
        return reversed_graph

    def _recursively_add_scc_element(self, current_vertex, visited: dict, scc: list):
        visited[current_vertex] = True
        for vertex in self._graph[current_vertex]:
            if visited[vertex] is False:
                scc.append(vertex)
                self._recursively_add_scc_element(vertex, visited, scc)

    def get_simple_cycles(self):
        return simple_cycles(self._graph)

    def get_cycle_breakers(self) -> set:
        intersection = set()
        for cycle in self.get_simple_cycles():
            if len(intersection) == 0:
                intersection = set(cycle)
            else:
                intersection = intersection.intersection(set(cycle))
        return intersection

    def is_circular(self, vertex) -> bool:
        if vertex not in self._graph:
            return False

        visited = self._create_default_visited_set()
        stack = self._create_default_visited_set()
        visited[vertex] = True
        stack[vertex] = True

        for child in self._graph[vertex]:
            if visited[child] is False:
                return self._is_circular(child, visited, stack)
        return False

    def _is_circular(self, current_vertex, visited: dict, stack: dict):
        visited[current_vertex] = True
        stack[current_vertex] = True

        for neighbour in self._graph[current_vertex]:
            if visited[neighbour] is False:
                if self._is_circular(neighbour, visited, stack) is True:
                    return True
            elif stack[neighbour] is True:
                return True

        stack[current_vertex] = False
        return False

    def get_topological_order(self) -> tuple:
        visited = self._create_default_visited_set()
        stack = []
        for element in self._graph.keys():
            if not visited[element]:
                self._get_topological_order(element, visited, stack)
        return tuple(stack)

    def _get_topological_order(self, n, visited: dict, stack: list):
        visited[n] = True
        for element in self._graph[n]:
            if not visited[element]:
                self._get_topological_order(element, visited, stack)
        stack.insert(0, n)


if __name__ == '__main__':
    graph = Graph()
    graph.add_edge('cash_bb', '+1')
    graph.add_edge('cash_eb', '+1')
    graph.add_edge('+1', '/')
    graph.add_edge('2', '/')
    graph.add_edge('/', 'base')
    graph.add_edge('base', 'x')
    graph.add_edge('interest_rate', 'x')
    graph.add_edge('x', 'interest_income')
    graph.add_edge('cash_bb', '+2')
    graph.add_edge('interest_income', '+2')
    graph.add_edge('+2', 'cash_eb')

    print(tuple(graph.get_simple_cycles()))
    # print(tuple(graph.get_topological_order()))
    # print(tuple(graph.get_strongly_connected_components()))
