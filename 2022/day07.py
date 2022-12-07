# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day07.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile

data = parsefile(file_name, [str, "\n"])

cmds = []

for d in data:
	if d[0]== "$":
		cmds.append([d[1:].strip().split(), []])
	else:
		cmds[-1][1].append(d.strip().split())
		
fs = [{}, {}]

cd = ["/"]

for cmd in cmds:
	if cmd[0][0] == "cd":
		path = cmd[0][1]
		if path == "/":
			cd = ["/"]
		elif path == "..":
			cd.pop()
		else:
			cd.append(path)
			
		d=fs
		for dir in cd:
			if dir not in d[0]:
				d[0][dir] = [{}, {}]
			d = d[0][dir]
	
	elif cmd[0][0] == "ls":
		d=fs
		for dir in cd:
			d=d[0][dir]
		
		for file in cmd[1]:
			if file[0] == "dir":
				if file[1] not in d[0]:
					d[0][file[1]] = [{}, {}]
			else:
				size = int(file[0])
				d[1][file[1]] = size
				
def pp(fs, lv):
	for dir, v in fs[0].items():
		print("  "*lv, dir)
		pp(v, lv+1)
		
	for k, v in fs[1].items():
		print("  "*lv, k, v)
	
#pp(fs, 0)

dir_sizes = {}
	
def size(fs, path):
	s=0
	for k, v in fs[0].items():
		s += size(v, path +"/"+k)
		
	for k, v in fs[1].items():
		s += v
			
	dir_sizes[path] = s
	return s

size(fs, "")
ls = list(dir_sizes.items())

def part1():
	ls_filter = list(filter(lambda x: x[1] <=100000, ls))
	return sum(map(lambda x: x[1], ls_filter))

def part2():
	ts = 70000000
	freesp=30000000
	root = None
	for d in ls:
		if d[0] == "//":
			root = d
			break
	
	freespfs = ts - root[1]
	reqsp = freesp - freespfs
	
	ls_filter = list(filter(lambda x: x[1] >= reqsp, ls))
	v = sorted(ls_filter, key=lambda x:x[1])[0]
	return v[1]

p1()
p2()
