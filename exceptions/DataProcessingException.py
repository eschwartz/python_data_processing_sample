class DataProcessingException(Exception):
    """
    Base exception for any errors from this
    data processing script.
    """
    def __init__(self, message, exit_code=1):
        self.exit_code = exit_code
        self.message = message
        super().__init__(message)