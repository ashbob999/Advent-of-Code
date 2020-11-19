import numpy as np

with open("Data_16.txt", "r") as file:
	lines = [line.strip() for line in file]

input_num = lines[0].strip()

# input_num = "80871224585914546619083218645595"
# input_num = "12345678"

# part 1

default = [0, 1, 0, -1]


def get_phase(num):
	# print(num)
	repeated = np.repeat(default, num)

	shifted = list(np.repeat(default, num))
	shifted.append(shifted.pop(0))

	return shifted


def get_output(inp_str_, times):
	inp_str = inp_str_.copy()
	length = len(inp_str)

	for t_ in range(times):
		print(t_)
		output_values = []

		for i in range(length):
			phase = get_phase(i + 1)

			total = 0

			for n in range(length):
				n_ = n % len(phase)

				total += inp_str[n] * phase[n_]

			output_values.append(abs(total) % 10)

		inp_str = output_values.copy()

	return inp_str


out_list = list(map(int, list(input_num)))

prev_output = out_list  # get_output(out_list, 100)

value = "".join(map(str, prev_output[:8]))

print("Part 1: (47357091) ", value)
print()

# part 2

# input_num = "03036732577212944063491565474664"

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
