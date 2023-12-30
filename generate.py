import argparse
import os
import sys
from datetime import datetime

sys.path.append(".")

from aoc.input_handler import create_input_file, load_session


def create_day(year: str, day: str, overwrite: bool, gen_session: bool):
	# create the path to the year folder
	start_path = os.path.join(year, "")
	# print(start_path)

	# creates the year folder
	os.makedirs(start_path, exist_ok=True)

	# creates the day file if it does not exist
	if overwrite or not os.path.isfile(start_path + "day" + day + ".py"):
		print("Day file does not exist (dayXX.py will be created)")

		# writes the boilerplate code for the day file
		with open(start_path + "day" + day + ".py", "w") as f:
			# turn formatter off
			f.write("# @formatter:off\n")

			# import the isfile, and join from os.path
			f.write("from os.path import isfile, join as path_join\n")

			# import the path class from sys
			f.write("from sys import path as sys_path\n")

			# add parent directory to path
			f.write("sys_path.insert(1, path_join(sys_path[0], '..'))\n")

			# create the day input file name
			f.write("file_name = path_join('input', 'day%s.txt')\n" % day)

			# function to get the input as a list
			f.write(
				"def to_list(mf: object = int, sep='\\n'): "
				"return [mf(x) for x in open(file_name).read().split(sep) if x]")
			f.write("\n")

			# function to get the input as a generator
			f.write(
				"def to_gen(mf: object = int, sep='\\n'): "
				"return (mf(x) for x in open(file_name).read().split(sep) if x)")
			f.write("\n")

			# function to print and return part1 result
			f.write("def p1(*args): ans = part1(*args); print(ans); return ans")
			f.write("\n")

			# function to print and return part2 result
			f.write("def p2(*args): ans = part2(*args); print(ans); return ans")
			f.write("\n\n")

			# stick imports and file creation inside an if statement
			# to be called if the input file does not exist
			f.write("if not isfile(file_name):\n")

			# add slow import
			f.write("\tfrom aoc import get_input_file\n")

			# create the input file
			f.write("\tget_input_file(")

			if gen_session:
				f.write("session_path={}".format(str(["..", ".env"])))

			f.write(")\n")

			# turn formatter on
			f.write("# @formatter:on\n")

			f.write("\n")

			f.write("from utils import *\n")

			f.write("\n")

			# part 1 and part 2 code
			code = ("def part1():"
			        "\n"
			        "\tpass"
			        "\n\n\n"
			        "def part2():"
			        "\n"
			        "\tpass"
			        "\n\n\n"
			        "p1()"
			        "\n"
			        "p2()"
			        "\n")

			f.write(code)
	else:
		print("Day file exists, use --overwrite to overwrite the file")


def min_value_type(min_value: int):
	def min_value_checker(arg):
		try:
			i = int(arg)
		except ValueError:
			raise argparse.ArgumentTypeError("invalid int value: '%s'" % str(arg))

		if i < min_value:
			raise argparse.ArgumentTypeError("must not be less than: %d" % min_value)

		return i

	return min_value_checker


def main():
	parser = argparse.ArgumentParser()

	# add year argument
	parser.add_argument("-y", "--year", action="store", default=datetime.today().year, type=min_value_type(0),
	                    help="The year of the files to generate. (must be positive)")

	# add day argument
	parser.add_argument("-d", "--day", action="store", default=datetime.today().day, type=int,
	                    choices=range(1, 26),
	                    metavar="[1-25]",
	                    help="The Day of the file to generate. (must be in range 1-25)")

	# adds session argument
	parser.add_argument("-s", "--session", action="store_true",
	                    help="Whether or not to add session loading to the pre-generated code.")

	# adds input argument
	parser.add_argument("-i", "--input", action="store_true",
	                    help="Whether or not to create the input file.")

	# adds overwrite argument
	parser.add_argument("-o", "--overwrite", action="store_true",
	                    help="Whether or not to overwrite any existing code.")

	# adds all argument
	parser.add_argument("-a", "--all", action="store_true",
	                    help="Sets --session, -- input, --overwrite to True")

	# adds get all input argument
	parser.add_argument("--get-all-inputs", action="store_true",
	                    help="Gets all of the input files for the specified year")

	# supress output
	parser.add_argument("-q", "--quiet", action="store_true", help="Suppresses all outputted text")

	args = parser.parse_args()

	if args.all:
		args.overwrite = True
		args.session = True
		args.input = True

	year = str(args.year)

	# load the session, so we can get the input
	load_session(session_path=[".env"])

	if args.get_all_inputs:
		# gets all the input files for the given year
		success: bool = True
		for day_num in range(1, 25 + 1):
			day_str = str(day_num).rjust(2, "0")

			# create the input path
			input_path = os.path.join(year, "input", "day" + day_str + ".txt")

			if not create_input_file(input_path, str(day_num), year, overwrite=args.overwrite, quiet=args.quiet):
				if not args.quiet:
					print("Could not get input file for %s day %s" % (year, day_str))
				success = False

		sys.exit(0 if success else 1)

	day = str(args.day).rjust(2, "0")

	# creates the specified day file
	create_day(year, day, overwrite=args.overwrite, gen_session=args.session)

	if args.input:
		# create the input path
		input_path = os.path.join(year, "input", "day" + day + ".txt")

		# create the input file
		if not create_input_file(input_path, day.lstrip("0"), year):
			print("Could not get input file for %s day %s" % (year, day))
			sys.exit(1)


if __name__ == "__main__":
	main()
