# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day24.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile

raw_ports = parsefile(file_name, [[int, "/"], "\n"])

ports = set()
for p in raw_ports:
	ports.add(tuple(sorted(p)))


def find_strongest(last_port_id, curr_strength, ports_left):
	max_strength = curr_strength

	next_ports = []

	for port in ports_left:
		next_port_id = None
		if port[0] == last_port_id:
			next_port_id = port[1]
		elif port[1] == last_port_id:
			next_port_id = port[0]
		else:
			continue

		next_ports.append([next_port_id, port])

	for np in next_ports:
		n_ports = ports_left.copy()
		n_ports.remove(np[1])
		strength = find_strongest(np[0], curr_strength + sum(np[1]), n_ports)

		max_strength = max(max_strength, strength)

	return max_strength


def part1():
	v = find_strongest(0, 0, ports.copy())
	return v


def find_longest(last_port_id, curr_length, curr_strength, ports_left):
	max_length = (curr_length, curr_strength)

	next_ports = []

	for port in ports_left:
		next_port_id = None
		if port[0] == last_port_id:
			next_port_id = port[1]
		elif port[1] == last_port_id:
			next_port_id = port[0]
		else:
			continue

		next_ports.append([next_port_id, port])

	for np in next_ports:
		n_ports = ports_left.copy()
		n_ports.remove(np[1])
		length = find_longest(np[0], curr_length + 1, curr_strength + sum(np[1]), n_ports)

		max_length = max(max_length, length)

	return max_length


def part2():
	v = find_longest(0, 0, 0, ports.copy())
	return v[1]


p1()
p2()
