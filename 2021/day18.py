from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day18.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])

from utils import parsefile

data = parsefile(file_name, [str, "\n"])

numbers = [l for l in data]


from math import floor, ceil

def reduce(number):
	depth = 0
	
	number = list(number)
	i = 0
	
	done_explodes = False
	def do_explodes(number):
		i=0
		depth=0
		while i < len(number):
			done_explodes = True
			if number[i] == "[":
				depth += 1
				i += 1
			elif number[i] == "]":
				depth -= 1
				i+= 1
				
			elif number[i] == ",":
				if depth > 4: # explode
					lb = i
					while number[lb] != "[":
						lb -= 1
						
					rb = i
					while number[rb] != "]":
						rb += 1
						
					has_lnum = True
					lnum = lb - 2
					while not number[lnum].isnumeric():
						lnum -= 1
						if lnum < 0:
							has_lnum = False
							break
							
					has_rnum = True
					rnum = rb + 2
					while not number[rnum].isnumeric():
						rnum += 1
						if rnum >= len(number):
							has_rnum = False
							break
					
					n1 = int("".join(number[lb+1:i]))
					n2 = int("".join(number[i+1:rb]))
					
					if has_lnum:
						number[lnum] = str(int(number[lnum]) + n1)
						
					if has_rnum:
						number[rnum] = str(int(number[rnum]) + n2)
						
					number = number[:lb] + ["0"] + number[rb+1:]
					
					i = 0
					depth = 0

				else:
					i += 1
				
			elif number[i].isnumeric():
				if i>0 and number[i-1].isnumeric():
					number[i-1] += number[i]
					del number[i]
					i -= 1
					
				i += 1
			
			else:
				i += 1
			
		return number
	
	number = do_explodes(number)
	
	i=0
	depth=0
	
	while i < len(number):
		done_explodes = True
		if number[i] == "[":
			depth += 1
			i += 1
		elif number[i] == "]":
			depth -= 1
			i+= 1
			
		elif number[i].isnumeric():
			if i>0 and number[i-1].isnumeric():
				number[i-1] += number[i]
				del number[i]
				i -= 1
				
			if int(number[i]) >= 10: # split
				n = int(number[i])
				ln = floor(n/2)
				hn = ceil(n/2)
				
				new_s = "[" + str(ln) + "," + str(hn) + "]"
				
				number = number[:i] + list(new_s) + number[i+1:]
				depth =0
				i=0
				number = do_explodes(number)
				continue
				
			i += 1
		
		else:
			i += 1
	
	return "".join(number)

def mag(number):
	n = number.replace("[", "(3*")
	n = n.replace("]", "*2)")
	n = n.replace(",", "+")
	return eval(n)

def part1():
	reduced_numbers = [reduce(number) for number in numbers]
	final_number = numbers[0]
	for i in range(1, len(numbers)):
		final_number = "[" + final_number +"," + numbers[i] + "]"
		final_number = reduce(final_number)

	return mag(final_number)

from itertools import permutations as perms

def part2():
	max_mag = 0
	for p in perms(range(len(numbers)), 2):
		final_number = "[" + numbers[p[0]] +"," + numbers[p[1]] + "]"
		final_number = reduce(final_number)
		
		m = mag(final_number)
		max_mag = max(max_mag, m)

	return max_mag


p1()
p2()
