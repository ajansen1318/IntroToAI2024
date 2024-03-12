"""

File for all user inputs


"""

from CityGraph import CityGraph
from SearchMethods import SearchMethods


class UserInputs:

    def __init__(self):
        pass

    def get_city_input(prompt, cities):
        city = input(prompt)
        while city not in cities:
            print("City not in database")
            city = input(prompt)
        return city

    def get_start_and_goal_cities(cities):
        start = UserInputs.get_city_input("Enter the starting city: ", cities)
        goal = UserInputs.get_city_input("Enter the goal city: ", cities)
        return start, goal

    def choose_search_method():
        search_method = input(
            "Choose a search method from the list: BFS, DFS, IDDFS, Best-First, or A*:  "
        )
        return search_method

    def get_max_depth():
        max_depth = int(input("Enter the max depth for the IDDFS search: "))
        return max_depth

    def compare_search_methods():
        compare = input("Would you like to compare search methods? (y/n): ")
        return compare.lower() == "y"

    def handle_search_methods(citygraph, search_method, start, goal):
        total_distance = 0
        if search_method == "BFS":
            path = SearchMethods.BFS(citygraph.adjacencies, start, goal)
        elif search_method == "DFS":
            path = SearchMethods.DFS(citygraph.adjacencies, start, goal)
        elif search_method == "IDDFS":
            # ask the user what they want the max depth to be
            max_depth = UserInputs.get_max_depth()
            path = SearchMethods.IDDFS(citygraph.adjacencies, start, goal, max_depth)
            if path is not None:
                total_distance = citygraph.calculate_path_distance(
                    citygraph.cities, path
                )
            else:
                print("No path found.")
                return  # Return or exit the function if no path is found
        elif search_method == "Best-First":
            path = SearchMethods.best_first_search(citygraph.adjacencies, start, goal)
        elif search_method == "A*":
            path = SearchMethods.astar(citygraph.adjacencies, start, goal)
        else:
            raise ValueError("Invalid search method")

        return path, total_distance
