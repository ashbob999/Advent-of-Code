from aoc import input_handler

# link to Day X: https://adventofcode.com/2019/day/3

# gets the input lines for the challenge
lines = input_handler.get_input(3)


def get_dirs(line):
    return [(direction[0], int(direction[1:])) for direction in line.split(",")]


wire1_directions = get_dirs(lines[0])
wire2_directions = get_dirs(lines[1])

# Part 1

center = (0, 0)


def create_path(start, dirs):
    current = list(start)

    path_points = []

    for dir_ in dirs:
        if dir_[0] == "U":  # Y increase
            new_y = current[1] + dir_[1]
            path_points.extend(get_points("V", current[0], current[1], new_y))
            current[1] = new_y
        elif dir_[0] == "D":  # Y decreases
            new_y = current[1] - dir_[1]
            path_points.extend(get_points("V", current[0], current[1], new_y))
            current[1] = new_y
        elif dir_[0] == "L":  # X decreases
            new_x = current[0] - dir_[1]
            path_points.extend(get_points("H", current[1], current[0], new_x))
            current[0] = new_x
        elif dir_[0] == "R":  # X increases
            new_x = current[0] + dir_[1]
            path_points.extend(get_points("H", current[1], current[0], new_x))
            current[0] = new_x
        # print(dir[0])
    return path_points


def get_points(dir_, const, start, end):
    if dir_ == "H":
        if start == end:
            return [(const, start)]
        else:
            if start < end:
                return [(const, i) for i in range(start + 1, end + 1, 1)]
            else:
                return [(const, i) for i in range(start - 1, end - 1, -1)]
    elif dir_ == "V":
        if start == end:
            return [(start, const)]
        else:
            if start < end:
                return [(i, const) for i in range(start + 1, end + 1, 1)]
            else:
                return [(i, const) for i in range(start - 1, end - 1, -1)]


def get_intersections(path1, path2):
    path1_set = set(path1)
    path2_set = set(path2)
    return path1_set & path2_set


def calc_manhattan_dist(start, point):
    x_dist = abs(start[0] - point[0])
    y_dist = abs(start[1] - point[1])
    return x_dist + y_dist


# wire1_directions = get_dirs("R8,U5,L5,D3")
# wire2_directions = get_dirs("U7,R6,D4,L4")

wire1_path = create_path(center, wire1_directions)
wire2_path = create_path(center, wire2_directions)

intersections = get_intersections(wire1_path, wire2_path)

# print(ints)

distances = {}

for intersection in intersections:
    distances[calc_manhattan_dist(center, intersection)] = intersection

closest_intersection_distance = sorted(distances.keys())[0]

print("Part 1: ", closest_intersection_distance)

# Part 2

# for each intersection: calculate the distance to it for each wire

intersection_steps = {}

for intersection in intersections:
    wire1_steps = wire1_path.index(intersection) + 1
    wire2_steps = wire2_path.index(intersection) + 1

    total_steps = wire1_steps + wire2_steps
    intersection_steps[total_steps] = intersection

closest_intersection_steps = sorted(intersection_steps.keys())[0]

print("Part 2: ", closest_intersection_steps)
