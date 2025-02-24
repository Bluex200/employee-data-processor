import os
import sys
import json
from parse_file import process_each_emp
from parse_file import generate_formatted_file
import usr_input 

'''   Main function that starts the file processing.
    - Calls `usr_input.get_usr_input()` to get the path from the user.
    - Calls `usr_input.check_path()` to validate the path and get valid file paths.
    - Calls `error_handle()` to handle errors before processing.
    - Calls `start_process()` to process valid files '''

def main():

    msg = "Please enter the path of the file or the folder containing the files: "
    #get the path from the user
    user_path = usr_input.get_usr_input(msg)
    #validating the path and get valid JSON files
    check_return = usr_input.check_path(user_path, [])
    #handle errors and process files
    error_handle(check_return)  # Handle errors
    start_process(check_return)  # Process files

''' Handles errors based on the return value of check_path '''

def error_handle(check_return):
    if check_return == 1:
        sys.exit()  # Exit with message
    elif check_return == 2:
        print("The file provided is already processed.")
        sys.exit()  # Exit with message
    elif check_return == ():
        print("There are no valid files to process in the folder provided.")
        sys.exit()  # Exit with message

''' Displays the number of files and employees processed in the required format '''

def print_output(num_files, num_emps):

    print("============================================================")
    print("---------------------Processing Summary---------------------")
    print("============================================================")
    print(f"Number of files processed:   {num_files}")
    print(f"Number of employee entries\n formatted and calculated:   {num_emps}")


''' Processes valid JSON file paths, formats employee data, and saves them '''

def start_process(tup):
    if not tup:  #preventing processing if no valid files
        return
    num_files = 0
    num_emps = 0

    for file_path in tup:
        if not file_path.endswith(".json") or file_path.endswith("_formatted.json"):
            continue  #skiping non-JSON or already formatted files
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                employees = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            continue  #skiping if file cannot be read
        #passing employees to procces each employee function
        formatted_employees = process_each_emp(employees)

        if not formatted_employees:  # Skip empty files
            continue  
        #add proccesed employees       
        num_emps += len(formatted_employees)
        num_files += 1

        # Call the separate function to generate the formatted file
        generate_formatted_file(formatted_employees, file_path)
    #print the proccesing summery
    print_output(num_files, num_emps)  
    
#entry point for the script
if __name__ == "__main__":
    main()