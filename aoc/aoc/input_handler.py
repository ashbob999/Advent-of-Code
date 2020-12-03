import os
import sys

def load_session(session_cookie: str = None, session_path: list = None) -> None:
	# always try to load from given session cookie first
	if session_cookie is not None:
		os.environ["SESSION"] = session_cookie
	else:
		if session_path is not None:  # if the session path is set
			try:
				from dotenv import load_dotenv
				from pathlib import Path

				path = Path(os.path.join(*session_path))  # gets a path to the .env file
				if not session_path[-1] == ".env":
					path /= ".env"

				if path.is_file():
					load_dotenv(dotenv_path=path)  # loads the .env file

					if os.getenv("SESSION") is None:  # the SESSION variable does not exist
						print("No SESSION variable set in:", str(path.absolute()))
						sys.exit()
				else:  # the .env file does not exist
					print("The file", str(path.absolute()), "does not exist.")
					sys.exit()

			except ImportError:
				pass

		else:  # use default path
			pass


def create_input_file(input_file_path: str, day: str, year: str) -> None:
	# url to the input text
	url = "https://adventofcode.com/" + year + "/day/" + day + "/input"

	print("url:", url)
	print("Input File Location:", input_file_path)

	headers = {}

	# cookie so we can access the input text
	cookies = {
		"session": os.getenv("SESSION")
	}

	import requests

	# send the request
	request = requests.get(url, headers=headers, cookies=cookies)

	if request.status_code != 200:  # if it can't get the input from the url
		print("Error", request.status_code)
		if request.status_code == 404:
			print("Page Not Found, check Session Cookie and Year/Day")
		sys.exit()

	# creates the input folder
	os.makedirs(os.path.dirname(input_file_path), exist_ok=True)

	# create the input file
	with open(input_file_path, "w") as file:
		file.write(request.content.decode("utf-8"))


def get_input_file(re_download: bool = False):
	# split the path into its folders
	path = os.path.abspath(sys.argv[0]).split(os.sep)
	year = path[-2]  # extract the year
	day = path[-1][-5:-3]  # extract the day

	# construct the input file path, based on the year and day
	input_path = os.path.join("input", "day" + day + ".txt")

	# create the input file if it doesnt exist, or we should reset the input
	if re_download or not os.path.isfile(input_path):
		create_input_file(input_path, day.lstrip("0"), year)

	# open the file and read its contents
	with open(os.path.join("input", "day" + day + ".txt"), "r") as file:
		data = file.read()

	from .util.aoc_input import Aoc_Input

	return Aoc_Input(data)
