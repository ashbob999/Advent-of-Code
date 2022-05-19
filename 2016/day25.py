# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day25.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file()
# @formatter:on

from utils import parsefile

instr = parsefile(file_name, [[" "], "\n"])


def part1():
	"""
	from looking at the input operations the number passed to function 7
	needs to consist of a alternating binary pattern starting with 0
	e.g. 1010 or 1010101010101010

	function 2 calculates a minimum number to start with
	a = answer + input_number * 7
	where the input_number is the number given on line 3 of the input
	e.g. cpy 365 b

	then once we have calculated that number
	we can find the next largest number that has the alternating pattern
	then subtract the two for the answer
	"""

	input_number = int(instr[2][1]) * 7

	min_value = int("10", 2)
	while min_value < input_number:
		min_value <<= 2
		min_value |= 2  # 0b10

	answer = min_value - input_number
	return answer


def part2():
	pass


p1()
p2()

"""
part 1 solution

loops found

cpy a d
cpy 7 c
cpy 365 b  >2
inc d      >1
dec b
jnz b -2   <1
dec c
jnz c -5   <2
cpy d a    >7
jnz 0 0    >6
cpy a b
cpy 0 a
cpy 2 c    >4
jnz b 2    >3
jnz 1 6
dec b
dec c
jnz c -4   <3
inc a
jnz 1 -7   <4
cpy 2 b
jnz c 2    >5
jnz 1 4
dec b
dec c
jnz 1 -4   <5
jnz 0 0
out b
jnz a -19  <6
jnz 1 -21  <7

functions made from the loops

func 1 {
	do {
		d++
		b--
	} while b > 0
}

func 1a {
	d+=b
	b=0
}

func 2 {
	do {
		b=365 (input)
		func 1()
		c--
	} while c > 0
}

func 2a {
	do {
		b=365
		d+=b
		b=0
		c--
	} while c > 0
}

func 2b {
	b=365
	d+=b*c
	b=0
	c=0
}

func 3 {
	do {
		if b == 0 {
			jump +6 -> line 21
		} else {
			jump +2 -> line 16
			
			#line 16:
			b--
			c--
		}
	} while c > 0
}

func 4 {
	do {
		c=2
		func 3()
		a++
	} while true
}

func 4a {
	do {
		c=2
		do {
			if b == 0 {
				#jump +6 -> line 21
				return
			} else {
				b--
				c--
			}
		} while c > 0
		a++
	} while true
}

func 4b {
	do {
		c=2
		
		if b == 0 || b == 1 {
			c-=b
			# c -= b % 2
			b=0
			#jump +6 -> line 21
			return
		}
		
		b-=2
		
		a++
	} while true
}

func 4c {
	a+= b // 2 (floor division)
	c = 2 - (b % 2)
	b=0
	#jump +6 -> line 21
	return
}

func 5 {
	# c is either 1 or 2
	# b = 2
	do {
		if c == 0 {
			jump +4 -> line 27
		} else {
			jump +2 -> line 24
			
			#line 24:
			b--
			c--
		}
	} while true
}

func 5a {
	# c is either 1 or 2
	# b = 2
	
	b-=c
	
	jump +4 -> line 27
}

func 6 {
	do {
		# skip line 10 (jnz 0 0)
		b=a
		a=0
		func 4()
		# c is either 1 or 2
		
		#line 21
		b=2
		func 5() # b -= c
		
		#line 27
		# skip line 27 (jnz 0 0)
		output b
	} while a !=0
}

func 6a {
	# loop happens ceil(log2(a)) times
	# for output to be 0/1/0/1 repeating
	# the input a must have alteranting binary digits starting with 0
	do {
		# skip line 10 (jnz 0 0)
		b=a
		
		a = b // 2 (floor division)
		c = 2 - (b % 2)
		
		# c is either 1 or 2
		
		b = 2-c
		
		# skip line 27 (jnz 0 0)
		output b
	} while a !=0
}



func 7 {
	do {
	a=d
		func 6()
	} while true
}

func main {
	a=input
	d=a
	c=7
	
	func 2()
	
	func 7()
}

func main_a {
	a=input
	d=a
	c=7
	
	b=365
	d+=b*c
	b=0
	c=0
	
	do {
		a=d
		func 6a()
	} while true
}
"""
