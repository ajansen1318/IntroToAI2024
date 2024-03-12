"""

This file contains the search methods used in the project:
    - Breadth-First Search
    - Depth-First Search
    - Iterative Deepening Depth-First Search
    - Best-First Search
    - A* Search

"""

from CityGraph import CityGraph
from queue import PriorityQueue

city_graph = CityGraph(
    "coordinates.csv", "adjacencies.txt"
)  # need to change this somehow


class SearchMethods:
    def __init__(self):
        pass

    def BFS(
        graph, start, goal
    ):  # Breadth-First Search that makes a dictionary with goal
        queue = [(start, [])]
        visited_nodes = []

        while queue:
            current_node, visited_nodes = queue.pop()

            if current_node == goal:
                visited_nodes.append(current_node)
                return visited_nodes

            if current_node not in visited_nodes:
                visited_nodes.append(current_node)
                neighbors = graph.get(current_node, [])
                for neighbor in neighbors:
                    queue.append((neighbor, visited_nodes.copy()))

        return visited_nodes

    def DFS(graph, start, goal):  # Depth-First Search
        stack = [(start, [])]

        while stack:
            current_node, visited_nodes = stack.pop()

            if current_node == goal:
                visited_nodes.append(current_node)
                return visited_nodes

            if current_node not in visited_nodes:
                visited_nodes.append(current_node)
                neighbors = graph.get(current_node, [])

                for neighbor in graph[current_node]:
                    stack.append((neighbor, visited_nodes.copy()))

        return visited_nodes

    def IDDFS(graph, start, goal, max_depth):  # Iterative Deepening Depth-First Search
        for depth_limit in range(max_depth + 1):
            result = SearchMethods.depth_limited_DFS(graph, start, goal, depth_limit)
            if result is not None:
                return result
        return None

    def depth_limited_DFS(graph, start, goal, depth_limit):
        stack = [(start, [start])]
        visited_nodes = set()

        while stack:
            current_node, path = stack.pop()

            if current_node == goal:
                visited_nodes.add(current_node)
                return path

            if current_node not in visited_nodes and len(path) < depth_limit:
                visited_nodes.add(current_node)

                for neighbor in graph[current_node]:
                    stack.append((neighbor, path + [neighbor]))

        return None

    def best_first_search(graph, start, goal):
        open_set = PriorityQueue()
        open_set.put((0, start))

        parents = {start: None}  # parent nodes
        visited_nodes = set()

        while not open_set.empty():
            _, current_node = open_set.get()

            if current_node == goal:
                path = []

                while current_node:
                    path.append(current_node)
                    current_node = parents[current_node]
                return path[::-1]

            if current_node not in visited_nodes:
                visited_nodes.add(current_node)
                neighbors = graph.get(current_node, [])

                for neighbor in neighbors:
                    if neighbor not in visited_nodes:
                        heuristic_value = city_graph.euclidean_distance(
                            city_graph.cities, neighbor, goal
                        )
                        open_set.put((heuristic_value, neighbor))
                        parents[neighbor] = current_node

        return visited_nodes

    def astar(adjacencies, start, goal):
        open_set = PriorityQueue()
        open_set.put((0, start))

        cost = {city: float("inf") for city in adjacencies}
        cost[start] = 0

        parents = {start: None}  # parent nodes
        visited_nodes = set()  # visited nodes

        while not open_set.empty():
            current_cost, current_node = open_set.get()

            if current_node == goal:
                path = []

                while current_node:
                    path.append(current_node)
                    current_node = parents[current_node]
                return path[::-1]
            if current_node not in visited_nodes:
                visited_nodes.add(current_node)

                for neighbor in adjacencies[current_node]:
                    new_cost = cost[current_node] + city_graph.euclidean_distance(
                        city_graph.cities, current_node, neighbor
                    )
                    if new_cost < cost[neighbor]:
                        cost[neighbor] = new_cost
                        heuristic = city_graph.euclidean_distance(
                            city_graph.cities, current_node, goal
                        )
                        total_cost = new_cost + heuristic
                        open_set.put((total_cost, neighbor))
                        parents[neighbor] = current_node

        return None, visited_nodes
