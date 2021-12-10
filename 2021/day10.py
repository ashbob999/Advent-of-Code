from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day10.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])

from utils import parsefile

data = parsefile(file_name, ["\n"])

score_corrupt = {")":3, "]":57, "}":1197, ">":25137}
score_closing = {")":1, "]":2, "}":3, ">":4}

open_c = set(["(", "[", "{", "<"])
close_c = set([")", "]", "}", ">"])

match_open = {")":"(", "]":"[", "}":"{", ">":"<"}
match_close = {"(":")", "[":"]", "{":"}", "<":">"}

def check_corrupted(line):
	stack = []
	
	for c in line:
		if c in open_c:
			stack.append(c)
		else:
			if stack[-1] == match_open[c]:
				stack.pop()
			else:
				return True, c
	
	return False, ""

non_corrupt = []

def part1():
	s = 0
	for line in data:
		res = check_corrupted(line)
		if res[0]:
			s += score_corrupt[res[1]]
		else:
			non_corrupt.append(line)

	return s


def check_closing(line):
	stack = []
	
	for c in line:
		if c in open_c:
			stack.append(c)
		else:
			if stack[-1] == match_open[c]:
				stack.pop()
			else:
				pass
	
	if len(stack) > 0:
		return False, stack
	return True, []

def calc_score(ending):
	s = 0
	for c in ending:
		s *= 5
		s += score_closing[c]
		
	return s


def part2():
	s = []
	
	for line in non_corrupt:
		res = check_closing(line)
		if not res[0]:
			ending = list(map(lambda x: match_close[x], list(res[1][::-1])))
			s.append(calc_score(ending))
	
	s = sorted(s)
	mid_i = len(s) // 2
	return s[mid_i]

p1()
p2()
