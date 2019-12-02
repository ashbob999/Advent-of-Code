import math

with open("Day_01_data.txt", "r") as file:
	masses = [int(line.strip()) for line in file]

# part 1

fuels = []

for mass in masses:
	fuel = int(mass / 3) - 2
	fuels.append(fuel)

total_fuel = sum(fuels)
	
print("Part 1: ", total_fuel)

# part 2

def calc_fuel(mass, fuel_tally=0):
	fuel = int(mass / 3) - 2
	if fuel > 0:
		return calc_fuel(fuel, fuel_tally + fuel)
	else:
		return fuel_tally

fuels = []

for mass in masses:
	new_fuel = calc_fuel(mass)
	fuels.append(new_fuel)
	
total_fuel = sum(fuels)

print("Part 2: ", total_fuel)

