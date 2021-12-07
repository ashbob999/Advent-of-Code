from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day07.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])

from utils import parsefile

data = parsefile(file_name, [int, ","])
daata = list(map(int, "16,1,2,0,4,2,7,1,2,14".split(",")))

def part1():
	minv = min(data)
	maxv = max(data)
	
	min_diff = 1000000000000
	min_hp = 0
	
	for hp in range(minv, maxv +1):
		diff = 0
		for v in data:
			diff += abs(hp - v)
			
		if diff < min_diff:
			min_diff = diff
			min_hp = hp
			
	return min_diff

def ls(n):
	return n * (n-1) * 0.5

def part2():
	minv = min(data)
	maxv = max(data)
	
	min_diff = 1000000000000
	min_hp = 0
	
	for hp in range(minv, maxv +1):
		diff = 0
		for v in data:
			diff += int(ls(abs(hp - v)+1))
			
		if diff < min_diff:
			min_diff = diff
			min_hp = hp
			
	return min_diff, min_hp


p1()
p2()
