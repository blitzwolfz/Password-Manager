# Author: Samin Q

# Reason for making this:
# Two Reasons. One, my favourite password manager decided to burn bridges with it's user base
# by making free features go behind a paywall. Second, I have horrible time remembering my passwords, so I need a 
# password manager.

# Basic dict struct for each password:
#       {"name":"basic identifier", "website":"https://www.google.com", "password":"something"}

# Basic dict struct for dictuser file:
#       {"name":"something", "password": "something", user_passwords:[]}

import base64  # To be used for password hashing
import json  # Needed for reading user data
import os  # Allows for OS related functions
from random import choice  # Just need choice function
from time import sleep  # Just need sleep function


# ANSI Colours for terminal printing
# Got to make the terminal look nice
# Does not work well on IDE/Text Editor's Shell
class terminal_colours:
	HEADER = '\033[95m'
	BLUE = '\033[94m'
	CYAN = '\033[96m'
	GREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


LOGO = """
      ___                       ___           ___                         ___           ___     
     /  /\        ___          /__/\         /  /\                       /  /\         /  /\    
    /  /::\      /  /\         \  \:\       /  /::|                     /  /:/_       /  /::\   
   /  /:/\:\    /  /:/          \  \:\     /  /:/:|     ___     ___    /  /:/ /\     /  /:/\:\  
  /  /:/~/:/   /__/::\      _____\__\:\   /  /:/|:|__  /__/\   /  /\  /  /:/ /:/_   /  /:/~/:/  
 /__/:/ /:/___ \__\/\:\__  /__/::::::::\ /__/:/ |:| /\ \  \:\ /  /:/ /__/:/ /:/ /\ /__/:/ /:/___
 \  \:\/:::::/    \  \:\/\ \  \:\~~\~~\/ \__\/  |:|/:/  \  \:\  /:/  \  \:\/:/ /:/ \  \:\/:::::/
  \  \::/~~~~      \__\::/  \  \:\  ~~~      |  |:/:/    \  \:\/:/    \  \::/ /:/   \  \::/~~~~ 
   \  \:\          /__/:/    \  \:\          |  |::/      \  \::/      \  \:\/:/     \  \:\     
    \  \:\         \__\/      \  \:\         |  |:/        \__\/        \  \::/       \  \:\    
     \__\/                     \__\/         |__|/                       \__\/         \__\/    
"""


# Storing dashes in a variable allows for me to only have to change the amount once
DASHES = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"


def user_file_path(user: str) -> str:
	"""Users may have different OS. Handle file paths for both Windows and UNIX"""

	return os.path.abspath(os.path.join(os.path.dirname(__file__), f'{user}.json'))


def check_file(path_to_file: str) -> bool:
	"""Returns a bool which indicates if a file exists or doesn't"""
	return os.path.isfile(path_to_file)


def login():
	"""Handles user auth. Failure results in delation of user file. Should return a bool and file path of
	user passwords if auth is passed or not."""

	user = input(f'{terminal_colours.GREEN}What is your username: {terminal_colours.ENDC}').lower()

	file_path = user_file_path(user)

	user_exists = check_file(file_path)

	if user_exists:
		with open(file_path) as f:
			user_file = json.load(f)
			password = input(f'{terminal_colours.GREEN}Password: {terminal_colours.ENDC}')

			i = 1
			while str(base64.b64encode(password.encode("utf-8"))) != user_file["password"]:
				i += 1
				if i > 0:
					print(f'{terminal_colours.FAIL} Try #{i}{terminal_colours.ENDC}')
				password = input(
					f'{terminal_colours.FAIL}Password failed. After 10th try, data will be erased. Please enter again: {terminal_colours.ENDC}')

				if i == 10:
					f.close()
					os.remove(file_path)

					print(
						f'{terminal_colours.FAIL}{terminal_colours.BOLD} All data has been deleted. You can create a new account{terminal_colours.ENDC}')
					print(
						f'{terminal_colours.FAIL}{terminal_colours.BOLD} Please wait 20 seconds before you can continue.{terminal_colours.ENDC}')

					sleep(20)
					return False, None

			return True, file_path

	else:
		return False, None


