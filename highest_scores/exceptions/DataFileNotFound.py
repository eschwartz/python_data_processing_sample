from highest_scores.exceptions.DataProcessingException import DataProcessingException


class DataFileNotFound(DataProcessingException):
    """
    Indicates that the provided data file cannot be found
    """

    def __init__(self, file_path):
        message = f"Data file not found at {file_path}"
        super().__init__(message, exit_code=1)
