import math

from util import input_handler

lines = input_handler.get_input(10)

asteroids = []
for i, line in enumerate(lines):
    for j, ast in enumerate(line):
        if ast == "#":
            asteroids.append((j, i))

# part 1

best = 0
best_position = None
num = len(asteroids)


def get_patterns(pos, points):
    blocked_ = 1
    patterns_ = set()
    for j in points:
        if pos == j:
            continue
        dx, dy = j[0] - pos[0], j[1] - pos[1]
        normal = (dx // math.gcd(dx, dy), dy // math.gcd(dx, dy))
        if normal in patterns_:
            blocked_ += 1
        patterns_.add(normal)

    return blocked_


aa = asteroids.copy()

for i in asteroids:
    blocked = get_patterns(i, asteroids)

    if num - blocked > best:
        best = num - blocked
        best_position = i

best_position_ = best_position

print("Part 1: ", best_position_, "  :  ", best)


def get_bearing(point1, point2):
    theta = math.atan2(point2[0] - point1[0], point1[1] - point2[1])
    if theta < 0:
        theta += math.pi * 2
    return math.degrees(theta)


def get_patterns2(pos, points):
    blocked_ = 1
    patterns_ = set()
    rel_list = {}
    for j in points:
        if pos == j:
            continue
        dx, dy = j[0] - pos[0], j[1] - pos[1]
        normal = (dx // math.gcd(dx, dy), dy // math.gcd(dx, dy))
        if normal in patterns_:
            blocked_ += 1

        if normal in rel_list:
            rel_list[normal].append(j)
        else:
            rel_list[normal] = [j]
        patterns_.add(normal)

    return blocked_, rel_list


def get_distance(point1, point2):
    x_diff = point2[0] - point1[0]
    y_diff = point2[1] - point1[1]
    return math.sqrt((x_diff ** 2) + (y_diff ** 2))


rel = get_patterns2(best_position_, asteroids)[1]

closest_ast = {}  # rel: actual

for k in rel:
    closest_dist = 10000000000
    closest_point = None
    rel_points = rel[k]
    for p in rel_points:
        dist = get_distance(best_position_, p)
        if dist < closest_dist:
            closest_dist = dist
            closest_point = p

    closest_ast[k] = closest_point


def get_bearing(p1, p2):
    theta = math.atan2(p2[0] - p1[0], p1[1] - p2[1])
    if theta < 0:
        theta += math.pi * 2
    return math.degrees(theta)


bearings = {}

for k, v in closest_ast.items():
    bearings[v] = get_bearing(best_position_, v)

bearings_sorted = {k: v for k, v in sorted(bearings.items(), key=lambda item: item[1])}

n200 = list(bearings_sorted.keys())[199]

print("Part 2: ", n200, " : ", n200[0] * 100 + n200[1])
