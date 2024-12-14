# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day14.txt')
def to_list(mf=int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf=int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

data = parsefile(file_name, "\n")

w = 101
h = 103

robots = []
for d  in data:
	s = d.split()
	p = s[0].split(",")
	v = s[1].split(",")
	
	x = int(p[0][2:])
	y = int(p[1])
	
	vx = int(v[0][2:])
	vy = int(v[1])
	
	robots.append((x, y ,vx ,vy))
	
print(robots[0])

def part1():
	q1 = 0
	q2 = 0
	q3 = 0
	q4 = 0
	
	poses = []
	
	for r in robots:
		nx = r[0] + 100 * r[2]
		ny = r[1] + 100 * r[3]
		
		nx %= w
		ny %= h
		
		if nx < w//2 and ny < h//2:
			q1 += 1
		
		if nx > w//2 and ny < h//2:
			q2 += 1
			
		if nx < w//2 and ny > h//2:
			q3 += 1
			
		if nx > w//2 and ny > h//2:
			q4 += 1
			
	return q1 * q2 * q3 * q4


from typing import Iterator, Tuple
from itertools import groupby

def run_length_encode(data: str) -> Iterator[Tuple[str, int]]:
    """Returns run length encoded Tuples for string"""
    # A memory efficient (lazy) and pythonic solution using generators
    return [(x, sum(1 for _ in y)) for x, y in groupby(data)]


from PIL import Image

def part2():
	min_100 = []
	min_v = None
	
	for i in range(1, w*h+1):
		if i % 1000 == 0: print(i)
		rbs = set()
		for r in robots:
			nx = r[0] + i * r[2]
			ny = r[1] + i * r[3]
		
			nx %= w
			ny %= h
			
			rbs.add((nx, ny))
			
		ng = [1 if (x, y) in rbs else 0 for x in range(w) for y in range(h)]
		
		#rl = run_length_encode(ng)
		
		diffs = 0
		cv = None
		
		fail = False
		for y in range(h):
			for x in range(w):
				v = 1 if (x, y) in rbs else 0
				if cv is None:
					cv = v
				else:
					if cv != v:
						cv = v
						diffs += 1
						
						if min_v is not None and diffs > min_v[1]:
							fail = True
							break
							
			if fail:
				break
				
		if fail:
			continue
						
		if min_v is None or diffs < min_v[1]:
			min_v = (i, diffs)
		
		"""
		if min_v is None or len(rl) < min_v[1]:
			min_v = (i, len(rl))
		"""
		"""
		if len(min_100) < 100:
			min_100.append((i, rl))
			
			min_100.sort(key=lambda x: len(x[1]))
		else:
			if len(min_100[-1][1]) > len(rl):
				min_100[-1] = (i, rl)
				
				min_100.sort(key=lambda x: len(x[1]))
		"""
	
	"""
	for v in min_100:
		rbs = set()
		for r in robots:
			nx = r[0] + v[0] * r[2]
			ny = r[1] + v[0] * r[3]
		
			nx %= w
			ny %= h
			
			rbs.add((nx, ny))
	
	
		img = Image.new("RGB", (w, h))
	
		pix = img.load()
		for r in rbs:
			#print(r)
			pix[r] = (255, 255, 255)
	
		img.save("min_100/" + str(v[0]) + ".jpg")
	
	"""
	
	rbs = set()
	for r in robots:
		nx = r[0] + min_v[0] * r[2]
		ny = r[1] + min_v[0] * r[3]
	
		nx %= w
		ny %= h
		
		rbs.add((nx, ny))


	img = Image.new("RGB", (w, h))

	pix = img.load()
	for r in rbs:
		#print(r)
		pix[r] = (255, 255, 255)

	img.save("day14_p2_min_v_" + str(min_v[0]) + ".jpg")
	
	return min_v[0]
	
	
	for i in range(2000, 3000):
		print(i)
		rbs = set()
		for r in robots:
			nx = r[0] + i * r[2]
			ny = r[1] + i * r[3]
		
			nx %= w
			ny %= h
			
			rbs.add((nx, ny))
	
	
		img = Image.new("RGB", (w, h))
	
		pix = img.load()
		for r in rbs:
			#print(r)
			pix[r] = (255, 255, 255)
	
		img.save("day14_3/" + str(i) + ".jpg")


p1()
p2()
