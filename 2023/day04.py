# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day04.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

data = parsefile(file_name, [[[None, 1, int], [[int], "|"], ":"], "\n"])

def part1():
	sum = 0
	
	for card in data:
		nums = set(card[1][1])
		wins = set(card[1][0])
		match = nums & wins
		if len(match) > 0:
			sum += 1 << (len(match) -1)
		
	return sum


def part2():
	card_counts = [1] * len(data)
	
	for i in range(len(data)):
		card = data[i]
		nums = set(card[1][1])
		wins = set(card[1][0])
		match = nums & wins
		for i in range(len(match)):
			if card[0][0] + i < len(card_counts):
				card_counts[card[0][0]+ i] +=  card_counts[card[0][0]-1]
		
	return sum(card_counts)


p1()
p2()
