from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day08.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])


from utils import parsefile, parse

data = parsefile(file_name, [[[str], "|"], "\n"])

seg_count = {2:[1], 3:[7], 4:[4], 5:[2, 3, 5], 6:[0, 6, 9], 7:[7]}
seg_pos = {
	frozenset([0, 1, 2, 4, 5, 6]):0,
	frozenset([2, 5]):1,
	frozenset([0, 2, 3, 4, 6]):2,
	frozenset([0, 2, 3, 5, 6]):3,
	frozenset([1, 2, 3, 5]):4,
	frozenset([0, 1, 3, 5, 6]):5,
	frozenset([0, 1, 3, 4, 5, 6]):6,
	frozenset([0, 2, 5]):7,
	frozenset([0, 1, 2, 3, 4, 5, 6]):8,
	frozenset([0, 1, 2, 3, 5, 6]):9
}

def part1():
	c=0
	for v in data:
		for seg in v[1]:
			for k, v in seg_count.items():
				if len(v) == 1:
					if len(seg) == k:
						c+= 1
						
	return c

from itertools import permutations as perms

def part2():
	s = 0
	#={i:list("abcdefg") for i in range(7)}
	for v in data:
		for p in perms("abcdefg", 7):
			mapping = {ord(c):str(i) for i, c in enumerate(p)}
			
			success=True
			
			cv = 0
			mp={}
			
			for seg in v[0] + v[1]:
				seg_set = set(map(int, seg.translate(mapping)))
				
				if frozenset(seg_set) in seg_pos:
					cv += 1
					mp[frozenset(seg)] = seg_pos[frozenset(seg_set)]
				else:
					success = False
					break
			
			if success:
				num = 0
				for seg in v[1]:
					seg_set = set(map(int, seg.translate(mapping)))
					n = seg_pos[frozenset(seg_set)]
					num *= 10
					num += n
					
				s += num
				
				break

	return s

p1()
p2()
