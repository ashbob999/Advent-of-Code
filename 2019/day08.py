from typing import Callable
from os.path import isfile, join as path_join

file_name = path_join('input', 'day08.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file()

pixels = list(map(int, list(open(file_name).read().strip())))


def chunks(l, n):
	n = max(1, n)
	return [l[i:i + n] for i in range(0, len(l), n)]


w = 25
h = 6
length = len(pixels)

layers = chunks(pixels, w * h)

layer_num = -1
fewest_zeros = 100000000

for i, layer in enumerate(layers):
	zero_count = 0
	for num in layer:
		if num == 0:
			zero_count += 1

	if zero_count < fewest_zeros:
		fewest_zeros = zero_count
		layer_num = i


def part1():
	num_1_mult_2 = layers[layer_num].count(1) * layers[layer_num].count(2)
	return num_1_mult_2


def part2():
	final_layer = [0] * (w * h)

	for i in range(len(final_layer)):
		for layer in layers:
			if layer[i] != 2:
				final_layer[i] = layer[i]
				break

	for r in chunks(final_layer, w):
		print("".join(str(e) for e in r).replace("0", " ").replace("1", "\u2588"))


print(part1())
part2()
