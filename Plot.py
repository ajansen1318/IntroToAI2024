"""

This file contains the functions to plot the cities and the path taken

"""

import matplotlib.pyplot as plt
from CityGraph import CityGraph


class Plot:
    def __init__(self):
        pass

    def plot_cities(cities):
        for city, coordinates in cities.items():
            plt.plot(*coordinates, "o")
            plt.text(*coordinates, city)
        plt.show()

    def plot_path(cities, path, search_method):
        for i in range(len(path) - 1):
            city1 = path[i]
            city2 = path[i + 1]
            x1, y1 = cities[city1]
            x2, y2 = cities[city2]
            plt.plot([x1, x2], [y1, y2], "ko-")
            plt.text(x1, y1, city1)
            plt.text(x2, y2, city2)
            plt.title(search_method)
        plt.show()

    # plot all the cities with adjacenies being connected with lines. highlight and animate the adjacencies being looked at in the search, then highlight the path found
    def animate_plot(cities, path, adjacencies, search_method):
        for city, coordinates in cities.items():
            plt.plot(*coordinates, "ko")
            plt.text(
                *coordinates,
                city,
                bbox=dict(facecolor="white", edgecolor="black", boxstyle="round"),
            )
        for city, neighbors in adjacencies.items():
            for neighbor in neighbors:
                x1, y1 = cities[city]
                x2, y2 = cities[neighbor]
                plt.plot([x1, x2], [y1, y2], "ko-")
        # animated plot path including the goal city
        for i in range(len(path) - 1):
            city1 = path[i]
            city2 = path[i + 1]
            x1, y1 = cities[city1]
            x2, y2 = cities[city2]
            plt.plot([x1, x2], [y1, y2], "ro-")
            plt.text(
                x1,
                y1,
                city1,
                bbox=dict(facecolor="white", edgecolor="black", boxstyle="round"),
            )
            plt.text(
                x2,
                y2,
                city2,
                bbox=dict(facecolor="white", edgecolor="black", boxstyle="round"),
            )
            plt.title(search_method)
        plt.pause(1)
        plt.show()

    def plot_comparison(cities, path_1, path_2, search_method_1, search_method_2):
        path_1_x = [cities[city][0] for city in path_1]
        path_1_y = [cities[city][1] for city in path_1]
        path_2_x = [cities[city][0] for city in path_2]
        path_2_y = [cities[city][1] for city in path_2]
        for city in path_1:
            x1, y1 = cities[city]
            plt.text(
                x1,
                y1,
                city,
                bbox=dict(facecolor="white", edgecolor="black", boxstyle="round"),
                va="center",
                ha="center",
            )
        for city in path_2:
            x2, y2 = cities[city]
            plt.text(
                x2,
                y2,
                city,
                bbox=dict(facecolor="white", edgecolor="black", boxstyle="round"),
                va="center",
                ha="center",
            )

        plt.plot(path_1_x, path_1_y, "ro-", label="Path 1")
        plt.plot(path_2_x, path_2_y, "bo-", label="Path 2")
        plt.title(f"{search_method_1} vs {search_method_2}")
        plt.legend()
        plt.show()
