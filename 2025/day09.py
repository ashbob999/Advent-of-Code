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

data = parsefile(file_name, [[int, ","], "\n"])

raw = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""
#data = parse(raw, [[int, ","], "\n"])


corners = data.copy()
print(len(corners))

def part1():
	ma = 0
	mv = None
	
	for i in range(len(corners)):
		for j in range(i+1, len(corners)):
			a = corners[i]
			b = corners[j]
			dx = abs(a[0] - b[0]) +1
			dy = abs(a[1] - b[1]) +1
			area = dx * dy
			if area > ma:
				ma = area
				mv = (a, b)
	
	print(mv)
	return ma



class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


cache = {}
cuc = 0
# Checking if a point is inside a polygon
def point_in_polygon(point, polygon):
    global cuc
    if point in cache:
        cuc += 1
        return cache[point]
	
    num_vertices = len(polygon)
    x, y = point[0], point[1]
    inside = False

    # Store the first point in the polygon and initialize the second point
    p1 = polygon[0]

    # Loop through each edge in the polygon
    for i in range(1, num_vertices + 1):
        # Get the next point in the polygon
        p2 = polygon[i % num_vertices]

        # Check if the point is above the minimum y coordinate of the edge
        if y > min(p1[1], p2[1]):
            # Check if the point is below the maximum y coordinate of the edge
            if y <= max(p1[1], p2[1]):
                # Check if the point is to the left of the maximum x coordinate of the edge
                if x <= max(p1[0], p2[0]):
                    # Calculate the x-intersection of the line connecting the point to the edge
                    x_intersection = (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1]) + p1[0]

                    # Check if the point is on the same line as the edge or to the left of the x-intersection
                    if p1[0] == p2[0] or x <= x_intersection:
                        # Flip the inside flag
                        inside = not inside

        # Store the current point as the first point for the next iteration
        p1 = p2

    cache[point] = inside
    # Return the value of the inside flag
    return inside



def part2():
	tl_ = [min([v[0] for v in corners]), min(v[1] for v in corners)]
	br_ = [max(v[0] for v in corners), max(v[1] for v in corners)]
	
	print(tl_, br_)

	ma = 0
	mv = None

	pip = point_in_polygon

	for i in range(len(corners)):
		print("i", i)
		for j in range(i+1, len(corners)):
			a = corners[i]
			b = corners[j]
			
			tl = (min(a[0], b[0]), min(a[1], b[1]))
			tr = (max(a[0], b[0]), min(a[1], b[1]))
			bl = (min(a[0], b[0]), max(a[1], b[1]))
			br = (max(a[0], b[0]), max(a[1], b[1]))
			
			dx = tr[0] - tl[0] +1
			dy = bl[1] - tl[1] +1
			
			area = dx * dy
			if area <= ma:
				print("less area", a,b)
				continue
			
			print(tl, tr, bl, br)
			
			valid = True
			if dx > 2 and dy > 2:
				for v in corners:
					vx, vy = v
					if vx > tl[0] and vx < tr[0] and vy > tl[1] and vy < bl[1]:
						valid = False
						print(v)
						break
			
			if not valid:
				continue
			
			# will this break
			if dx < 3 or dy < 3:
				continue
			
			valid = True
			for x in range(tl[0]+1, tr[0]):
				p = (x, tl[1]+1)
				if not pip(p, corners):
					valid = False
					break
			
			if not valid:
				continue
			
			for y in range(tl[1]+1, bl[1]):
				p = (tl[0]+1, y)
				if not pip(p, corners):
					valid = False
					break
			
			if not valid:
				continue
				

			"""
			if tl != a and tl != b and not pip(tl, corners):
				continue
			if tr != a and tr != b and not pip(tr, corners):
				continue
			if bl != a and bl != b and not pip(bl, corners):
				continue
			if br != a and br != b and not pip(br, corners):
				continue
			"""
				
			ma = area
			mv = (a, b)


	print(mv)
	return ma







def part20():
	tl_ = [min([v[0] for v in corners]), min(v[1] for v in corners)]
	br_ = [max(v[0] for v in corners), max(v[1] for v in corners)]
	
	print(tl_, br_)

	ma = 0
	mv = None

	pip = point_in_polygon

	valids = []

	for i in range(len(corners)):
		print("i", i)
		for j in range(i+1, len(corners)):
			a = corners[i]
			b = corners[j]
			
			tl = (min(a[0], b[0]), min(a[1], b[1]))
			tr = (max(a[0], b[0]), min(a[1], b[1]))
			bl = (min(a[0], b[0]), max(a[1], b[1]))
			br = (max(a[0], b[0]), max(a[1], b[1]))
			
			dx = tr[0] - tl[0] +1
			dy = bl[1] - tl[1] +1
			
			area = dx * dy
			if area <= ma:
				#print("less area", a,b)
				continue
			
			#print(tl, tr, bl, br)
			
			valid = True
			if dx > 2 and dy > 2:
				for v in corners:
					vx, vy = v
					if vx > tl[0] and vx < tr[0] and vy > tl[1] and vy < bl[1]:
						valid = False
						#print(v)
						break
			
			if not valid:
				continue
			
			# will this break
			if dx < 3 or dy < 3:
				continue
			
			valids.append((tl, tr, bl, br, dx, dy, area))
			continue
			
			valid = True
			for x in range(tl[0]+1, tr[0]):
				p = (x, tl[1]+1)
				if not pip(p, corners):
					valid = False
					break
			
			if not valid:
				continue
			
			for y in range(tl[1]+1, bl[1]):
				p = (tl[0]+1, y)
				if not pip(p, corners):
					valid = False
					break
			
			if not valid:
				continue
				

			"""
			if tl != a and tl != b and not pip(tl, corners):
				continue
			if tr != a and tr != b and not pip(tr, corners):
				continue
			if bl != a and bl != b and not pip(bl, corners):
				continue
			if br != a and br != b and not pip(br, corners):
				continue
			"""
				
			ma = area
			mv = (a, b)

	print(len(valids))
	valids = sorted(valids, key=lambda x: x[6], reverse=True)

	for i, v in enumerate(valids):
		tl, tr, bl, br, dx, dy, area = v
		
		print("vi", i, dx, dy, tl, tr, bl, br)
		print("cuc", cuc)
		
		valid = True
		
		"""
		for x in range(tl[0]+1, tr[0]):
			p = (x, tl[1]+1)
			if not pip(p, corners):
				valid = False
				break
		
		if not valid:
			continue
		
		for y in range(tl[1]+1, bl[1]):
			p = (tl[0]+1, y)
			if not pip(p, corners):
				valid = False
				break
		"""
		
		for d in range(1, min(dx, dy) -1):
			p = (tl[0]+d, tl[1]+d)
			if not pip(p, corners):
				valid = False
				break
		
		if not valid:
			continue
		
		#print("True after check diag")
		
		dd = [0, 0]
		if dx != dy:
			if dx < dy:
				dd[1] = 1
			else:
				dd[0] = 1
			
			for d in range(min(dx, dy)-2, max(dx, dy)-2):
				print(d)
				p = (tl[0] + d*dd[0]+1, tl[1] + d*dd[1]+1)
				if not pip(p, corners):
					valid = False
			
			if not valid:
				continue
		
		mv = (tl, tr, bl, br)
		ma = area
		break
		

	print(mv)
	return ma






p1()
#p2()
print(part20())
