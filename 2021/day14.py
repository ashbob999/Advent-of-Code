from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day14.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])

from utils import parsefile, parse

start, *data = parsefile(file_name, [str, 1, [[str, " -> "], "\n"], "\n\n"])

rules = {}
for rule in data[0]:
	rules[rule[0]] = rule[1]

def part1():
	s = start
	
	for it in range(10):
		new_s = ""
		for i in range(1, len(s)):
			new_s += s[i-1]
			new_s += rules[s[i-1:i+1]]
			
		new_s += s[-1]
		s = new_s

	count = {chr(v):0 for v in range(ord("A"), ord("Z")+1)}
	for c in s:
		count[c] += 1
		
	min_count = min([v for v in count.values() if v > 0])
	max_count = max(count.values())
	return max_count - min_count

mem = {}
rules_int = {(ord(k[0])-65, ord(k[1])-65):ord(v)-65 for k, v in rules.items()}
zeroes = [0]*26

"""
based on this
20 is original length
39 is length after transform
split into 2 halves to stop memory overload
each tab represents a iteration
use memorisation or it will take forever
20 -> 39 -> 20, 20
	20 -> 39 -> 20, 20
		20 -> 39 -> 20, 20
		20 -> 39 -> 20, 20
	20 -> 39 -> 20, 20
		20 -> 39 -> 20, 20
		20 -> 39 -> 20, 20
"""


def rec(s, depth, max_depth, mid):
	if depth >= max_depth:
		c = zeroes.copy()
		for v in s[:-1]:
			c[v] += 1
		return c

	depth += 1

	if (tuple(s), depth) in mem:
		return mem[(tuple(s), depth)]

	new_s = [0] * (2*mid-1)
	new_s_i = 0
	for i in range(1, mid):
		new_s[new_s_i] = s[i - 1]
		new_s[new_s_i+1] = rules_int[tuple(s[i-1:i+1])]
		new_s_i += 2

	new_s[-1] = s[-1]

	count = zeroes.copy()

	c1 = rec(new_s[:mid], depth, max_depth, mid)
	c2 = rec(new_s[mid-1:], depth, max_depth, mid)

	for i in range(26):
		count[i] += c1[i] + c2[i]

	mem[(tuple(s), depth)] = count

	return count


def part2():
	mid = len(start)

	start_int = [ord(c) - 65 for c in start]
	iterations = 40
	count = rec(start_int, 0, iterations, mid)

	count[start_int[-1]] += 1

	min_count = min([v for v in count if v > 0])
	max_count = max(count)
	return max_count - min_count


p1()
p2()
