import json
import os
import sys
import unittest
from unittest.mock import patch
import sys
from contextlib import contextmanager

import parse_file
import usr_input
import main

@contextmanager
def stdout_redirected(new_stdout):  # https://peps.python.org/pep-0343/
    '''Redirect stdout temporarily.'''
    save_stdout = sys.stdout
    sys.stdout = new_stdout
    try:
        yield None
    finally:
        sys.stdout = save_stdout


class TestMainMethods(unittest.TestCase):
    '''This class tests all methods in the main.py
       script to ensure they work as intended.'''

    test_dir = os.getcwd()
    test_subdir = test_dir + os.sep + 'test_files'
    
    def setUp(self):
        '''Runs before each test case.'''
        # in case of errors display
        # untruncated list of dictionaries
        self.maxDiff = None


    def tearDown(self):
        '''Runs after each test case.'''
        # Remove any formatted json files that are made while testing.
        for file in os.listdir(self.test_dir):
            if os.path.join(self.test_dir, file).endswith("_formatted.json"):
                os.remove(os.path.join(self.test_dir, file))
        for file in os.listdir(self.test_subdir):
            if os.path.join(self.test_subdir, file).endswith("_formatted.json"):
                os.remove(os.path.join(self.test_subdir, file))


    ### error_handle(check_return) ###
    def test01_error_handle_exits_and_displays_correct_message_when_check_return_is_empty_tuple(self):
        '''Ensure error_handle exits and displays the following message:
           "There are no valid files to process in the folder provided."
           in case check_return is empty tuple.'''
        msg = "test01_error_handle_exits_and_displays_correct_message_when_check_return_is_empty_tuple:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')
        # arrange
        check_return = ()
        expected_out_msg = 'There are no valid files to process in the folder provided.\n'
        # act & assert
        with open(self.test_subdir + os.sep + 'out_test_no_files_to_process.txt', "w") as f:
            with stdout_redirected(f):
                with self.assertRaises(SystemExit) as se:
                    main.error_handle(check_return)
        # check the displayed message
        with open(self.test_subdir + os.sep + 'out_test_no_files_to_process.txt', "r") as f:
            actual_out_msg = f.read()
        message = "error_handle() should exit with this message when check_return is empty tuple:\n'" + expected_out_msg.rstrip('\n') + "'"
        if actual_out_msg == '':
            message = message + "\nInstead error_handle() displayed no message."
        else:
            message = message + "\nInstead error_handle() displayed this message:\n'" + actual_out_msg + "'"        
        self.assertEqual(actual_out_msg, expected_out_msg, msg=message)
        os.remove(os.path.join(self.test_subdir, 'out_test_no_files_to_process.txt'))
        print("\033[91m ok\n")


    def test02_error_handle_exits_with_no_message_when_check_return_is_1(self):
        '''Ensure error_handle exits with no message displayed when check return is 1.'''
        msg = "test02_error_handle_exits_with_no_message_when_check_return_is_1:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')
        # arrange
        check_return = 1
        expected_out_msg = ''
        # act & assert
        # check if sys.exit() used to exit the script
        with open(self.test_subdir + os.sep + 'out_test_invalid_path.txt', "w") as f:
            with stdout_redirected(f):
                with self.assertRaises(SystemExit) as se:
                    main.error_handle(check_return)        
        # check there is no message displayed
        with open(self.test_subdir + os.sep + 'out_test_invalid_path.txt', "r") as f:
            actual_out_msg = f.read()
        message = "error_handle() should exit with no message when check_return is 1."
        message = message + "\nInstead error_handle() displayed this message:\n'" + actual_out_msg + "'"
        self.assertEqual(actual_out_msg, expected_out_msg, msg=message)
        os.remove(os.path.join(self.test_subdir, 'out_test_invalid_path.txt'))
        print("\033[91m ok\n")


    def test03_error_handle_exits_and_displays_correct_message_when_check_return_is_2(self):
        '''Ensure error_handle exits and displays the following message:
           "The file provided is already processed."
           in case check_return is 2.'''
        msg = "test03_error_handle_exits_and_displays_correct_message_when_check_return_is_2:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')
        # arrange
        check_return = 2
        expected_out_msg = 'The file provided is already processed.\n'
        # act & assert
        # check if sys.exit() used to exit the script
        with open(self.test_subdir + os.sep + 'out_test_file_already_processed.txt', "w") as f:
            with stdout_redirected(f):
                with self.assertRaises(SystemExit) as se:
                    main.error_handle(check_return)
        # check the displayed message
        with open(self.test_subdir + os.sep + 'out_test_file_already_processed.txt', "r") as f:
            actual_out_msg = f.read()
        message = "error_handle() should exit with this message when check_return is 2:\n'" + expected_out_msg.rstrip('\n') + "'"
        if actual_out_msg == '':
            message = message + "\nInstead error_handle() displayed no message."
        else:
            message = message + "\nInstead error_handle() displayed this message:\n'" + actual_out_msg + "'"
        self.assertEqual(actual_out_msg, expected_out_msg, msg=message)
        os.remove(os.path.join(self.test_subdir, 'out_test_file_already_processed.txt'))
        print("\033[91m ok\n")


    ### start_process(tup) ###
    def test04_start_process_displays_correct_report_when_check_return_is_tuple_with_1_file_for_1_employee(self):
        '''Ensure start_process displays the report as required for print_output() in case"
           check_return is a tuple containing path to one valid json file to format.'''
        msg = "test04_start_process_displays_correct_report_when_check_return_is_tuple_with_1_file_for_1_employee:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')
        # arrange
        path_tuple = (self.test_subdir + os.sep + '01_one_dict.json',)
        expected_main_return = None
        # act
        with open(self.test_subdir + os.sep + 'out_file_1_1.txt', "w") as f:
            with stdout_redirected(f):
                actual_main_return = main.start_process(path_tuple)
        # assert
        with open(self.test_subdir + os.sep + 'out_file_1_1.txt', "r") as f:
            out_file_1_1 = f.read()
        with open(self.test_subdir + os.sep + 'test_file_1_1.txt', "r") as f:
            test_file_1_1 = f.read()
        # check the displayed report
        self.assertEqual(out_file_1_1, test_file_1_1)
        # check the returned value from main
        self.assertEqual(actual_main_return, expected_main_return)
        os.remove(os.path.join(self.test_subdir, 'out_file_1_1.txt'))
        print("\033[91m ok\n")


    def test05_start_process_displays_correct_report_when_check_return_is_tuple_with_2_files_for_4_employees(self):
        '''Ensure start_process displays the report as required for print_output() in case"
           check_return is a tuple containing paths to multiple json files to format.'''
        msg = "test05_start_process_displays_correct_report_when_check_return_is_tuple_with_2_files_for_4_employees:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')
        # arrange
        paths_tuple = (self.test_subdir + os.sep + '01_one_dict.json',
                       self.test_subdir + os.sep + '01_three_dict.json')
        expected_main_return = None
        # act
        with open(self.test_subdir + os.sep + 'out_file_2_4.txt', "w") as f:
            with stdout_redirected(f):
                actual_main_return = main.start_process(paths_tuple)
        # assert
        with open(self.test_subdir + os.sep + 'out_file_2_4.txt', "r") as f:
            out_file_2_4 = f.read()
        with open(self.test_subdir + os.sep + 'test_file_2_4.txt', "r") as f:
            test_file_2_4 = f.read()
        # check the displayed report
        self.assertEqual(out_file_2_4, test_file_2_4)
        # check the returned value from main
        self.assertEqual(actual_main_return, expected_main_return)
        os.remove(os.path.join(self.test_subdir, 'out_file_2_4.txt'))
        print("\033[91m ok\n")


    def test06_start_process_displays_correct_report_when_check_return_is_tuple_with_3_files_for_6_employees(self):
        '''Ensure start_process displays the report as required for print_output() in case"
           check_return is a tuple containing paths to 3 json files for 6 employees to format.'''
        msg = "test06_start_process_displays_correct_report_when_check_return_is_tuple_with_3_files_for_6_employees:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')
        # arrange
        paths_tuple = (self.test_dir + os.sep + 'test_file.json',
                       self.test_subdir + os.sep + '01_one_dict.json',
                       self.test_subdir + os.sep + '01_three_dict.json')
        expected_main_return = None
        # act
        with open(self.test_dir + os.sep + 'out_file_3_6.txt', "w") as f:
            with stdout_redirected(f):
                actual_main_return = main.start_process(paths_tuple)
        # assert
        with open(self.test_dir + os.sep + 'out_file_3_6.txt', "r") as f:
            out_file_3_6 = f.read()
        with open(self.test_dir + os.sep + 'test_file_3_6.txt', "r") as f:
            test_file_3_6 = f.read()
        # check the displayed report            
        self.assertEqual(out_file_3_6, test_file_3_6)
        # check the returned value from main       
        self.assertEqual(actual_main_return, expected_main_return)
        os.remove(os.path.join(self.test_dir, 'out_file_3_6.txt'))
        print("\033[91m ok\n")


    ### main() ###
    @patch('usr_input.get_usr_input')
    def test07_one_formatted_json_file_generated_for_path_to_unformatted_json_file(self, mock_get_usr_input):
        '''Ensure that path to an unformatted JSON file passed in input
           generates one JSON file in the same folder named as original"
           file followed by _formatted.'''
        msg = "test07_one_formatted_json_file_generated_for_path_to_unformatted_json_file:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')
        # arrange
        mock_get_usr_input.return_value = self.test_subdir + os.sep + '01_one_dict.json'
        expected_main_return = None
        # act
        # discard the output from main() as not needed
        with open(os.devnull, "w") as f:
            with stdout_redirected(f):
                actual_main_return = main.main()
        # assert
        # check that 01_one_dict_formatted.json has been created in self.test_subdir folder
        message = '\nThe formatted file for 01_one_dict.json has not been created in the folder ' + self.test_subdir
        self.assertIn('01_one_dict_formatted.json', os.listdir(self.test_subdir), msg=message)
        # check that only one formatted file has been created in self.test_subdir folder
        list_of_files = os.listdir(self.test_subdir)
        count_formatted_files = 0
        for file in list_of_files:
            if file.endswith("_formatted.json"):
                count_formatted_files += 1
        message = '\n' + str(count_formatted_files) + ' formatted files for 01_one_dict.json have been created in the folder ' + self.test_subdir
        self.assertEqual(count_formatted_files, 1, msg=message)    
        # check the returned value from main()
        self.assertEqual(actual_main_return, expected_main_return)        
        print("\033[91m ok\n")


    @patch('usr_input.get_usr_input')
    def test08_two_formatted_json_files_generated_for_path_to_folder_with_two_unformatted_json_files(self, mock_get_usr_input):
        '''Ensure that path to a folder containing two unformatted JSON
           files passed in input generates two JSON files in the same folder
           named as respective original file followed by _formatted.'''
        msg = "test08_two_formatted_json_files_generated_for_path_to_folder_with_two_unformatted_json_files:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')
        # arrange
        mock_get_usr_input.return_value = self.test_subdir
        expected_main_return = None
        # act
        # discard the output from main() as not needed
        with open(os.devnull, "w") as f:
            with stdout_redirected(f):
                actual_main_return = main.main()
        # assert
        # check that two formatted files have been created in self.test_subdir folder        
        message = '\nThe formatted file for 01_one_dict.json has not been created in the folder ' + self.test_subdir
        self.assertIn('01_one_dict_formatted.json', os.listdir(self.test_subdir), msg=message)
        message = '\nThe formatted file for 01_three_dict.json has not been created in the folder ' + self.test_subdir
        self.assertIn('01_three_dict_formatted.json', os.listdir(self.test_subdir), msg=message)
        # check that only two formatted files have been created in self.test_subdir folder
        list_of_files = os.listdir(self.test_subdir)
        count_formatted_files = 0
        for file in list_of_files:
            if file.endswith("_formatted.json"):
                count_formatted_files += 1
        message = '\n' + str(count_formatted_files) + ' formatted files for 01_one_dict.json and ' + \
                  '01_three_dict.json have been created in the folder ' + self.test_subdir
        self.assertEqual(count_formatted_files, 2, msg=message)    
        # check the returned value from main()
        self.assertEqual(actual_main_return, expected_main_return)        
        print("\033[91m ok\n")


    @patch('usr_input.get_usr_input')
    def test09_three_formatted_json_files_generated_for_path_to_folder_with_one_and_subfolder_with_two_unformatted_json_files(self, mock_get_usr_input):
        '''Ensure that path to a folder containing one unformatted JSON and
           subfolder containing two unformatted JSON files passed in input
           generates three JSON files in the same folder as respective
           original file(s) and named as respective original file followed
           by _formatted.'''
        msg = "test09_three_formatted_json_files_generated_for_path_to_folder_with_one_and_subfolder_with_two_unformatted_json_files:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')
        # arrange
        mock_get_usr_input.return_value = self.test_dir
        expected_main_return = None
        # act
        # discard the output from main() as not needed
        with open(os.devnull, "w") as f:
            with stdout_redirected(f):
                actual_main_return = main.main()
        # assert
        # check that one formatted file has been created in self.test_dir folder
        message = '\nThe formatted file for test_file.json has not been created in the folder ' + self.test_dir
        self.assertIn('test_file_formatted.json', os.listdir(self.test_dir), msg=message)
        # check that only one formatted file has been created in self.test_dir folder
        list_of_files = os.listdir(self.test_dir)
        count_formatted_files = 0
        for file in list_of_files:
            if file.endswith("_formatted.json"):
                count_formatted_files += 1
        message = '\n' + str(count_formatted_files) + ' formatted files for test_file.json have been created in this folder.'
        self.assertEqual(count_formatted_files, 1, msg=message)    
        # check that two formatted files have been created in self.test_subdir folder
        message = '\nThe formatted file for 01_one_dict.json has not been created in the folder ' + self.test_subdir
        self.assertIn('01_one_dict_formatted.json', os.listdir(self.test_subdir), msg=message)
        message = '\nThe formatted file for 01_three_dict.json has not been created in the folder ' + self.test_subdir
        self.assertIn('01_three_dict_formatted.json', os.listdir(self.test_subdir), msg=message)
        # check that only two formatted files have been created in self.test_subdir folder
        list_of_files = os.listdir(self.test_subdir)
        count_formatted_files = 0
        for file in list_of_files:
            if file.endswith("_formatted.json"):
                count_formatted_files += 1
        message = '\n' + str(count_formatted_files) + ' formatted files for 01_one_dict.json and 01_three_dict.json have been created in this folder.'
        self.assertEqual(count_formatted_files, 2, msg=message)    
        # check the returned value from main()
        self.assertEqual(actual_main_return, expected_main_return)        
        print("\033[91m ok\n")


    @patch('usr_input.get_usr_input')
    def test10_no_formatted_json_file_generated_for_path_to_folder_with_no_unformatted_json_files(self, mock_get_usr_input):
        '''Ensure that path to a folder containing no unformatted JSON
           files passed in input generates no JSON file in the same
           folder.'''
        msg = "test10_no_formatted_json_file_generated_for_path_to_folder_with_no_unformatted_json_files:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')
        # arrange
        mock_get_usr_input.return_value = self.test_subdir + os.sep + 'test_folder'
        # act
        # discard the output from main() as not needed
        with open(os.devnull, "w") as f:
            with stdout_redirected(f):
                with self.assertRaises(SystemExit) as se:
                    main.main()
        # assert
        message = '\nThere are formatted file(s) created in the folder ' + mock_get_usr_input.return_value
        # ensure there are no formatted JSON files in the folder provided
        list_of_files = os.listdir(mock_get_usr_input.return_value)
        list_of_formatted_files = []
        for file in list_of_files:
            if file.endswith("_formatted.json"):
                list_of_formatted_files.append(file)
        self.assertEqual(len(list_of_formatted_files), 0, msg=message)
        print("\033[91m ok\n")


if __name__ == '__main__':
    unittest.main()