import os
import sys

'''Prompting the user with a given message stoered in main 
            and geting their input.
      Returns the user's input as a string '''

def get_usr_input(msg):
    #appending ": " to the message
    prompt_message = msg + ": "
    #display the prompt message to the user
    print(prompt_message, end="")
    # Get user input
    user_input = input().strip()
    return str(user_input)


''' Validates the file path and returns a tuple of valid JSON files.'''

def check_path(file_path, data_files):
    if not os.path.exists(file_path):
        print(f"{file_path} does not exist.")
        return 1  #error code for non-existent path
    elif os.path.isdir(file_path):
        for file in os.listdir(file_path):
            #cheking teh folders with subfolders
            check_path(os.path.join(file_path, file), data_files)
    #if file_path is a formatted file
    if file_path.endswith("_formatted.json"):
        return 2  #indicates file is already formatted
    #add only if it is a .json file and not already added
    if file_path.endswith(".json") and file_path not in data_files:
        data_files.append(file_path)
    return tuple(data_files)
