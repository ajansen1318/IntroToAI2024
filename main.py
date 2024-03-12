import time
from SearchMethods import SearchMethods
from UserInputs import UserInputs
from Plot import Plot
from CityGraph import CityGraph


# compare search methods for time, memory, distance, and route


def main():
    """
    Read coordinates and adjacencies of cities from csv files
    Get start and goal cities from user, as well as the search method
    Find the path while meausring time, memory, and distance
    Plot the path
    """
    citygraph = CityGraph("coordinates.csv", "adjacencies.txt")

    start, goal = UserInputs.get_start_and_goal_cities(citygraph.cities)
    search_method = UserInputs.choose_search_method()

    start_time = time.time()

    path_1, total_distance = UserInputs.handle_search_methods(
        citygraph, search_method, start, goal
    )

    total_time_1 = citygraph.measure_time(start_time)  # measure time

    if path_1:
        print(f"Route found: {path_1}")
        Plot.plot_path(citygraph.cities, path_1, search_method)
    else:
        print("Route not found")

    memory_1 = citygraph.memory_used([citygraph.cities, citygraph.adjacencies, path_1])
    distance_1 = citygraph.calculate_path_distance(citygraph.cities, path_1)

    Plot.animate_plot(citygraph.cities, path_1, citygraph.adjacencies, search_method)

    compare = UserInputs.compare_search_methods()
    if compare:
        search_method_2 = UserInputs.choose_search_method()
        start_time_2 = time.time()
        path_2, _ = UserInputs.handle_search_methods(
            citygraph, search_method_2, start, goal
        )
        total_time_2 = citygraph.measure_time(start_time_2)
        memory_2 = citygraph.memory_used(
            [citygraph.cities, citygraph.adjacencies, path_2]
        )
        total_distance_2 = citygraph.calculate_path_distance(citygraph.cities, path_2)
        Plot.animate_plot(
            citygraph.cities, path_2, citygraph.adjacencies, search_method_2
        )

        if path_2:
            print(f"Route found: {path_2}")
            Plot.plot_path(citygraph.cities, path_2, search_method_2)
        else:
            print("Route not found")

        Plot.plot_comparison(
            citygraph.cities, path_1, path_2, search_method, search_method_2
        )


if __name__ == "__main__":
    main()
