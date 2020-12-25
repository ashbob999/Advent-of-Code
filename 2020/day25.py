from typing import Callable
from os.path import isfile, join as path_join
file_name = path_join('input', 'day25.txt')
def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])

import math

data = to_list()

adata = [5764801, 17807724]

card_key = data[0]
door_key = data[1]

"""
(((1 * s % p) * s % p) * s % p)
1 * s^3 % 3
"""

p = 20201227

def find_loop(key, p):
	l = 1
	b = 7
	while b != key:
		b = b*7 % p
		l += 1

	return l


def enc(key, loop, p):
	v = 1
	for i in range(loop):
		v = v*key % p

	return v

def part1():
	card_loop = find_loop(card_key, p)
	print("card loop:", card_loop)

	enc_key = enc(door_key, card_loop, p)
	print("enc_key:", enc_key)


def part2():
	pass


part1()
part2()
