# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day10.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file()
# @formatter:on

from utils import parsefile
from copy import deepcopy

data = parsefile(file_name, [[" "], "\n"])

instr = []

inputs_og = {}
outputs_og = {}
bots_og = {}

targets_og = sorted([61, 17])

for ins in data:
	if ins[0] == "bot":  # transfer
		bot_source = int(ins[1])
		bot_low = int(ins[6])
		low_out = ins[5] == "output"
		bot_high = int(ins[11])
		high_out = ins[10] == "output"

		instr.append((1, bot_source, (low_out, bot_low), (high_out, bot_high)))
		bots_og[bot_source] = [(low_out, bot_low), (high_out, bot_high), []]
	else:  # store
		value = int(ins[1])
		bot = int(ins[5])
		instr.append((0, value, bot))
		if bot in inputs_og:
			inputs_og[bot].append(value)
		else:
			inputs_og[bot] = [value]


def solve(bots, inputs, outputs, check_values=False, targets=None):
	# do initial inputs
	for bot, value in inputs.items():
		bots[bot][2] += value

	# keep going till match or all bots done
	while len(bots) > 0:
		# loop over bots
		for bot_id in list(bots.keys()):
			bot = bots[bot_id]
			# check if bot has 2 values
			if len(bot[2]) == 2:
				# do transfer
				values = sorted(bot[2])

				# check compare values
				if check_values and values[0] == targets[0] and values[1] == targets[1]:
					return bot_id

				# handle low
				if bot[0][0]:  # output
					outputs[bot[0][1]] = values[0]
				else:
					bots[bot[0][1]][2].append(values[0])

				# handle high
				if bot[1][0]:  # output
					outputs[bot[1][1]] = values[1]
				else:
					bots[bot[1][1]][2].append(values[1])

				# remove bot
				bots.pop(bot_id)


def part1():
	inputs = deepcopy(inputs_og)
	outputs = deepcopy(outputs_og)
	bots = deepcopy(bots_og)
	id = solve(bots, inputs, outputs, True, targets_og)
	return id


def part2():
	inputs = deepcopy(inputs_og)
	outputs = deepcopy(outputs_og)
	bots = deepcopy(bots_og)
	id = solve(bots, inputs, outputs, False)
	return outputs[0] * outputs[1] * outputs[2]


p1()
p2()
