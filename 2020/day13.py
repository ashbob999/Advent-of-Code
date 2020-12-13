from typing import Callable
from os.path import isfile, join as path_join
file_name = path_join('input', 'day13.txt')
def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])

data = to_list(mf=str)

start_time = int(data[0])
bus_ids = [int(v) for v in data[1].split(",") if v != "x"]

def part1():
	ed = start_time
	while True:
		for bus in bus_ids:
			if ed % bus == 0:
				print(bus * (ed - start_time))
				return

		ed += 1

def ee(a, b):
	if a == 0:
		return (b, 0, 1)

	g, y, x = ee(b % a, a)
	return (g, x - (b // a) * y, y)

def mi(a, m):
	g, x, y = ee(a, m)
	return x % m

def crt(m, x):
	while True:
		temp = mi(m[1], m[0]) * x[0] * m[1]
		temp += mi(m[0], m[1]) * x[1] * m[0]

		temp2 = m[0] * m[1]

		x.remove(x[0])
		x.remove(x[0])
		x = [temp % temp2] + x

		m.remove(m[0])
		m.remove(m[0])
		m = [temp2] + m

		if len(x) == 1:
			break

	return x[0]

def part2():
	bus_times = data[1].split(",")
	m = []
	x = []

	for i, v in enumerate(bus_times):
		if v == "x":
			continue

		v = int(v)

		m.append(v)
		x.append(-i % v)

	# n +xq % b1 == 0
	# n +x2 % b2 == 0

	print(crt(m, x))

part1()
part2()
