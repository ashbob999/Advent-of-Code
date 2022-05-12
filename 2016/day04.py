# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day04.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file()
# @formatter:on

from utils import parsefile, parse

data = parsefile(file_name, [[[str, "-"], [str, 1, "]"], "["], "\n"])

text = """aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]"""

# data = parse(text, [[[str, "-"], [str, 1, "]"], "["], "\n"])

data = [["".join(d[0][:-1]), int(d[0][-1]), d[1][0], "-".join(d[0][:-1])] for d in data]


def check(code):
	counts = {}
	for c in code[0]:
		if c in counts:
			counts[c] += 1
		else:
			counts[c] = 1

	chars = [(count, ord('a') - ord(char)) for char, count in counts.items()]
	chars = sorted(chars, reverse=True)

	id = "".join([chr(ord('a') - c[1]) for c in chars[:5]])

	if id == code[2]:
		return True
	else:
		return False


correct_codes = []


def part1():
	s = 0

	for code in data:
		# print(code)
		if check(code):
			s += code[1]
			correct_codes.append(code)

	return s


def decrypt(code):
	chars = list(code[3])
	id = code[1]

	for i in range(len(chars)):
		if chars[i] == "-":
			chars[i] = " "
		else:
			index = ord(chars[i]) - ord("a")
			index += id
			index %= 26
			char = chr(ord("a") + index)
			chars[i] = char

	return "".join(chars)


def part2():
	for code in correct_codes:
		decrypted = decrypt(code)
		# print(decrypted)
		if "northpole" in decrypted:
			return code[1]


p1()
p2()
