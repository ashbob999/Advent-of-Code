from typing import Callable
from os.path import isfile, join as path_join
file_name = path_join('input', 'day15.txt')
def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])

#data = to_list(mf=str)
file = "6,3,15,13,1,0"
#file = "0,3,6"
data = [int(v) for v in file.split(",")]

def get_last_diff(arr, v):
	c = 0
	i = 0
	index = []
	tmp = arr[::-1]
	while c < 2:
		if tmp[i] == v:
			c += 1
			index.insert(0, i)
		i += 1

	index[0] = len(arr) - index[0]
	index[1] = len(arr) - index[1]
	#print(arr, index)
	return index[1] - index[0]

def part1(target):
	prev = data[:-1]
	next = data[-1]
	last = data[-1]

	i = len(data)


	while i < target:
		i += 1

		prev.append(last)

		if prev.count(last) > 1:
			next = get_last_diff(prev, last)
		else:
			next = 0

		#print(i, last, next)

		last = next

	return prev, last
	#print(prev, last)

def part2(target):
	prev = {}
	last = None

	for i in range(target):
		if i % 1000000 == 0: print(i)
		if i < len(data):
			num = data[i]
		elif last not in prev:
			num = 0
		else:
			num = i - 1 - prev[last]

		prev[last] = i - 1
		last = num

	return prev, num

t1 = 2020
t2 = 30_000_000

print(part1(t1)[1])
p, l = part2(t2)
print(l)
