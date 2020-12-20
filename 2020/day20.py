from typing import Callable
from os.path import isfile, join as path_join
file_name = path_join('input', 'day20.txt')
def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])

from math import sqrt

data = to_list(mf=str, sep="\n\n")

adata = "Tile 2311:_..##.#..#._##..#....._#...##..#._####.#...#_##.##.###._##...#.###_.#.#.#..##_..#....#.._###...#.#._..###..###__Tile 1951:_#.##...##._#.####...#_.....#..##_#...######_.##.#....#_.###.#####_###.##.##._.###....#._..#.#..#.#_#...##.#..__Tile 1171:_####...##._#..##.#..#_##.#..#.#._.###.####._..###.####_.##....##._.#...####._#.##.####._####..#..._.....##...__Tile 1427:_###.##.#.._.#..#.##.._.#.##.#..#_#.#.#.##.#_....#...##_...##..##._...#.#####_.#.####.#._..#..###.#_..##.#..#.__Tile 1489:_##.#.#...._..##...#.._.##..##..._..#...#..._#####...#._#..#.#.#.#_...#.#.#.._##.#...##._..##.##.##_###.##.#..__Tile 2473:_#....####._#..#.##..._#.##..#..._######.#.#_.#...#.#.#_.#########_.###.#..#._########.#_##...##.#._..###.#.#.__Tile 2971:_..#.#....#_#...###..._#.#.###..._##.##..#.._.#####..##_.#..####.#_#..#.#..#._..####.###_..#.#.###._...#.#.#.#__Tile 2729:_...#.#.#.#_####.#...._..#.#....._....#..#.#_.##..##.#._.#.####..._####.#.#.._##.####..._##..#.##.._#.##...##.__Tile 3079:_#.#.#####._.#..######_..#......._######...._####.#..#._.#...#.##._#.#####.##_..#.###..._..#......._..#.###...".replace("_", "\n").split("\n\n")

tiles = [t.split("\n") for t in data]
tiles = {int(t[0].split(" ")[1][:-1]): t[1:] for t in tiles}

size = int(sqrt(len(tiles)))

# 2297 / 2311
tw = len(tiles[2297][0])
th = len(tiles[2297])

#print(len(tiles), size, tw, th)

sides = {}
all_sides = set()

for id, tile in tiles.items():
	arr = set()
	arr.add(tile[0])
	arr.add(tile[0][::-1])
	arr.add(tile[-1])
	arr.add(tile[-1][::-1])

	ls = "".join(tile[i][0] for i in range(len(tile)))
	rs = "".join(tile[i][-1] for i in range(len(tile)))

	arr.add("".join(ls))
	arr.add(ls[::-1])
	arr.add("".join(rs))
	arr.add(rs[::-1])

	sides[id] = arr
	all_sides.update(arr)

m_count = {}
m_bords = set()
c_id = {2: [], 3: [], 4: []}
all_sides = set()

def part1():
	for k, v in sides.items():
		m_count[k] = set()
		for k2, v2 in sides.items():
			if k == k2:
				continue
			if v & v2:
				m_bords.add((frozenset((k, k2)), frozenset(v&v2)))
				m_count[k].add(k2)
				all_sides.update(v&v2)

	p = 1

	#print(len(m_bords))
	for id, ms in m_count.items():
		#print(id, len(ms))
		c_id[len(ms)].append(id)
		if len(ms) == 2:
			p *= id

	#for i in c_id.keys():
	#	print(i, len(c_id[i]))

	print(p)

image = [[None] * size for _ in range(size)]
img_ids = [[None] * size for _ in range(size)]

def flip(tile, dir):
	if dir == 0:
		return [tile[i] for i in range(len(tile)-1, -1, -1)]
	elif dir == 1:
		return [t[::-1] for t in tile]

def transpose(tile):
	return ["".join(x) for x in zip(*tile)]

def rotate(tile, dir):
	if dir == 0:
		return tile
	if dir == 90:
		tile = transpose(tile)
		return flip(tile, 1)


def get_adj(id):
	return list(filter(lambda x: id in x[0], m_bords))

locked = {id:[False, False, False, False] for id in tiles.keys()}

been_placed = set()

def get_next(adj, pid, count):
	for ad in adj:
		#print(ad)
		n_id = list(ad[0] ^ set([pid]))[0]
		if n_id in c_id[count] and n_id not in been_placed:
			return n_id


def fill_row(start, end, col, count):
	for x in range(start, end-1):
		pid = img_ids[col][x-1]
		adj = get_adj(pid)
		curr_id = get_next(adj, pid, count)

		if curr_id:
			img_ids[col][x] = curr_id
			been_placed.add(curr_id)

def fill_col(start, end, row, count):
	for x in range(start, end-1):
		pid = img_ids[x-1][row]
		adj = get_adj(pid)
		curr_id = get_next(adj, pid, count)

		if curr_id:
			img_ids[x][row] = curr_id
			been_placed.add(curr_id)


def get_side(x, y, loc):
	# assumes pid orientation is correct
	#cadj = get_adj(cid)
	#sides = list(filter(lambda x: cid in x[0] and pid in x[0], m_bords))

	if loc == 0:
		return image[y][x][0]
	elif loc == 2:
		return image[y][x][-1]
	elif loc == 1:
		return "".join([t[-1] for t in image[y][x]])
	elif loc == 3:
		return "".join([t[0] for t in image[y][x]])

