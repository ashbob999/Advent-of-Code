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

def step(pair_count, char_count):
	for pair, count in pair_count.copy().items():
		c1 = pair[0]
		c2 = pair[1]
		nc = rules[c1+c2]
		
		pair_count[c1+c2] -= count
		
		pair_count[c1+nc] += count
		pair_count[nc+c2] += count
		
		char_count[nc] += count
	

def part2():
	pair_count = {v:0 for v in rules.keys()}
	char_count = {chr(v):0 for v in range(ord("A"), ord("Z")+1)}
	
	char_count[start[0]] = 1
	for i in range(1, len(start)):
		pair_count[start[i-1:i+1]] += 1
		
		char_count[start[i]] += 1
	
	for index in range(40):
		step(pair_count, char_count)
		
	min_count = min([v for v in char_count.values() if v > 0])
	max_count = max(char_count.values())
	return max_count - min_count


p1()
p2()
