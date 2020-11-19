# new div method

# end of new div

with open("Data_16.txt", "r") as file:
	lines = [line.strip() for line in file]

input_num = lines[0].strip()

input_num_big = input_num * 10000

offset = int(input_num_big[:7])
print(len(input_num_big) - offset)
phase = 100

# util functions

pre_comp_fact = {0: 1, 1: 1}


def fact(n):
	if n in pre_comp_fact:
		return pre_comp_fact[n]
	# if n % 10 == 0:
	#	ans = fact(n - 1)
	# else:
	ans = n * fact(n - 1)
	pre_comp_fact[n] = ans
	return ans


def nCr(n, r):
	if r > n - r:
		r = n - r
	ans = 1
	i = 1
	n_r = n - r

	while i <= r:
		ans *= n_r + i
		ans //= i
		i += 1

	return ans;


# main code

def getValue(phase, index):
	sum = 0
	# pre-init variables
	r = 0
	n = 0
	i = 0
	n_r = 0
	# end pre-init variables
	for i in range(index, len(input_num_big) + index):
		if i % 10000 == 0: print(i)
		r = i - index
		n = phase + r
		# nCr
		if r > n - r:
			r = n - r
		ans = 1
		i = 1
		n_r = n - r

		while i <= r:
			ans *= n_r + i
			ans //= i
			i += 1
		# end nCr
		sum += ans * int(input_num_big[i])
	return sum % 10


values = [offset + i for i in range(0, 8)]
output = []
for v in values:
	print(v)
	output.append(getValue(phase, v))

message = "".join(map(str, output[:8]))

"""
input_sliced = input_num_big[offset:]

def get_fft_v2(signal_, times):
	signal = signal_.copy()
	length = len(signal) - 1
	print(length)
	last_num = signal[-1]
	
	for i in range(times):
		print(i)
		total = last_num
		
		for i in reversed(range(length)):
			total += signal[i]
			signal[i] = total % 10
	
	return signal

output = list(map(int, list(input_sliced)))

output = get_fft_v2(output, 100)

message = "".join(map(str, output[:8]))

"""
message = 0
print("Part 2: ", message)
