# Emapix specific exceptions

# Temporary solution


class ServiceException(Exception):
    """Exception related to service."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
