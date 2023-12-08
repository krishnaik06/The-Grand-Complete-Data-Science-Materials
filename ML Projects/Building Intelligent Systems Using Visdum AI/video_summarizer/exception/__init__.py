import os, sys

class CustomException(Exception):

    def __init__(self,error_message:Exception,error_details:sys):
        self.error_message = CustomException.get_detailed_error_message(error_message=error_message,
                                                                        error_details=error_details)
        
    @staticmethod
    def get_detailed_error_message(error_message:Exception,error_details:sys)->str:
            _,_, exec_tb= error_details.exc_info()

            # a, b, c = 1,2,3 -> _, _, c 

            exception_block_line_number =exec_tb.tb_frame.f_lineno # 
            try_block_line_number =exec_tb.tb_lineno 
            file_name=exec_tb.tb_frame.f_code.co_filename

            error_message = f"""
            Error occurred in execution of :
            [{file_name}] at
            try block line number : [{try_block_line_number}]
            and exception block line number : [{exception_block_line_number}]
            error message : [{error_message}]
            
            """

            return error_message
    
    def __str__(self): 
        """
        Formating how a object should be visible if used in print statement.
        """
        return self.error_message
    
    def __repr__(self):
        return CustomException.__name__.str()
        

        
        


