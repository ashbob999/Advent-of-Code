from typing import Iterator


class Aoc_Input:
	def __init__(self, input_text: str) -> None:
		self.text: str = input_text

	def to_list(self, mf=int, sep: str = ",") -> list:
		return [mf(x) for x in self.text.split(sep) if x]

	def to_gen(self, mf=int, sep: str = ",") -> Iterator:
		return (mf(x) for x in self.text.split(sep) if x)
