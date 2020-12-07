from typing import Callable
from os.path import isfile, join as path_join
file_name = path_join('input', 'day05.txt')
def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])


data = to_list(mf=str, sep="\n")

seats = []

def part1():
	m = 0
	for p in data:
		f = 0
		b = 127

		for c in p[:7]:
			if c == "F":
				b -= (b-f +1) // 2
			else:
				f += (b-f +1) // 2

		l = 0
		r = 7

		for c in p[7:]:
			if c == "L":
				r -= (r-l +1) // 2
			else:
				l += (r-l +1) // 2

		id = f*8 + l
		m = max(m, id)
		seats.append(id)

	print(m)

def part2():
	global seats
	seats = sorted(seats)
	for i in range(0, len(seats)-1):
		if seats[i+1] - seats[i] == 2:
			print(seats[i] +1)
			return


part1()
part2()
