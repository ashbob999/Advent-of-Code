"""
import os


class DayTemplate:
	def __init__(self, year: int, day: int) -> None:
		self.year: int = year
		self.day: int = day
		self.path: str = "./aoc/" + str(self.year) + "/input/Day" + str(self.day).rjust(2, "0") + ".txt"

		if self.check_input_file_exists():
			with open(self.path, "r+") as f:
				self.input: list[str] = f.readlines()

	def check_input_file_exists(self) -> bool:
		return os.path.isfile(self.path)

	@property
	def get_input_as_stream(self) -> str:
		with open(self.path, "r+") as f:
			for line in f:
				yield line

	def part1(self) -> None:
		pass

	def part2(self) -> None:
		pass
"""
