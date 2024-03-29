from typing import Callable
from os.path import isfile, join as path_join

file_name = path_join('input', 'day16.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file()

input_num = open(file_name).read().strip()

default = [0, 1, 0, -1]

shifted_mem = {}


def get_phase(num):
	if num in shifted_mem:
		return shifted_mem[num]
	shifted = ([0] * num) + ([1] * num) + ([0] * num) + ([-1] * num)
	shifted.append(shifted.pop(0))

	shifted_mem[num] = shifted
	return shifted


def get_output(inp_str_, times):
	inp_str = inp_str_.copy()
	length = len(inp_str)

	for t_ in range(times):
		output_values = [0] * length

		for i in range(length):
			phase = get_phase(i + 1)
			phase_len = (i + 1) * 4

			total = 0

			for n in range(length):
				n_ = n % phase_len

				total += inp_str[n] * phase[n_]

			output_values[i] = abs(total) % 10

		inp_str = output_values.copy()

	return inp_str


def part1():
	out_list = list(map(int, list(input_num)))

	prev_output = get_output(out_list, 100)

	value = "".join(map(str, prev_output[:8]))

	return value


def get_fft_v2(signal_, times):
	signal = signal_.copy()
	length = len(signal) - 1
	last_num = signal[-1]

	for i in range(times):
		total = last_num

		for j in reversed(range(length)):
			total += signal[j]
			signal[j] = total % 10

	return signal


def part2():
	input_num_big = input_num * 10000

	offset = int(input_num_big[:7])

	input_sliced = input_num_big[offset:]

	output = list(map(int, list(input_sliced)))

	output = get_fft_v2(output, 100)

	message = "".join(map(str, output[:8]))

	return message


print(part1())
print(part2())
