from typing import Callable
from os.path import isfile, join as path_join
file_name = path_join('input', 'day22.txt')
def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])

data = to_list(mf=str, sep="\n\n")

p1_deck = [int(x) for x in data[0].strip().split("\n")[1:]]
p2_deck = [int(x) for x in data[1].strip().split("\n")[1:]]


def part1():
	round = 0

	while True:
		p1_card = p1_deck.pop(0)
		p2_card = p2_deck.pop(0)

		if p1_card > p2_card:
			p1_deck.append(p1_card)
			p1_deck.append(p2_card)
		else:
			p2_deck.append(p2_card)
			p2_deck.append(p1_card)

		round += 1

		if not p1_deck:
			winner = 2
			wd = p2_deck
			break
		elif not p2_deck:
			winner = 1
			wd = p1_deck
			break

	tot = 0
	for i in range(len(wd)):
		tot += wd[i] * (len(wd) - i)

	print(tot)


def part2(p1_deck, p2_deck):
	seen = set()

	while True:
		winner = None
		if (":".join(map(str, p1_deck)), ":".join(map(str, p2_deck))) in seen:
			return 1, []

		seen.add((":".join(map(str, p1_deck)), ":".join(map(str, p2_deck))))


		p1_card = p1_deck.pop(0)
		p2_card = p2_deck.pop(0)

		if len(p1_deck) >= p1_card and len(p2_deck) >= p2_card:
			winner = part2(p1_deck[:p1_card], p2_deck[:p2_card])[0]
		else:
			if p1_card > p2_card:
				winner = 1
			elif p2_card > p1_card:
				winner = 2

		if winner == 1:
			p1_deck.append(p1_card)
			p1_deck.append(p2_card)
		elif winner == 2:
			p2_deck.append(p2_card)
			p2_deck.append(p1_card)

		if not p1_deck:
			return 2, p2_deck
		elif not p2_deck:
			return 1, p1_deck


part1()

p1_deck = [int(x) for x in data[0].strip().split("\n")[1:]]
p2_deck = [int(x) for x in data[1].strip().split("\n")[1:]]

w, wd = part2(p1_deck, p2_deck)

tot = 0
for i in range(len(wd)):
	tot += wd[i] * (len(wd) - i)

print(tot)
