from typing import Callable
from os.path import isfile, join as path_join

file_name = path_join('input', 'day01.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file()

masses = list(map(int, open(file_name).read().strip().split("\n")))


def part1():
	fuels = []

	for mass in masses:
		fuel = int(mass / 3) - 2
		fuels.append(fuel)

	total_fuel = sum(fuels)
	return total_fuel


def calc_fuel(mass_, fuel_tally=0):
	fuel_ = int(mass_ / 3) - 2
	if fuel_ > 0:
		return calc_fuel(fuel_, fuel_tally + fuel_)
	else:
		return fuel_tally


def part2():
	fuels = []

	for mass in masses:
		new_fuel = calc_fuel(mass)
		fuels.append(new_fuel)

	total_fuel = sum(fuels)
	return total_fuel


print(part1())
print(part2())
