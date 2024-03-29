from typing import Callable
from os.path import isfile, join as path_join

file_name = path_join('input', 'day20.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file()

from math import sqrt, floor

fact = [1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800, 39916800, 479001600, 6227020800, 87178291200]

number = int(open(file_name).read().strip())


def divisor_sum_both(n):  # incorrect for n=1
	max_n = floor(sqrt(n))
	s1 = n + 1
	s2 = n + 1
	for i in range(2, max_n + 1):
		if n % i == 0:
			s1 += i
			if i * 50 >= n:
				s2 += i
			d = n // i
			if d != i:
				s1 += d
				if d * 50 >= n:
					s2 += d

	return s1, s2


def run_both_parts():
	# 4 => 1*10 + 2*10 + 4*10 = (1+2+4)*10
	# divisors of 4 are 1,2,4
	# so 4 => div-sum * 10
	min_div_sum1 = number // 10
	min_div_sum2 = number // 11

	found1 = False
	found2 = False

	answer1 = 0
	answer2 = 0

	# given that div_sum(n!) has the highest divisor sum from 1->n!
	# we can use use div_sum(n!) to find n1 and n2 where ds(n1!) <= ds(t) <= ds(n2!)

	min_target = min(min_div_sum1, min_div_sum2)
	start_i = 1
	for i in range(len(fact) - 1):
		if divisor_sum_both(fact[i])[1] <= min_target < divisor_sum_both(fact[i + 1])[0]:
			start_i = fact[i]
			break

	i = start_i
	while True:
		s = divisor_sum_both(i)
		# print(s)
		if not found1 and s[0] >= min_div_sum1:
			answer1 = i
			found1 = True

		if not found2 and s[1] >= min_div_sum2:
			answer2 = i
			found2 = True

		if found1 and found2:
			break

		i += 1

	return answer1, answer2


solution = run_both_parts()


def part1():
	return solution[0]


def part2():
	return solution[1]


print(part1())
print(part2())
