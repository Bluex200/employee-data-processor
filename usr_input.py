import os.path

import os.path

def check_path(file_path, data_files):
    if not os.path.exists(file_path):
        print(file_path + " does not exist.")
        return 1  # error code for non-existent path
    elif os.path.isdir(file_path):
        for file in os.listdir(file_path):
            # The line below features calling the function within itself, which is refereed to
            # as 'recursion'. Recursion is needed here to meet the requirement : "to check the
            # contents of any nested folders". To understand how it works refer to the note in
            # the solution for question 1 - task 10 of exercises for module 6.            
            check_path(os.path.join(file_path, file), data_files)
     
    # Here, file_path is a file.
    if file_path.endswith("_formatted.json"):
        return 2  # Indicates file is already formatted.
    
    # Only add if it is a .json file and not already added.
    if file_path.endswith(".json") and file_path not in data_files:
        data_files.append(file_path)
    return tuple(data_files)

