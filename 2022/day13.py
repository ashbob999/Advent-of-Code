# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day13.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile

data = parsefile(file_name, [[str, "\n"], "\n\n"])

packets = []

for d in data:
	pack1 = eval(d[0])
	pack2 = eval(d[1])
	
	packets.append((pack1, pack2))

def check(pack1, pack2):
	for i in range(len(pack1)):
		# right is smaller
		if i >= len(pack2):
			return False
			
		# both ints
		if isinstance(pack1[i], int) and isinstance(pack2[i], int):
			if pack1[i] == pack2[i]:
				continue
			else:
				return pack1[i] < pack2[i]
				
		# both lists
		if isinstance(pack1[i], list) and isinstance(pack2[i], list):
			if pack1[i] == pack2[i]:
				continue
			else:
				return check(pack1[i], pack2[i])
				
		# left list, right int
		if isinstance(pack1[i], int) and isinstance(pack2[i], list):
			v1 = [pack1[i]]
			if v1 == pack2[i]:
				continue
			else:
				return check(v1, pack2[i])
				
		# left int, right list
		if isinstance(pack1[i], list) and isinstance(pack2[i], int):
			v2 = [pack2[i]]
			if pack1[i] == v2:
				continue
			else:
				return check(pack1[i], v2)
				
	return True


def part1():
	s=0
	for i, packet in enumerate(packets):
		if check(*packet):
			s+= i+1
	return s

def cmp(pack1, pack2):
	if check(pack1, pack2):
		return -1
	else:
		return 1

from functools import cmp_to_key

def part2():
	packs = []
	for packet in packets:
		packs.append(packet[0])
		packs.append(packet[1])
	packs.append([[2]])
	packs.append([[6]])
	
	packs = sorted(packs, key=cmp_to_key(cmp))
	
	i1 = packs.index([[2]]) +1
	i2 = packs.index([[6]]) +1
	
	return i1 * i2


p1()
p2()
