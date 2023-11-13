
class InvalidOperationException(Exception):
    """
    Exception raised when an operation can't be performed
    """

    def __init__(self, *args,  msg=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg = msg
