from typing import Callable
from os.path import isfile, join as path_join

file_name = path_join('input', 'day21.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file()

weapons = [("Dagger", 8, 4, 0),
           ("Shortsword", 10, 5, 0),
           ("Warhammer", 25, 6, 0),
           ("Longsword", 40, 7, 0),
           ("Greataxe", 74, 8, 0)]

armour = [("None", 0, 0, 0),
          ("Leather", 13, 0, 1),
          ("Chainmail", 31, 0, 2),
          ("Splintmail", 53, 0, 3),
          ("Bandedmail", 75, 0, 4),
          ("Platemail", 102, 0, 5)]

rings = [("None 1", 0, 0, 0),
         ("None 2", 0, 0, 0),
         ("Damage +1", 25, 1, 0),
         ("Damage +2", 50, 2, 0),
         ("Damage +3", 100, 3, 0),
         ("Defense +1", 20, 0, 1),
         ("Defense +2", 40, 0, 2),
         ("Defense +3", 80, 0, 3)]

from itertools import product

data = open(file_name).read().strip().split("\n")
boss_health = int(data[0].split(": ")[1])
boss_damage = int(data[1].split(": ")[1])
boss_armour = int(data[2].split(": ")[1])

person_health = 100


def part1():
	min_gold = 100000000

	for p in product(weapons, armour, rings, rings):
		if p[2] == p[3]:
			continue

		cost = sum(map(lambda x: x[1], p))

		damage = sum(map(lambda x: x[2], p)) - boss_armour
		if damage < 1:
			damage = 1

		protection = sum(map(lambda x: x[3], p))

		boss_dmg = boss_damage - protection
		if boss_dmg < 1:
			boss_dmg = 1

		win_turns = (boss_health // damage) + (0 if boss_health % damage == 0 else 1)
		loss_turns = (person_health // boss_dmg) + (0 if person_health % boss_dmg == 0 else 1)

		if win_turns <= loss_turns:
			min_gold = min(min_gold, cost)

	return min_gold


def part2():
	max_gold = 0

	for p in product(weapons, armour, rings, rings):
		if p[2] == p[3]:
			continue

		cost = sum(map(lambda x: x[1], p))

		damage = sum(map(lambda x: x[2], p)) - boss_armour
		if damage < 1:
			damage = 1

		protection = sum(map(lambda x: x[3], p))

		boss_dmg = boss_damage - protection
		if boss_dmg < 1:
			boss_dmg = 1

		win_turns = (boss_health // damage) + (0 if boss_health % damage == 0 else 1)
		loss_turns = (person_health // boss_dmg) + (0 if person_health % boss_dmg == 0 else 1)

		if loss_turns < win_turns:
			max_gold = max(max_gold, cost)

	return max_gold


print(part1())
print(part2())  # < 233 (< 211)
