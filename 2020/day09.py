from typing import Callable
from os.path import isfile, join as path_join
file_name = path_join('input', 'day09.txt')
def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])

data = to_list()


def part1():
	pre = data[:25]

	pre_set = set(data[:25])

	for i in range(25, len(data)):
		num = data[i]

		valid = False

		for v in pre_set:
			res = num - v
			if res != v and res in pre_set:
				valid = True
				break

		if not valid:
			return num

		pre_set.remove(pre[0])
		pre_set.add(num)

		pre.pop(0)
		pre.append(num)


def part2(invalid):
	max_len = 0
	max_i = 0

	for i in range(len(data)):
		for j in range(i+1, len(data)):
			s = sum(data[i:j+1])
			if s == invalid:
				if j-i+1 > max_len:
					max_len = j-i+1
					max_i = i
			elif s > invalid:
				break

	print(min(data[max_i:max_i+max_len]) + max(data[max_i:max_i+max_len]))


invalid = part1()
print(invalid)

part2(invalid)
