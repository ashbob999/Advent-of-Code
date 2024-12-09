# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day09.txt')
def to_list(mf=int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf=int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

data = parsefile(file_name, None)

disk = []
id = 0

blocks = []
for i, c in enumerate(data):
	type = i % 2 # 0 = file, 1 = free space
	if type == 0:
		disk.append((type, int(c), id))
	else:
		disk.append((type, int(c), -1))
	
	for j in range(int(c)):
		if type == 0:
			blocks.append(id)
		else:
			blocks.append(None)
	
	if type == 0:
		id += 1


def compact_file(disk_):
	disk = disk_[:]
	
	i = len(disk) -1
	while i >= 0:
		if disk[i][0] == 1:
			i -= 1
			continue
		
		f = disk[i]
		
		for j in range(i):
			if disk[j][0] == 0:
				continue
			
			s = disk[j]
			
			if f[1] <= s[1]:
				
				if f[1] == s[1]:
					disk[j] = f
					disk[i] = s
				else:
					disk[j] = f
					disk[i] = (1, f[1], -1)
					ns = (1, s[1] - f[1], -1)
					disk.insert(j+1, ns)
					i += 1
				
				break

		i -= 1

	return disk
	
	
def compact_block(disk_):
	disk = disk_[:]
	
	i = len(disk) -1
	j = 0
	
	while i >= 0:
		if disk[i] is None:
			i -= 1
			continue
		
		while j < i:
			if disk[j] is not None:
				j += 1
				continue
			
			f = disk[i]
			s = disk[j]
			
			disk[j] = f
			disk[i] = s
			#j += 1
			break
				
		i -= 1
	
	return disk


def part1():
	cd = compact_block(blocks)
	
	t = 0
	
	for i in range(len(cd)):
		if cd[i] is None:
			break
			
		t += i * cd[i]
	
	return t


def part2():
	cd = compact_file(disk)
	
	t = 0
	index = 0
	for v in cd:
		for j in range(v[1]):
			if v[0] == 0:
				t+= index * v[2]
			index += 1
	
	return t


p1()
p2()
