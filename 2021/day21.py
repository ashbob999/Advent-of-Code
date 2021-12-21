from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day21.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])

from utils import parsefile

start_pos = parsefile(file_name, [[None, 4, int, " "], "\n"])

p1_start_pos = start_pos[0][0]
p2_start_pos = start_pos[1][0]

def part1():
	num_rolls = 0
	p1_score = 0
	p1_pos = p1_start_pos
	p2_score = 0
	p2_pos = p2_start_pos
	won = None
	
	while p1_score < 1000 and p2_score < 1000:
		# p1 turn
		roll = num_rolls % 100 +1
		roll += (num_rolls+1) % 100 +1
		roll += (num_rolls+2) % 100 +1
		num_rolls += 3
		p1_pos = (p1_pos + roll-1) % 10 +1
		p1_score += p1_pos
		
		if p1_score >= 1000:
			won = 1
			break
		
		# p2 turn
		roll = num_rolls % 100 +1
		roll += (num_rolls+1) % 100 +1
		roll += (num_rolls+2) % 100 +1
		num_rolls += 3
		p2_pos = (p2_pos + roll-1) % 10 +1
		p2_score += p2_pos
		
		if p2_score >= 1000:
			won = 2
			break
			
	if won == 1:
		return num_rolls * p2_score
	elif won == 2:
		return num_rolls * p1_score

from itertools import permutations as perms

def part2():
	p1_wins = 0
	p2_wins = 0
	turns = {}
	turns[(p1_start_pos, p2_start_pos, 0, 0)] = 1 # (p1_pos, p2_pos, p1_score, p2_score)
	
	poss_rolls = sorted(list(map(sum, set(perms([1,2,3]*3, 3)))))
	roll_prob = {}
	for p in poss_rolls:
		if p in roll_prob:
			roll_prob[p] += 1
		else:
			roll_prob[p] = 1
	
	while len(turns) > 0:
		new_turns = {}
		for turn, count in turns.items():
			for roll, prob in roll_prob.items():
				p1_pos = (turn[0] + roll -1) %10 +1
				p1_score = turn[2] + p1_pos
				
				tup = (p1_pos, turn[1], p1_score, turn[3])
				if tup in new_turns:
					new_turns[tup] += count * prob
				else:
					new_turns[tup] = count * prob
		
		for turn, count in new_turns.copy().items():
			if turn[2] >= 21:
				del new_turns[turn]
				p1_wins += count
		
		turns = new_turns
					
		new_turns = {}
		for turn, count in turns.items():
			for roll, prob in roll_prob.items():
				p2_pos = (turn[1] + roll -1) %10 +1
				p2_score = turn[3] + p2_pos
				
				tup = (turn[0], p2_pos, turn[2], p2_score)
				if tup in new_turns:
					new_turns[tup] += count * prob
				else:
					new_turns[tup] = count * prob
	
		for turn, count in new_turns.copy().items():
			if turn[3] >= 21:
				del new_turns[turn]
				p2_wins += count
	
		turns = new_turns
	
	return p1_wins

p1()
p2()