def create_user():
	"""Creates user file"""
	username = input(
		f'{terminal_colours.GREEN}What do you want your username to be. Case does not matter: {terminal_colours.ENDC}'
		).lower()

	password = base64.b64encode(input(
		f'{terminal_colours.GREEN}What do you want your Password to be. Case does matter: {terminal_colours.ENDC}')
								.encode("utf-8"))

	user_data = {
		"name": username,
		"password": str(password),
		"user_passwords": []
		}

	path_to_file = user_file_path(username)

	write_to_json(path_to_file, user_data)

	print(f'{terminal_colours.GREEN}You will be asked to login again{terminal_colours.ENDC}')


def search(array: list, goal: str, identifier: str):
	"""Binary Search function adapted for dicts with string keys. Returns Index for given array"""
	# Since the dict is sorted, this will work hopefully
	left = 0
	right = len(array) - 1  # length is last index + 1.

	# Binary Search's worst cases handled first
	if len(array) == 0:
		return None

	if array[left][identifier] == goal:
		return 0

	if array[right][identifier] == goal:
		return right

	while left <= right:
		middle = (left + right) // 2

		if array[middle][identifier] == goal:
			return middle

		elif array[middle][identifier] > goal:
			right = middle - 1

		elif array[middle][identifier] < goal:
			left = middle + 1

	return None


def sort_dict(array: list, identifier: str, sort_reversed=False):
	"""Sorts a dictionary"""
	return sorted(array, key=lambda i: i[identifier], reverse=sort_reversed)


def write_to_json(path_to_file: str, user_data):
	"""Takes two arguments: path_to_file a string and file. Writes to the the file"""
	user_data["user_passwords"] = sort_dict(user_data["user_passwords"], "name")
	
	# Use context manager so we do not have to worry about closing ahead or not
	with open(path_to_file, "w") as file:
		json.dump(user_data, file, indent=4)


def load_json(path_to_file):
	"""Takes one argument: path_to_file a string. Uses this as the path to get the file"""

	# Use context manager so we do not have to worry about closing ahead or not
	with open(path_to_file, "r") as f:
		user_file = json.load(f)

		return user_file


def print_logo_to_screen():
	"""Function prints the logo with colours and dashes"""
	print(f'{terminal_colours.FAIL}{terminal_colours.BOLD}{DASHES}{terminal_colours.ENDC}')
	print(f'{terminal_colours.FAIL}{terminal_colours.BOLD}{LOGO}{terminal_colours.ENDC}')
	print(f'{terminal_colours.FAIL}{terminal_colours.BOLD}{DASHES}{terminal_colours.ENDC}')
	print(f'{terminal_colours.CYAN}{terminal_colours.BOLD}{choice(sub_text)}{terminal_colours.ENDC}\n\n\n')


def clear_terminal():
	"""General function to clear the terminal"""
	os.system('cls' if os.name == 'nt' else 'clear')


def add(path_to_file: str):
	"""Takes path to user file, and adds passwords"""
	user_file = load_json(path_to_file)

	new_name = input(
		f'{terminal_colours.GREEN}What word you like to use to identify this password: {terminal_colours.ENDC}')

	if search(user_file["user_passwords"], new_name, "name"):
		print(
			f'{terminal_colours.FAIL}This name is already being used. Please use another name {terminal_colours.ENDC}')
		new_name = ""

	while new_name == "":
		new_name = input(
			f'{terminal_colours.FAIL}Failed.{terminal_colours.ENDC}{terminal_colours.GREEN}Please enter a word: {terminal_colours.ENDC}')

		if search(user_file["user_passwords"], new_name, "name"):
			print(
				f'{terminal_colours.FAIL}This name is already being used. Please use another name {terminal_colours.ENDC}')
			new_name = ""

	new_website = input(f'{terminal_colours.GREEN}Website: {terminal_colours.ENDC}')

	new_password = input(
		f'\r{terminal_colours.GREEN}What is the password: {terminal_colours.ENDC}')

	while new_password == "":
		new_password = input(
			f'\r{terminal_colours.FAIL}Failed.{terminal_colours.ENDC}{terminal_colours.GREEN}Please enter a password: {terminal_colours.ENDC}')

	new_data = {
		"name": new_name,
		"website": new_website,
		"password": str(base64.b64encode(new_password.encode("utf-8")))
		}

	user_file["user_passwords"].append(new_data)

	write_to_json(path_to_file, user_file)

	print(f'{terminal_colours.GREEN}Password has been added to user data {terminal_colours.ENDC}')
	input(f'{terminal_colours.GREEN}Press enter to continue {terminal_colours.ENDC}')


