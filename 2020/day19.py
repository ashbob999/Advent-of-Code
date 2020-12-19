from typing import Callable
from os.path import isfile, join as path_join
file_name = path_join('input', 'day19.txt')
def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])

#import re
import regex as re

data = to_list(mf=str, sep="\n\n")

rules = {int(x.split(":")[0]): x.split(":")[1].replace("\"", "") for x in data[0].split("\n")}

for i in rules.keys():
	if "|" in rules[i]:
		rules[i] = " ( " + rules[i].replace("|", " )|( ") + " ) "

messages = data[1].split("\n")

numbers = set("0123456789")


def part1():
	rule0 = rules[0] + " "

	#while set(rule0) & numbers:
	#	rule0 = re.sub(" \d+", rep, rule0)

	while set(rule0) & numbers:
		vals = rule0.split(" ")
		for i in range(len(vals)):
			if vals[i].isdigit():
				vals[i] = " ( " + rules[int(vals[i])] + " ) "

		rule0 = " ".join(vals)

	rule0 = rule0.replace(" ", "")

	rule0 = "^(" + rule0 + ")$"

	reg = re.compile(rule0, re.MULTILINE)

	"""
	matched = 0
	for msg in messages:
		if reg.match(msg):
			matched += 1

	print(matched)
	"""
	print(len(reg.findall(data[1])))

def expand(i):
	rule = rules[i]
	while set(rule) & numbers:
		vals = rule.split(" ")
		for i in range(len(vals)):
			if vals[i].isdigit():
				vals[i] = " ( " + rules[int(vals[i])] + " ) "

		rule = " ".join(vals)

	return rule

def part2():
	rule0 = rules[0] + " "

	r1 = " 42 | 42 8"
	reg1 = " (( 42 )+ ) "

	r2 = " 42 31 | 42 11 31"
	reg2 = " (?P<rec> 42 (?&rec)* 31 ) "

	rules[42] = expand(42)
	rules[31] = expand(31)

	rules[8] = reg1
	rules[11] = reg2

	while set(rule0) & numbers:
		vals = rule0.split(" ")
		for i in range(len(vals)):
			if vals[i].isdigit():
				vals[i] = " ( " + rules[int(vals[i])] + " ) "

		rule0 = " ".join(vals)

	rule0 = rule0.replace(" ", "")

	rule0 = "^(" + rule0 + ")$"

	reg = re.compile(rule0, re.MULTILINE)

	"""
	matched = 0
	for msg in messages:
		if reg.match(msg):
			matched += 1

	print(matched)
	"""
	print(len(reg.findall(data[1])))


part1()
part2()
