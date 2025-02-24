import os
import sys

def get_usr_input(msg):
    """
    Prompts the user with a given message and gets their input.
    - Appends a colon and space (": ") to the message.
    - Returns the user's input as a string.
    """
    # Append ": " to the message
    prompt_message = msg + ": "
    # Display the prompt message to the user
    print(prompt_message, end="")
    # Get user input
    user_input = input().strip()
    return user_input


def check_path(file_path, data_files):
    """
    Validates the file path and returns a tuple of valid JSON files.
    """
    if not os.path.exists(file_path):
        print(f"{file_path} does not exist.")
        return 1  # Error code for non-existent path
    elif os.path.isdir(file_path):
        for file in os.listdir(file_path):
            check_path(os.path.join(file_path, file), data_files)
    
    # If file_path is a file
    if file_path.endswith("_formatted.json"):
        return 2  # Indicates file is already formatted
    
    # Only add if it is a .json file and not already added
    if file_path.endswith(".json") and file_path not in data_files:
        data_files.append(file_path)
    return tuple(data_files)