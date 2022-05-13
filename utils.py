def parsefile(file_name: str, pattern):
	return parse(open(file_name).read().strip(), pattern)


class Merge:
	def __init__(self, pattern: object, separator: str = ""):
		self.pattern = to_tuple(pattern)
		self.separator = separator


# pattern syntax
# 0. A: None or B: ()
# 1. A: (function) or B: function or C: sep
# 2. (function, [sep])
# 3. (function, [count], [sep])
# 4. (function, [count], function, [count], [sep])
# 5. (tuple, [sep])
# 6. (tuple, [count], [sep])
# 7. (tuple, [count], Merge(tuple), [count], [sep])

# function = any 1 argument callable
# sep = seperator to split the current text. (default = whitespace), (if function is None ignore element)
# count = number of sections to apply the function to. (default = 1), (0 apply function on all sections),
#                                                      (if only 1 function given, it will apply to all)
# tuple = parse each section based on the given pattern
# Merge(tuple) = merges count elements back into a single element, then applies tuple to the element

def parse(text_: str, pattern_: object = None):
	# memorisation variables
	mem_function_list: dict = {}
	mem_sub_function: dict = {}
	mem_pattern_type: dict = {}  # 0=None 1=list/tuple, 2=callable, 2=str

	iterable_type = tuple

	# determines whether to call the map or parse function
	def handle_sub(sub_pattern, sub_sections, for_list: bool):
		# print("handle_sub", sub_pattern, sub_sections)
		if sub_pattern in mem_pattern_type:
			t = mem_pattern_type[sub_pattern]
		else:
			if isinstance(sub_pattern, iterable_type):
				t = 1
			elif isinstance(sub_pattern, Merge):
				t = 3
			elif callable(sub_pattern):
				t = 2
			else:
				t = 0
			# t = 1 if isinstance(sub_pattern, iterable_type) else 3 if isinstance(sub_pattern, Merge) else 2 if callable(
			# 	sub_pattern) else 0
			mem_pattern_type[sub_pattern] = t

		# print(sub_pattern, sub_sections, for_list)

		if for_list:  # and len(sub_sections) > 1:  # handle multiple sections
			if t == 1:
				return [do_parse(section, sub_pattern) for section in sub_sections]
			elif t == 2:
				return list(map(sub_pattern, sub_sections))
			elif t == 3:
				return [*do_parse(sub_pattern.separator.join(sub_sections), sub_pattern.pattern)]
			else:
				return []
		else:  # handle a single section
			if t == 1:
				if len(sub_sections) == 1:
					sub_sections = sub_sections[0]
				return do_parse(sub_sections, sub_pattern)
			elif t == 2:
				return sub_pattern(sub_sections)
			elif t == 3:
				return do_parse(sub_pattern.separator.join(sub_sections), sub_pattern.pattern)
			else:
				return ""

	def create_function_list(pattern, has_separator: bool):
		if pattern in mem_function_list:
			return mem_function_list[pattern]

		# list of tuples containing (function, times)
		functions = []

		i = 0
		length = len(pattern) - has_separator

		while i < length:
			func = None
			count: int = 1

			if callable(pattern[i]) or isinstance(pattern[i], iterable_type) or isinstance(pattern[i], Merge) or \
					pattern[i] is None:
				func = pattern[i]
				i += 1

			if i < length and isinstance(pattern[i], int):
				count = max(pattern[i], 0)
				i += 1

			functions.append((func, count))

		mem_function_list[pattern] = functions
		return functions

	def do_parse(text: str, pattern):
		text = text.strip()

		# option 0.A
		if pattern is None:
			return text

		if pattern in mem_pattern_type:
			pattern_type = mem_pattern_type[pattern]
		else:
			if isinstance(pattern, iterable_type):
				pattern_type = 1
			elif isinstance(pattern, str):
				pattern_type = 3
			else:
				pattern_type = 0

			mem_pattern_type[pattern] = pattern_type

		# is the pattern a tuple/list
		is_list: bool = pattern_type == 1  # isinstance(pattern, iterable_type)

		# option 0.B
		if is_list and len(pattern) == 0:
			return text

		# does the pattern specify a separator?
		has_separator: bool = is_list and isinstance(pattern[-1], str)

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
		if pattern_type == 3:  # isinstance(pattern, str):
			if pattern == "":
				return list(text)
			else:
				return text.split(pattern)

		length = len(pattern)

		# option 1.A, 2
		if is_list and length == 1 + has_separator:
			if length == 1 and has_separator:  # ([sep])
				return sections
			elif pattern[0] is None:  # (None)
				return sections
			else:
				return handle_sub(pattern[0], sections, True)

		# option 3, 4, 5, 6, 7
		if is_list:
			# list of tuples containing (function, times)
			functions = create_function_list(pattern, has_separator)
			function_length = len(functions)

			if function_length == 0:  # no functions given
				return sections
			elif function_length == 1:  # only 1 function given
				if functions[0][1] == 0:
					return handle_sub(functions[0][0], sections, True)
				else:
					return handle_sub(functions[0][0], sections[:functions[0][1]], True)
			else:  # apply each function count times
				curr_func_i: int = 0
				curr_func = functions[curr_func_i]

				section_i: int = 0

				new_sections = []
				sections_length = len(sections)

				while section_i < sections_length and curr_func_i < function_length:
					if curr_func[0] is not None:
						if curr_func[1] > 0:  # parse count values
							mapped_values = handle_sub(curr_func[0], sections[section_i:section_i + curr_func[1]], True)
							new_sections += mapped_values
							section_i += curr_func[1]
						else:  # parse remaining values
							mapped_values = handle_sub(curr_func[0], sections[section_i:], True)
							new_sections += mapped_values
							break

					else:
						if curr_func[1] > 0:  # skip count values
							section_i += curr_func[1]
						else:  # skip remaining values
							break

					# update next function
					curr_func_i += 1
					if curr_func_i >= function_length:
						break

					curr_func = functions[curr_func_i]

				return new_sections

	# outer parse function
	return do_parse(text_, to_tuple(pattern_))


