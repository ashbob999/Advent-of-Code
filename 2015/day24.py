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

package_set = set(packages)
package_length = len(packages)

matches_p1 = []
matches_p2 = []


def get_sums(s, i, max_sum, used_conts, matches):
	if i >= package_length:
		return

	get_sums(s, i + 1, max_sum, used_conts.copy(), matches)

	# tmp = used_conts.copy()
	# tmp.add(packages[i])
	if s + packages[i] < max_sum:
		get_sums(s + packages[i], i + 1, max_sum, used_conts + [packages[i]], matches)
	elif s + packages[i] == max_sum:
		matches.append(used_conts + [packages[i]])


def part1():
	matches = []
	group_weight = sum(packages) // 3
	get_sums(0, 0, group_weight, [], matches)

	matches = sorted(matches, key=lambda x: (len(x), prod(x)))
	matches_length = len(matches)

	for i in range(matches_length - 1):
		m1 = set(matches[i])
		for j in range(i + 1, matches_length):
			m2 = set(matches[j])
			if not m1 & m2:
				m3 = (m1 | m2) ^ package_set
				if sum(m3) == group_weight:
					return prod(m1)


def part2():
	matches = []
	group_weight = sum(packages) // 4
	get_sums(0, 0, group_weight, [], matches)

	matches = sorted(matches, key=lambda x: (len(x), prod(x)))
	matches_length = len(matches)

	for i in range(matches_length - 2):
		m1 = set(matches[i])
		for j in range(i + 1, matches_length - 1):
			m2 = set(matches[j])
			for k in range(j + 1, matches_length):
				m3 = set(matches[k])
				if not m1 & m2 and not m1 & m3 and not m2 & m3:
					m4 = (m1 | m2 | m3) ^ package_set
					if sum(m4) == group_weight:
						return prod(m1)


print(part1())
print(part2())
