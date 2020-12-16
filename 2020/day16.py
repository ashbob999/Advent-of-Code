from typing import Callable
from os.path import isfile, join as path_join
file_name = path_join('input', 'day16.txt')
def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])

data = to_list(mf=str, sep="\n\n")

ranges = {}
n_i = {}
i_n = {}

for i, r in enumerate(data[0].split("\n")):
	#print(r)
	r = r.split(":")
	name = r[0].strip()
	#print(r)
	rs = []
	for rng in r[1].split("or"):
		rng = rng.strip()
		rs.append(tuple(map(int, rng.split("-"))))

	ranges[name] = rs
	i_n[i] = name
	n_i[name] = i

#print(ranges)
#print(indexes)

my_ticket = data[1].split("\n")[1].strip()

other_tickets = [val.strip() for val in data[2].strip().split("\n")[1:]]

def cr(val):
	for rngs in ranges.values():
		for rng in rngs:
			if rng[0] <= val <= rng[1]:
				return True

	return False

valid = set()
invalid = set()

def part1():
	s = 0
	values = map(int, ",".join(other_tickets).split(","))

	#valid = set()
	#invalid = set()

	for val in values:
		if val in valid:
			continue
		elif val in invalid:
			s += val
			continue

		if cr(val):
			valid.add(val)
		else:
			invalid.add(val)
			s += val

	print(s)



def part2():
	global my_ticket
	vt = []

	other_tickets.append(my_ticket)

	for t in other_tickets:
		tv = list(map(int, t.strip().split(",")))
		#print(tv)
		tmps = set(tv)
		if tmps & invalid:
			continue

		vt.append(tv)

	new_vt = [None] * len(vt[0])
	for i in range(len(vt[0])):
		s = set()
		for t in vt:
			s.add(t[i])

		new_vt[i] = s

	poss = {i: [] for i in range(len(vt[0]))}

	#print(len(new_vt))

	#print([t[0] for t in vt])

	for i in range(len(vt[0])):
		for name, rng in ranges.items():
			#print("\n", name, rng)
			index = n_i[name]
			rval = True

			def check_ranges(v):
				return any(
						map(lambda x: v>=x[0] and v<=x[1],
							rng
						)
					)

			#for t in vt:
			#	if not check_ranges(t[i]):
			#		print(False, t[i], name, rng)

			val = all(
				map(
					check_ranges,
					[t[i] for t in vt]
				)
			)

			if val:
				poss[i].append(name)

	#print(poss)

	#return

	corr = [None] * len(vt[0])
	while None in corr:
		#print(corr)
		for k, v in poss.items():
			if len(v) == 1:
				rm_val = v[0]
				corr[k] = rm_val
				#print("len 1", k, v)

				for k2 in poss.keys():
					#print("rm", poss, k2, v)
					if rm_val in poss[k2]:
						poss[k2].remove(rm_val)

				break

	#print("corr", corr)

	p = 1

	my_ticket = [int(v) for v in my_ticket.strip().split(",")]

	for i,v in enumerate(corr):
		if v.startswith("departure"):
			p *= my_ticket[i]

	print(p)

part1()
part2()
