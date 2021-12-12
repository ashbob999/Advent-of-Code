def parsefile(file_name: str, pattern):
	return parse(open(file_name).read().strip(), pattern)


# pattern syntax
# 0. A: None or B: ()
# 1. A: (function) or B: function or C: sep
# 2. (function, [sep])
# 3. (function, [count], [sep])
# 4. (function, [count], function, [count], [sep])
# 5. (tuple, [sep])
# 6. (tuple, [count], [sep])

# function = any 1 argument callable
# sep = seperator to split the current text. (default = whitespace), (if function is None ignore element)
# count = number of sections to apply the function to. (default = 1), (0 apply function on all sections),
#                                                      (if only 1 function given, it will apply to all)
# tuple = parse each section based on the given pattern

def parse(text: str, pattern: object = None):
	# determines whether to call the map or parse function
	def handle(sub_pattern, sub_sections):
		if isinstance(sub_sections, (tuple, list)):  # handle multiple sections
			if isinstance(sub_pattern, (tuple, list)):
				return [parse(section, sub_pattern) for section in sub_sections]
			elif callable(sub_pattern):
				return list(map(sub_pattern, sub_sections))
			else:
				return []
		elif isinstance(sub_sections, str):  # handle a single section
			if isinstance(sub_pattern, (tuple, list)):
				return parse(sub_sections, sub_pattern)
			elif callable(sub_pattern):
				return sub_pattern(sub_sections)
			else:
				return ""

	text = text.strip()

	# option 0.A
	if pattern is None:
		return text

	# option 0.B
	if isinstance(pattern, (tuple, list)) and len(pattern) == 0:
		return text

	# is the pattern a tuple/list
	is_list: bool = isinstance(pattern, (tuple, list))

	# does the pattern specify a separator?
	has_separator: bool = isinstance(pattern, (tuple, list)) and isinstance(pattern[-1], str)

	# split the text into sections
	if has_separator:
		if pattern[-1] == "":  # split by char
			sections = list(text)
		else:
			sections = text.split(pattern[-1])
	else:
		sections = text.split()

	# option 1.B
	if callable(pattern):
		return list(map(pattern, sections))

	# option 1.C
	if isinstance(pattern, str):
		if pattern == "":
			return list(text)
		else:
			return text.split(pattern)

	# option 1.A, 2
	if isinstance(pattern, (tuple, list)) and len(pattern) == 1 + has_separator:
		if len(pattern) == 1 and has_separator:  # ([sep])
			return sections
		elif pattern[0] is None:  # (None)
			return sections
		else:
			return handle(pattern[0], sections)

	# option 3, 4, 5, 6
	if isinstance(pattern, (tuple, list)):
		# list of tuples containing (function, times)
		functions = []

		i = 0
		while i < len(pattern) - has_separator:
			func = None
			count: int = 1

			if callable(pattern[i]) or isinstance(pattern[i], (tuple, list)) or pattern[i] is None:
				func = pattern[i]
				i += 1

			if i < len(pattern) - has_separator and isinstance(pattern[i], int):
				count = max(pattern[i], 0)
				i += 1

			functions.append((func, count))

		if len(functions) == 0:  # no functions given
			return sections
		elif len(functions) == 1:  # only 1 function given
			if functions[0][1] == 0:
				# return list(map(functions[0][0], sections))
				return handle(functions[0][0], sections)
			else:
				# return list(map(functions[0][0], sections[:functions[0][1]]))
				return handle(functions[0][0], sections[:functions[0][1]])
		else:  # apply each function count times
			curr_func_i: int = 0
			curr_func = functions[curr_func_i]
			rem_times: int = curr_func[1]

			section_i: int = 0

			new_sections = []

			while section_i < len(sections) and curr_func_i < len(functions):
				if curr_func[0] is not None:
					mapped_value = handle(curr_func[0], sections[section_i])
					new_sections.append(mapped_value)

				if curr_func[1] > 0:
					rem_times -= 1

					if rem_times <= 0:
						curr_func_i += 1
						if curr_func_i >= len(functions):
							break

						curr_func = functions[curr_func_i]
						rem_times = curr_func[1]

				section_i += 1

			return new_sections


# testing
if __name__ == '__main__':
	# 0
	assert parse("1 2 3 4 5") == "1 2 3 4 5"
	assert parse("1 2 3 4 5", None) == "1 2 3 4 5"
	# assert parse("1 2 3 4 5", tuple([None])) == "1 2 3 4 5"
	# assert parse("1 2 3 4 5", [None]) == "1 2 3 4 5"

	# 1
	assert parse("1 2 3 4 5", int) == [1, 2, 3, 4, 5]
	assert parse("1 2 3 4 5", (int, " ")) == [1, 2, 3, 4, 5]
	assert parse("1 2 3 4 5", lambda x: int(x) ** 2) == [1, 4, 9, 16, 25]

	# 2
	assert parse("1 2 3 4 5", [int]) == [1, 2, 3, 4, 5]
	assert parse("1 2 3 4 5", [int, " "]) == [1, 2, 3, 4, 5]

	# 3
	assert parse("1 2 3 4 5", [int, 0]) == [1, 2, 3, 4, 5]
	assert parse("1 2 3 4 5", [int, 0, " "]) == [1, 2, 3, 4, 5]
	assert parse("1 2 3 4 5", [int, 2]) == [1, 2]
	assert parse("1 2 3 4 5", [int, 2, " "]) == [1, 2]

	# 4
	assert parse("1 2 3 4 5", [int, 1, int, 0]) == [1, 2, 3, 4, 5]
	assert parse("1 2 3 4 5", [int, 1, int, 0, " "]) == [1, 2, 3, 4, 5]

	# 5
	assert parse("1 2,3 4", [[int], ","]) == [[1, 2], [3, 4]]
	assert parse("1 2,3 4", [[int, " "], ","]) == [[1, 2], [3, 4]]

	# 6
	assert parse("1 2,3 4", [[int], 1, ","]) == [[1, 2]]
	assert parse("1 2,3 4", [[int, " "], 1, ","]) == [[1, 2]]
	assert parse("1 2,3 4", [[int], [int], ","]) == [[1, 2], [3, 4]]

	# mixed

	# misc
	assert parse("1 2 3 4 5", tuple(" ")) == ["1", "2", "3", "4", "5"]
	assert parse("1 2 3 4 5", [" "]) == ["1", "2", "3", "4", "5"]
	assert parse("12345", [int, ""]) == [1, 2, 3, 4, 5]
	assert parse("12345", "") == ["1", "2", "3", "4", "5"]
	assert parse("1 2 3 4 5", " ") == ["1", "2", "3", "4", "5"]
