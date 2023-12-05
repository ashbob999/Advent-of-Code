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

from utils import *

data = parsefile(file_name,  [[None, 1, int, 0], 1, [[[str, 1, None, 1, str, 1, "-"], None], 1, [int], 0, "\n"], 0, "\n\n"])

seeds = data[0]

maps = {}

str_ids = {}
str_ids["seed"] = 0

for map in data[1:]:
	#print(map)
	from_ = map[0][0][0]
	to_ = map[0][0][1]
	v1 = None
	v2 = None
	
	if from_ not in str_ids:
		v1 = len(str_ids)
		str_ids[from_] = v1
	else:
		v1 = str_ids[from_]
		
	if to_ not in str_ids:
		v2 = len(str_ids)
		str_ids[to_] = v2
	else:
		v2 = str_ids[to_]
		
		
	res = [v2, []]
	for range_ in map[1:]:
		res[1].append(range_)
		
	maps[v1] = res

location = str_ids["location"]


def part1():
	numbers = seeds[:]
	id = str_ids["seed"]
	
	while id != location:
		new_numbers = []
		map = maps[id]
		for num in numbers:
			match = False
			for rng in map[1]:
				if rng[1] <= num < rng[1] + rng[2]:
					new_numbers.append(rng[0] + (num-rng[1]))
					match = True
			if not match:
				new_numbers.append(num)
					
		id = map[0]
		numbers = new_numbers
		
	return min(numbers)


class Range:
	def __init__(self, left, right):
		assert left <= right
		self.left = left
		self.right = right
		
	def check(self, rng):
		res = [None, [None, None]]
		
		if rng.right < self.left or rng.left > self.right:
			res[1][0] = Range(rng.left, rng.right)
			return res
		
		# left edge
		if rng.left < self.left:
			left_rng = Range(rng.left, self.left-1)
			rng.left = self.left
			res[1][0] = left_rng
		
		# right edge
		if rng.right > self.right:
			right_rng = Range(self.right+1, rng.right)
			rng.right = self.right
			res[1][1] = right_rng
			
		# centre
		if rng.left >= self.left and rng.right <= self.right:
			res[0] = rng
			
		return res
		
	def __repr__(self):
		return "Range(" + str(self.left) + ", " + str(self.right) + ")"


def part2():
	numbers = []
	for i in range(0, len(seeds), 2):
		numbers.append(Range(seeds[i], seeds[i]+seeds[i+1]-1))
	id = str_ids["seed"]
	
	while id != location:
		new_numbers = []
		map = maps[id]
		i = 0
		while i < len(numbers):
			num = numbers[i]
			
			match = False
			for rng in map[1]:
				rng_ = Range(rng[1], rng[1]+rng[2]-1)
				ch = rng_.check(num)
				if ch[0]:
					if ch[1][0]:
						numbers.append(ch[1][0])
					if ch[1][1]:
						numbers.append(ch[1][1])
					in_rng = ch[0]
					
					left = rng[0] + in_rng.left-rng[1]
					right = rng[0] + in_rng.right-rng[1]
					new_numbers.append(Range(left, right))
					match = True
					break
			if not match:
				new_numbers.append(num)
				
			i += 1
					
		id = map[0]
		numbers = new_numbers
		#print(id, len(numbers))
		
	return min([num.left for num in numbers])


p1()
p2()
