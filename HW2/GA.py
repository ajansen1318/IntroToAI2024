import random
import numpy as np

# from scipy.special import softmax

# Activities, Rooms, Times, Facilitators
ACTIVITIES = [
    "SLA100A",
    "SLA100B",
    "SLA191A",
    "SLA191B",
    "SLA201",
    "SLA291",
    "SLA303",
    "SLA304",
    "SLA394",
    "SLA449",
    "SLA451",
]

ROOMS = [
    "Slater 003",
    "Roman 216",
    "Loft 206",
    "Roman 201",
    "Loft 310",
    "Beach 201",
    "Beach 301",
    "Logos 325",
    "Frank 119",
]

TIMES = ["10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM"]

FACILITATORS = [
    "Lock",
    "Glen",
    "Banks",
    "Richards",
    "Shaw",
    "Singer",
    "Uther",
    "Tyler",
    "Numen",
    "Zeldin",
]

# Facilitator data
facilitator_data = {
    "SLA100A": {
        "expected_enrollment": 50,
        "preferred": ["Glen", "Lock", "Banks", "Zeldin"],
        "other": ["Numen", "Richards"],
    },
    "SLA100B": {
        "expected_enrollment": 50,
        "preferred": ["Glen", "Lock", "Banks", "Zeldin"],
        "other": ["Numen", "Richards"],
    },
    "SLA191A": {
        "expected_enrollment": 50,
        "preferred": ["Glen", "Lock", "Banks", "Zeldin"],
        "other": ["Numen", "Richards"],
    },
    "SLA191B": {
        "expected_enrollment": 50,
        "preferred": ["Glen", "Lock", "Banks", "Zeldin"],
        "other": ["Numen", "Richards"],
    },
    "SLA201": {
        "expected_enrollment": 50,
        "preferred": ["Glen", "Banks", "Zeldin", "Shaw"],
        "other": ["Numen", "Richards", "Singer"],
    },
    "SLA291": {
        "expected_enrollment": 50,
        "preferred": ["Lock", "Banks", "Zeldin", "Singer"],
        "other": ["Numen", "Richards", "Shaw", "Tyler"],
    },
    "SLA303": {
        "expected_enrollment": 60,
        "preferred": ["Glen", "Zeldin", "Banks"],
        "other": ["Numen", "Singer", "Shaw"],
    },
    "SLA304": {
        "expected_enrollment": 25,
        "preferred": ["Glen", "Banks", "Tyler"],
        "other": ["Numen", "Singer", "Shaw", "Richards", "Uther", "Zeldin"],
    },
    "SLA394": {
        "expected_enrollment": 20,
        "preferred": ["Tyler", "Singer"],
        "other": ["Richards", "Zeldin"],
    },
    "SLA449": {
        "expected_enrollment": 60,
        "preferred": ["Tyler", "Singer", "Shaw"],
        "other": ["Zeldin", "Uther"],
    },
    "SLA451": {
        "expected_enrollment": 100,
        "preferred": ["Tyler", "Singer", "Shaw"],
        "other": ["Zeldin", "Uther", "Richards", "Banks"],
    },
}

ROOM_CAPACITY = {
    "Slater 003": 45,
    "Roman 216": 30,
    "Loft 206": 75,
    "Roman 201": 50,
    "Loft 310": 108,
    "Beach 201": 60,
    "Beach 301": 75,
    "Logos 325": 450,
    "Frank 119": 60,
}

# Genetic Algorithm Parameters
POPULATION_SIZE = 500
MUTATION_RATE = 0.0003125
GENERATIONS = 100


# Initialize population
def initialize_population(population_size):
    population = []
    for _ in range(population_size):
        schedule = {}
        for activity in ACTIVITIES:
            room = random.choice(ROOMS)
            time = random.choice(TIMES)
            facilitator = random.choice(FACILITATORS)
            schedule[activity] = {
                "room": room,
                "time": time,
                "facilitator": facilitator,
            }
        population.append(schedule)
    return population


