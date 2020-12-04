from aoc import get_input_file
import re

input_text = get_input_file(session_path=['..', '.env'])

data = input_text.to_list(mf=str, sep="\n\n")

req = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]

check = {
	"byr": lambda x: len(x) == 4 and 1920 <= int(x) <= 2002,
	"iyr": lambda x: len(x) == 4 and 2010 <= int(x) <= 2020,
	"eyr": lambda x: len(x) == 4 and 2020 <= int(x) <= 2030,
	"hgt": lambda x: (150 <= int(x[:-2]) <= 193) if x[-2:] == "cm" else ((59 <= int(x[:-2]) <= 76) if x[-2:] == "in" else False),
	"hcl": lambda x: re.fullmatch("#[0-9a-f]{6}", x),
	"ecl": lambda x: x in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"],
	"pid": lambda x: re.fullmatch("[0-9]{9}", x)
}

p1 = 0
p2 = 0

for p in data:
	p = p.replace("\n", " ")

	d = {e.split(":")[0]: e.split(":")[1] for e in p.split(" ") if e}

	if len(d) >= 7:
		f = True
		f2 = True
		for r in req:
			if r not in d:
				f = False
				break
			if r != "cid" and not check[r](d[r]):
				f2 = False

		if f:
			p1 += 1
			if f2:
				p2 += 1


def part1():
	print(p1)

def part2():
	print(p2)

part1()
part2()
