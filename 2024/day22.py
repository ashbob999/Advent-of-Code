# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day22.txt')
def to_list(mf=int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf=int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

nums = parsefile(file_name,  [int, "\n"])


def gen(n):
	v = n
	
	v *= 64
	v ^= n
	v %= 16777216
	n = v

	v //= 32
	v ^= n
	v %= 16777216
	n = v
	
	v *= 2048
	v ^= n
	v %= 16777216
	
	return v

def get_n(i, n):
	ns = []
	v = i
	for i in range(n):
		v = gen(v)
		ns.append(v % 10)
	return v, ns
	
vals = []
nss  = []

for n in nums:
	v, ns = get_n(n, 2000)
	vals.append(v)
	nss.append(ns)

def part1():
	return sum(vals)


def part2():
	seqs = []
	for ns in nss:
		seq = {}
		for i in range(1, len(ns)-3):
			v1 = ns[i-1:i+3]
			v2 = ns[i:i+4]
			
			diffs = [v2[i] - v1[i] for i in range(4)]
			
			ev = ns[i+3]
			
			if tuple(diffs) not in seq:
				seq[tuple(diffs)] = ev
		
		seqs.append(seq)
		
	un_seq = set()
	for s in seqs:
		un_seq |= set(list(s.keys()))
	
	max_r = 0
	for seq in un_seq:
		t = 0
		for s in seqs:
			if seq in s:
				t += s[seq]
				
		if t > max_r:
			max_r = t
			
	return max_r
	


p1()
p2()
