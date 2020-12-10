from typing import Callable
from os.path import isfile, join as path_join
file_name = path_join('input', 'day10.txt')
def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])

data = to_list()

data = sorted(data)

def part1():
	a = [None, 0, 0, 0]

	a[data[0]] += 1

	for i in range(len(data) - 1):
		a[data[i+1] - data[i]] += 1

	a[3] += 1

	print(a[1] * a[3])


part1()

data.append(data[-1] + 3)

from collections import defaultdict

def part2():
	ways = defaultdict(int)
	ways[0] = 1
	for v in data:
		ways[v] = ways[v-1] + ways[v-2] + ways[v-3]

	print(ways[data[-1]])


part2()
