from typing import Callable
from os.path import isfile, join as path_join

file_name = path_join('input', 'day05.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file()

strings = open(file_name).read().strip().split("\n")


def part1():
	count = 0
	vowels = ("a", "e", "i", "o", "u")
	invalid = ("ab", "cd", "pq", "xy")
	for s in strings:
		match = [False, False, True]

		# contain 3 vowels
		vowel_count = 0
		for c in s:
			if c in vowels:
				vowel_count += 1
				if vowel_count >= 3:
					match[0] = True
					break

		if not match[0]:
			continue

		for i in range(len(s) - 1):
			# letter twice in a row
			if s[i] == s[i + 1]:
				match[1] = True

			# doesnt contain invalid strings
			if s[i:i + 2] in invalid:
				match[2] = False
				break

		if not match[2]:
			continue

		if not match[1]:
			continue

		count += 1

	return count


def part2():
	count = 0
	for s in strings:
		match1 = False
		match2 = False
		for i in range(len(s) - 2):
			if s[i] == s[i + 2]:
				match1 = True
				break

		if not match1:
			continue

		for i in range(len(s) - 3):
			for j in range(i + 2, len(s) - 1):
				if (s[i] == s[j]) and (s[i + 1] == s[j + 1]):
					match2 = True
					break

		if not match2:
			continue

		count += 1

	return count


print(part1())
print(part2())
