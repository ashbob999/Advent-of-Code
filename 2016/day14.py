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
	get_input_file()
# @formatter:on

from utils import parsefile

salt = parsefile(file_name, None)

from hashlib import md5

mem_hash = {}


def get_hash(salt, number):
	if number in mem_hash:
		return mem_hash[number]

	full_text = salt + str(number)
	result = md5(full_text.encode())
	hash = result.hexdigest()

	mem_hash[number] = hash
	return hash


def check_n(s, n):
	for i in range(0, len(s) - n + 1):
		c = s[i]
		if all(s[i + j] == c for j in range(1, n)):
			return True, c
	return False, ""


def check_match(s, n, c):
	for i in range(0, len(s) - n + 1):
		if all(s[i + j] == c for j in range(0, n)):
			return True
	return False


def is_key(salt, number, hs):
	hash = hs(salt, number)

	# contain 3 characters in a row
	res = check_n(hash, 3)
	if res[0]:
		# check next 1000 hashes
		for n in range(1, 1000 + 1):
			h = hs(salt, number + n)
			c = check_match(h, 5, res[1])
			if c:
				return True

	return False


def part1():
	i = 0
	key_count = 0

	while True:
		if is_key(salt, i, get_hash):
			key_count += 1

		if key_count == 64:
			break

		i += 1

	return i


mem_hash2 = {}


def get_hash2(salt, number):
	if number in mem_hash2:
		return mem_hash2[number]

	full_text = salt + str(number)
	for i in range(2016 + 1):
		result = md5(full_text.encode())
		full_text = result.hexdigest()

	mem_hash2[number] = full_text
	return full_text


def part2():
	i = 0
	key_count = 0

	while True:
		if is_key(salt, i, get_hash2):
			key_count += 1

		if key_count == 64:
			break

		i += 1

	return i


p1()
p2()
