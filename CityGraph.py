"""

This sets up the graph of the cities and the path taken

"""

import csv
import time
import sys
import math


class CityGraph:
    def __init__(self, coordinates_file, adjacencies_file):
        self.cities = self.read_coordinates(coordinates_file)
        self.adjacencies = self.read_adjacencies(adjacencies_file)

    def read_coordinates(self, filename):
        with open(filename, "r") as file:
            data = csv.reader(file)
            cities = {}  # create a dictionary to store the cities and their coordinates
            for column in data:
                try:
                    cities[column[0]] = (
                        float(column[2]),  # longitude
                        float(column[1]),  # latitude
                    )
                except (ValueError, IndexError):
                    print(f"Skipping invalid data: {column}")
        return cities

    def read_adjacencies(self, filename):
        with open(filename, "r") as file:
            adjacencies = {}
            for line in file:
                data = line.split()
                city = data[0]
                neighbor = data[1]

                if city not in adjacencies:
                    adjacencies[city] = [neighbor]
                else:
                    adjacencies[city].append(neighbor)

                if neighbor not in adjacencies:
                    adjacencies[neighbor] = [city]
                else:
                    adjacencies[neighbor].append(city)

        return adjacencies

    def measure_time(self, start_time):
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Total time: {total_time} seconds")
        return total_time

    def memory_used(self, arrays):
        total_memory = sum(sys.getsizeof(array) for array in arrays)
        print(f"Total memory used: {total_memory} bytes")
        return total_memory

    def euclidean_distance(self, cities, city1, city2):
        # take the coordinates of the two cities and calculate the distance in miles
        x1, y1 = cities[city1]
        x2, y2 = cities[city2]
        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        return distance

    def haversine_distance(self, lat1, lon1, lat2, lon2):
        """
        Calculate the Haversine distance between two points specified by latitude and longitude.
        The result is in miles.
        """
        # Radius of the Earth in miles
        R = 3958.8

        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        # Calculate differences in coordinates
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        # Haversine formula
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        # Calculate distance
        distance = R * c
        return distance

    def calculate_path_distance(self, cities, path):
        total_distance = 0
        for city1, city2 in zip(path, path[1:]):
            lat1, lon1 = cities[city1]
            lat2, lon2 = cities[city2]
            distance = self.haversine_distance(lat1, lon1, lat2, lon2)
            total_distance += distance
        print(f"Total distance: {total_distance} miles")
        return total_distance
