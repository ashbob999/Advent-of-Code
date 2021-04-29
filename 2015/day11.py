from typing import Callable
from os.path import isfile, join as path_join

file_name = path_join('input', 'day11.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file()

old_password = open(file_name).read().strip()

inc = {"a": "b", "b": "c", "c": "d", "d": "e", "e": "f", "f": "g", "g": "h", "h": "i", "i": "j", "j": "k",
       "k": "l", "l": "m", "m": "n", "n": "o", "o": "p", "p": "q", "q": "r", "r": "s", "s": "t", "t": "u",
       "u": "v", "v": "w", "w": "x", "x": "y", "y": "z", "z": "a"}


def next(password, size):
	if password[-1] == 'z':  # overflow
		i = size - 1
		overflow = True
		while overflow and i >= 0:
			password[i] = 'a'
			i -= 1
			overflow = (password[i] == 'z')
			if not overflow:
				password[i] = inc[password[i]]
	else:
		password[-1] = inc[password[-1]]

	return password


def part1(password):
	new_pass = list(password)
	size = len(password)

	while True:
		new_pass = next(new_pass, size)

		# not contain i, o, l
		if "i" in new_pass or "o" in new_pass or "l" in new_pass:
			continue

		# increasing straight of 3 letters
		has_straight = False
		for i in range(size - 2):
			c1 = new_pass[i]
			c2 = inc[c1]
			c3 = inc[c2]

			if new_pass[i + 1] == c2 and new_pass[i + 2] == c3:
				has_straight = True
				break

		if not has_straight:
			continue

		# 2 different pairs
		def check_pairs():
			has_pairs = False
			for i in range(size - 2):
				if new_pass[i] == new_pass[i + 1]:
					pair1 = new_pass[i]
					for j in range(i + 2, size - 1):
						if new_pass[j] != pair1 and new_pass[j] == new_pass[j + 1]:
							return True
			return False

		if not check_pairs():
			continue

		return "".join(new_pass)


def part2(p):
	return part1(p)


p = part1(old_password)
print(p)
print(part2(p))
