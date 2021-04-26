from typing import Callable
from os.path import isfile, join as path_join
file_name = path_join('input', 'day04.txt')
def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file()

puzzle_input = open(file_name).read().strip()

import hashlib

def check_hash(key, number, number_of_zeroes):
    full_key = key + str(number)
    result = hashlib.md5(full_key.encode())
    hash = result.hexdigest()

    if hash[:number_of_zeroes] == "0" * number_of_zeroes:
        return True
    return False

def part1():
    number = 0

    while True:
        if check_hash(puzzle_input, number, 5):
            return number
        else:
            number += 1


def part2(start_val):
    number = start_val

    while True:
        if check_hash(puzzle_input, number, 6):
            return number
        else:
            number += 1


p1 = part1()
print(p1)
print(part2(p1))
