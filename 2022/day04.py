# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day04.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile

data = parsefile(file_name, [[[int, "-"], ","], "\n"])

def part1():
	fully=0
	for pair in data:
		p1 = pair[0]
		p2 = pair[1]
			
		if p1[0]>=p2[0] and p1[1]<=p2[1]:
			fully +=1
		elif p2[0]>=p1[0] and p2[1]<=p1[1]:
			fully +=1
				
	return fully


def part2():
	fully=0
	for pair in data:
		p1 = pair[0]
		p2 = pair[1]
			
		if p1[0]>=p2[0] and p1[0]<=p2[1]:
			fully +=1
		elif p1[1] >=p2[0] and p1[1] <=p2[1]:
			fully +=1
		elif p2[0] >=p1[0] and p2[0] <=p1[1]:
			fully +=1
		elif p2[1] >=p1[0] and p2[1] <=p1[1]:
			fully +=1
				
	return fully


p1()
p2()
