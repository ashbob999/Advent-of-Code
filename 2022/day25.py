# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day25.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile, parse

nums = parsefile(file_name, [str, "\n"])
rd = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""
numsa = parse(rd, [str, "\n"])

def decode(s):
	n = 0
	pow = 1
	for c in s[::-1]:
		if c in ("0", "1", "2"):
			n += int(c) * pow
		elif c == "-":
			n += -1 * pow
		elif c == "=":
			n += -2 * pow
			
		pow *= 5
		
	return n
	
def encode(num):
	s = ""
	
	return s

def part1():
	tot = 0
	for num in nums:
		tot += decode(num)
	
	print(tot)
	
	s = encode(tot)
	
	return s


def part2():
	pass


p1()
p2()
