from typing import Callable
from os.path import isfile, join as path_join

file_name = path_join('input', 'day04.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file()

input = open(file_name).read().strip().split("-")

min_number = int(input[0])
max_number = int(input[1])


def check_number(number):
	value = str(number)
	is_correct = False

	for pair in range(0, len(value) - 1, 1):
		n1 = int(value[pair])
		n2 = int(value[pair + 1])

		if n2 < n1:
			return False

		if n1 == n2:
			is_correct = True

	return is_correct


def part1():
	correct_values = 0
	corr_l = []

	for i in range(min_number, max_number, 1):
		if check_number(i):
			correct_values += 1
			corr_l.append(i)

	return correct_values


def check_number_2(number):
	value = str(number)
	is_correct = False

	for pair in range(0, len(value) - 1, 1):
		n1 = int(value[pair])
		n2 = int(value[pair + 1])

		if n2 < n1:
			return False

		if n1 == n2:
			is_correct = True

	previous_number = value[0]
	current_amount = 0
	for char in value:
		if char == previous_number:
			current_amount += 1
		else:
			if current_amount == 2:
				return True

			previous_number = char
			current_amount = 1

	if current_amount == 2:
		return True

	return False


def part2():
	correct_numbers = 0

	for i in range(min_number, max_number, 1):
		if check_number_2(i):
			correct_numbers += 1

	return correct_numbers


print(part1())
print(part2())
