from aoc import get_input_file

input_text = get_input_file(session_path=["..", ".env"])

#data = input_text.to_list(mf=str,sep="\n")
data = input_text.text.split("\n")

def part1(dx, dy):
	trees = 0
	start = [0,0]
	while start[1] < len(data) - 2:
		start[0] += dx
		start[0] %= len(data[1])
		start[1] += dy

		if data[start[1]][start[0]] == "#":
			trees += 1

	return trees


def part2(one):
	v = one
	v *= part1(1,1)
	v *= part1(5,1)
	v *= part1(7,1)
	v *= part1(1,2)

	print(v)


one = part1(3,1)
print(one)
part2(one)
