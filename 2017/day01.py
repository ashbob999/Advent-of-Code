# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day01.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file()
# @formatter:on

from utils import parsefile

nums = parsefile(file_name, [int, ""])


# take an input list of numbers and return the sum of all numbers that are the same as the next number, given that the list is circular
def circular_sum(nums):
	sum = 0
	for i in range(len(nums)):
		if nums[i] == nums[(i + 1) % len(nums)]:
			sum += nums[i]
	return sum


def part1():
	return circular_sum(nums)


# take an input list of numbers and return the sum of all numbers that are the same as the number halfway around the list, given that the list is circular
def circular_sum_halfway(nums):
	sum = 0
	for i in range(len(nums)):
		if nums[i] == nums[(i + len(nums) // 2) % len(nums)]:
			sum += nums[i]
	return sum


def part2():
	return circular_sum_halfway(nums)


p1()
p2()
