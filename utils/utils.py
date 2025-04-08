import platform
import os


#############################################################


def yes_or_no(prompt):
    while True:
        response = input(prompt).strip().lower()
        if response in ['yes', 'no']:
            return response
        else:
            print("    [!] Please enter 'yes' or 'no'.")


#############################################################


def clear_console():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')


#############################################################
