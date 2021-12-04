from os.path import isfile, join as path_join
file_name = path_join('input', 'day04.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])


data = to_list(mf=str, sep="\n\n")

numbers = list(map(int, data[0].split(",")))
boards = [[[int(i) for i in r.strip().split(" ")] for r in b.strip().replace("  ", " ").split("\n")] for b in data[1:]]

w = len(boards[0][0])
h = len(boards[0])

def part1():
	marked = [[[1 for i in range(len(r))] for r in b] for b in boards]
	
	used_nums = numbers[:]
	
	while len(used_nums):
		num = used_nums.pop(0)
		
		for bi in range(len(boards)):
			b = boards[bi]
			
			for y in range(h):
				for x in range(w):
					if b[y][x]==num:
						marked[bi][y][x]=0
						
		for bi in range(len(marked)):
			found=False
			if any(sum(r) == 0 for r in marked[bi]):
				found = True
			elif any(sum(r)==0 for r in zip(*marked[bi])):
				found=True
				
			if found:
				b = boards[bi]
				m= marked[bi]
				s =0
				for y in range(h):
					for x in range(w):
						if m[y][x] == 1:
							s+=b[y][x]
				s *= num
				return s


def part2():
	marked = [[[1 for i in range(len(r))] for r in b] for b in boards]
	
	used_nums = numbers[:]
	won=[]
	
	while len(used_nums):
		if len(boards) == len(won):
			break
		num = used_nums.pop(0)
		
		for bi in range(len(boards)):
			b = boards[bi]
			
			for y in range(h):
				for x in range(w):
					if b[y][x]==num:
						marked[bi][y][x]=0
						
		for bi in range(len(marked)):
			found=False
			if any(sum(r) == 0 for r in marked[bi]):
				found = True
			elif any(sum(r)==0 for r in zip(*marked[bi])):
				found=True
				
			if found:
				if bi not in won:
					won.append(bi)
					
	i=won[-1]
	b = boards[i]
	m= marked[i]
	s =0
	for y in range(h):
		for x in range(w):
			if m[y][x] == 1:
				s+=b[y][x]
	s *= num
	return s


p1()
p2()
