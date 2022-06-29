# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day14.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile

key = parsefile(file_name, None)

from functools import reduce
from operator import xor


def calc_round(nums_, lengths, index=0, skip_size=0):
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


def calc_hash(key):
	lengths = list(map(ord, key))
	lengths.extend([17, 31, 73, 47, 23])
	nums = list(range(256))

	index = 0
	skip_size = 0
	for i in range(64):
		res = calc_round(nums, lengths, index, skip_size)
		nums = res[0]
		index = res[1]
		skip_size = res[2]

	dense = [reduce(xor, nums[i:i + 16]) for i in range(0, 256, 16)]

	h = "".join(hex(x)[2:].rjust(2, "0") for x in dense)
	return h


grid = None


def part1():
	global grid
	grid = [bin(int(calc_hash(key + "-" + str(i)), 16))[2:].rjust(128, "0") for i in range(128)]

	c = 0
	for r in grid:
		c += r.count("1")

	return c


def find_region(start):
	points = set()
	points.add(start)

	to_check = [start]

	while len(to_check) > 0:
		curr_pos = to_check[0]
		to_check.pop(0)
		# print(len(points), to_check)

		points.add(curr_pos)

		for y in range(-1, 2):
			new_y = curr_pos[1] + y
			if y != 0 and 0 <= new_y < 128:
				p = (curr_pos[0], new_y)
				if p not in points and grid[new_y][p[0]] == "1":
					to_check.append(p)

		for x in range(-1, 2):
			new_x = curr_pos[0] + x
			if x != 0 and 0 <= new_x < 128:
				p = (new_x, curr_pos[1])
				if p not in points and grid[p[1]][new_x] == "1":
					to_check.append(p)

	return points


def part2():
	positions = set()
	for y in range(128):
		for x in range(128):
			if grid[y][x] == "1":
				positions.add((x, y))

	region_count = 0

	while len(positions) > 0:
		curr_pos = list(positions)[0]

		r = find_region(curr_pos)

		positions.difference_update(r)
		region_count += 1

	return region_count


p1()
p2()