def delete(path_to_file: str):
	"""Takes path to user file, and deletes passwords"""
	user_file = load_json(path_to_file)

	item_to_be_deleted = input(
		f'{terminal_colours.GREEN}Please enter the name of the item you like to delete: {terminal_colours.ENDC}')

	index = search(user_file["user_passwords"], item_to_be_deleted, "name")

	confirm = input(f'{terminal_colours.GREEN}Are you sure (yes/no): {terminal_colours.ENDC}').lower()

	if confirm == "no":
		print(f'{terminal_colours.GREEN}Item will not be deleted {terminal_colours.ENDC}')
		input(f'{terminal_colours.GREEN}Press enter to continue {terminal_colours.ENDC}')
		return

	del user_file["user_passwords"][index]

	write_to_json(path_to_file, user_file)

	print(f'{terminal_colours.GREEN}Item has been deleted {terminal_colours.ENDC}')
	input(f'{terminal_colours.GREEN}Press enter to continue {terminal_colours.ENDC}')


def lookup(path_to_file: str):
	"""Lookup menu"""
	user_file = load_json(path_to_file)

	options = [
		"all", "search", "exit"
		]

	while True:
		clear_terminal()
		print(f'{terminal_colours.GREEN}Welcome to the Lookup Menu. Here are your options: {terminal_colours.ENDC}')

		for x in range(len(options)):
			print(f'{terminal_colours.GREEN}{x + 1}) {options[x].capitalize()} {terminal_colours.ENDC}')

		print()

		option_input = input(f'{terminal_colours.GREEN}What would you like to do: {terminal_colours.ENDC}').lower()

		if option_input not in options:
			print()
			print(f'{terminal_colours.FAIL}{terminal_colours.BOLD}Invalid Option. {terminal_colours.ENDC}')
			for x in range(len(options)):
				print(f'{terminal_colours.GREEN}{x + 1}) {options[x].capitalize()} {terminal_colours.ENDC}')

			print()

			option_input = input(
				f'{terminal_colours.GREEN}{terminal_colours.BOLD}What would you like to do: {terminal_colours.ENDC}').lower()

		if option_input == "all":
			clear_terminal()

			print(f'{terminal_colours.WARNING}To view individual passwords, please use search{terminal_colours.ENDC}\n')
			for password in user_file["user_passwords"]:
				print(f'Name: {password["name"]}\nWebsite:{password["website"]}\n')

			print(f'{terminal_colours.WARNING}To view individual passwords, please use search{terminal_colours.ENDC}\n')

		if option_input == "search":
			name = input(
				f'{terminal_colours.GREEN}What is the name of the password you are searching up for (Case Matters): {terminal_colours.ENDC}')

			index = search(user_file["user_passwords"], name, "name")

			if index is None:
				print(
					f'{terminal_colours.WARNING}Password does not exist. Check if you entered the right name using Search in Lookup Menu{terminal_colours.ENDC}\n')

			else:
				password_info = user_file["user_passwords"][index]
				# {"name": "basic identifier", "website": "https://www.google.com", "password": "something"}
				password = str(
						base64.b64decode(password_info["password"].replace("b\'", "").replace("\'", ""))
					).replace("b\'", "").replace("\'", "")

				print(f'{terminal_colours.CYAN}Password Info for {password_info["name"]}:\n{terminal_colours.ENDC}')
				print(f'{terminal_colours.CYAN}Website: {password_info["website"]}\n{terminal_colours.ENDC}')
				print(f'{terminal_colours.CYAN}Password: {password}\n{terminal_colours.ENDC}')

		if option_input == "exit":
			break

		print()
		input(f'{terminal_colours.GREEN}To continue click enter{terminal_colours.ENDC}')