def to_tuple(pattern):
	if isinstance(pattern, (list, tuple)):
		result = [None] * len(pattern)
		for i, v in enumerate(pattern):
			result[i] = to_tuple(v)

		return tuple(result)
	else:
		return pattern


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
	# print(parse("1 2 3 4 5", [int, 1, int, 0]))
	assert parse("1 2 3 4 5", [int, 1, int, 0]) == [1, 2, 3, 4, 5]
	assert parse("1 2 3 4 5", [int, 1, int, 0, " "]) == [1, 2, 3, 4, 5]

	# 5
	assert parse("1 2,3 4", [[int], ","]) == [[1, 2], [3, 4]]
	assert parse("1 2,3 4", [[int, " "], ","]) == [[1, 2], [3, 4]]

	# 6
	assert parse("1 2,3 4", [[int], 1, ","]) == [[1, 2]]
	assert parse("1 2,3 4", [[int, " "], 1, ","]) == [[1, 2]]
	assert parse("1 2,3 4", [[int], [int], ","]) == [[1, 2], [3, 4]]

	# 7
	assert parse("A123", [str, 1, Merge(int), 0, ""]) == ["A", 123]
	assert parse("A1,2,3", [str, 1, Merge([int, ","]), 0, ""]) == ["A", 1, 2, 3]
	assert parse("A123", [str, 1, Merge(int), 1, Merge(int), 2, ""]) == ["A", 1, 23]
	assert parse("A123", [str, 1, Merge([int, ","], ","), 0, ""]) == ["A", 1, 2, 3]

	# mixed

	# misc
	assert parse("1 2 3 4 5", tuple(" ")) == ["1", "2", "3", "4", "5"]
	assert parse("1 2 3 4 5", [" "]) == ["1", "2", "3", "4", "5"]
	assert parse("12345", [int, ""]) == [1, 2, 3, 4, 5]
	assert parse("12345", "") == ["1", "2", "3", "4", "5"]
	assert parse("1 2 3 4 5", " ") == ["1", "2", "3", "4", "5"]

	assert parse("12345", [None, 1, int, 0, ""]) == [2, 3, 4, 5]
	assert parse("12345", [int, 1, None, 1, int, 0, ""]) == [1, 3, 4, 5]

	assert to_tuple(1) == 1
	assert to_tuple([1]) == (1,)
	assert to_tuple([1, "a", True]) == (1, "a", True)
	assert to_tuple([[int], [int], ","]) == ((int,), (int,), ",")
