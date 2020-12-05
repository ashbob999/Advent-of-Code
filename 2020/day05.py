from aoc import get_input_file

input_text = get_input_file(session_path=['..', '.env'])

data = input_text.to_list(mf=str, sep="\n")

seats = []

def part1():
	m = 0
	for p in data:
		f = 0
		b = 127

		for c in p[:7]:
			if c == "F":
				b -= (b-f +1) // 2
			else:
				f += (b-f +1) // 2

		l = 0
		r = 7

		for c in p[7:]:
			if c == "L":
				r -= (r-l +1) // 2
			else:
				l += (r-l +1) // 2

		id = f*8 + l
		m = max(m, id)
		seats.append(id)

	print(m)

def part2():
	global seats
	seats = sorted(seats)
	for i in range(0, len(seats)-1):
		if seats[i+1] - seats[i] == 2:
			print(seats[i] +1)
			return


part1()
part2()
