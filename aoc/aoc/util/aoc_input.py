from typing import Iterator


class Aoc_Input:
	def __init__(self, input_text: str) -> None:
		self.text: str = input_text

	def to_list(self, map_function=str, sep: str = ",") -> list:
		return list(map(map_function, self.text.split(sep)))

	def to_gen(self, map_function=str, sep: str = ",") -> Iterator:
		yield from map(map_function, self.text.split(sep))
