# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day03.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile

data = parsefile(file_name, [list, "\n"])

def part1():
	s=0
	for line in data:
		mid = len(line)//2
		c1=line[:mid]
		c2=line[mid:]
		
		same = set(c1) & set(c2)
		v = list(same)[0]
		if "A"<=v<="Z":
			p = 27 + (ord(v) - ord("A"))
		else:
			p= 1+ord(v) - ord("a")
		#print(p, v)
		s+=p
	return s

def part2():
	s=0
	for i in range(0, len(data), 3):
		group = data[i:i+3]
		common = set(group[0]) & set(group[1]) & set(group[2])
		
		v = list(common)[0]
		if "A"<=v<="Z":
			p=27 + (ord(v) - ord("A"))
		else:
			p=1+(ord(v) - ord("a"))
		
		s+=p
	return s



p1()
p2()