# Fitness function
def calculate_fitness(schedule):
    fitness = 0

    # Add fitness for each activity
    for activity, details in schedule.items():
        # Check for duplicate activities considering room, time, and facilitator
        duplicate_activities = [
            act
            for act, det in schedule.items()
            if det["room"] == details["room"]
            and det["time"] == details["time"]
            and det["facilitator"] == details["facilitator"]
            and act != activity
        ]
        if duplicate_activities:
            fitness -= 0.5

        # Check room size
        room_capacity = ROOM_CAPACITY[details["room"]]
        if room_capacity < facilitator_data[activity]["expected_enrollment"]:
            fitness -= 0.5
        elif room_capacity > 3 * facilitator_data[activity]["expected_enrollment"]:
            fitness -= 0.2
        elif room_capacity > 6 * facilitator_data[activity]["expected_enrollment"]:
            fitness -= 0.4
        else:
            fitness += 0.3

        # Check facilitator
        if details["facilitator"] in facilitator_data[activity]["preferred"]:
            fitness += 0.5
        elif details["facilitator"] in facilitator_data[activity]["other"]:
            fitness += 0.2
        else:
            fitness -= 0.1

        # Check facilitator load
        facilitator_activities = [
            act
            for act, det in schedule.items()
            if det["facilitator"] == details["facilitator"]
            and det["time"] == details["time"]
            and act != activity
        ]
        if facilitator_activities != 1:
            fitness += 0.2
        elif len(facilitator_activities) > 1:
            fitness -= 0.2

        if len(facilitator_activities) > 4:
            fitness -= 0.5
        elif (
            len(facilitator_activities) == 1 or len(facilitator_activities) == 2
        ) and details[
            "facilitator"
        ] != "Tyler":  # this might be wrong too
            fitness -= 0.4

        # # if facilitator is scheduled for consecutive activities
        # if schedule["time"]["facilitator"] == schedule["time"]["facilitator"]:
        #     fitness -= 0.25
        # if (
        #     abs(
        #         int(schedule["time"]["facilitator"].split()[0])
        #         - int(schedule["time"]["facilitator"].split()[0])
        #     )
        #     == 1
        # ):
        #     fitness += 0.5
        # if (
        #     abs(
        #         int(schedule["time"]["facilitator"].split()[0])
        #         - int(schedule["time"]["facilitator"].split()[0])
        #     )
        #     == 2
        # ):
        #     fitness += 0.25

        # Check if facilitator is scheduled for consecutive activities
        if schedule[activity]["facilitator"] == schedule[activity]["facilitator"]:
            fitness -= 0.25
        if (
            abs(
                int(schedule[activity]["time"].split()[0])
                - int(schedule[activity]["time"].split()[0])
            )
            == 1
        ):
            fitness += 0.5
        if (
            abs(
                int(schedule[activity]["time"].split()[0])
                - int(schedule[activity]["time"].split()[0])
            )
            == 2
        ):
            fitness += 0.25

        # Check for specific SLA 191 and SLA 101 constraints
        if schedule["SLA191A"]["time"] == schedule["SLA191B"]["time"]:
            fitness -= 0.5
        if schedule["SLA100A"]["time"] == schedule["SLA100B"]["time"]:
            fitness -= 0.5
        if (
            abs(
                int(schedule["SLA100A"]["time"].split()[0])
                - int(schedule["SLA100A"]["time"].split()[0])
            )
            or abs(
                int(schedule["SLA191B"]["time"].split()[0])
                - int(schedule["SLA191A"]["time"].split()[0])
            )
        ) >= 4:
            fitness += 0.5
        if (
            (schedule["SLA191A"]["time"] == schedule["SLA100A"]["time"])
            or (schedule["SLA191A"]["time"] == schedule["SLA100B"]["time"])
            or (schedule["SLA191B"]["time"] == schedule["SLA100A"]["time"])
            or (schedule["SLA191B"]["time"] == schedule["SLA100B"]["time"])
        ):
            fitness -= 0.25
        if (
            abs(
                int(schedule["SLA191A"]["time"].split()[0])
                - int(schedule["SLA100A"]["time"].split()[0])
            )
            or (
                abs(
                    int(schedule["SLA191A"]["time"].split()[0])
                    - int(schedule["SLA100B"]["time"].split()[0])
                )
            )
            or (
                abs(
                    int(schedule["SLA191B"]["time"].split()[0])
                    - int(schedule["SLA100A"]["time"].split()[0])
                )
            )
            or (
                abs(
                    int(schedule["SLA191B"]["time"].split()[0])
                    - int(schedule["SLA100B"]["time"].split()[0])
                )
            )
            == 2
        ):
            fitness += 0.25
        if (
            abs(
                int(schedule["SLA191A"]["time"].split()[0])
                - int(schedule["SLA100A"]["time"].split()[0])
            )
            or (
                abs(
                    int(schedule["SLA191A"]["time"].split()[0])
                    - int(schedule["SLA100B"]["time"].split()[0])
                )
            )
            or (
                abs(
                    int(schedule["SLA191B"]["time"].split()[0])
                    - int(schedule["SLA100A"]["time"].split()[0])
                )
            )
            or (
                abs(
                    int(schedule["SLA191B"]["time"].split()[0])
                    - int(schedule["SLA100B"]["time"].split()[0])
                )
            )
            == 1
        ):
            fitness += 0.5

            if (
                "Roman" in schedule["SLA191A"]["room"]  # this might be wrong too
                or "Beach" in schedule["SLA191A"]["room"]
            ):
                if (
                    "Roman" in schedule["SLA100A"]["room"]
                    and "Beach" in schedule["SLA100A"]["room"]
                ):
                    fitness -= 0.4
            elif (
                "Roman" in schedule["SLA191A"]["room"]
                or "Beach" in schedule["SLA191A"]["room"]
            ):
                if (
                    "Roman" not in schedule["SLA100B"]["room"]
                    and "Beach" not in schedule["SLA100B"]["room"]
                ):
                    fitness += 0.5
                else:
                    fitness -= 0.4
            else:
                fitness -= 0.4

        if fitness is None:
            print("Invalid schedule:", schedule)
            return 0
        else:
            return fitness


