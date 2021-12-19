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
	get_input_file(session_path=['..', '.env'])

from utils import parsefile, parse

data = parsefile(file_name, [[[None, 2, int, 1, " "], 1, [int, ","], 0, "\n"], "\n\n"])

raw = """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14"""

daata = parse(raw, [[[None, 2, int, 1, " "], 1, [int, ","], 0, "\n"], "\n\n"])

scanners = {}
for d in data:
	id = d[0][0]
	s = set()
	for p in d[1:]:
		s.add(tuple(p))
		
	scanners[id] = sorted(s)

rots = [
{"x":(0, 1), "y":(1, 1), "z":(2, 1)},#1
{"x":(0, -1), "y":(1, -1), "z":(2, 1)},#2
{"x":(0, -1), "y":(1, 1), "z":(2, -1)},#3
{"x":(0, 1), "y":(1, -1), "z":(2, -1)},#4
{"x":(2, 1), "y":(0, 1), "z":(1, 1)},#5
{"x":(2, -1), "y":(0, -1), "z":(1, 1)},#6
{"x":(2, -1), "y":(0, 1), "z":(1, -1)},#7
{"x":(2, 1), "y":(0, -1), "z":(1, -1)},#8
{"x":(1, 1), "y":(2, 1), "z":(0, 1)},#9
{"x":(1, -1), "y":(2, -1), "z":(0, 1)},#10
{"x":(1, -1), "y":(2, 1), "z":(0, -1)},#11
{"x":(1, 1), "y":(2, -1), "z":(0, -1)},#12
{"x":(0, 1), "y":(2, -1), "z":(1, 1)},#13
{"x":(0, 1), "y":(2, 1), "z":(1, -1)},#14
{"x":(0, -1), "y":(2, 1), "z":(1, 1)},#15
{"x":(0, -1), "y":(2, -1), "z":(1, -1)},#16
{"x":(1, 1), "y":(0, 1), "z":(2, -1)},#17
{"x":(1, -1), "y":(0, 1), "z":(2, 1)},#18
{"x":(1, 1), "y":(0, -1), "z":(2, 1)},#19
{"x":(1, -1), "y":(0, -1), "z":(2, -1)},#20
{"x":(2, -1), "y":(1, 1), "z":(0, 1)},#21
{"x":(2, 1), "y":(1, -1), "z":(0, 1)},#22
{"x":(2, 1), "y":(1, 1), "z":(0, -1)},#23
{"x":(2, -1), "y":(1, -1), "z":(0, -1)},#24
]

found_rots = {0:rots[0]}

points = set([p for p in scanners[0]])

scanner_pos = {0:(0, 0, 0)}
rel_0_points = {0:scanners[0]}

def translate(points, rot):
	return [(p[rot["x"][0]] * rot["x"][1], p[rot["y"][0]] * rot["y"][1], p[rot["z"][0]] * rot["z"][1]) for p in points]
	"""
	new_points = []
	
	for p in points:
		nx = p[rot["x"][0]] * rot["x"][1]
		ny = p[rot["y"][0]] * rot["y"][1]
		nz = p[rot["z"][0]] * rot["z"][1]
		
		new_points.append((nx, ny, nz))
		
	return new_points
	"""
		
def get_12_offsets(p1_points, p2_points):
	offsets = {}
	for p_a in p1_points:
		for p_b in p2_points:
			offset = (p_b[0]-p_a[0], p_b[1]-p_a[1], p_b[2]-p_a[2])
			if offset in offsets:
				offsets[offset] += 1
				if offsets[offset] >= 12:
					return  True, offset
			else:
				offsets[offset] = 1
				
	return False, None

def check_match(p1, p2, p1_rot):
	p1_points = rel_0_points[p1]
	
	for rot in rots:
		p2_points = translate(scanners[p2], rot)
		
		# find most common offest between p1 and p2 points
		has12, best_offset = get_12_offsets(p1_points, p2_points)
		if has12:
			return True, p2_points, best_offset
			
	return False, None, None

def find_pairs(rem_ids):
	for p1 in found_rots.keys():
		for p2 in rem_ids:
			res = check_match(p1, p2, found_rots[p1])
			if res[0]:
				scanner_pos[p2] = (-res[2][0], -res[2][1], -res[2][2])
				found_rots[p2] = res[1]
				
				rel_0_points[p2] = [(p[0]-res[2][0], p[1]-res[2][1], p[2]-res[2][2]) for p in res[1]]
				points.update(rel_0_points[p2])
				return p1, p2
				"""
				rel_0_points[p2] = []
				for p in res[1]:
					np = (p[0]-res[2][0], p[1]-res[2][1], p[2]-res[2][2])
					points.add(np)
					rel_0_points[p2].append(np)
				return p1, p2
				"""
				
	return None, None

def find_all_pairs():
	rem_ids = set(scanners.keys())
	rem_ids.remove(0)
	
	while len(found_rots) < len(scanners):
		p1, p2 = find_pairs(rem_ids)
		rem_ids.discard(p2)
		print(rem_ids)

def part1():
	find_all_pairs()
	return len(points)


def part2():
	max_dist = 0
	for s1 in scanner_pos.keys():
		for s2 in scanner_pos.keys():
			if s1 == s2:
				continue
				
			p1 = scanner_pos[s1]
			p2 = scanner_pos[s2]
			
			dist = abs(p1[0]-p2[0]) + abs(p1[1]-p2[1]) + abs(p1[2]-p2[2])
			max_dist = max(max_dist, dist)
			
	return max_dist

p1()
p2()
