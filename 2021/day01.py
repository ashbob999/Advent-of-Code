from os.path import isfile, join as path_join
file_name = path_join('input', 'day01.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])

data  = to_list(sep="\n")

#data=list(map(int, """199 200 208 210 200 207 240 269 260 263""".split(" ")))

def part1():
	return sum(1 for a,b in zip(data, data[1:]) if a<b)
	"""
	c= 0
	for i in range(len(data)-1):
		if data[i] < data[i+1]:
			c +=1
			
	return c
	"""


def part2():
	return sum(1 for a, b in zip(data, data[3:]) if a < b)
	"""
	c=0
	sp=data[0]+data[1]+data[2]
	for i in range(3,len(data)):
		sc = sp - data[i-3]
		sc += data[i]
		if sc > sp:
			c +=1
		sp=sc
		
	return c
	"""


p1()
p2()
