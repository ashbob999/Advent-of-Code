import math
import re

# gets the input lines for the challenge
with open("Data_04.txt", "r") as file:
	lines = [line.strip() for line in file]

puzzle_input = "109165-576723".split("-")

min_number = int(puzzle_input[0])
max_number = int(puzzle_input[1])


# Part 1

def check_number(number):
	value = str(number)
	is_correct = False
	
	for pair in range(0, len(value) - 1, 1):
		n1 = int(value[pair])
		n2 = int(value[pair + 1])
		
		if n2 < n1:
			return False
		
		if n1 == n2:
			is_correct = True
		
	return is_correct

correct_values = 0
corr_l = []
		
for i in range(min_number, max_number, 1):
	if check_number(i):
		correct_values += 1
		corr_l.append(i)

print("Part 1: ", correct_values)
#print(corr_l[:100])

# Part 2

def check_number_2(number):
	value = str(number)
	is_correct = False
	
	for pair in range(0, len(value) - 1, 1):
		n1 = int(value[pair])
		n2 = int(value[pair + 1])
		
		if n2 < n1:
			return False
		
		if n1 == n2:
			is_correct = True
			#double_indexes.append((pair, pair + 1))
	
	previous_number = value[0]
	current_amount = 0		
	for char in value:
		#print(previous_number, " : ", current_amount, " : ", char)
		if char == previous_number:
			current_amount += 1
		else:
			if current_amount == 2:
				return True
			
			previous_number = char
			current_amount = 1
			
	if current_amount == 2:
		return True
	#print(value)
	return False
		
correct_numbers = 0

for i in range(min_number, max_number, 1):
	if check_number_2(i):
		correct_numbers += 1

check_number_2(555677)

print("Part 2: ", correct_numbers)

# 2322 high, 1678 low
