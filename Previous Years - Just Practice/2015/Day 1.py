# link to Day 1: https://adventofcode.com/2015/day/1

# splits the input file into a list of lines
with open("inputs/Day_2_Input.txt.txt", "r") as file:
    lines = [line.strip() for line in file]

instructions = lines[0]

# Part 1

total = 0

for char in instructions:
    if char == "(":
        total += 1
    elif char == ")":
        total -= 1

print("Part 1: ", total)

# Part 2

total = 0

index_at_basement = 0

for i in range(0, len(instructions), 1):
    if instructions[i] == "(":
        total += 1
    elif instructions[i] == ")":
        total -= 1

    if total == -1:
        index_at_basement = i + 1  # first instruction is: index = 1
        break

print("Part 2: ", index_at_basement)
