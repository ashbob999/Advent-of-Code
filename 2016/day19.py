# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day19.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file()
# @formatter:on

from utils import parsefile

elves = int(parsefile(file_name, None))


# elves = 5
# elves = 1001


class Elf:
	def __init__(self, id):
		self.id = id
		self.presents = 1
		self.prev = None
		self.next = None

	def take(self):
		self.presents += self.next.presents
		self.next = self.next.next


def part1():
	elf1 = Elf(1)

	prev_elf = elf1
	for i in range(1, elves):
		elf = Elf(i + 1)
		elf.prev = prev_elf
		prev_elf.next = elf
		prev_elf = elf

	# fix last and first
	prev_elf.next = elf1
	elf1.prev = prev_elf

	curr_elf = elf1
	while curr_elf.next != curr_elf:
		curr_elf.take()
		curr_elf = curr_elf.next

	return curr_elf.id


from skiplist import SkipList


class Elf_v2:
	count = 0
	elf_arr = []
	skiplist = None

	def __init__(self, id):
		self.id = id
		self.presents = 1
		self.prev = None
		self.next = None

	def take(self):
		steal_count = Elf_v2.count // 2
		curr_index = Elf_v2.skiplist.index(self.id)

		steal_index = (curr_index + steal_count) % Elf_v2.count

		steal_obj = Elf_v2.skiplist[steal_index]
		steal_id = steal_obj[0]
		steal_from = steal_obj[1]

		self.presents += steal_from.presents
		steal_from.prev.next = steal_from.next
		steal_from.next.prev = steal_from.prev
		Elf_v2.skiplist.remove(steal_id)
		Elf_v2.count -= 1


def part2():
	Elf_v2.count = elves

	# uses skiplist for O(logN) deletion and O(logN) index
	# from: https://github.com/geertj/pyskiplist
	skiplist = SkipList()

	elf1 = Elf_v2(1)
	skiplist.insert(1, elf1)

	elf_arr = [None] * elves
	Elf_v2.elf_arr = elf_arr

	elf_arr[0] = elf1

	prev_elf = elf1
	for i in range(1, elves):
		elf = Elf_v2(i + 1)
		skiplist.insert(i + 1, elf)
		elf.prev = prev_elf
		prev_elf.next = elf
		elf_arr[i] = elf
		prev_elf = elf

	# fix last and first
	prev_elf.next = elf1
	elf1.prev = prev_elf

	Elf_v2.skiplist = skiplist

	print("done setup")

	curr_elf = elf1
	while Elf_v2.count > 1:
		curr_elf.take()
		# print("elf1", elf1.prev.id, elf1.next.id)
		if Elf_v2.count % 100000 == 0: print(Elf_v2.count)
		curr_elf = curr_elf.next

	curr_elf = curr_elf.next

	return curr_elf.id


p1()
p2()