def modify(path_to_file: str):
	"""Takes the path to user file, and modifies passwords"""
	user_file = load_json(path_to_file)

	options = [
		"account", "individual", "exit"
		]

	while True:
		clear_terminal()
		print(f'{terminal_colours.GREEN}Welcome to the Modify Menu. Here are your options: {terminal_colours.ENDC}')

		for x in range(len(options)):
			print(f'{terminal_colours.GREEN}{x + 1}) {options[x].capitalize()} {terminal_colours.ENDC}')

		print()

		option_input = input(f'{terminal_colours.GREEN}What would you like to do: {terminal_colours.ENDC}').lower()

		if option_input not in options:
			print()
			print(f'{terminal_colours.FAIL}{terminal_colours.BOLD}Invalid Option. {terminal_colours.ENDC}')
			for x in range(len(options)):
				print(f'{terminal_colours.GREEN}{x + 1}) {options[x].capitalize()} {terminal_colours.ENDC}')

			print()

			option_input = input(
				f'{terminal_colours.GREEN}{terminal_colours.BOLD}What would you like to do: {terminal_colours.ENDC}').lower()

		if option_input == "account":
			clear_terminal()

			print(
				f'{terminal_colours.WARNING}'
				f'This will change the password used to access the file. If you don\'t want to change that then enter nothing.'
				f'{terminal_colours.ENDC}\n'
				)

			password = input(
				f'{terminal_colours.GREEN}What do you want your Password to be. Case does matter: {terminal_colours.ENDC}')

			if password == "":
				continue

			else:
				user_file["password"] = str(base64.b64encode(password.encode("utf-8")))
				print(f'{terminal_colours.CYAN}Password has been changed\n{terminal_colours.ENDC}')
				write_to_json(path_to_file, user_file)

		if option_input == "individual":
			name = input(
				f'{terminal_colours.GREEN}'
				f'What is the name of the password you are changing up for (Case Matters): '
				f'{terminal_colours.ENDC}')

			index = search(user_file["user_passwords"], name, "name")

			if index is None:
				print(
					f'{terminal_colours.WARNING}Password does not exist. '
					f'Check if you entered the right name using Search in Lookup Menu'
					f'{terminal_colours.ENDC}\n')

			else:
				# {"name": "basic identifier", "website": "https://www.google.com", "password": "something"}
				password = input(
					f'{terminal_colours.GREEN}'
					f'What do you want your Password to be. Case does matter: '
					f'{terminal_colours.ENDC}')

				user_file["user_passwords"][index]["password"] = str(base64.b64encode(password.encode("utf-8")))
				print(f'{terminal_colours.CYAN}Password has been changed\n{terminal_colours.ENDC}')
				write_to_json(path_to_file, user_file)

		if option_input == "exit":
			break

		print()
		input(f'{terminal_colours.GREEN}To continue click enter{terminal_colours.ENDC}')


def menu(file_path: str) -> bool:
	"""Menu program. Will display menu with options on what this password manager can do. Returns a bool if program
	should exit """
	print_logo_to_screen()

	print(f'{terminal_colours.GREEN}Welcome to the Main Menu. Here are your options: {terminal_colours.ENDC}')

	options = [
		"lookup", "add", "delete", "modify", "exit"
		]

	for x in range(len(options)):
		print(f'{terminal_colours.GREEN}{x + 1}) {options[x].capitalize()} {terminal_colours.ENDC}')

	print()

	option_input = input(f'{terminal_colours.GREEN}What would you like to do: {terminal_colours.ENDC}').lower()

	while option_input not in options:
		print()
		print(f'{terminal_colours.FAIL}{terminal_colours.BOLD}Invaild Option. {terminal_colours.ENDC}')
		for x in range(len(options)):
			print(f'{terminal_colours.GREEN}{x + 1}) {options[x].capitalize()} {terminal_colours.ENDC}')

		print()

		option_input = input(
			f'{terminal_colours.GREEN}{terminal_colours.BOLD}What would you like to do: {terminal_colours.ENDC}').lower()

	if option_input == "lookup":
		lookup(file_path)
		clear_terminal()
		return False

	if option_input == "add":
		add(file_path)
		clear_terminal()
		return False

	if option_input == "delete":
		delete(file_path)
		clear_terminal()
		return False

	if option_input == "modify":
		modify(file_path)
		clear_terminal()
		return False

	if option_input == "exit":
		clear_terminal()
		return True


if __name__ == "__main__":

	# Witty Banter
	sub_text = [
		"Named after my favourite character in Tron Franchise. Disney don\'t sue lol",
		"Another password manager? Bruh",
		"So secure your grandmother couldn't beat it"
		]

	print_logo_to_screen()

	auth_passed, file_path = login()

	# Best to clear the screen after login attempt
	clear_terminal()

	while True:
		if not auth_passed:
			print(f'{terminal_colours.FAIL}{terminal_colours.BOLD}Your user file does not exist{terminal_colours.ENDC}')
			create_user()
			auth_passed, file_path = login()

			if auth_passed:
				clear_terminal()

		else:
			exit = menu(file_path)

			if exit:
				clear_terminal()

				print(f'{terminal_colours.GREEN}Have a wonderful day!{terminal_colours.ENDC}')