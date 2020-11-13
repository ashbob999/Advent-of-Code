from aoc import input_handler

lines = input_handler.get_input(12)


class Moon:
    def __init__(self, pos):
        self.pos = list(pos)
        self.vel = [0, 0, 0]


moons_start = [
    (16, -8, 13),
    (4, 10, 10),
    (17, -5, 6),
    (13, -3, 0)
]

"""
moons_start = [
(-1, 0, 2),
(2, -10, -7),
(4, -8, 8),
(3, 5, -1)
]
"""

moons = [Moon(p) for p in moons_start]

# part 1

pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]


# smaller: +1, larger: -1

def calc_gravity(v1, v2):
    if v1 == v2:
        return (0, 0)
    elif v1 > v2:
        return (-1, +1)
    else:
        return (+1, -1)


def change_velocity(m1, m2):
    x_change = calc_gravity(m1.pos[0], m2.pos[0])
    m1.vel[0] += x_change[0]
    m2.vel[0] += x_change[1]

    y_change = calc_gravity(m1.pos[1], m2.pos[1])
    m1.vel[1] += y_change[0]
    m2.vel[1] += y_change[1]

    z_change = calc_gravity(m1.pos[2], m2.pos[2])
    m1.vel[2] += z_change[0]
    m2.vel[2] += z_change[1]


def step_moons(moons_):
    for pair in pairs:
        moon1 = moons_[pair[0]]
        moon2 = moons_[pair[1]]

        change_velocity(moon1, moon2)

    for moon in moons_:
        moon.pos[0] += moon.vel[0]
        moon.pos[1] += moon.vel[1]
        moon.pos[2] += moon.vel[2]


for i in range(1000):
    step_moons(moons)

total_energy = 0

for moon in moons:
    pot = sum(map(abs, moon.pos))
    kin = sum(map(abs, moon.vel))

    total_energy += pot * kin

print("Part 1: ", total_energy)
print()

# part 2

moons = [Moon(p) for p in moons_start]

get_axis_values = lambda axis: [(m.pos[axis], m.vel[axis]) for m in moons]

x_base_values = (
    moons[0].pos[0],
    moons[1].pos[0],
    moons[2].pos[0],
    moons[3].pos[0],
    moons[0].vel[0],
    moons[1].vel[0],
    moons[2].vel[0],
    moons[3].vel[0]
)

y_base_values = (
    moons[0].pos[1],
    moons[1].pos[1],
    moons[2].pos[1],
    moons[3].pos[1],
    moons[0].vel[1],
    moons[1].vel[1],
    moons[2].vel[1],
    moons[3].vel[1]
)

z_base_values = (
    moons[0].pos[2],
    moons[1].pos[2],
    moons[2].pos[2],
    moons[3].pos[2],
    moons[0].vel[2],
    moons[1].vel[2],
    moons[2].vel[2],
    moons[3].vel[2]
)

xStep = 1
yStep = 1
zStep = 1

xRepeat = False
yRepeat = False
zRepeat = False

while (not xRepeat) or (not yRepeat) or (not zRepeat):
    step_moons(moons)

    x_values = (
        moons[0].pos[0],
        moons[1].pos[0],
        moons[2].pos[0],
        moons[3].pos[0],
        moons[0].vel[0],
        moons[1].vel[0],
        moons[2].vel[0],
        moons[3].vel[0]
    )

    y_values = (
        moons[0].pos[1],
        moons[1].pos[1],
        moons[2].pos[1],
        moons[3].pos[1],
        moons[0].vel[1],
        moons[1].vel[1],
        moons[2].vel[1],
        moons[3].vel[1]
    )

    z_values = (
        moons[0].pos[2],
        moons[1].pos[2],
        moons[2].pos[2],
        moons[3].pos[2],
        moons[0].vel[2],
        moons[1].vel[2],
        moons[2].vel[2],
        moons[3].vel[2]
    )

    if not xRepeat:
        if x_base_values == x_values:
            xRepeat = True
        else:
            xStep += 1

    if not yRepeat:
        if y_base_values == y_values:
            yRepeat = True
        else:
            yStep += 1

    if not zRepeat:
        if z_base_values == z_values:
            zRepeat = True
        else:
            zStep += 1


def gcd(a, b):
    while b > 0:
        a, b = b, a % b
    return a


def lcm(a, b):
    return a * b // gcd(a, b)


total_steps = lcm(lcm(xStep, yStep), zStep)
print("Part 2: ", total_steps)
