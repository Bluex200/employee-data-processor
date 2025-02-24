import json 
import re 
import os
import math

''' Reading the json file content and passing for further proccesing 

    as a list of dictionaries - dictionary per employee -  '''

def get_json_content(file):
    #opening and reading json file 
    with open(file, "r", encoding="utf-8") as f:
        #returns a list of dictionaries 
        return json.load(f)


''' Generate the company email using the format:
<first letter of first name><full last name>@comp.com
           All in lower case.
    Example: John Smith -> jsmith@comp.com '''

def generate_email(first_name, last_name):
    #concatenating using a function
    return f"{first_name[0].lower()}{last_name.lower()}@comp.com" 


''' Generating new formatted JSON files for each

        JSON file already in the folder '''

def generate_formatted_file(emp_list, orig_path): 
    #getting the directory where the original file is located
    dir_name = os.path.dirname(orig_path)
    #extracting the base file name
    base_name = os.path.basename(orig_path)
    #spliting the base name into name and extension
    name, ext = os.path.splitext(base_name)
    #creating the new file name with "_formatted.json" appended.
    new_file = os.path.join(dir_name, f"{name}_formatted{ext}")
    
    #writing the formatted employee data to the new JSON file.
    with open(new_file, "w", encoding="utf-8") as f:
        json.dump(emp_list, f, indent=4)

''' Calculating salaryes according to the base salary per possition 
                        "SA": 60000,  
                        "HR": 70000,  
                        "IT": 80000 
    where 5% is added to MNG position and 1.5% to employees from
            "NY", "CA", "OR", "WA", "VT" states 
    taking into account both increases for qualified employees'''

def generate_salary(job_id, state):
    #extracting department from job_id
    emp_department = job_id.split('_')[0]
    #base salary for each department
    department_salaries = {
        "SA": 60000,  
        "HR": 70000,  
        "IT": 80000   
    }
    #retrieving base salary
    base_salary = department_salaries.get(emp_department, 0)
    # seeting bonus states criteria where employees get an additional 1.5%
    bonus_states = {"NY", "CA", "OR", "WA", "VT"}
    #checking if the person is a manager
    is_manager = "MNG" in job_id
    #applying salary increases based on conditions
    if is_manager and state in bonus_states:
        base_salary *= 1.065  #manager in bonus state gets 6.5% increase
    elif is_manager:
        base_salary *= 1.05   #manager in non-bonus state gets 5% increase
    elif state in bonus_states:
        base_salary *= 1.015  #non-managers in bonus states get 1.5% increase

    #rounding the amount and passing it as integer
    return int(math.ceil(base_salary))


''' Validating phone numbers to ensure they are formated correctly '''

def validate_phone_number(phone_number):

    #allowing numbers with +1 to pass through
    if phone_number.startswith("+1"):
        if " " not in phone_number:  #if +1 number has no spaces, reject it
            print(f"{phone_number} is not a valid US phone number, skipping this employee entry...\n", end="")
            return 1
    if phone_number.startswith("1-"):
        phone_number = phone_number[2:]
    #cleaning the Number removing `()`, `-`, spaces
    phone_number = phone_number.replace("(", "").replace(")", "").replace(" ", "").replace("-", "")

    #remove all remaining non-numeric characters**
    cleaned_number = re.sub(r"[^\d]", "", phone_number)

    #reject if it's exactly 11 digits and does NOTnot start with +1
    if len(cleaned_number) == 11 and phone_number[0] != '+':
        print(f"{phone_number} is not a valid US phone number, skipping this employee entry...\n", end="")
        return 1  #reject only if it's 11 digits and NOT a `+1` number

    #if it's 11 digits but starts with 1, remove the leading 1
    if len(cleaned_number) == 11 and cleaned_number.startswith("1"):
        cleaned_number = cleaned_number[1:]

    #ensure the final number is exactly 10 digits**
    if len(cleaned_number) == 10:
        return int(cleaned_number)

    #if invalid, print the error message and return 1**
    print(f"{phone_number} is not a valid US phone number, skipping this employee entry...\n", end="")
    return 1


""" Validating  zip codes, ensuring it is exactly 5 digits 

             and returned an integer """

def validate_zip(zip_code):
    #storing the original input
    original_zip = zip_code 
   #reject any zip codes that start with +
    if zip_code.startswith("+"):
        print(f"{original_zip} is not a valid US zip code, skipping this employee entry...\n", end="")
        return 1
    #removing all non-numeric characters
    cleaned_zip = re.sub(r"[^\d]", "", zip_code) 
    #ensure it's exactly 5 digits
    if len(cleaned_zip) == 5:
        return int(cleaned_zip)
    #if invalid, print the error message using the original input and return 1
    print(f"{original_zip} is not a valid US zip code, skipping this employee entry...\n", end="")
    return 1


''' Cleaning and formatting employee details for easier proccessing.

Validated phone numbers and zip codes are per criteria and are passed to main.
        
        Names and addresses are cleaned and capitalized  '''

def process_each_emp(emp_list):
    #creating an empty list for storing valid phone numbers and zip codes 
    valid_employees = []
    for emp in emp_list:
        # Remove the last key-value pair in the dictionary
        emp.pop("I declare that the above information is accurate.", None)
        # checking validated phone number before proceeding
        phone = validate_phone_number(str(emp.get("Phone Number", "")))
        if phone == 1:
            # Skip this entry if phone is invalid
            continue  
        emp["Phone Number"] = phone
         #validate zip code before proceeding
        zip_c = validate_zip(str(emp.get("Zip Code", "")))
        if zip_c == 1:  
            continue  #skip this entry if zip is invalid
        emp["Zip Code"] = zip_c

        # Ensure proper casing and no extra sapces for city and job title
        if "City" in emp and isinstance(emp["City"], str):
            emp["City"] = re.sub(r'\s+', ' ', emp["City"]).strip().title()  
        if "Job Title" in emp and isinstance(emp["Job Title"], str):
            emp["Job Title"] = re.sub(r'\s+', ' ', emp["Job Title"]).strip().title()
       
        #creating new variables for processing names and address lines separately
        name = ["First Name", "Last Name"]
        address_lines = ["Address Line 1","Address Line 2"]
        #proccesing first and last name
        for key in name:
            if key in emp and isinstance(emp[key],str):
                #removing leading and treiling spaces 
                cleaned = re.sub(r'\s+', ' ', emp[key]).strip()
                #applying title casing to the first and last names
                emp[key] = cleaned.title()
        #proccesing address lines
        for key in address_lines:
            if key in emp and isinstance(emp[key], str):
                cleaned = re.sub(r'\s+', ' ', emp[key]).strip()
                words = cleaned.split()
                #creating empty list for new addresses 
                new_address = []
            for word in words:
                if word and word[0].isdigit(): 
                    new_address.append(word.lower())  #lowercase if starting with digit
                else:
                    new_address.append(word.capitalize())  #capitalize otherwise

            emp[key] = ' '.join(new_address)  #convert list back to string

        # Generate and add the company email.
        emp["Company Email"] = generate_email(emp["First Name"], emp["Last Name"])
        # Generate and add the salary.
        emp["Salary"] = generate_salary(emp["Job ID"], emp["State"])
        #add proccesed employees to valid employees
        valid_employees.append(emp)
    #returning list of dictionaries for valid employees
    return valid_employees
    
#reading employeed data as employee      
employees = get_json_content('test_file.json')
# return a list of dictionaries with data for each employee
processed = process_each_emp(employees)
print(processed)



