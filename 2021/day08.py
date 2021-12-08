from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day08.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])


from utils import parsefile, parse

data = parsefile(file_name, [[[str], "|"], "\n"])

seg_count = {2:[1], 3:[7], 4:[4], 5:[2, 3, 5], 6:[0, 6, 9], 7:[7]}
seg_pos = {
	frozenset([0, 1, 2, 4, 5, 6]):0,
	frozenset([2, 5]):1,
	frozenset([0, 2, 3, 4, 6]):2,
	frozenset([0, 2, 3, 5, 6]):3,
	frozenset([1, 2, 3, 5]):4,
	frozenset([0, 1, 3, 5, 6]):5,
	frozenset([0, 1, 3, 4, 5, 6]):6,
	frozenset([0, 2, 5]):7,
	frozenset([0, 1, 2, 3, 4, 5, 6]):8,
	frozenset([0, 1, 2, 3, 5, 6]):9
}

char_ord = {c:ord(c) for c in "abcdefg"}

def part1():
	c=0
	for v in data:
		for seg in v[1]:
			for k, v in seg_count.items():
				if len(v) == 1:
					if len(seg) == k:
						c+= 1
						
	return c

from itertools import permutations as perms


def check_segments(segment_data, segment_mapping) -> bool:
	for seg in segment_data[0] + segment_data[1]:
		seg_set = set(map(int, seg.translate(segment_mapping)))

		if frozenset(seg_set) not in seg_pos:
			return False

	return True


def calc_number(segment_data: list, mapping: dict) -> int:
	num = 0
	for seg in segment_data[1]:
		seg_set = frozenset(map(int, seg.translate(mapping)))
		n = seg_pos[seg_set]
		num *= 10
		num += n

	return num


def interleave(original, new, indices: dict) -> str:
	result = original
	for k, v in indices.items():
		result = result[:v] + new[k] + result[v:]

	return result


def get_sum(segment_data, left_values, poss_values, indices) -> int:
	poss_len = len(poss_values)
	left_len = len(left_values)
	for poss_seg in perms(poss_values, poss_len):
		for left_seg in perms(left_values, left_len):
			p = interleave("".join(left_seg), "".join(poss_seg), indices)

			mapping = {char_ord[c]: str(i) for i, c in enumerate(p)}

			success = check_segments(segment_data, mapping)
			if success:
				return calc_number(segment_data, mapping)

	return 0


def part2():
	s = 0
	for v in data:
		# count of 2/3/4 unique (also 7 but ignoring) -> numbers 1/4/7 (ignoring number 8)
		count = {2:0, 3:0, 4:0}
		poss_segs = set()
		for seg in v[0] + v[1]:
			if len(seg) <= 4:
				count[len(seg)] += 1
				poss_segs |= set(seg)

		left_values = set("abcdefg") ^ poss_segs
		left_values = sorted(list(left_values))
		poss_values = sorted(list(poss_segs))

		if len(poss_segs) == 2:  # just 1
			indices = {0:2, 1:5}
		elif len(poss_segs) == 3:  # just 1/7
			indices = {0:0, 1:2, 2:5}
		elif len(poss_segs) == 4:  # just 1/4
			indices = {0:1, 1:2, 2:3, 3:5}
		else:  # just 1/4/7
			indices = {0:0, 1:1, 2:2, 3:3, 4:5}

		cs = get_sum(v, left_values, poss_values, indices)
		s += cs

	return s

p1()
p2()
