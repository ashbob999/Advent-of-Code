from typing import Callable
from os.path import isfile, join as path_join
file_name = path_join('input', 'day14.txt')
def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file()

lines = open(file_name).read().strip().split("\n")

class Reaction:
	def __init__(self, reaction):
		l = reaction.split("=>")
		inputs_str = l[0].strip().split(",")
		result_ = l[1].strip().split(" ")

		self.result = {result_[1]: int(result_[0])}

		inputs_ = [i_.strip().split(" ") for i_ in inputs_str]
		self.inputs = {i[1].strip(): int(i[0].strip()) for i in inputs_}

	def get_res(self):
		return list(self.result.keys())[0]

	def get_amount(self):
		return list(self.result.values())[0]


reactions = {}

for line in lines:
	r = Reaction(line)
	reactions[list(r.result.keys())[0]] = r


def gcd(a, b):
	while b > 0:
		a, b = b, a % b
	return a


def lcm(a, b):
	return a * b // gcd(a, b)


final_reaction = reactions["FUEL"]

ore_outputs = []

for r in reactions.values():
	if list(r.inputs.keys())[0] == "ORE":
		ore_outputs.append(r.get_res())


def get_ore_for_fuel(amount):
	amounts = {"FUEL": amount}
	excess_amount = {"FUEL": 0}

	def check_lists():
		a = set(amounts.keys())
		b = set(ore_outputs)
		return a == b

	while not check_lists():
		amount_copy = amounts.copy()
		for ore_result in ore_outputs:
			amount_copy.pop(ore_result, None)

		first_craft = list(amount_copy.keys())[0]
		amount_of_item = amount_copy[first_craft]
		excess_crafts = excess_amount.get(first_craft, 0)

		amount_needed = amount_of_item - excess_crafts
		# print(amount_needed)

		craft_item = reactions[first_craft]

		amounts.pop(first_craft, None)

		if amount_needed > 0:

			if amount_needed % craft_item.get_amount() == 0:
				lowest_amount = amount_needed
				lowest_craft_num = amount_needed // craft_item.get_amount()
				excess_craft = 0
			else:
				lowest_craft_num = (amount_needed // craft_item.get_amount()) + 1
				lowest_amount = lowest_craft_num * craft_item.get_amount()
				excess_craft = lowest_amount - amount_needed

			excess_amount[first_craft] = excess_craft

			for ing, amt in craft_item.inputs.items():
				if ing in amounts:
					amounts[ing] = amounts[ing] + amt * lowest_craft_num
				else:
					amounts[ing] = amt * lowest_craft_num
		else:
			excess_amount[first_craft] = 0

	total_ore = 0

	for item, amount in amounts.items():
		craft_item = reactions[item]

		if amount % craft_item.get_amount() == 0:
			amount_of_crafts = amount // craft_item.get_amount()
		else:
			amount_of_crafts = (amount // craft_item.get_amount()) + 1
		ore_needed = list(craft_item.inputs.values())[0] * amount_of_crafts

		total_ore += ore_needed

	return total_ore


def part1():
	ore_1_fuel = get_ore_for_fuel(1)
	return ore_1_fuel


def part2(ore_1_fuel):
	ore_trillion = 1000000000000

	average_fuel = ore_trillion // ore_1_fuel

	average_ore = get_ore_for_fuel(average_fuel)

	total_fuel = average_fuel

	while get_ore_for_fuel(total_fuel) < ore_trillion:
		total_fuel += 1000

	while get_ore_for_fuel(total_fuel) > ore_trillion:
		total_fuel -= 1
		
	return total_fuel


ore_1_fuel = part1()
print(ore_1_fuel)
print(part2(ore_1_fuel))
