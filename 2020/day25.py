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

def find_loop(key):
	l = 1
	b = 7
	while b % p != key:
		b *= 7
		l += 1

	return l

def bsgs(a,b,p,N = None):
    if not N: N = 1 + int(math.sqrt(p))

    #initialize baby_steps table
    baby_steps = {}
    baby_step = 1
    for r in range(N+1):
        baby_steps[baby_step] = r
        baby_step = baby_step * a % p

    #now take the giant steps
    giant_stride = pow(a,(p-2)*N,p)
    giant_step = b
    for q in range(N+1):
        if giant_step in baby_steps:
            return q*N + baby_steps[giant_step]
        else:
            giant_step = giant_step * giant_stride % p
    return "No Match"

def part1():
	card_loop = bsgs(7, card_key, p)
	print("card loop:", card_loop)

	enc_key = (door_key ** card_loop) % p
	print("enc_key:", enc_key)


def part2():
	pass


part1()
part2()
