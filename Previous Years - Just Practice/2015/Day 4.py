import hashlib

# link to Day 1: https://adventofcode.com/2015/day/4

# splits the input file into a list of lines
with open("inputs/Day_4_Input.txt", "r") as file:
    lines = [line.strip() for line in file]

puzzle_input = "yzbqklnj"


# Part 1

def check_hash(key, number, number_of_zeroes):
    full_key = key + str(number)
    result = hashlib.md5(full_key.encode())
    hash = result.hexdigest()

    if hash[:number_of_zeroes] == "0" * number_of_zeroes:
        return True
    return False


number = 0

while True:
    if check_hash(puzzle_input, number, 5):
        break
    else:
        number += 1

print("Part 1: ", number)

# Part 2

# number = 0

while True:
    if check_hash(puzzle_input, number, 6):
        break
    else:
        number += 1

print("Part 2: ", number)
