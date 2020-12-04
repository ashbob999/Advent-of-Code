from aoc import get_input_file

input_text = get_input_file(session_path=["..", ".env"])

p1_count = 0
p2_count = 0

for r in input_text.to_gen(mf=str, sep="\n"):
	s = r.split(":")
	p = s[-1][1:]
	c = s[0][-1]

	i1 = int(s[0].split("-")[0])
	i2 = int(s[0][i1//10 +2:-2])

	p1_count += (i1 <= p.count(c) <= i2)
	p2_count += (p[i1-1] == c) ^ (p[i2-1] == c)


def part1():
	print(p1_count)


def part2():
	print(p2_count)


part1()
part2()
