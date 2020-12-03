from aoc import get_input_file

input_text = get_input_file(session_path=["..", ".env"])

data = input_text.to_list(sep="\n")

def part1():
	for i in range(0, len(data)):
		for j in range(i+1, len(data)):
			if data[i] + data[j] == 2020:
				return data[i] * data[j]


def part2():
	for i in range(0, len(data)):
		for j in range(i+1, len(data)):
			for k in range(j+1, len(data)):
				if data[i] + data[j] + data[k] == 2020:
					return data[i] * data[j] * data[k]


print(part1())
print(part2())
