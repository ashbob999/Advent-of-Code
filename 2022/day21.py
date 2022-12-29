# @formatter:off
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
# @formatter:on

from utils import parsefile, parse

data = parsefile(file_name, [[str, " "], "\n"])
rd = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""
dataa = parse(rd, [[str, " "], "\n"])

monkeys = []
nums = {}
ops = {}

#print(data)
for d in data:
	id = d[0][:-1]
	if len(d) == 2: # num
		number = int(d[1])
		monkeys.append((id, number))
		nums[id] = number
	else: # op
		id1 = d[1]
		id2 = d[3]
		op = d[2]
		ops[id] = (id1, op, id2)
		
#print(nums)

def part1():
	nums_ = nums.copy()
	ops_ = ops.copy()
	
	while "root" not in nums_:
		for k in list(ops_.keys()):
			v = ops_[k]
			if v[0] in nums_ and v[2] in nums_:
				if v[1] == "+":
					res = nums_[v[0]] + nums_[v[2]]
				elif v[1] == "-":
					res = nums_[v[0]] - nums_[v[2]]
				elif v[1] == "*":
					res = nums_[v[0]] * nums_[v[2]]
				elif v[1] == "/":
					res = nums_[v[0]] // nums_[v[2]]
					
				nums_[k] = res
				ops_.pop(k)
				#print("added", k, v, res)
				
	return nums_["root"]

root_r1 = ops["root"][0]
root_r2 = ops["root"][2]
print(root_r1)
print(root_r2)

def check(n):
	nums_ = nums.copy()
	ops_ = ops.copy()
	
	nums_["humn"] = n
	
	while root_r1 not in nums_ or root_r2 not in nums_:
		for k in list(ops_.keys()):
			v = ops_[k]
			if v[0] in nums_ and v[2] in nums_:
				if v[1] == "+":
					res = nums_[v[0]] + nums_[v[2]]
				elif v[1] == "-":
					res = nums_[v[0]] - nums_[v[2]]
				elif v[1] == "*":
					res = nums_[v[0]] * nums_[v[2]]
				elif v[1] == "/":
					res = nums_[v[0]] // nums_[v[2]]
					
				nums_[k] = res
				ops_.pop(k)
				#print("added", k, v, res)
	
	return nums_[root_r1] == nums_[root_r2]

def part2():
	i = 1
	while True:
		if i %1000==0:print("i", i)
		if check(i):
			return i
		i += 1


p1()
p2()
