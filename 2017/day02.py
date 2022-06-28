# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day02.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file()
# @formatter:on

from utils import parsefile

nums = parsefile(file_name, [[int], "\n"])


# calculate the sum of the difference between the min and max number in each row of a 2d list
def row_sum_diff(nums):
	sum = 0
	for row in nums:
		sum += max(row) - min(row)
	return sum


def part1():
	return row_sum_diff(nums)


# for each row sort them in reverse order
# then find the only 2 values that are evenly divisible by each other
# return the sum of these values divided by each other
def evenly_divisible(nums):
	sum = 0
	for row in nums:
		row.sort(reverse=True)
		for i in range(len(row)):
			for j in range(i + 1, len(row)):
				if row[i] % row[j] == 0:
					sum += row[i] // row[j]
					break
	return sum


def part2():
	return evenly_divisible(nums)


p1()
p2()
