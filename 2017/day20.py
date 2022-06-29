# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day20.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile

raw_particles = parsefile(file_name, [[str, ", "], "\n"])

particles = []
for p in raw_particles:
	part = []
	for d in p:
		values = list(map(int, d[3:-1].split(",")))
		part.append(values)

	particles.append(part)


def tick(particles):
	for p in particles:
		# increase velocity
		for axis in range(3):
			p[1][axis] += p[2][axis]

		# increase position
		for axis in range(3):
			p[0][axis] += p[1][axis]


def part_sort(p):
	abs_a = abs(p[2][0]) + abs(p[2][1]) + abs(p[2][2])
	abs_v = abs(p[1][0]) + abs(p[1][1]) + abs(p[1][2])
	abs_p = abs(p[0][0]) + abs(p[0][1]) + abs(p[0][2])
	return abs_a, abs_v, abs_p


def part1():
	parts = sorted(particles, key=part_sort)
	index = particles.index(parts[0])
	return index


def part2():
	parts = [[v[:] for v in p] for p in particles]
	c = 0
	last_count = None
	check_every = 100

	while True:
		tick(parts)
		new_parts = []
		for i in range(len(parts)):
			fp = parts[i][0]
			collided = False

			for j in range(len(parts)):
				if i == j:
					continue
				if parts[j][0] == fp:
					collided = True
					break

			if not collided:
				new_parts.append(parts[i])

		parts = new_parts
		if c % check_every == 0:
			if last_count == len(new_parts) and last_count < len(particles):
				return last_count

		last_count = len(new_parts)

		c += 1


p1()
p2()
