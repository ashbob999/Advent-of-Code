with open("Data_16.txt", "r") as file:
	lines = [line.strip() for line in file]

input_num = lines[0].strip()

input_num_big = input_num * 10000

offset = int(input_num_big[:7])

# print(offset)

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

# print(dt.utcnow().strftime("%H:%M:%S.%f"))

print("Part 2: ", message)
