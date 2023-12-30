import argparse
import subprocess
import sys
import os
import shutil
from datetime import datetime


def create_cpp_files(year: str, quiet: bool = False):
	# create the path to the year folder
	start_path = os.path.join(year, "")

	# don't do anything if the folder already exists
	if os.path.isdir(start_path):
		if not quiet:
			print("CPP folder for year: %s, already exists" % year)
		return

	# creates the year folder
	os.makedirs(start_path, exist_ok=True)

	# create the CMakeLists.txt file
	if not quiet:
		print("Creating CMakeLists.txt file")
	template_cmakelists = open("./template_CMakeLists.txt").read()
	template_cmakelists = template_cmakelists.replace("%YEAR%", year)

	with open(start_path + "CMakeLists.txt", "w") as f:
		f.write(template_cmakelists)

	# copy the CMakeSettings.json file
	if not quiet:
		print("Creating CMakeSettings.json file")
	shutil.copyfile("./template_CMakeSettings.json", start_path + "CMakeSettings.json")

	# create the main file
	if not quiet:
		print("Creating main.cpp file")
	shutil.copyfile("./template_main.cpp", start_path + "main.cpp")

	# create the day01.cpp file
	if not quiet:
		print("Creating day01.cpp file")
	template_day01 = open("./day_template_cpp.cpp").read()
	template_day01 = template_day01.replace("00", "01")

	with open(start_path + "day01.cpp", "w") as f:
		f.write(template_day01)


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

	# supress output
	parser.add_argument("-q", "--quiet", action="store_true", help="Suppresses all outputted text")

	# ignore getting input errors
	parser.add_argument("--ignore-errors", action="store_true", help="Ignores errors when running generate.py")

	args = parser.parse_args()

	year = str(args.year)

	# run generate.py to create all the required input files
	process_args = ["python", "generate.py", "--year", year, "--get-all-input"]
	if args.quiet:
		process_args.append("--quiet")

	completed_process = subprocess.run(process_args, cwd="..")
	if completed_process.returncode != 0:
		if not args.quiet:
			print("Running generate.py failed")
		if not args.ignore_errors:
			sys.exit(1)

	# create the cpp files
	create_cpp_files(year, args.quiet)


if __name__ == "__main__":
	main()
