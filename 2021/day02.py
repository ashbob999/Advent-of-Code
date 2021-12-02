from os.path import isfile, join as path_join
file_name = path_join('input', 'day02.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])


data = to_list(mf=str,sep="\n")

pos=[x.split(" ") for x in data]


def part1():
	d=0
	h=0
	
	for p in pos:
		if p[0] == "forward":
			h+= int(p[1])
		elif p[0] == "up":
			d-= int(p[1])
		elif p[0] == "down":
			d+= int(p[1])
	
	return d* h


def part2():
	d=0
	h=0
	a=0
	
	for p in pos:
		if p[0] == "forward":
			h+= int(p[1])
			d += a * int(p[1])
		elif p[0] == "up":
			a-= int(p[1])
		elif p[0] == "down":
			a+= int(p[1])
	
	return d* h


p1()
p2()
