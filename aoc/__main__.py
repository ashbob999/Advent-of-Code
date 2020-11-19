# print("main")
# print("main: ", __package__)
# print("main: ", __name__)
"""
import argparse
import sys
from datetime import datetime
from importlib import import_module

sys.path.insert(0, ".")

__package__ = "aoc"

from .aoc.util import load_session, get_input_file
from .aoc.util import DayTemplate


def run_day(year: str, day: str) -> None:
	day_file_path = "." + year + ".day" + day
	day_class_name = "Day" + day
	day_file = None

	try:
		day_file = import_module(day_file_path, package="aoc")
	except ModuleNotFoundError:  # the day file does not exist
		print("day" + day + ".py", "in aoc/" + year + "/ does not exist.")
		print("Make sure you have ran generate.py first")
		sys.exit()

	try:
		day_class: DayTemplate = getattr(day_file, day_class_name)(int(year), int(day))
	except AttributeError:  # the day class does not exist
		print("class " + day_class_name, "in day" + day + ".py does not exist.")
		print("Make sure you have ran generate.py first")
		sys.exit()

	day_class.part1()
	day_class.part2()


def main():
	parser = argparse.ArgumentParser()

	# add optional year argument
	parser.add_argument("-y", "--year", action="store", default=datetime.today().year, type=int,
	                    help="The year of the files to generate. (must be positive)")

	# add optional day argument
	parser.add_argument("-d", "--day", action="store", default=datetime.today().day, type=int,
	                    choices=range(1, 26),
	                    metavar="[1-25]",
	                    help="The Day of the file to generate. (must be in range 1-25)")

	# add optional session argument
	parser.add_argument("-s", "--session", action="store", default=None, type=str,
	                    help="The Session Cookie for your Advent Of Code Account. \
	                        So it can automatically get the input files")

	# add optional .env boolean
	parser.add_argument("-e", "--use-env", action="store_true", dest="use_env",
	                    help="Specifies whether you will use a .env file to store the Session Cookie")

	# add optional .env path
	parser.add_argument("-p", "--env-path", action="store", default=".", type=str, dest="env_path",
	                    help="The path to a .env file, which includes the Session Cookie (SESSION=session). \
		                        \nRequires -e/--env to be set. \
		                        \nOnly works is the package python-dotenv is installed (pip install python-dotenv).")

	# add get input argument
	parser.add_argument("-i", "--input", action="store_false",
	                    help="Specifies whether you want to create the input file for a specified day, \
	                        or not. When you run the specified Day.\nDefault is true")

	parser.add_argument("-l", "--load-input", action="store_true", dest="load_input",
	                    help="Specifies whether you just want to load the input file Only.")

	args = parser.parse_args()

	# print(args)

	if args.year < 0:  # checks if the year is negative
		print("__main__.py: error: argument -y/--year: invalid year value: '" +
		      str(args.year) + "' (Year must be positive)")
		sys.exit()

	# loads the session key
	if args.use_env:
		load_session(session_cookie=args.session, session_path=args.env_path)
	else:
		load_session(session_cookie=args.session, session_path=None)

	if args.load_input:  # only loads the input file
		get_input_file(str(args.year), str(args.day).rjust(2, "0"))
		sys.exit()

	if args.input:  # if args.input is True, then load the input file
		get_input_file(str(args.year), str(args.day).rjust(2, "0"))

	# runs the specified day
	run_day(str(args.year), str(args.day).rjust(2, "0"))


main()
"""
