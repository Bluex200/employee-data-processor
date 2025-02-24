import usr_input
import sys
import json
import os
from parse_file import process_each_emp  # Ensure this function exists

def main():
    """
    Main function that starts the file processing.
    - Calls `usr_input.check_path()` to get valid file paths.
    - Calls `error_handle()` to handle errors before processing.
    - Calls `start_process()` to process valid files.
    """
    check_return = usr_input.check_path('test_files', [])
    error_handle(check_return)  # Ensures exit when no files found
    start_process(check_return)


def error_handle(check_return):
    """
    Handles errors based on the return value of check_path.
    """
    if check_return == 1:
        sys.exit()  # Exits if path is invalid (no message needed)
    elif check_return == 2:
        print("The file provided is already processed.")
        sys.exit()  # Exits with message
    elif check_return == ():
        print("There are no valid files to process in the folder provided.")
        sys.exit()  # Exits properly when empty tuple is passed

"""
Displays the number of files and employees processed in the required format.
"""

def print_output(num_files, num_emps):

    print("============================================================")
    print("---------------------Processing Summary---------------------")
    print("============================================================")
    print(f"Number of files processed:   {num_files}")
    print(f"Number of employee entries\n formatted and calculated:   {num_emps}")


"""
 Processes valid JSON file paths, formats employee data, and saves them.
"""

def start_process(tup):

    if not tup:  
        return  # Prevents processing if no valid files

    num_files = len(tup)
    num_emps = 0
    processed_files = set() #Prevent duplicate processing

    for file_path in tup:
        if not file_path.endswith(".json"):
            continue  # Skips non-JSON files

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                employees = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading {file_path}: {e}")
            continue  # Skip if file cannot be read

        formatted_employees = process_each_emp(employees)
        num_emps += len(formatted_employees)

        formatted_file_path = file_path.replace(".json", "_formatted.json")

        try:
            with open(formatted_file_path, 'w', encoding='utf-8') as new_file:
                json.dump(formatted_employees, new_file, indent=4)
        except Exception:
            continue  # Skip if file cannot be written
            

    print_output(num_files, num_emps)


if __name__ == "__main__":
    main()
