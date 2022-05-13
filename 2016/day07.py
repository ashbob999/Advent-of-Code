# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day07.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file()
# @formatter:on

from utils import parsefile

packets = parsefile(file_name, [[[str, "]"], "["], "\n"])

# flatten the list of lists
# odd indexes are hypernet sequences (contained by square brackets)
packets = [[ss for s in p for ss in s] for p in packets]


def check_abba(s):
	if len(s) < 4:
		return False
	for i in range(0, len(s) - 4 + 1):
		if s[i] != s[i + 1] and s[i] == s[i + 3] and s[i + 1] == s[i + 2]:
			return True

	return False


def part1():
	count = 0

	for p in packets:
		correct = False
		for i in range(len(p)):
			if check_abba(p[i]):
				# print(p[i])
				if i % 2 == 0:  # even
					correct = True
				else:  # odd
					correct = False
					break

		if correct:
			count += 1

	return count


def check_aba(s):
	if len(s) < 3:
		return []
	found = []

	for i in range(0, len(s) - 3 + 1):
		if s[i] == s[i + 2] and s[i] != s[i + 1]:
			found.append(s[i:i + 3])

	return found


def part2():
	count = 0

	for p in packets:
		correct = False
		abas = set()
		for i in range(0, len(p), 2):
			for aba in check_aba(p[i]):
				abas.add(aba)

		for aba in abas:
			bab = aba[1] + aba[0] + aba[1]
			for i in range(1, len(p), 2):
				babs = check_aba(p[i])
				if bab in babs:
					correct = True
					break

			if correct:
				break

		if correct:
			count += 1

	return count


p1()
p2()
