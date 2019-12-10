import math

from util import input_handler

lines = input_handler.get_input(10)

"""
lines = [
    ".#..##.###...#######",
    "##.############..##.",
    ".#.######.########.#",
    ".###.#######.####.#.",
    "#####.##.#.##.###.##",
    "..#####..#.#########",
    "####################",
    "#.####....###.#.#.##",
    "##.#################",
    "#####.##.###..####..",
    "..######..##.#######",
    "####.##.####...##..#",
    ".#####..#.######.###",
    "##...#.##########...",
    "#.##########.#######",
    ".####.#.###.###.#.##",
    "....##.##.###..#####",
    ".#.#.###########.###",
    "#.#.#.#####.####.###",
    "###.##.####.##.#..##"
]
"""
asteroids = []
for i, line in enumerate(lines):
    for j, ast in enumerate(line):
        if ast == "#":
            asteroids.append((j, i))

# part 1
sight_number = -1
pos = None
sights_ = None

for asteroid in asteroids:
    sights = {}
    # (type, x^1 coeff, x^0 coeff, dist, x, y)

    # asteroid = (5,-8)

    for ast in asteroids:
        if asteroid == ast: continue

        xDiff = ast[0] - asteroid[0]
        yDiff = ast[1] - asteroid[1]

        if xDiff == 0:

            type = "x"
            gradient = 0
            y_intercept = asteroid[0]
        elif yDiff == 0:
            type = "y"
            gradient = 0
            y_intercept = asteroid[1]
        else:
            type = "y"
            gradient = (yDiff) / (xDiff)
            y_intercept = ast[1] - (gradient * ast[0])
        # y = mx +c
        # c = y - mx

        dist = 0  # math.sqrt(math.pow(ast[0] - asteroid[0], 2) + math.pow(ast[1] - asteroid[1], 2))

        if xDiff >= 0:
            if yDiff >= 0:
                quad = "TL"
            else:
                quad = "BL"
        else:
            if yDiff >= 0:
                quad = "TR"
            else:
                quad = "BR"

        key = (type, gradient, y_intercept, quad)
        value = (dist, ast[0], ast[1])

        """
        if asteroid == (5, -8) and ast==(9,-9):
            print(key,"  :  ",value)
            print(key in sights)
        """

        if key not in sights:
            sights[key] = value
        else:
            if value[0] < sights[key][0]:
                sights[key] = value

    if len(sights) > sight_number:
        sight_number = len(sights)
        pos = asteroid
        sights_ = sights.copy()

    # if asteroid == (11, -13):
    # for k, v in sights.items():
    # print("  :  ", v)
    # print(len(sights))
    # sights_ = sights.copy()
    # break

# break

print("Part 1: ", sight_number, " : ", pos)

l2 = list(list(l) for l in lines.copy())
l2[17][17] = "O"

for k, v in sights_.items():
    x = v[1]
    y = v[2]
    l2[-y][x] = "X"

print("\n")
for row in l2:
    pass
    # print("".join(row))

print("\n")
for k, v in sights_.items():
    pass
#     print(k, " : ", v, ">")

# ----------------------------------------------------------------------------------

best = 0
best_position = None
num = len(asteroids)
patterns_best = None


def get_patterns(pos, points):
    blocked_ = 1
    patterns_ = list()
    correct_patterns = list()
    points_ = list()
    for j in points:
        if i == j:
            continue
        dx, dy = j[0] - pos[0], j[1] - pos[1]
        normal = (dx // math.gcd(dx, dy), dy // math.gcd(dx, dy))
        if normal in set(patterns_):
            blocked_ += 1
        else:
            points_.append(j)
            correct_patterns.append(normal)
        patterns_.append(normal)

        # print("J: ", j)
    return blocked_, patterns_, points_, correct_patterns


for i in asteroids:
    blocked, patterns, p = get_patterns(i, asteroids)[:3]

    if num - blocked > best:
        best = num - blocked
        best_position = i
        patterns_best = p.copy()  # patterns.copy()
best_position_ = best_position

print("best: ", best, " : ", best_position_)  # 340??

# part 2

print(len(patterns_best))
# print(patterns_best)
print("\n")


def get_angle_from_point(start_point, point):
    if start_point[0] == point[0]:
        if point[1] > start_point[1]:
            return math.pi
        return 0
    elif start_point[1] == point[1]:
        if point[0] > start_point[0]:
            return 0.5 * math.pi
        return 1.5 * math.pi
    delta_x = point[0] - start_point[0]
    delta_y = start_point[1] - point[1]
    theta_radians = math.atan2(delta_y, delta_x)
    return theta_radians


def get_angle(rel_point):
    quadrant_angle = math.degrees(math.atan2(rel_point[1], rel_point[0]))
    if quadrant_angle < 0:
        quadrant_angle += 360
    return (quadrant_angle + 90) % 360


def get_delta_pos(start_point, point, normal):
    delta_x = point[0] - start_point[0]
    delta_y = point[1] - start_point[1]

    if delta_x != 0:
        factor = delta_x // normal[0]
    else:
        factor = delta_y // normal[1]

    return normal[0] * factor, normal[1] * factor


remaining_asteroids = patterns_best.copy()
n = 200
amount_destroyed = 0

while amount_destroyed <= n:
    point_list, asts = get_patterns(best_position_, remaining_asteroids)[2:]

    angles = [tuple([get_angle(get_delta_pos(best_position_, point_list[i], ast)), point_list[i]]) for i, ast in
              enumerate(asts)]

    angles.sort(key=lambda d: d[0])

    # index_of_answer = point_list.index((26, 28))
    # print(index_of_answer)

    # print(angles)
    # for angle in angles:
    #     pos = angle[1]
    #     # remaining_asteroids.remove(pos)
    #
    #     amount_destroyed += 1
    #
    #     if amount_destroyed == n:
    #         print("n200: ", pos)
    #         break
    break

# Part 2 answer == 2628 (26, 28)
