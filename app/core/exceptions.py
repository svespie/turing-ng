class HostVerificationError(Exception):
    """
    Raised when a host cannot be reached or verified.
    """

class ModelVerificationError(Exception):
    """
    Raised when a model cannot be verified.
    """

class ChatResponseError(Exception):
    """
    Raised when model interaction fails.
    """