# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day06.txt')
def to_list(mf=int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf=int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

#data = parsefile(file_name, [[int], 0, [str], 1, "\n"])
data = parsefile(file_name, [[str], "\n"])
raw_data = open(file_name).read().split("\n")#parsefile(file_name, [[str, ""], "\n"])

numbers = data[:-1]
ops = data[-1]

numbers = []
for d in data[:-1]:
	numbers.append(list(map(int, d)))
	
ops = data[-1]


def part1():
	s = 0
	
	for i in range(len(ops)):
		op = ops[i]
		
		v = numbers[0][i]
		
		for y in range(1, len(numbers)):
			if op == "+":
				v += numbers[y][i]
			elif op == "*":
				v *= numbers[y][i]
			else:
				assert(False)
				
		s += v
	
	return s


raw_ops = raw_data[-2]
ops_idxs=[]
prev_idx = 0
for i in range(len(raw_ops)):
	c = raw_ops[i]
	if c != " ":
		ops_idxs.append((prev_idx, i-1))
		prev_idx = i


ops_idxs.append((prev_idx, len(raw_ops)))

ops_idxs.pop(0)


def part2():
	s = 0
	
	for idx in ops_idxs:
		op = raw_ops[idx[0]]
		v = None
		
		for x in range(idx[0], idx[1]):
			num = 0
			for y in range(len(raw_data)-2):
				c = raw_data[y][x]
				if c == " ":
					continue
				
				n = int(c)
				num *= 10
				num += n
				
			if v is None:
				v = num
			else:
				if op == "+":
					v += num
				else:
					v *= num

		s += v
	
	return s


p1()
p2()
