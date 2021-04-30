from typing import Callable
from os.path import isfile, join as path_join

file_name = path_join('input', 'day22.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file()

from enum import IntEnum


class SpellType(IntEnum):
	MagicMissile = 0,
	Drain = 1,
	Shield = 2,
	Poison = 3,
	Recharge = 4

	def __repr__(self):
		if self.value == 0:
			return "MagicMissile"
		elif self.value == 1:
			return "Drain"
		elif self.value == 2:
			return "Shield"
		elif self.value == 3:
			return "Poison"
		elif self.value == 4:
			return "Recharge"


spells = {SpellType.MagicMissile: (53, 4),  # Magic Missile, costs 53 mana, does 4 damage
          SpellType.Drain: (73, 2, 2),  # Drain, costs 73 mana, does 2 damage, heals for 2 health
          SpellType.Shield: (113, 6, 7),  # Shield, costs 113 mana, last for 6 turns, armour increased by 7 each turn
          SpellType.Poison: (173, 6, 3),  # Poison, costs 173 mana, lasts for 6 turns, does 3 damage each turn
          SpellType.Recharge: (229, 5, 101)}  # Recharge, costs 229 mana, last for 5 turns, gives 101 mana each turn

sr = {k: spells[k] for k in spells.keys().__reversed__()}

min_spell_cost = min(map(lambda k: spells[k][0], spells.keys()))


class Player:
	games = 0

	def __init__(self, health, damage, armour, mana):
		Player.games += 1
		self.health = health
		self.damage = damage
		self.armour = armour
		self.mana = mana
		self.spent = 0

	def copy(self):
		p = Player(self.health, self.damage, self.armour, self.mana)
		p.spent = self.spent
		return p

	def __del__(self):
		Player.games -= 1


class Effects:
	def __init__(self):
		self.running = {k: False for k in spells.keys()}
		self.left = {k: 0 for k in spells.keys()}

	def use(self, spell, person: Player, boss: Player):
		person.mana -= spells[spell][0]
		person.spent += spells[spell][0]

		if spell == SpellType.MagicMissile:
			boss.health -= spells[spell][1]  # does damage
		elif spell == SpellType.Drain:
			boss.health -= spells[spell][1]  # does damage
			person.health += spells[spell][2]  # heals
		else:
			self.running[spell] = True  # make spell active
			self.left[spell] = spells[spell][1]  # set spell duration

	def tick(self, person: Player, boss: Player):
		for k, v in self.running.items():
			if v:
				if k == SpellType.Shield:
					person.armour = spells[SpellType.Shield][2]  # increase armour
				elif k == SpellType.Poison:
					boss.health -= spells[SpellType.Poison][2]  # does damage
				elif k == SpellType.Recharge:
					person.mana += spells[SpellType.Recharge][2]  # increase mana

				self.left[k] -= 1
				if self.left[k] == 0:
					if k == SpellType.Shield:
						person.armour = 0
					self.running[k] = False

	def copy(self):
		e = Effects()
		e.running = self.running.copy()
		e.left = self.left.copy()
		return e


data = open(file_name).read().strip().split("\n")
boss_health = int(data[0].split()[2])
boss_damage = int(data[1].split()[1])

boss_og = Player(boss_health, boss_damage, 0, 0)

person_health = 50
person_mana = 500

person_og = Player(person_health, 0, 0, person_mana)

min_mana = 100000000000000000


def get_min_mana(person: Player, boss: Player, effects: Effects, hardmode):
	global min_mana

	if person.spent >= min_mana:
		return min_mana

	# handle player
	if hardmode:
		person.health -= 1
		if person.health <= 0:
			return min_mana  # lost

	effects.tick(person, boss)

	# check boss health
	if boss.health <= 0:
		return person.spent  # won

	# can't afford any spells
	if person.mana < min_spell_cost:
		return min_mana  # lost

	# recursively choose spells
	for spell, stats in sr.items():
		if person.mana >= stats[0] and not effects.running[spell]:  # can afford spell, and spell not running
			# copy person, boss, effects
			p = person.copy()
			b = boss.copy()
			e = effects.copy()

			# buy spell
			e.use(spell, p, b)

			if p.spent >= min_mana:
				continue

			# handle boss
			e.tick(p, b)

			# check boss health
			if b.health <= 0:
				# return p.spent  # won
				min_mana = min(min_mana, p.spent)
				continue

			# do boss damage
			b_damage = b.damage - p.armour if b.damage > p.armour else 1
			p.health -= b_damage

			# check person health
			if p.health <= 0:
				continue

			# get min_mana from next turn, only if person won
			mana = get_min_mana(p, b, e, hardmode)
			min_mana = min(min_mana, mana)

	return min_mana


def part1():
	return get_min_mana(person_og.copy(), boss_og.copy(), Effects(), False)


def part2():
	global min_mana
	min_mana = 1000000000000
	return get_min_mana(person_og.copy(), boss_og.copy(), Effects(), True)


print(part1())
print(part2())
