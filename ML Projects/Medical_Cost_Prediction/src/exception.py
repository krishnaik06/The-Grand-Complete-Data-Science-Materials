'''
Custom Exception Handling
'''

import sys

# a function to load the execution information and return the error message
def error_message_details(error, error_details:sys):
    # exc_info() returns the information about the error
    _,_,exc_tb = error_details.exc_info()

    # get file name from the exc_info() function
    file_name = exc_tb.tb_frame.f_code.co_filename

    # construct the error message to return
    error_message = "Error occured in Python script [{0}] at line number [{1}] error message [{2}]".format(file_name, exc_tb.tb_lineno, str(error))

    return error_message

# Inheriting the Exception class
class CustomException(Exception):
    def __init__(self, error_message, error_details:sys) -> None:
        super().__init__(error_message)
        self.error_message = error_message_details(error_message, error_details=error_details)

    def __str__(self):
        return self.error_message