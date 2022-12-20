# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day20.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile, parse

numbers = parsefile(file_name, [int, "\n"])

numbers = [(i, n) for i, n in enumerate(numbers)]

zeroval = None
for n in numbers:
	if n[1] == 0:
		zeroval = n
		break
			
def part1():
	order = numbers[:]
	
	nums = numbers[:]
	
	for num in order:
		i = nums.index(num)
		nums.pop(i)
		i += num[1]
		i %= len(nums)
		#print(i, num)
		nums.insert(i, num)
		
	#print(nums)
	zero = nums.index(zeroval)
	s = 0
	v1 = nums[(zero+1000)% len(nums)][1]
	v2 = nums[(zero+2000)% len(nums)][1]
	v3 = nums[(zero+3000)% len(nums)][1]
	s = v1 + v2 + v3
	
	return s


def part2():
	order = [(i, n*811589153) for i, n in numbers]
	
	nums = order[:]
	
	#print(nums)
	for _ in range(10):
		for num in order:
			i = nums.index(num)
			nums.pop(i)
			i += num[1]
			i %= len(nums)
			#print(i, num)
			nums.insert(i, num)
		
	#print(nums)
	zero = nums.index(zeroval)
	s = 0
	v1 = nums[(zero+1000)% len(nums)][1]
	v2 = nums[(zero+2000)% len(nums)][1]
	v3 = nums[(zero+3000)% len(nums)][1]
	s = v1 + v2 + v3
	
	return s


p1()
p2()
