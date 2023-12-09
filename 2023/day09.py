# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day09.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

data = parsefile(file_name, [[int], "\n"])


def predict(values):
	diff = [values[i+1] - values[i] for i in range(len(values) -1)]

	if sum(diff) == 0:
		return values[0]
	else:
		return values[-1] + predict(diff)

def part1():
	return sum([predict(v) for v in data])


def predict2(values):
	diff = [values[i+1] - values[i] for i in range(len(values) -1)]

	if sum(diff) == 0:
		return values[0]
	else:
		return values[0] - predict2(diff)

def part2():
	return sum([predict2(v) for v in data])


p1()
p2()
