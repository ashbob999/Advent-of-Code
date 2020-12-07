from os.path import isfile

if not isfile("input/day01.txt"):
	from aoc import get_input_file

	input_text = get_input_file(session_path=["..", ".env"])

	data = input_text.to_list(sep="\n")


data = (int(x) for x in open("input/day01.txt").read().split("\n") if x)

data = sorted(data)

s = set(data)

def part1():
	for v1 in data:
		rem = 2020 - v1
		if rem in s:
			return v1 * rem


def part2():
	for i in range(0, len(data)):
		for j in range(i+1, len(data)):
			rem = 2020 - data[i] - data[j]
			if rem in s:
				return data[i] * data[j] * rem


print(part1())
print(part2())
