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

from utils import *

data = parsefile(file_name,  [[Merge([list]), 1, int], "\n"])

for d in data:
	cards = d[0]
	for i in range(5):
		c = cards[i]
		if c.isdigit():
			cards[i] = int(c)
		else:
			if c == "T":
				cards[i] = 10
			elif c == "J":
				cards[i] = 11
			elif c == "Q":
				cards[i] = 12
			elif c == "K":
				cards[i] = 13
			elif c == "A":
				cards[i] = 14
			else:
				assert "invalid char: " + c

def rank(cards):
	#print(cards)
	d = {}
	for c in cards[0]:
		if c not in d:
			d[c] = 1
		else:
			d[c] += 1
		
	nums = list(d.values())
	numl = len(nums)
		
	if numl == 1:
		return 7 # 5 kind
	if numl == 2:
		if 4 in nums:
			return 6 # 4 kind
		else:
			return 5 # full house
	if 3 in nums:
		return 4 # 3 kind
	if 2 in nums:
		if nums.count(2) == 2:
			return 3 # 2 pair
		else:
			return 2 # 1 pair
	if numl == 5:
		return 1 # high card
		
	assert "Invalid return"

def part1():
	v = [(rank(c), c) for c in data]
	
	v = sorted(v)
	
	res = 0
	
	for i, v in enumerate(v):
		res += (i+1) * v[1][1]
	
	return res


def rank2(cards):
	js = []
	d = {}
	
	for i, c in enumerate(cards[0]):
		if c == 11:
			js.append(i)
			continue
		if c not in d:
			d[c] = 1
		else:
			d[c] += 1
	
	jsc = len(js)
	
	if jsc == 0:
		return rank(cards)
	
	if jsc == 5:
		return 7 # 5 kind
	if jsc == 4:
		return 7 # 5 kind

	
	nums = list(d.values())

	if jsc == 3:
		if 2 in nums:
			return 7 # 5 kind
		return 6 # 4 kind
	
	if jsc == 2:
		if 3 in nums:
			return 7 # 5 kind
		if 2 in nums:
			return 6 # 4 kind
		return 4 # 3 kind
		
	if jsc == 1:
		if 4 in nums:
			return 7 # 5 kind
		if 3 in nums:
			return 6 # 4 kind
		if 2 in nums:
			if nums.count(2) == 2:
				return 5 # full house
			return 4 # 3 kind
		return 2 # 1 pair

	assert "brute"


def part2():
	v = [(rank2(c), [[x if x!= 11 else 0 for x in c[0]], c[1]]) for c in data]
	
	v = sorted(v)
	
	res = 0
	
	for i, v in enumerate(v):
		res += (i+1) * v[1][1]
	
	return res


p1()
p2()
