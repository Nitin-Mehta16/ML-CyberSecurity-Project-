import sys 
from NetworkSecurity.logging import logger

class CustomException(Exception):
    def __init__(self,error, error_detail:sys):
        _,_,exc_tb = error_detail.exc_info()

        self.file_name = exc_tb.tb_frame.f_code.co_filename
        self.line_no = exc_tb.tb_lineno
        self.error = error
        
    def __str__(self):
        error_message = "Error occured in python ⚠️⚠️ script name --> [{0}], line number--> [{1}], error message --> [{2}]".format(
        self.file_name,self.line_no,str(self.error) )

        return error_message
    
# if __name__ == "__main__":
#     try:
#         a=1/0
#     except Exception as e:
#         logger.logging.info("Divide by zero")
#         raise CustomException(e,sys)