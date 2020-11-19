with open("Data_24.txt", "r") as file:
	lines = [line.strip() for line in file]

lines_ = [
	"....#"
	"#..#.",
	"#..##",
	"..#..",
	"#...."
]


def chunks(l, n):
	n = max(1, n)
	return [l[i:i + n] for i in range(0, len(l), n)]


area = "".join(lines[:5])

width = 5
height = 5

# part 1

# y * w + x

prev_areas = set()
prev_area = area

prev_areas.add(prev_area)

dy = [-1, 0, 1, 0]
dx = [0, 1, 0, -1]

z = 0

while True:
	new_area = [None] * width * height

	for i in range(len(prev_area)):
		y = i // 5
		x = i % 5

		empty_count = 0
		bug_count = 0

		for j in range(4):
			new_x = x + dx[j]
			new_y = y + dy[j]

			new_pos = new_y * width + new_x

			if new_x >= 0 and new_x < width and \
					new_y >= 0 and new_y < height:
				if prev_area[new_pos] == "#":
					bug_count += 1
				# print("bug ", new_x, new_y, new_pos)
				else:
					empty_count += 1
			else:
				empty_count += 1

		if prev_area[i] == "#":
			if bug_count == 1:
				new_area[i] = "#"
			else:
				new_area[i] = "."
		else:
			if bug_count == 1 or bug_count == 2:
				new_area[i] = "#"
			else:
				new_area[i] = "."

	# print(i, x, y, bug_count, empty_count)

	# print("old: \n", "\n".join(chunks(prev_area, 5)))
	new_area_str = "".join(new_area)
	# print("\nnew: \n", "\n".join(chunks(new_area_str, 5)))
	# print()

	prev_area = new_area_str
	if new_area_str in prev_areas:
		break
	else:
		prev_areas.add(new_area_str)

# break

rating = 0

for i in range(len(prev_area)):
	if prev_area[i] == "#":
		rating += 2 ** i

# print(prev_areas)
print("Part 1: ", rating)

# part 2
