from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day06.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])


from utils import parsefile

data = parsefile(file_name, [int, ","])

def part1():
	fish = data[:]

	for i in range(80):
		for fi in range(len(fish)):
			if fish[fi]==0:
				fish[fi]=6
				fish.append(8)
			else:
				fish[fi]-=1

	return len(fish)


def part2():
	fish = [0]*9

	for f in data:
		fish[f]+=1

	for i in range(256):
		fish.append(fish[0])
		fish.pop(0)
		fish[6] += fish[8]

	return sum(fish)


p1()
p2()
