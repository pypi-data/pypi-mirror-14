class ArgumentError(Exception):
    """Class to handle bad arguments."""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class MissingResourceId(Exception):
    """Class to handle missing required argument on resource init."""
    pass
