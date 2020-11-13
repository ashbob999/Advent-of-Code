from aoc import input_handler

# link to Day X: https://adventofcode.com/2019/day/1

# gets the input lines for the challenge
lines = input_handler.get_input(1)

masses = list(map(int, lines))

# part 1

fuels = []

for mass in masses:
    fuel = int(mass / 3) - 2
    fuels.append(fuel)

total_fuel = sum(fuels)

print("Part 1: ", total_fuel)


# part 2

def calc_fuel(mass_, fuel_tally=0):
    fuel_ = int(mass_ / 3) - 2
    if fuel_ > 0:
        return calc_fuel(fuel_, fuel_tally + fuel_)
    else:
        return fuel_tally


fuels = []

for mass in masses:
    new_fuel = calc_fuel(mass)
    fuels.append(new_fuel)

total_fuel = sum(fuels)

print("Part 2: ", total_fuel)
