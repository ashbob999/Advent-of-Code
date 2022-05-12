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
	get_input_file()
# @formatter:on

from utils import parsefile

puzzle_input = parsefile(file_name, str)[0]

import hashlib


def check_hash(key, number, number_of_zeroes):
	full_key = key + str(number)
	result = hashlib.md5(full_key.encode())
	hash = result.hexdigest()

	if hash[:number_of_zeroes] == "0" * number_of_zeroes:
		return True, hash
	return False, hash


def part1():
	found = 0
	number = 0
	password = ""

	while found < 8:
		res = check_hash(puzzle_input, number, 5)
		if res[0]:
			password += res[1][5]
			found += 1
		number += 1

	return password


def part2():
	found = 0
	number = 0
	password = ["-"] * 8

	while found < 8:
		res = check_hash(puzzle_input, number, 5)
		if res[0]:
			pos = res[1][5]
			if "0" <= pos <= "7":
				pos_ = int(pos)
				if password[pos_] == "-":
					password[pos_] = res[1][6]
					found += 1
		number += 1

	return "".join(password)


p1()
p2()
