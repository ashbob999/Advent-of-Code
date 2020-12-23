from typing import Callable
from os.path import isfile, join as path_join
file_name = path_join('input', 'day23.txt')
def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])

data = "167248359"

nums = list(map(int, list(data)))


def part1():
	numbers = nums[:]

	curr_i = 0
	curr_val = numbers[0]

	for i in range(100):
		picked_up = []
		for j in range(3):
			ind = numbers.index(curr_val)
			picked_up.append(numbers.pop((ind + 1) % len(numbers)))

		min_v = min(numbers)
		max_v = max(numbers)

		dest = curr_val -1
		while dest not in numbers:
			dest -= 1
			if dest < min_v:
				dest = max_v

		di = numbers.index(dest)

		numbers.insert(di +1, picked_up[0])
		numbers.insert(di +2, picked_up[1])
		numbers.insert(di +3, picked_up[2])

		ci = numbers.index(curr_val) + 1
		curr_val = numbers[ci % len(numbers)]

		#print(numbers, curr_val)

	ans = ""
	ind = numbers.index(1)
	for i in range(1, len(numbers)):
		ans += str(numbers[(ind +i) % len(numbers)])
	print(ans)


class Node:
	def __init__(self, value, next=None):
		self.next = next
		self.value = value

	def __str__(self):
		return "Node(" + str(self.value) + ")"

	def __repr__(self):
		return self.__str__()

def part2():
	numbers = nums[:]
	mv = max(numbers)
	l = len(numbers)
	size = 1_000_000
	for i in range(mv +1, mv + 1 + size - l):
		numbers.append(i)

	#print(numbers)

	val_node = {}
	st = Node(numbers[0])
	val_node[numbers[0]] = st
	curr = st
	for v in numbers[1:]:
		#if v % 100000 == 0: print(v)
		curr.next = Node(v)
		val_node[v] = curr.next
		curr = curr.next

	curr.next = st

	numbers_og = numbers[:]

	curr_i = 0
	curr_val = numbers[0]
	curr_node = st

	for i in range(10_000_000):
		#if i % 100000 == 0: print(i)
		picked_up = []
		for j in range(3):
			cn = curr_node.next
			picked_up.append(cn)
			curr_node.next = curr_node.next.next

		# get dest node
		dest_value = curr_node.value - 1
		if dest_value <= 0:
			dest_value = size

		while dest_value == picked_up[0].value or dest_value == picked_up[1].value or dest_value == picked_up[2].value:
			dest_value -= 1
			if dest_value <= 0:
				dest_value = size

		dest = val_node[dest_value]

		aft = dest.next
		for i in range(3):
			dest.next = picked_up[-1 -i]
			dest.next.next = aft
			aft = dest.next

		curr_node = curr_node.next

		#print(curr_node)

	on = val_node[1]
	print(on.next, on.next.next)
	print(on.next.value * on.next.next.value)


part1()
part2()
