# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day05.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile

data = parsefile(file_name, [["\n"], 1, [[None, int, None, int, None, int, " "], "\n"], 0, "\n\n"])

st = data[0][:-1]
size = len(data[0][-1].split())
stacks = [None] * size

for l in st[::-1]:
	for i in range(size):
		if stacks[i] == None:
			stacks[i]=[]
		j = i*4 + 1
		if l[j] != " ":
			stacks[i].append(l[j])

def part1():
	st = [s[:] for s in stacks]
	
	for mv in data[1]:
		d = st[mv[1]-1][-mv[0]:]
		st[mv[1]-1] = st[mv[1]-1][:-mv[0]][:]
		st[mv[2]-1] +=d[::-1]

	res = "".join([s[-1] for s in st if s])
	return res

def part2():
	st = [s[:] for s in stacks]
	
	for mv in data[1]:
		d = st[mv[1]-1][-mv[0]:]
		st[mv[1]-1] = st[mv[1]-1][:-mv[0]][:]
		st[mv[2]-1] +=d[:]

	res = "".join([s[-1] for s in st if s])
	return res


p1()
p2()
