# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day02.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile

data = parsefile(file_name, [[str, " "], "\n"])

def part1():
	s = 0
	for pair in data:
		p1 = ord(pair[0]) - ord("A")
		p2 = ord(pair[1]) - ord("X")
		if p1 == p2: # draw
			s += p2+1 + 3
		elif (p1==0 and p2 ==1) or (p1==1 and p2==2) or (p1==2 and p2==0):
			s+= p2+1 + 6
		else:
			s+= p2+1
			
	return s

def part2():
	s=0
	
	for pair in data:
		if pair[1] == "X":
			diff =-1
			s+=0
		elif pair[1] == "Y":
			diff = 0
			s+=3
		elif pair[1] == "Z":
			diff = 1
			s+=6
			
		p1 =ord(pair[0]) - ord("A")
		val = (p1 + diff) %3
		s+=val+1
	
	return s


p1()
p2()
