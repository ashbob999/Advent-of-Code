import cProfile

num1 = "123"
num2 = "123" * 1000


def run(n):
	t = n
	for i in range(1000):
		t *= n


# cProfile.run("run("+num1+")")

# print("="*100)

# cProfile.run("run("+num2+")")

max = 100000


def r1(n):
	s = n
	for i in range(max):
		s += n
	print("s: ", s % 10)


def r2(n):
	s = n
	for i in range(max):
		s += n % 10
	print("s: ", s % 10)


cProfile.run("r1(" + num2 + ")")

cProfile.run("r2(" + num2 + ")")
