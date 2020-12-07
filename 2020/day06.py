"""from aoc import get_input_file

input_text = get_input_file(session_path=['..', '.env'])

data = input_text.to_list(mf=str, sep="\n\n")
"""

def gif(mf=int, sep=","):
	return [mf(x) for x in open("input/day06.txt").read().split(sep) if x]

data = gif(mf=str, sep="\n\n")

s1 = 0
s2 = 0

for g in data:#input_text.to_gen(mf=str, sep="\n\n"):
	ps = [x for x in g.split("\n") if x]

	set1 = set(ps[0])
	set2 = set(ps[0])
	for p in ps[1:]:
		set1.update(p)
		set2 &= set(p)

	s1 += len(set1)
	s2 += len(set2)


def part1():
	print(s1)

def part2():
	print(s2)


part1()
part2()
