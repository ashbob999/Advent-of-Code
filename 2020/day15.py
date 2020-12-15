from os.path import isfile, join as path_join
from typing import Callable

file_name = path_join('input', 'day15.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file(session_path=['..', '.env'])

file = "6,3,15,13,1,0"
data = [int(v) for v in file.split(",")]


def part1(target):
	prev = [-1] * (target + 1)
	last = 1
	dl = len(data)

	for i in range(1, target + 1):
		# if i % 1000000 == 0: print(i)
		if i - 1 < dl:  # False when i >= len(data)
			num = data[i - 1]
		elif prev[last] == -1:
			num = 0
		else:
			num = i - prev[last]

		prev[last] = i
		last = num

	return prev, num


def part2():
	pass


t1 = 2020
t2 = 30_000_000

print(part1(t1)[1])  # 5ms
print(part1(t2)[1])  #
