'''
file: exception.py

This file handles all exceptions that occur during program execution and provides a concise error message in a single line:
"Error occurred in python script name [{0}], line number [{1}], error message [{2}]"
'''

# Required modules
import sys
from src.logger import logging

# Function for generating error details and returning an error message string in a single line
def error_message_detail(error, error_detail: sys):
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    message = 'Error occurred in python script name [{0}], line number [{1}], error message [{2}]'.format(
        file_name, exc_tb.tb_lineno, str(error))
    return message

# CustomException class which inherits from Exception class for handling CustomExceptions
class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        # Generate the error message detail using the error_message_detail function
        self.error_message = error_message_detail(error=error_message, error_detail=error_detail)

    def __str__(self):
        return self.error_message