# Mutation
def mutate(schedule):
    if random.random() < MUTATION_RATE:
        activity = random.choice(ACTIVITIES)
        schedule[activity]["room"] = random.choice(ROOMS)
        schedule[activity]["time"] = random.choice(TIMES)
        schedule[activity]["facilitator"] = random.choice(FACILITATORS)
    return schedule


def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()


# Main genetic algorithm function
def genetic_algorithm(crossover_method):
    population = initialize_population(POPULATION_SIZE)
    for generation in range(GENERATIONS):
        # Calculate fitness for each schedule
        scores = [calculate_fitness(schedule) for schedule in population]

        # Softmax normalization
        scores_array = np.array(scores, dtype=float)
        if np.any(np.isnan(scores_array)):
            scores_array[np.isnan(scores_array)] = 0

        probabilities = softmax(scores_array)

        # Selection and crossover
        new_population = []
        for _ in range(POPULATION_SIZE):
            parents = np.random.choice(population, 2, p=probabilities, replace=False)

            if crossover_method == "uniform":
                child = uniform_crossover(parents[0], parents[1])
            elif crossover_method == "multi-point":
                child = multi_point_crossover(parents[0], parents[1])

            child = mutate(child)
            new_population.append(child)

        population = new_population

    best_schedule = max(population, key=calculate_fitness)
    best_fitness = calculate_fitness(best_schedule)
    return best_schedule, best_fitness


# Crossover (Single point crossover)
def crossover(parent1, parent2):
    child = {}
    crossover_point = random.randint(1, len(ACTIVITIES) - 1)
    activities = list(parent1.keys())
    for activity in activities[:crossover_point]:
        child[activity] = parent1[activity]
    for activity in activities[crossover_point:]:
        child[activity] = parent2[activity]
    return child


def uniform_crossover(parent1, parent2):
    child = {}
    for activity in ACTIVITIES:
        if random.random() < 0.5:
            child[activity] = parent1[activity]
        else:
            child[activity] = parent2[activity]
    return child


def multi_point_crossover(parent1, parent2):
    child = {}
    crossover_points = sorted(random.sample(range(len(ACTIVITIES)), 2))

    for i, activity in enumerate(ACTIVITIES):
        if i < crossover_points[0] or i >= crossover_points[1]:
            child[activity] = parent1[activity]
        else:
            child[activity] = parent2[activity]
    return child


def create_schedule(schedule):
    # Output to a file
    with open("schedule_output.txt", "w") as f:
        for activity, details in schedule.items():
            f.write(
                f"{activity}: Room - {details['room']}, Time - {details['time']}, Facilitator - {details['facilitator']}\n"
            )


# Main program
if __name__ == "__main__":
    crossover_method = "uniform"
    best_schedule, best_fitness = genetic_algorithm(crossover_method)
    create_schedule(best_schedule)
    print(f"Best Fitness: {best_fitness}")
