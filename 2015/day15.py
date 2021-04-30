from typing import Callable
from os.path import isfile, join as path_join

file_name = path_join('input', 'day15.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file()

ingredients = {}
size = 100

raw = """Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3"""

for line in open(file_name).read().strip().split("\n"):
	parts = line.replace(",", "").split()

	name = parts[0][:-1]
	capacity = int(parts[2])
	durability = int(parts[4])
	flavor = int(parts[6])
	texture = int(parts[8])
	calories = int(parts[10])

	ingredients[name] = (capacity, durability, flavor, texture, calories)

key_list = list(ingredients.keys())
limit = 100


def part1():
	max_score = 0
	for a in range(0, limit + 1):
		for b in range(0, limit - a + 1):
			for c in range(0, limit - a - b + 1):
				d = limit - a - b - c

				capacity: int = (ingredients[key_list[0]][0] * a) + (ingredients[key_list[1]][0] * b) + (
						ingredients[key_list[2]][0] * c) + (ingredients[key_list[3]][0] * d)
				capacity = max(capacity, 0)

				durability: int = (ingredients[key_list[0]][1] * a) + (ingredients[key_list[1]][1] * b) + (
						ingredients[key_list[2]][1] * c) + (ingredients[key_list[3]][1] * d)
				durability = max(durability, 0)

				flavor: int = (ingredients[key_list[0]][2] * a) + (ingredients[key_list[1]][2] * b) + (
						ingredients[key_list[2]][2] * c) + (ingredients[key_list[3]][2] * d)
				flavor = max(flavor, 0)

				texture: int = (ingredients[key_list[0]][3] * a) + (ingredients[key_list[1]][3] * b) + (
						ingredients[key_list[2]][3] * c) + (ingredients[key_list[3]][3] * d)
				texture = max(texture, 0)

				score = capacity * durability * flavor * texture
				max_score = max(max_score, score)

	return max_score


def part2():
	max_score = 0
	for a in range(0, limit + 1):
		for b in range(0, limit - a + 1):
			for c in range(0, limit - a - b + 1):
				d = limit - a - b - c

				calories: int = (ingredients[key_list[0]][4] * a) + (ingredients[key_list[1]][4] * b) + (
						ingredients[key_list[2]][4] * c) + (ingredients[key_list[3]][4] * d)

				if calories == 500:
					capacity: int = (ingredients[key_list[0]][0] * a) + (ingredients[key_list[1]][0] * b) + (
							ingredients[key_list[2]][0] * c) + (ingredients[key_list[3]][0] * d)
					capacity = max(capacity, 0)

					durability: int = (ingredients[key_list[0]][1] * a) + (ingredients[key_list[1]][1] * b) + (
							ingredients[key_list[2]][1] * c) + (ingredients[key_list[3]][1] * d)
					durability = max(durability, 0)

					flavor: int = (ingredients[key_list[0]][2] * a) + (ingredients[key_list[1]][2] * b) + (
							ingredients[key_list[2]][2] * c) + (ingredients[key_list[3]][2] * d)
					flavor = max(flavor, 0)

					texture: int = (ingredients[key_list[0]][3] * a) + (ingredients[key_list[1]][3] * b) + (
							ingredients[key_list[2]][3] * c) + (ingredients[key_list[3]][3] * d)
					texture = max(texture, 0)

					score = capacity * durability * flavor * texture
					max_score = max(max_score, score)

	return max_score


print(part1())
print(part2())
