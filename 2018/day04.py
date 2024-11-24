# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day04.txt')
def to_list(mf=int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf=int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

data = parsefile(file_name, "\n")

records = []
for d in data:
	s = d.split(" ")
	date = tuple([int(v) for v in s[0][1:].split("-")])
	time = tuple([int(v) for v in s[1][:-1].split(":")])
	
	type = -1
	id = None
	if s[2] == "Guard":
		type = 0
		id = int(s[3][1:])
	elif s[2] == "falls":
		type = 1
	elif s[2] == "wakes":
		type = 2
		
	records.append((date, time, type, id))

records = sorted(records, key=lambda x: (x[0], x[1]))

sleeps = {}
	
id = None
date = None
start_time = 0
state = 0 # awake

for r in records:
	if r[2] == 0:
		if state == 1:
			if date not in sleeps:
				sleeps[date] = []
			sleeps[date].append((id, start_time, (00, 60)))
		
		id = r[3]
		start_time = 0
		
		state = 0
	elif r[2] == 1: # falls asleep
		assert state == 0
		if date is None:
			date = r[0]
		state = 1
		start_time = r[1]
	elif r[2] == 2: # wakes up
		assert state == 1
		if state == 1:
			if date not in sleeps:
				sleeps[date] = []
			sleeps[date].append((id, start_time, r[1]))
		state = 0


def part1():
	counts = {}
	for date, ss in sleeps.items():
		for s in ss:
			if s[0] not in counts:
				counts[s[0]] = 0
			counts[s[0]] += s[2][1] - s[1][1]
	
	id = max(counts.items(), key=lambda x:x[1])[0]
	
	time_counts = [0] * 60
	
	for date, ss in sleeps.items():
		for s in ss:
			if s[0] == id:
				for t in range(s[1][1], s[2][1]):
					time_counts[t] += 1
	
	time = max([(i, tc) for i, tc in enumerate(time_counts)], key=lambda x: x[1])[0]
	
	return time * id


def part2():
	time_counts = {}
	
	for date, ss in sleeps.items():
		for s in ss:
			id = s[0]
			if id not in time_counts: 
				time_counts[id] = [0] * 60
			
			for t in range(s[1][1], s[2][1]):
				time_counts[id][t] += 1
	
	id = max(time_counts. items(), key=lambda x: max(x[1]))[0]
	
	time = max([(i, tc) for i, tc in enumerate(time_counts[id])], key=lambda x: x[1])[0]
	
	return id * time


p1()
p2()