def gs(tile, loc):
	if loc == 0:
		return tile[0]
	elif loc == 2:
		return tile[-1]
	elif loc == 1:
		return "".join([t[-1] for t in tile])
	elif loc == 3:
		return "".join([t[0] for t in tile])


def o_to_fit(cid, side, loc):
	tile = tiles[cid]

	while gs(tile, loc) != side and gs(tile, loc) != side[::-1]:
		tile = rotate(tile, 90)

	if gs(tile, loc) == side:
		return tile
	elif loc in (0, 2):
		return flip(tile, 1)
	elif loc in (1, 3):
		return flip(tile, 0)

def part2():
	c1 = c_id[2][0]
	c1_tile = tiles[c1]

	c1_adj = get_adj(c1)
	#print(c1_adj)

	# top left
	img_ids[0][0] = c1
	been_placed.add(c1)

	# top row
	fill_row(1, size, 0, 3)

	# top right
	pid = img_ids[0][-2]
	adj = get_adj(pid)
	img_ids[0][-1] = get_next(adj, pid, 2)
	been_placed.add(img_ids[0][-1])

	# left col
	fill_col(1, size, 0, 3)

	# bottom left
	pid = img_ids[-2][0]
	adj = get_adj(pid)
	img_ids[-1][0] = get_next(adj, pid, 2)
	been_placed.add(img_ids[-1][0])

	# bottom row
	fill_row(1, size, -1, 3)

	# right col
	fill_col(1, size, -1, 3)

	# bottom right
	pid = img_ids[-1][-2]
	adj = get_adj(pid)
	img_ids[-1][-1] = get_next(adj, pid, 2)
	been_placed.add(img_ids[-1][-1])

	# fill guts
	for y in range(1, size-1):
		for x in range(1, size-1):
			pid1 = img_ids[y-1][x]
			pid2 = img_ids[y][x-1]

			adj1 = get_adj(pid1)
			adj2 = get_adj(pid2)

			for ad1 in adj1:
				for ad2 in adj2:
					nv = (ad1[0] ^ set([pid1])) & (ad2[0] ^ set([pid2]))
					if nv:
						nvv = list(nv)[0]
						if nvv not in been_placed:
							n_id = nvv

			img_ids[y][x] = n_id
			been_placed.add(n_id)

	#for r in img_ids:
	#	print(r)

	# rotate first tile to match
	tile = tiles[img_ids[0][0]]
	cid = img_ids[0][0]
	tid = img_ids[0][1]

	adj_side = list(filter(lambda x: tid in x[0], get_adj(cid)))[0]

	tar_side = list(adj_side[1])[0]

	while gs(tile, 1) != tar_side and gs(tile, 1) != tar_side[::-1]:
		tile = rotate(tile, 90)

	if gs(tile, 2) not in all_sides:
		tile = flip(tile, 0)

	image[0][0] = tile

	# rotate tile to match
	# top row
	for x in range(1, size):
		cid = img_ids[0][x]

		side = get_side(x-1, 0, 1)

		ct = o_to_fit(cid, side, 3)

		image[0][x] = ct

	# do left col
	for y in range(1, size):
		cid = img_ids[y][0]

		side = get_side(0, y-1, 2)

		ct = o_to_fit(cid, side, 0)

		image[y][0] = ct

	for y in range(1, size):
		for x in range(1, size):
			cid = img_ids[y][x]

			side = get_side(x, y-1, 2)

			ct = o_to_fit(cid, side, 0)

			image[y][x] = ct

	# remove border
	for y in range(len(image)):
		for x in range(len(image[0])):
			tile = image[y][x]
			image[y][x] = [r[1:-1] for r in tile[1:-1]]


	# merge them
	# 3d -> 2d
	new_image = []
	for row in image:
		new_row = []
		for h in range(len(row[0])):
			new_row_val = ""
			for i in range(len(image[0])):
				new_row_val += row[i][h]
			new_row.append(new_row_val)

		new_image.append(new_row)

	# 2d -> 1d
	new_image = [x for l in new_image for x in l]

	# check for monsters
	smw = 20
	smh = 3
	def is_monster(x, y, image):
		if image[y+1][x] == ".":
			return False
		if image[y+2][x+1] == ".":
			return False
		if image[y+2][x+4] == ".":
			return False
		if image[y+1][x+5] == ".":
			return False
		if image[y+1][x+6] == ".":
			return False
		if image[y+2][x+7] == ".":
			return False
		if image[y+2][x+10] == ".":
			return False
		if image[y+1][x+11] == ".":
			return False
		if image[y+1][x+12] == ".":
			return False
		if image[y+2][x+13] == ".":
			return False
		if image[y+2][x+16] == ".":
			return False
		if image[y+1][x+17] == ".":
			return False
		if image[y+1][x+18] == ".":
			return False
		if image[y][x+18] == ".":
			return False
		if image[y+1][x+19] == ".":
			return False
		return True

	def get_count(image):
		count = 0
		for y in range(len(image)-smh):
			for x in range(len(image[0])-smw):
				if is_monster(x, y, image):
					count += 1
		return count

	max_count = 0

	# create all orientations
	images = []
	for i in range(4):
		tmp_img = new_image

		for j in range(i):
			tmp_img = rotate(tmp_img, 90)
		images.append(tmp_img)
		images.append(flip(tmp_img, 0))
		images.append(flip(tmp_img, 1))

	for img in images:
		max_count = max(max_count, get_count(img))

	sm_count = max_count * 15
	hash_count = sum(x.count("#") for x in new_image)

	print(hash_count - sm_count)

part1()
part2()
