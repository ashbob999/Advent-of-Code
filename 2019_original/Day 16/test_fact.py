import sys

sys.setrecursionlimit(10000)

fr1 = {1: 1}


def f1(n):
	if n in fr1:
		return fr1[n]
	ans = n * f1(n - 1)
	fr1[n] = ans
	return ans


fr2 = {1: 1}


def f2(n):
	if n in fr2:
		return fr2[n]
	if n % 10 == 0:
		ans = f2(n - 1)
	else:
		ans = n * f2(n - 1)

	fr2[n] = ans
	return ans


num = 5

for i in range(1, 20):
	fact1 = f1(i)
	fact2 = f2(i)
	ans1 = (fact1 * num) % 10
	ans2 = (fact2 * num) % 10
	if ans1 != ans2:
		print(i)

import cProfile


def t1(max):
	sum = 0
	for i in range(1, max):
		sum += num * f1(i)
	print("t1: ", sum % 10, len(str(sum)))


def t2(max):
	sum = 0
	for i in range(1, max):
		sum += num * f2(i)
	print("t2: ", sum % 10, len(str(sum)))


cProfile.run("t1(10000)")

cProfile.run("t2(10000)")
