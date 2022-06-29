# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day10.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile

lengths = parsefile(file_name, [int, ","])

nums = list(range(256))


def calc_hash(nums_, lengths, index=0, skip_size=0):
	nums = nums_[:]
	num_length = len(nums)

	for l in lengths:
		for ni in range(l // 2):
			i1 = (index + ni) % num_length
			i2 = (index + l - 1 - ni) % num_length

			tmp = nums[i1]
			nums[i1] = nums[i2]
			nums[i2] = tmp

		index += skip_size + l
		skip_size += 1

	return nums, index, skip_size


def part1():
	res = calc_hash(nums, lengths)
	return res[0][0] * res[0][1]


from functools import reduce
from operator import xor


def part2():
	global lengths, nums
	lengths = list(map(ord, ",".join(map(str, lengths))))
	lengths.extend([17, 31, 73, 47, 23])

	index = 0
	skip_size = 0
	for i in range(64):
		res = calc_hash(nums, lengths, index, skip_size)
		nums = res[0]
		index = res[1]
		skip_size = res[2]

	dense = [reduce(xor, nums[i:i + 16]) for i in range(0, 256, 16)]

	h = "".join(hex(x)[2:].rjust(2, "0") for x in dense)
	return h


p1()
p2()
