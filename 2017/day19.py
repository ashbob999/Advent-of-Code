# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day19.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile

grid = parsefile(file_name, [str, "\n"], strip=False)

width = len(grid[0])
height = len(grid)

# dirs: 0: up, 1: right, 2: down, 3: left
adj = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def solve():
	steps = 1
	start_pos = [grid[0].index("|"), 0]
	dir = 2  # down

	found_chars = []

	curr_pos = start_pos

	while True:
		if dir == 0:  # up
			next_pos = [curr_pos[0], curr_pos[1] - 1]
		elif dir == 1:  # right
			next_pos = [curr_pos[0] + 1, curr_pos[1]]
		elif dir == 2:  # down
			next_pos = [curr_pos[0], curr_pos[1] + 1]
		elif dir == 3:  # left
			next_pos = [curr_pos[0] - 1, curr_pos[1]]

		if 0 <= next_pos[0] < width and 0 <= next_pos[1] < height:
			c = grid[next_pos[1]][next_pos[0]]

			if c == "|":  # vertical
				curr_pos = next_pos
				steps += 1
			elif c == "-":  # horizontal
				curr_pos = next_pos
				steps += 1
			elif c == "+":  # change dir
				dirs = []
				next_poses = []

				for i, ad in enumerate(adj):
					np = [next_pos[0] + ad[0], next_pos[1] + ad[1]]
					if 0 <= np[0] < width and 0 <= np[1] < height and np != curr_pos and grid[np[1]][np[0]] != " ":
						next_poses.append(np)
						dirs.append(i)

				if len(next_poses) > 1:
					print("error, multiple nextposses")
					return "ERROR"

				curr_pos = next_pos
				dir = dirs[0]
				steps += 1

			elif "A" <= c <= "Z":
				found_chars.append(c)
				curr_pos = next_pos
				steps += 1
			else:  # end of path
				break
		else:  # out of grid
			break

	return "".join(found_chars), steps


res = solve()


def part1():
	return res[0]


def part2():
	return res[1]


p1()
p2()
