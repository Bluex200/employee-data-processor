import os
import unittest
from unittest.mock import MagicMock, patch
import sys
from contextlib import contextmanager

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


class TestUsrInputMethods(unittest.TestCase):
    '''This class tests all the methods in the usr_input.py
       script to ensure they work as intended.'''
    
    test_dir = os.getcwd()
    test_subdir = test_dir + os.sep + 'test_files'

    def setUp(self):
        '''Runs before each test case.'''
        # in case of errors display
        # untruncated tuple with paths
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


    ### get_usr_input(prompt) ###
    def test01_get_usr_input_is_called_once_only_and_with_correct_message(self):
        '''Ensure get_usr_input is called once with correct message.'''
        msg = "test01_get_usr_input_is_called_once_only_and_with_correct_message:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')
        # arrange
        usr_input.get_usr_input = MagicMock()
        argument = 'Please enter the path of the file or the folder containing the files: '       
        # act & assert
        # discard the output from main() as not needed
        with open(os.devnull, "w") as f:
            with stdout_redirected(f):       
                with self.assertRaises(SystemExit) as se:
                    actual_main_return = main.main()
        usr_input.get_usr_input.assert_called_once_with(argument)       
        print("\033[91m ok\n")

                
    ### 1. passing a folder ###
    @patch('usr_input.get_usr_input')
    def test02_get_usr_input_returns_inexistent_path_entered_by_user(self, mock_get_usr_input):
        '''Ensure get_usr_input returns the path entered by the user -
           case of inexistent path.'''
        msg = "test02_get_usr_input_returns_inexistent_path_entered_by_user:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')
        # arrange
        mock_get_usr_input.return_value = self.test_subdir + os.sep + 'inexistent_path'
        expected_out_msg = mock_get_usr_input.return_value + ' does not exist.\n'
        # act & assert
        # check if sys.exit() used to exit the script
        with open(self.test_subdir + os.sep + 'out_test_inexistent_path.txt', "w") as f:
            with stdout_redirected(f):
                with self.assertRaises(SystemExit) as se:
                    actual_main_return = main.main()
        # check the displayed message
        with open(self.test_subdir + os.sep + 'out_test_inexistent_path.txt', "r") as f:
            actual_out_msg = f.read()
        self.assertEqual(actual_out_msg, expected_out_msg)
        os.remove(os.path.join(self.test_subdir, 'out_test_inexistent_path.txt'))
        print("\033[91m ok\n")


    @patch('usr_input.get_usr_input')
    def test03_get_usr_input_returns_path_entered_by_user_with_no_files_and_no_employees_to_process(self, mock_get_usr_input):
        '''Ensure get_usr_input returns the path entered by the user -
           case of path with no files and employees to process.'''
        msg = "test03_get_usr_input_returns_path_entered_by_user_with_no_files_and_no_employees_to_process:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')
        # arrange
        mock_get_usr_input.return_value = self.test_subdir + os.sep + 'test_folder'
        expected_out_msg = 'There are no valid files to process in the folder provided.\n'
        # act & assert
        # check if sys.exit() used to exit the script
        with open(self.test_subdir + os.sep + 'out_test_no_files_to_process.txt', "w") as f:
            with stdout_redirected(f):
                with self.assertRaises(SystemExit) as se:
                    actual_main_return = main.main()
        # check the displayed message
        with open(self.test_subdir + os.sep + 'out_test_no_files_to_process.txt', "r") as f:
            actual_out_msg = f.read()
        self.assertEqual(actual_out_msg, expected_out_msg)
        os.remove(os.path.join(self.test_subdir, 'out_test_no_files_to_process.txt'))
        print("\033[91m ok\n")


    @patch('usr_input.get_usr_input')
    def test04_get_usr_input_returns_path_entered_by_user_with_2_files_and_4_employees_to_process(self, mock_get_usr_input):
        '''Ensure get_usr_input returns the path entered by the user -
           case of path with 2 files and 4 employees to process.'''  
        msg = "test04_get_usr_input_returns_path_entered_by_user_with_2_files_and_4_employees_to_process:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')
        # arrange
        mock_get_usr_input.return_value = self.test_subdir
        expected_main_return = None
        # act
        with open(self.test_subdir + os.sep + 'out_file_2_4.txt', "w") as f:
            with stdout_redirected(f):
                actual_main_return = main.main()
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


    @patch('usr_input.get_usr_input')
    def test05_get_usr_input_returns_path_entered_by_user_with_3_files_and_6_employees_to_process(self, mock_get_usr_input):
        '''Ensure get_usr_input returns the path entered by the user -
           case of path with 3 files and 6 employees to process.''' 
        msg = "test05_get_usr_input_returns_path_entered_by_user_with_3_files_and_6_employees_to_process:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')
        # arrange
        mock_get_usr_input.return_value = self.test_dir
        expected_main_return = None
        # act
        with open(self.test_dir + os.sep + 'out_file_3_6.txt', "w") as f:
            with stdout_redirected(f):
                actual_main_return = main.main()
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


    @patch('usr_input.get_usr_input')
    def test06_get_usr_input_returns_path_entered_by_user_containing_formatted_and_unformatted_files_to_ignore_formated_json_files(self, mock_get_usr_input):
        '''Ensure get_usr_input returns the path entered by the user -
           case of path with already formatted files
           (ensure formatted json files are skipped).'''
        msg = "test06_get_usr_input_returns_path_entered_by_user_containing_formatted_and_unformatted_files_to_ignore_formated_json_files:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')
        # arrange
        # generate formatted JSON files
        with open(self.test_dir + os.sep + 'file_1_formatted.json', 'w') as f:
            pass
        with open(self.test_subdir + os.sep + 'file_2_formatted.json', 'w') as f:
            pass
        with open(self.test_subdir + os.sep + 'file_3_formatted.json', 'w') as f:
            pass
        mock_get_usr_input.return_value = self.test_dir
        expected_main_return = None
        # act
        with open(self.test_dir + os.sep + 'out_file_3_6.txt', "w") as f:
            with stdout_redirected(f):
                actual_main_return = main.main()
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


    ### get_usr_input(prompt) ###
    ### 2. passing a file ###
    @patch('usr_input.get_usr_input')        
    def test07_get_usr_input_returns_path_for_unformated_json_file_entered_by_user(self, mock_get_usr_input):
        '''Ensure get_usr_input returns the path entered by the user -
           case when passed a file path to unformated json file.'''
        msg = "test07_get_usr_input_returns_path_for_unformated_json_file_entered_by_user:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')
        # arrange
        mock_get_usr_input.return_value = self.test_subdir + os.sep +  '01_three_dict.json'
        expected_main_return = None
        # act
        with open(self.test_subdir + os.sep + 'out_file_1_3.txt', "w") as f:
            with stdout_redirected(f):
                actual_main_return = main.main()
        # assert
        with open(self.test_subdir + os.sep + 'out_file_1_3.txt', "r") as f:
            out_file_1_3 = f.read()
        with open(self.test_subdir + os.sep + 'test_file_1_3.txt', "r") as f:
            test_file_1_3 = f.read()
        # check the displayed report
        self.assertEqual(out_file_1_3, test_file_1_3)
        # check the returned value from main
        self.assertEqual(actual_main_return, expected_main_return)
        os.remove(os.path.join(self.test_subdir, 'out_file_1_3.txt'))
        print("\033[91m ok\n")


    @patch('usr_input.get_usr_input')
    def test08_get_usr_input_returns_path_for_formated_json_file_entered_by_user(self, mock_get_usr_input):
        '''Ensure get_usr_input returns the path entered by the user -
           case when the file provided is already processed.'''
        msg = "test08_get_usr_input_returns_path_for_formated_json_file_entered_by_user:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')
        # arrange
        # generate a formatted JSON file
        with open(self.test_subdir + os.sep + 'file_1_formatted.json', 'w') as f:
            pass
        mock_get_usr_input.return_value = self.test_subdir + os.sep + 'file_1_formatted.json'
        expected_out_msg = 'The file provided is already processed.\n'
        # act & assert
        with open(self.test_subdir + os.sep + 'out_test_file_already_processed.txt', "w") as f:
            with stdout_redirected(f):
                with self.assertRaises(SystemExit) as se:
                    actual_main_return = main.main()
        with open(self.test_subdir + os.sep + 'out_test_file_already_processed.txt', "r") as f:
            actual_out_msg = f.read()
        # check the displayed message
        self.assertEqual(actual_out_msg, expected_out_msg)
        os.remove(os.path.join(self.test_subdir, 'out_test_file_already_processed.txt'))
        print("\033[91m ok\n")


    ### check_path(file_path, data_files) ###
    ### 1. passing a folder ###
    def test09_check_path_returns_1_when_inexistent_path_passed(self):
        '''Ensure check_path returns int 1 when passed a path that does not exist.'''
        msg = "test09_check_path_returns_1_when_inexistent_path_passed:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')
        # arrange
        test_dummy = self.test_dir + os.sep + 'inexistent_path'
        expected_return = 1
        expected_out_msg = test_dummy + ' does not exist.\n'
        # act & assert
        with open(self.test_dir + os.sep + 'out_test_inexistent_path.txt', "w") as f:
            with stdout_redirected(f):
                actual_return = usr_input.check_path(test_dummy, [])
        with open(self.test_dir + os.sep + 'out_test_inexistent_path.txt', "r") as f:
            actual_out_msg = f.read()
        # check the displayed message
        self.assertEqual(actual_out_msg, expected_out_msg)
        # check the returned int value
        self.assertIsInstance(actual_return, int)
        self.assertEqual(actual_return, expected_return)        
        os.remove(os.path.join(self.test_dir, 'out_test_inexistent_path.txt'))
        print("\033[91m ok\n")


    def test10_check_path_returns_tuple_with_multiple_paths_for_folder_with_and_subfolders_without_unformated_json_files(self):
        '''Ensure check_path returns a tuple when passed a path containing unformated json files.'''        
        msg = "test10_check_path_returns_tuple_with_multiple_paths_for_folder_with_and_subfolders_without_unformated_json_files:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')        
        # arrange
        '''
        lst_expected_return = []
        for file_name in os.listdir(self.test_subdir):
            if file_name.endswith(".json") and not file_name.endswith("_formatted.json"):
                lst_expected_return.append(self.test_subdir + os.sep + file_name)
        expected_return = tuple(lst_expected_return)
        '''
        expected_return = (self.test_subdir + os.sep + '01_one_dict.json',
                           self.test_subdir + os.sep + '01_three_dict.json')
        # act
        actual_return = tuple(sorted(usr_input.check_path(self.test_subdir, [])))
        # assert
        self.assertIsInstance(actual_return, tuple)
        self.assertEqual(actual_return, expected_return)
        print("\033[91m ok\n")


    def test11_check_path_returns_tuple_with_multiple_paths_for_folder_with_and_subfolders_with_unformated_json_files(self):
        '''Ensure check_path returns a tuple with multiple valid file paths
           if passed a folder containning unformated json files and subfolders.
           It should check the folder and its subfolders for valid files.'''
        msg = "test11_check_path_returns_tuple_with_multiple_paths_for_folder_with_and_subfolders_with_unformated_json_files:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')        
        # arrange
        expected_return = (self.test_dir + os.sep + 'test_file.json',
                           self.test_subdir + os.sep + '01_one_dict.json',
                           self.test_subdir + os.sep + '01_three_dict.json')
        # act
        actual_return = usr_input.check_path(self.test_dir, [])
        # assert
        self.assertIsInstance(actual_return, tuple)
        self.assertEqual(actual_return, expected_return)
        print("\033[91m ok\n")


    def test12_check_path_returns_empty_tuple_for_path_without_unformated_json_files(self):
        '''Ensure check_path returns an empty tuple for a path without any unformated json files.'''
        msg = "test12_check_path_returns_empty_tuple_for_path_without_unformated_json_files:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')        
        # arrange
        test_sub_subdir = self.test_subdir + os.sep + 'test_folder'
        expected_return = ()
        # act
        actual_return = usr_input.check_path(test_sub_subdir, [])
        # assert
        self.assertEqual(actual_return, expected_return)
        print("\033[91m ok\n")


    def test13_tuple_returned_by_check_path_does_not_include_formated_json_files(self):
        '''Ensure the tuple returned by check_path does not include any path 
           with json files that have _formatted appended at the end
           (ensure formatted json files are skipped).'''
        msg = "test13_tuple_returned_by_check_path_does_not_include_formated_json_files:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')        
        # arrange
        # generate formatted JSON files
        with open(self.test_dir + os.sep + 'file_1_formatted.json', 'w') as f:
            pass
        with open(self.test_subdir + os.sep + 'file_2_formatted.json', 'w') as f:
            pass
        with open(self.test_subdir + os.sep + 'file_3_formatted.json', 'w') as f:
            pass
        incorrect_return = (self.test_dir + os.sep + 'file_1_formatted.json',
                            self.test_subdir + os.sep + 'file_2_formatted.json',
                            self.test_subdir + os.sep + 'file_3_formatted.json')
        # act
        actual_return = usr_input.check_path(self.test_dir, [])
        # assert
        self.assertNotIn(actual_return[0], incorrect_return)
        self.assertNotIn(actual_return[1], incorrect_return)
        self.assertNotIn(actual_return[2], incorrect_return)
        print("\033[91m ok\n")


    ### check_path(file_path, data_files) ###
    ### 2. passing a file ###
    def test14_check_path_returns_tuple_with_same_file_for_unformated_json_file(self):
        '''If passed a file path to unformated json file, ensure check_path
           returns a tuple with the same unformated json file.'''
        msg = "test14_check_path_returns_tuple_with_same_file_for_unformated_json_file:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')        
        # arrange
        test_file = self.test_dir + os.sep + 'test_file.json'
        expected_return = (test_file,)
        # act
        actual_return = usr_input.check_path(test_file, [])
        # assert
        self.assertEqual(actual_return, expected_return)
        print("\033[91m ok\n")


    def test15_check_path_returns_2_for_formated_json_file(self):
        '''Ensure check_path returns int 2 when passed an already formatted JSON file.'''
        msg = "test15_check_path_returns_2_for_formated_json_file:"
        print()
        print("\033[1;32;40m" + msg + "\033[0m" + "\033[91m ...", end='')        
        # arrange
        # generate a formatted JSON file
        with open(self.test_dir + os.sep + 'file_1_formatted.json', 'w') as f:
            pass
        test_file = self.test_dir + os.sep + 'file_1_formatted.json'
        expected_return = 2
        # act
        actual_return = usr_input.check_path(test_file, [])
        # assert
        self.assertEqual(actual_return, expected_return)
        print("\033[91m ok\n")


if __name__ == '__main__':
    unittest.main()
