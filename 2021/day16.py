from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day16.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])

from utils import parsefile

data = parsefile(file_name, None)

binary = bin(int(data, 16))[2:]

if len(binary) % 4 != 0:
	diff = 4 - len(binary) % 4
	binary = binary.rjust(len(binary) + diff, "0")

def decode(binary):
	version = int(binary[:3], 2)
	type_id = int(binary[3:6], 2)
	chars_read = 3 + 3

	if type_id == 4: # literal value
		value_str = binary[6:]
		bin_str = ""
		i = 0
		while i < len(value_str):
			bin_str += value_str[i+1:i+5]
			chars_read += 5

			if value_str[i] == "0":
				break
				
			i += 5
		
		value = int(bin_str, 2)
		
		return (version, type_id, value, chars_read)
		
	else:
		length_id = int(binary[6:7], 2)
		chars_read += 1
		
		if length_id == 0:
			sub_length = int(binary[7:7+15], 2)
			chars_read += 15
			sub_str = binary[7+15:]
			
			subs = []
			i = 0
			while i < sub_length:
				sub = decode(sub_str[i:])
				subs.append(sub)
				i += sub[-1]
				chars_read += sub[-1]
			
			return (version, type_id, sub_length, subs, chars_read)
		else:
			sub_count = int(binary[7:7+11], 2)
			chars_read += 11
			sub_str = binary[7+11:]
			
			subs = []
			
			i = 0
			
			for c in range(sub_count):
				sub = decode(sub_str[i:])
				subs.append(sub)
				i += sub[-1]
				chars_read += sub[-1]
				
			return (version, type_id, sub_count, subs, chars_read)

decoded = decode(binary)


def part1(decoded):
	if (decoded[1] == 4):
		return decoded[0]
	else:
		s = decoded[0]
		for sub in decoded[3]:
			s += part1(sub)

		return s

from math import prod

def part2(decoded):
	id = decoded[1]
	if id == 4:
		return decoded[2]
	elif id == 0:
		return sum(part2(sub) for sub in decoded[3])
	elif id == 1:
		return prod(part2(sub) for sub in decoded[3])
	elif id == 2:
		return min(part2(sub) for sub in decoded[3])
	elif id == 3:
		return max(part2(sub) for sub in decoded[3])
	elif id == 5:
		return 1 if part2(decoded[3][0]) > part2(decoded[3][1]) else 0
	elif id == 6:
		return 1 if part2(decoded[3][0]) < part2(decoded[3][1]) else 0
	elif id == 7:
		return 1 if part2(decoded[3][0]) == part2(decoded[3][1]) else 0


p1(decoded)
p2(decoded)
