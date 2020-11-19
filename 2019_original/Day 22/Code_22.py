with open("Data_22_s2_1.txt", "r") as file:
	lines = [line.strip() for line in file]


# part 1

def new_stack(deck):
	return list(reversed(deck))


def cut(deck, n):
	top_half = deck[0:n]
	bottom_half = deck[n:]

	return bottom_half + top_half


def increment(deck, n):
	temp_deck = deck.copy()
	new_deck = [0] * len(deck)

	i = 0
	while len(temp_deck) > 0:
		new_deck[i] = temp_deck.pop(0)

		i += n

		if i >= len(deck):
			i %= len(deck)

	return new_deck


original_deck = list(range(10007))

deck = original_deck.copy()

for line in lines[0:1]:
	line = line.replace("x", str(10007 - 1))
	data = line.split(" ")
	if data[0] == "cut":
		deck = cut(deck, int(data[-1]))
	elif data[0] == "deal":
		if data[1] == "into":
			deck = new_stack(deck)
		elif data[1] == "with":
			deck = increment(deck, int(data[-1]))


# print("Part 1: ", deck.index(2019))

# part 2

def new_stack_index(length, index, n):
	return length - 1 - index


def cut_index(length, index, n):
	if n > 0:
		if index < n:
			return (length - n) + index
		else:
			return index - n
	else:
		if index < length + n:
			return index - n
		else:
			return index - (length + n)


def increment_index(length, index, n):
	return (index * n) % length


def parse_input(size):
	instr = []
	for line in lines:
		line = line.replace("x", str(size - 1))
		data = line.split(" ")
		if data[0] == "cut":
			instr.append((cut_index, int(data[-1])))
		elif data[0] == "deal":
			if data[1] == "into":
				instr.append((new_stack_index, 0))
			elif data[1] == "with":
				instr.append((increment_index, int(data[-1])))
	return instr


# part 1 quicker
instr = parse_input(10007)

index = 2019
for i in instr:
	index = i[0](10007, index, i[1])

print("Part 1: ", index)

# part 2 real

deck_size = 119315717514047
repeat_amount = 101741582076661

instr = parse_input(deck_size)

index = 2020
index_list = []

for x in range(1000):
	for i in instr:
		index = i[0](deck_size, index, i[1])

	# print(index)
	index_list.append(index)
# print(deck_size % index)


index_fact = []
for i in range(1, 1000):
	index_fact.append(index_list[i] / index_list[i - 1])
# print(index_fact[-1])

print()

print(cut_index(10, \
                increment_index(10, 5, 9), \
                1))

# inc a, inc b => inc a*b

# cut a, cut b => cut a+b

# cut x, inc y => inc y cut z
# z = x * y, x*y < len
