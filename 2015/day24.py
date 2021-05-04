from typing import Callable
from os.path import isfile, join as path_join

file_name = path_join('input', 'day24.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file()

from math import prod

packages = list(map(int, open(file_name).read().strip().split("\n")))
packages = sorted(packages, reverse=True)

# bin_match = {packages[i]: 1 << i for i in range(len(packages))}
bin_match_i = [1 << i for i in range(len(packages))]


def bin_to_arr(n):
	arr = set()
	i = 0
	while n:
		if n & 1:
			arr.add(packages[i])
		i += 1
		n >>= 1

	return arr


package_bin = (1 << len(packages)) - 1
package_length = len(packages)


def get_sums(s, i, max_sum, used_conts: int, matches):
	if i >= package_length:
		return

	get_sums(s, i + 1, max_sum, used_conts, matches)

	if s + packages[i] < max_sum:
		get_sums(s + packages[i], i + 1, max_sum, used_conts | bin_match_i[i], matches)
	elif s + packages[i] == max_sum:
		matches.append(used_conts | bin_match_i[i])


def sort_key(x):
	arr = bin_to_arr(x)
	return len(arr), prod(arr)


def part1():
	matches = []
	group_weight = sum(packages) // 3
	get_sums(0, 0, group_weight, 0, matches)

	matches = sorted(matches, key=sort_key)
	matches_length = len(matches)

	for i in range(matches_length - 1):
		m1 = matches[i]
		for j in range(i + 1, matches_length):
			m2 = matches[j]
			if not m1 & m2:
				m3 = (m1 | m2) ^ package_bin
				if sum(bin_to_arr(m3)) == group_weight:
					return prod(bin_to_arr(m1))


def part2():
	matches = []
	group_weight = sum(packages) // 4
	get_sums(0, 0, group_weight, 0, matches)

	matches = sorted(matches, key=sort_key)
	matches_length = len(matches)

	for i in range(matches_length - 2):
		m1 = matches[i]
		for j in range(i + 1, matches_length - 1):
			m2 = matches[j]
			for k in range(j + 1, matches_length):
				m3 = matches[k]
				if not m1 & m2 and not m1 & m3 and not m2 & m3:
					m4 = (m1 | m2 | m3) ^ package_bin
					if sum(bin_to_arr(m4)) == group_weight:
						return prod(bin_to_arr(m1))


print(part1())
print(part2())
