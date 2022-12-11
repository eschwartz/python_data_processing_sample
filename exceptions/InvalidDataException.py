from exceptions.DataProcessingException import DataProcessingException

class InvalidDataException(DataProcessingException):
    """
    Indicates that some data is invalid, and cannot be parsed
    """
    
    def __init__(self, line_no, message):
        message = f"Invalid data at line {line_no}:\n{message}"
        super().__init__(message, exit_code=2)