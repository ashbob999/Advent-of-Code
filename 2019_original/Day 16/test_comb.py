pre_comp_fact = {0: 1, 1: 1}


def fact(n):
	if n in pre_comp_fact:
		return pre_comp_fact[n]
	# if n % 10 == 0:
	#       ans = fact(n - 1)
	# else:
	ans = n * fact(n - 1)
	pre_comp_fact[n] = ans
	return ans


def nCr(n, r):
	if r > n - r:
		r = n - r
		# because C(n, r) == C(n, n - r)
	ans = 1
	i = 1
	n_r = n - r

	while i <= r:  # i = 1; i <= r; i++) {
		ans *= n_r + i
		ans //= i
		i += 1

	return ans;


def nCr2(n, r):
	f_n_r = fact(n - r)
	ans = 1
	while n > r:
		ans *= n
		n -= 1

	return ans // f_n_r


x = 1000
y = 90


def t():
	for n in range(100, x):
		for r in range(1, y):
			v1 = nCr(n, r)
			v2 = nCr2(n, r)
			if v1 != v2:
				print(n, r, "  :  ", v1, v2)


# t()

def t1():
	sum = 0
	for n in range(100, x):
		for r in range(1, y):
			sum += nCr(n, r)
	print(sum)


def t2():
	sum = 0
	ans = 0
	i = 0
	n_r = 0
	r = 0

	n = 100
	rl = 1
	while n < x:
		while rl < y:
			r = rl
			if r > n - r:
				r = n - r
			# because C(n, r) == C(n, n - r)
			ans = 1
			i = 1
			n_r = n - r

			while i <= r:  # i = 1; i <= r; i++) {
				ans *= n_r + i
				ans //= i
				i += 1
			sum += ans
			rl += 1
		n += 1
		rl = 1
	print(sum)


import cProfile

cProfile.run("t1()")

print("==========")

cProfile.run("t2()")
