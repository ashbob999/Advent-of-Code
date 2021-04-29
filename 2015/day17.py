from typing import Callable
from os.path import isfile, join as path_join

file_name = path_join('input', 'day17.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file()

containers = list(map(int, open(file_name).read().strip().split("\n")))
containers = sorted(containers, reverse=True)

amount = 150


def count(s, i, max_sum, used_conts, max_conts):
	cnt = 0

	if i >= len(containers) or s >= max_sum:
		if s == max_sum:
			return 1
		else:
			return 0

	cnt += count(s, i + 1, max_sum, used_conts, max_conts)

	if used_conts < max_conts:
		if s + containers[i] < max_sum:
			cnt += count(s + containers[i], i + 1, max_sum, used_conts + 1, max_conts)
		elif s + containers[i] == max_sum:
			cnt += 1

	return cnt


def min_count(s, i, max_sum, used_conts):
	min_used = 100000000000

	if i >= len(containers) or s >= max_sum:
		if s == max_sum:
			return used_conts
		else:
			return 10000000000

	min_used = min(min_count(s, i + 1, max_sum, used_conts), min_used)

	if s + containers[i] < max_sum:
		min_used = min(min_count(s + containers[i], i + 1, max_sum, used_conts + 1), min_used)
	elif s + containers[i] == max_sum:
		min_used = min(min_used, used_conts + 1)

	return min_used


def part1():
	return count(0, 0, amount, 0, len(containers))


def part2():
	min_amount = min_count(0, 0, amount, 0)
	return count(0, 0, amount, 0, min_amount)


print(part1())
print(part2())
