# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day06.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file()
# @formatter:on

from utils import parsefile

data = parsefile(file_name, [[""], "\n"])


def part1():
	message_columns = list(zip(*data))

	correct_message = ["-"] * len(data[0])

	for i in range(len(data[0])):
		freq = {}
		for c in message_columns[i]:
			if c in freq:
				freq[c] += 1
			else:
				freq[c] = 1

		most_freq = sorted(list(freq.items()), key=lambda x: x[1], reverse=True)[0][0]
		correct_message[i] = most_freq

	return "".join(correct_message)


def part2():
	message_columns = list(zip(*data))

	correct_message = ["-"] * len(data[0])

	for i in range(len(data[0])):
		freq = {}
		for c in message_columns[i]:
			if c in freq:
				freq[c] += 1
			else:
				freq[c] = 1

		most_freq = sorted(list(freq.items()), key=lambda x: x[1])[0][0]
		correct_message[i] = most_freq

	return "".join(correct_message)


p1()
p2()
