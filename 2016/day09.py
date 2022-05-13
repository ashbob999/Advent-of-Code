# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day09.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file()
# @formatter:on

from utils import parsefile

file_contents = parsefile(file_name, None)


def decompress(text):
	decompressed_text = ""

	i = 0
	length = len(text)
	while i < length:
		# print(i, length)
		if "A" <= text[i] <= "Z":
			decompressed_text += text[i]
			i += 1
		elif text[i] == "(":
			# find next )
			end_index = i
			while text[end_index] != ")":
				end_index += 1

			marker = text[i + 1:end_index].split("x")
			count = int(marker[0])
			times = int(marker[1])
			i += end_index - i + 1
			decompressed_text += text[i:i + count] * times
			i += count
		else:
			i += 1

	return decompressed_text


def part1():
	s = decompress(file_contents)
	return len(s)


def decompress_2(text):
	char_count = 0
	sub_sections = []

	i = 0
	length = len(text)
	while i < length:
		if "A" <= text[i] <= "Z":
			char_count += 1
			i += 1
		elif text[i] == "(":
			# find next )
			end_index = i
			while text[end_index] != ")":
				end_index += 1

			marker = text[i + 1:end_index].split("x")
			count = int(marker[0])
			times = int(marker[1])
			i += end_index - i + 1
			sub_sections.append([text[i:i + count], times])
			i += count
		else:
			i += 1

	for sub in sub_sections:
		char_count += decompress_2(sub[0]) * sub[1]

	return char_count


def part2():
	l = decompress_2(file_contents)
	return l


p1()
p2()
