from os.path import isfile, join as path_join
file_name = path_join('input', 'day03.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])

data = to_list(mf=list)

def part1():
	gamma=["0" for i in range(len(data[0]))]
	epsilon=["0" for i in range(len(data[0]))]

	for i in range(len(data[0])):
		c=0
		for v in data:
			if v[i]=="1":
				c+=1

		if c > len(data)//2:
			gamma[i]="1"
		else:
			epsilon[i]="1"

	return int("".join(gamma),2)*int("".join(epsilon),2)


def get_rating(r):
	left = data[:]

	i=0

	while len(left) > 1:
		if r==0:
			c = 0
			for v in left:
				if v[i] == "1":
					c += 1
			if c>= len(left)/2:
				left = list(filter(lambda x: x[i]=="1",left))
			else:
				left = list(filter(lambda x: x[i]=="0", left))

		else:
			c = 0
			for v in left:
				if v[i] == "1":
					c += 1

			if c >= len(left)/2:
				left = list(filter(lambda x: x[i] == "0", left))
			else:
				left = list(filter(lambda x: x[i] == "1", left))

		i+=1

	return int("".join(left[0]),2)

def part2():
	a=get_rating(0)
	b=get_rating(1)
	return a*b



p1()
p2()
