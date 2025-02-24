import json
import os
import unittest
from unittest.mock import patch
import sys
from contextlib import contextmanager

import parse_file

@contextmanager
def stdout_redirected(new_stdout):  # https://peps.python.org/pep-0343/
    '''Redirect stdout temporarily.'''
    save_stdout = sys.stdout
    sys.stdout = new_stdout
    try:
        yield None
    finally:
        sys.stdout = save_stdout


class TestParseFileMethods(unittest.TestCase):
    '''This class tests all methods in the parse_file.py
       script to ensure they work as intended.'''

    test_dir = os.getcwd() + os.sep + 'test_files'
    list_one_dict_raw = []
    list_three_dict_raw = []
    list_one_dict_formatted = [
        {"First Name": "John", "Last Name": "Smith", "Date Of Birth (mm/dd/yyyy)":  "05/27/1995", "Phone Number": 7390521875,
          "Address Line 1": "11002 62nd Ave", "Address Line 2": "Puyallup", "City": "Washington", "State": "WA", "Zip Code": 98373,
         "Job Title": "Project Manager", "Job ID": "IT_MNG", "Company Email": "jsmith@comp.com", "Salary": 85200}]
    list_three_dict_formatted = [
        {"First Name": "Peter", "Last Name": "Parker", "Date Of Birth (mm/dd/yyyy)": "9/09/1977", "Phone Number": 1234561234,
        "Address Line 1": "1521 Farley Terrace", "Address Line 2": "Flat 4", "City": "Sandston", "State": "VA", "Zip Code": 23150,
        "Job Title": "Software Developer", "Job ID": "IT_REP", "Company Email": "pparker@comp.com", "Salary": 80000},
        {"First Name": "Lesly", "Last Name": "Jones", "Date Of Birth (mm/dd/yyyy)": "5/18/1979", "Phone Number": 9876543210,
        "Address Line 1": "10801 Decker Ln", "Address Line 2": "3rd Floor", "City": "Austin", "State": "TX", "Zip Code": 78724,
        "Job Title": "Sales Manager", "Job ID": "SA_MNG", "Company Email": "ljones@comp.com", "Salary": 63000},
        {"First Name": "Ellie", "Last Name": "Davis", "Date Of Birth (mm/dd/yyyy)": "3/21/1998", "Phone Number": 5553214443,
        "Address Line 1": "368 Paris Hill Ave.", "Address Line 2": "Brooklyn", "City": "New York", "State": "NY", "Zip Code": 11238,
        "Job Title": "Hr Representative", "Job ID": "HR_REP", "Company Email": "edavis@comp.com", "Salary": 71050}]
    base_salaries_dict = {"SA": 60000, "HR": 70000, "IT": 80000}
    rep_list = ["SA_REP", "HR_REP", "IT_REP"]
    mng_list = ["SA_MNG", "HR_MNG", "IT_MNG"]
    exp_state_list = ["NY", "CA", "OR", "WA", "VT"]
    state_list = ["AK", "AL", "AR", "AZ", "CO", "CT", "DE", "FL", "GA", "HI", "IA",
                 "ID", "IL", "IN", "KS", "KY", "LA", "MA", "MD", "ME", "MI", "MN", 
                 "MO", "MS", "MT", "NC", "ND", "NE", "NH", "NJ", "NM", "NV", "OH", 
                 "OK", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VA", "WI", "WV", "WY"]


    def setUp(self):
        '''Runs before each test case.'''
        # in case of errors display
        # untruncated list of dictionaries
        self.maxDiff = None
        self.list_one_dict_raw = [
            {"First Name": " John ", "Last Name": "sMIth   ", "Date Of Birth (mm/dd/yyyy)": "05/27/1995", "Phone Number": " 7390521875",
             "Address Line 1": " 11002  62ND   AVE  ",  "Address Line 2": "  PUYALLUP", "City": "  washingTon ", "State": "WA",
             "Zip Code": "98373", "Job Title": "project manager", "Job ID": "IT_MNG",
             "I declare that the above information is accurate.": ":selected:" }]
        self.list_three_dict_raw = [
            {"First Name": " Peter", "Last Name": "   parKeR", "Date Of Birth (mm/dd/yyyy)": "9/09/1977", "Phone Number": " 1234561234  ",
             "Address Line 1": " 1521 farley Terrace", "Address Line 2": "flat   4 ", "City": "  SandSton", "State": "VA", "Zip Code": "23150",
             "Job Title": "  software Developer", "Job ID": "IT_REP",
             "I declare that the above information is accurate.": ":selected:"},
            {"First Name": "lesly", "Last Name": " jones ", "Date Of Birth (mm/dd/yyyy)": "5/18/1979", "Phone Number": "9876543210  ",
             "Address Line 1": "10801 DECKER LN ", "Address Line 2": "  3rd floor ", "City": "AUSTIN  ", "State": "TX",
             "Zip Code": "  78724", "Job Title": "Sales   manager  ", "Job ID": "SA_MNG",
             "I declare that the above information is accurate.": ":selected:"},
            {"First Name": "ElLie ", "Last Name": "Davis", "Date Of Birth (mm/dd/yyyy)": "3/21/1998", "Phone Number": "5553214443",
             "Address Line 1": " 368 paris Hill   AVE. ", "Address Line 2": " Brooklyn", "City": "  New   york  ", "State": "NY",
             "Zip Code": " 11238  ", "Job Title": " HR REPRESENTATIVE ", "Job ID": "HR_REP",
             "I declare that the above information is accurate.": ":selected:"}]
    
    
    def tearDown(self):
        '''Runs after each test case.'''
        # Remove any formatted json files that are made while testing.
        for file in os.listdir(self.test_dir):
            if os.path.join(self.test_dir, file).endswith("_formatted.json"):
                os.remove(os.path.join(self.test_dir, file))


    ### generate_email(first_name, last_name) ###
    def test01_generate_email_returns_str_with_correct_format(self):
        '''Ensure generate_email returns a string in the following format:
           <first letter of first_name><last_name>@comp.com
           all in lower case.'''
        msg = "test01_generate_email_returns_str_with_correct_format:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')        
        first_name = "John"
        last_name = "SmITh"
        expected_email = "jsmith@comp.com"
        actual_email = parse_file.generate_email(first_name, last_name)
        self.assertIsInstance(actual_email, str)
        self.assertEqual(actual_email, expected_email)
        print("\033[91m ok\n")


    ### generate_formatted_file(emp_list, orig_path) ###
    def test02_generate_formatted_file_creates_file_named_orig_file_name_with_formatted_appended(self):
        '''Ensure generate_formatted_file creates a json file named
           after the original file with _formatted appended at the end.
           The test file is written in the same directory as the test.'''
        msg = "test02_generate_formatted_file_creates_file_named_orig_file_name_with_formatted_appended:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')        
        orig_path = os.path.join(self.test_dir, "test_create_file.json")
        expected_file_name = os.path.join(self.test_dir, "test_create_file_formatted.json")
        parse_file.generate_formatted_file(self.list_one_dict_formatted, orig_path)
        self.assertTrue(os.path.exists(expected_file_name))
        print("\033[91m ok\n")


    def test03_generate_formatted_file_writes_contents_of_emp_list_to_file(self):
        '''Ensure generate_formatted_file writes the list of dictionaries
           in emp_list to the saved json file.
           The test file is written in the same directory as the test.'''
        msg = "test03_generate_formatted_file_writes_contents_of_emp_list_to_file:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')        
        orig_path = os.path.join(self.test_dir, "test_file_contents.json")
        expected_file_name = os.path.join(self.test_dir, "test_file_contents_formatted.json")
        parse_file.generate_formatted_file(self.list_one_dict_formatted, orig_path)
        if os.path.exists(expected_file_name):
            with open(expected_file_name) as test_file:
                actual_emp_list = json.load(test_file)
            self.assertEqual(actual_emp_list, self.list_one_dict_formatted)
        else:
            self.assertTrue(False, "The file was not created, cannot test contents")
        print("\033[91m ok\n")


    ### generate_salary(job_id, state) ###
    def test04_generate_salary_returns_80000_when_passed_IT_REP_and_FL(self):
        '''Ensure generate_salary returns the base salary
           when passed job id IT_REP and state FL.'''
        msg = "test04_generate_salary_returns_80000_when_passed_IT_REP_and_FL:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')        
        # arrange
        job_id = 'IT_REP'
        state = 'FL'
        expected_salary = 80000
        # act
        actual_salary = parse_file.generate_salary(job_id, state)
        # assess
        self.assertIsInstance(actual_salary, int)
        self.assertEqual(actual_salary, expected_salary)
        print("\033[91m ok\n")


    def test05_generate_salary_returns_81200_when_passed_IT_REP_and_NY(self):
        '''Ensure generate_salary returns an extra 1.5% on top of
           the base salary when passed job id IT_REP and state NY.'''
        msg = "test05_generate_salary_returns_81200_when_passed_IT_REP_and_NY:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')        
        # arrange
        job_id = 'IT_REP'
        state = 'NY'
        expected_salary = 81200
        # act
        actual_salary = parse_file.generate_salary(job_id, state)
        # assess
        self.assertIsInstance(actual_salary, int)
        self.assertEqual(actual_salary, expected_salary)
        print("\033[91m ok\n")


    def test06_generate_salary_returns_84000_when_passed_IT_MNG_and_TX(self):
        '''Ensure generate_salary returns an extra 5% on top of
           the base salary when passed job id IT_MNG and state TX.'''
        msg = "test06_generate_salary_returns_84000_when_passed_IT_MNG_and_TX:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')        
        # arrange
        job_id = 'IT_MNG'
        state = 'TX'
        expected_salary = 84000
        # act
        actual_salary = parse_file.generate_salary(job_id, state)
        # assess
        self.assertIsInstance(actual_salary, int)
        self.assertEqual(actual_salary, expected_salary)
        print("\033[91m ok\n")


    def test07_generate_salary_returns_85200_when_passed_IT_MNG_and_CA(self):
        '''Ensure generate_salary returns an extra 6.5% on top of
           the base salary when passed job id IT_MNG and state CA.'''
        msg = "test07_generate_salary_returns_85200_when_passed_IT_MNG_and_CA:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')        
        # arrange
        job_id = 'IT_MNG'
        state = 'CA'
        expected_salary = 85200
        # act
        actual_salary = parse_file.generate_salary(job_id, state)
        # assess
        self.assertIsInstance(actual_salary, int)
        self.assertEqual(actual_salary, expected_salary)
        print("\033[91m ok\n")


    def test08_generate_salary_returns_70000_when_passed_HR_REP_and_AR(self):
        '''Ensure generate_salary returns the base salary
           when passed job id HR_REP and state AR.'''
        msg = "test08_generate_salary_returns_70000_when_passed_HR_REP_and_AR:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')
        # arrange
        job_id = 'HR_REP'
        state = 'AR'
        expected_salary = 70000
        # act
        actual_salary = parse_file.generate_salary(job_id, state)
        # assess
        self.assertIsInstance(actual_salary, int)
        self.assertEqual(actual_salary, expected_salary)
        print("\033[91m ok\n")


    def test09_generate_salary_returns_71050_when_passed_HR_REP_and_OR(self):
        '''Ensure generate_salary returns an extra 1.5% on top of
           the base salary when passed job id HR_REP and state OR.'''
        msg = "test09_generate_salary_returns_71050_when_passed_HR_REP_and_OR:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')        
        # arrange
        job_id = 'HR_REP'
        state = 'OR'
        expected_salary = 71050
        # act
        actual_salary = parse_file.generate_salary(job_id, state)
        # assess
        self.assertIsInstance(actual_salary, int)
        self.assertEqual(actual_salary, expected_salary)
        print("\033[91m ok\n")


    def test10_generate_salary_returns_73500_when_passed_HR_MNG_and_AL(self):
        '''Ensure generate_salary returns an extra 5% on top of
           the base salary when passed job id HR_MNG and state AL.'''
        msg = "test10_generate_salary_returns_73500_when_passed_HR_MNG_and_AL:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')        
        # arrange
        job_id = 'HR_MNG'
        state = 'AL'
        expected_salary = 73500
        # act
        actual_salary = parse_file.generate_salary(job_id, state)
        # assess
        self.assertIsInstance(actual_salary, int)
        self.assertEqual(actual_salary, expected_salary)
        print("\033[91m ok\n")


    def test11_generate_salary_returns_74550_when_passed_HR_MNG_and_WA(self):
        '''Ensure generate_salary returns an extra 6.5% on top of
           the base salary when passed job id HR_MNG and state WA.'''
        msg = "test11_generate_salary_returns_74550_when_passed_HR_MNG_and_WA:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')        
        # arrange
        job_id = 'HR_MNG'
        state = 'WA'
        expected_salary = 74550
        # act
        actual_salary = parse_file.generate_salary(job_id, state)
        # assess
        self.assertIsInstance(actual_salary, int)
        self.assertEqual(actual_salary, expected_salary)
        print("\033[91m ok\n")


    def test12_generate_salary_returns_60000_when_passed_SA_REP_and_OH(self):
        '''Ensure generate_salary returns the base salary
           when passed job id SA_REP and state OH.'''
        msg = "test12_generate_salary_returns_60000_when_passed_SA_REP_and_OH:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')        
        # arrange
        job_id = 'SA_REP'
        state = 'OH'
        expected_salary = 60000
        # act
        actual_salary = parse_file.generate_salary(job_id, state)
        # assess
        self.assertIsInstance(actual_salary, int)
        self.assertEqual(actual_salary, expected_salary)
        print("\033[91m ok\n")


    def test13_generate_salary_returns_60900_when_passed_SA_REP_and_VT(self):
        '''Ensure generate_salary returns an extra 1.5% on top of
           the base salary when passed job id SA_REP and state VT.'''
        msg = "test13_generate_salary_returns_60900_when_passed_SA_REP_and_VT:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')        
        # arrange
        job_id = 'SA_REP'
        state = 'VT'
        expected_salary = 60900
        # act
        actual_salary = parse_file.generate_salary(job_id, state)
        # assess
        self.assertIsInstance(actual_salary, int)
        self.assertEqual(actual_salary, expected_salary)
        print("\033[91m ok\n")


    def test14_generate_salary_returns_63000_when_passed_SA_MNG_and_TN(self):
        '''Ensure generate_salary returns an extra 5% on top of
           the base salary when passed job id SA_MNG and state TN.'''
        msg = "test14_generate_salary_returns_63000_when_passed_SA_MNG_and_TN:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')        
        # arrange
        job_id = 'SA_MNG'
        state = 'TN'
        expected_salary = 63000
        # act
        actual_salary = parse_file.generate_salary(job_id, state)
        # assess
        self.assertIsInstance(actual_salary, int)
        self.assertEqual(actual_salary, expected_salary)
        print("\033[91m ok\n")


    def test15_generate_salary_returns_63900_when_passed_SA_MNG_and_OR(self):
        '''Ensure generate_salary returns an extra 6.5% on top of
           the base salary when passed job id SA_MNG and state OR.'''
        msg = "test15_generate_salary_returns_63900_when_passed_SA_MNG_and_OR:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')        
        # arrange
        job_id = 'SA_MNG'
        state = 'OR'
        expected_salary = 63900
        # act
        actual_salary = parse_file.generate_salary(job_id, state)
        # assess
        self.assertIsInstance(actual_salary, int)
        self.assertEqual(actual_salary, expected_salary)
        print("\033[91m ok\n")


    ### get_json_content(file) ###
    def test16_get_json_content_returns_list_of_1_dict_when_passed_json_file_with_1_dict(self):
        '''Ensure get_json_content returns a list with 1 dictionary
           inside when passed a JSON file with 1 dictionary.
           The JSON file being passed is in the same folder as this test.'''
        msg = "test16_get_json_content_returns_list_of_1_dict_when_passed_json_file_with_1_dict:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')        
        one_dict_json_path = os.path.join(self.test_dir, "01_one_dict.json")
        actual_list_one_dict = parse_file.get_json_content(one_dict_json_path)
        self.assertEqual(actual_list_one_dict, self.list_one_dict_raw)
        print("\033[91m ok\n")


    def test17_get_json_content_returns_list_of_3_dicts_when_passed_json_file_with_3_dicts(self):
        '''Ensure get_json_content returns a list with 3 dictionaries
           inside when passed a JSON file.
           The JSON file being passed is in the same folder as this test.'''
        msg = "test17_get_json_content_returns_list_of_3_dicts_when_passed_json_file_with_3_dicts:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')        
        three_dict_json_path = os.path.join(self.test_dir, "01_three_dict.json")
        actual_list_three_dict = parse_file.get_json_content(three_dict_json_path)
        self.assertEqual(actual_list_three_dict, self.list_three_dict_raw)
        print("\033[91m ok\n")


    # ### process_each_emp(empList) ###
    @patch('parse_file.generate_salary')
    @patch('parse_file.generate_email')
    @patch('parse_file.validate_zip')
    @patch('parse_file.validate_phone_number')
    def test18_process_each_emp_returns_list_of_1_dict_when_passed_list_of_1_valid_dict(self, mock_phone_number, mock_zip_code,
                                                                                        mock_email, mock_salary):
        '''Ensure process_each_emp returns a list with 1 dictionary
           when passed a list with 1 dictionary with valid entries.
           The returned dictionary should follow the key names and
           value formatting/generation shown in the documentation.'''
        msg = "test18_process_each_emp_returns_list_of_1_dict_when_passed_list_of_1_valid_dict:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')        
        mock_phone_number.return_value = 7390521875
        mock_zip_code.return_value = 98373
        mock_email.return_value = "jsmith@comp.com"
        mock_salary.return_value = 85200
        actual_list_one_dict = parse_file.process_each_emp(self.list_one_dict_raw)
        self.assertEqual(actual_list_one_dict, self.list_one_dict_formatted)
        print("\033[91m ok\n")


    @patch('parse_file.generate_salary')
    @patch('parse_file.generate_email')
    @patch('parse_file.validate_zip')
    @patch('parse_file.validate_phone_number')
    def test19_process_each_emp_returns_list_of_3_dicts_when_passed_list_of_3_valid_dicts(self, mock_phone_number, mock_zip_code,
                                                                                          mock_email, mock_salary):
        '''Ensure process_each_emp returns a list with 3 dictionaries
           when passed a list with 3 dictionaries with valid entries.
           The returned dictionaries should follow the key names and
           value formatting/generation shown in the documentation.'''
        msg = "test19_process_each_emp_returns_list_of_3_dicts_when_passed_list_of_3_valid_dicts:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')        
        mock_phone_number.side_effect = [1234561234, 9876543210, 5553214443]
        mock_zip_code.side_effect = [23150, 78724, 11238]
        mock_email.side_effect = ["pparker@comp.com", "ljones@comp.com", "edavis@comp.com"]
        mock_salary.side_effect = [80000, 63000, 71050]    
        actual_list_three_dict = parse_file.process_each_emp(self.list_three_dict_raw)
        self.assertEqual(actual_list_three_dict, self.list_three_dict_formatted)
        print("\033[91m ok\n")


    @patch('parse_file.validate_phone_number')
    def test20_process_each_emp_returns_empty_list_when_passed_list_of_1_dict_with_invalid_phone_number(self, mock_phone_number):
        '''Ensure process_each_emp returns an empty list when passed a list 
           with 1 dictionary inside that has an invalid phone number.'''
        msg = "test20_process_each_emp_returns_empty_list_when_passed_list_of_1_dict_with_invalid_phone_number:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')        
        mock_phone_number.return_value = 1
        actual_list_one_dict = parse_file.process_each_emp(self.list_one_dict_raw)
        self.assertEqual(actual_list_one_dict, [])
        print("\033[91m ok\n")


    @patch('parse_file.validate_zip')
    def test21_process_each_emp_returns_empty_list_when_passed_list_of_1_dict_with_invalid_zip_code(self, mock_zip_code):
        '''Ensure process_each_emp returns an empty list when passed a list 
           with 1 dictionary inside that has an invalid zip code.'''
        msg = "test21_process_each_emp_returns_empty_list_when_passed_list_of_1_dict_with_invalid_zip_code:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')        
        mock_zip_code.return_value = 1
        actual_list_one_dict = parse_file.process_each_emp(self.list_one_dict_raw)
        self.assertEqual(actual_list_one_dict, [])
        print("\033[91m ok\n")


    @patch('parse_file.generate_salary')
    @patch('parse_file.generate_email')
    @patch('parse_file.validate_zip')
    @patch('parse_file.validate_phone_number')
    def test22_process_each_emp_returns_valid_list_of_1_dict_when_passed_list_of_3_dicts_with_invalid_phone_num_and_zip_code(self,
                                                                                                                             mock_phone_number,
                                                                                                                             mock_zip_code,
                                                                                                                             mock_email,
                                                                                                                             mock_salary):
        '''Ensure process_each_emp returns a list with 1 dictionary inside 
           after being passed a list with 3 dictionaries, but one has an
           invalid phone number and the other has an invalid zip code.'''
        msg = "test22_process_each_emp_returns_valid_list_of_1_dict_when_passed_list_of_3_dicts_with_invalid_phone_num_and_zip_code:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')        
        mock_phone_number.side_effect = [1, 9876543210, 5553214443]
        mock_zip_code.side_effect = [23150, 1, 11238]
        mock_email.side_effect = ["jsmith@comp.com", "ljones@comp.com", "edavis@comp.com"]
        mock_salary.side_effect = [80000, 63000, 71050]
        actual_list_three_dict_len = len(parse_file.process_each_emp(self.list_three_dict_raw))
        self.assertEqual(actual_list_three_dict_len, 1)
        print("\033[91m ok\n")


    ### validate_phone_number(phoneNumber) ###
    def test23_validate_phone_number_returns_10_digit_int_when_passed_valid_phone_number(self):
        '''Ensure validate_phone_number returns an int 10 digits
           in length when passed a valid phone number. A valid
           phone number is 10 digits with no other characters,
           ignoring any leading and/or trailing spaces.'''
        msg = "test23_validate_phone_number_returns_10_digit_int_when_passed_valid_phone_number:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')        
        expected_return = 1234789368
        actual_return_1 = parse_file.validate_phone_number("1234789368")
        actual_return_2 = parse_file.validate_phone_number("1234789368   ")
        actual_return_3 = parse_file.validate_phone_number(" 1234789368")
        actual_return_4 = parse_file.validate_phone_number(" 1234789368   ")       
        self.assertEqual(actual_return_1, expected_return)
        self.assertEqual(actual_return_2, expected_return)
        self.assertEqual(actual_return_3, expected_return)
        self.assertEqual(actual_return_4, expected_return)
        print("\033[91m ok\n")


    def test24_validate_phone_number_returns_1_when_passed_invalid_phone_number(self):
        '''Ensure validate_phone_number returns an int of 1
           when passed an invalid phone number.
           A valid phone number is 10 digits with no other characters.'''
        msg = "test24_validate_phone_number_returns_1_when_passed_invalid_phone_number:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')
        # arrange
        expected_return = 1
        # act
        with open(self.test_dir + os.sep + 'out_invalid_phone_numbers.txt', "w") as f:
            with stdout_redirected(f):
                actual_return_1 = parse_file.validate_phone_number("+1234567894")
                actual_return_2 = parse_file.validate_phone_number("+123-456-7894")
                actual_return_3 = parse_file.validate_phone_number("12345678945")
                actual_return_4 = parse_file.validate_phone_number("123456789")
                actual_return_5 = parse_file.validate_phone_number("123456789Z")
        with open(self.test_dir + os.sep + 'out_invalid_phone_numbers.txt', "r") as f:
            out_invalid_phone_numbers = f.read()
        with open(self.test_dir + os.sep + 'test_invalid_phone_numbers.txt', "r") as f:
            test_invalid_phone_numbers = f.read()
        # assert
        # check the displayed messages
        self.assertEqual(out_invalid_phone_numbers, test_invalid_phone_numbers)
        # check the returned int value
        self.assertEqual(actual_return_1, expected_return)
        self.assertEqual(actual_return_2, expected_return)
        self.assertEqual(actual_return_3, expected_return)
        self.assertEqual(actual_return_4, expected_return)
        self.assertEqual(actual_return_5, expected_return)
        os.remove(os.path.join(self.test_dir, 'out_invalid_phone_numbers.txt'))
        print("\033[91m ok\n")


    ### validate_zip(zipCode) ###
    def test25_validate_zip_returns_5_digit_int_when_passed_valid_zip_code(self):
        '''Ensure validate_zip returns an int 5 digits in length
           when passed a valid zip code.
           A valid zip code is 5 digits with no other characters,
           ignoring any leading and/or trailing spaces.'''
        msg = "test25_validate_zip_returns_5_digit_int_when_passed_valid_zip_code:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')        
        # arrange
        expected_return = 12347
        # act
        actual_return_1 = parse_file.validate_zip("12347")
        actual_return_2 = parse_file.validate_zip("12347   ")
        actual_return_3 = parse_file.validate_zip(" 12347")
        actual_return_4 = parse_file.validate_zip(" 12347   ")
        # assert
        self.assertEqual(actual_return_1, expected_return)
        self.assertEqual(actual_return_2, expected_return)
        self.assertEqual(actual_return_3, expected_return)
        self.assertEqual(actual_return_4, expected_return)
        print("\033[91m ok\n")


    def test26_validate_zip_returns_1_when_passed_invalid_zip_code(self):
        '''Ensure validate_zip returns an int of 1 when passed a valid zip code.
           A valid zip code is 5 digits with no other characters.'''
        msg = "test26_validate_zip_returns_1_when_passed_invalid_zip_code:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')
        # arrange
        expected_return = 1
        # act
        with open(self.test_dir + os.sep + 'out_invalid_zips.txt', "w") as f:
            with stdout_redirected(f):
                actual_return_1 = parse_file.validate_zip("+12345")
                actual_return_2 = parse_file.validate_zip("+12-3-45")
                actual_return_3 = parse_file.validate_zip("123456")
                actual_return_4 = parse_file.validate_zip("1234")
                actual_return_5 = parse_file.validate_zip("1234Z")
        with open(self.test_dir + os.sep + 'out_invalid_zips.txt', "r") as f:
            out_invalid_zips = f.read()
        with open(self.test_dir + os.sep + 'test_invalid_zips.txt', "r") as f:
            test_invalid_zips = f.read()
        # assert
        # check the displayed messages
        self.assertEqual(out_invalid_zips, test_invalid_zips)
        # check the returned int value
        self.assertEqual(actual_return_1, expected_return)
        self.assertEqual(actual_return_2, expected_return)
        self.assertEqual(actual_return_3, expected_return)
        self.assertEqual(actual_return_4, expected_return)
        self.assertEqual(actual_return_5, expected_return)
        os.remove(os.path.join(self.test_dir, 'out_invalid_zips.txt'))
        print("\033[91m ok\n")


if __name__ == '__main__':
    unittest.main()