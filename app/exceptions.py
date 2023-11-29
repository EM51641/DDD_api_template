class NoEntityFoundError(Exception):
    """
    Exception raised when no entity is found.
    """

    def __init__(self, message: str = "No entity found") -> None:
        super().__init__(message)


class NoPartFound(Exception):
    """
    Exception raised when no entity is found.
    """

    def __init__(self, message: str = "No part found") -> None:
        super().__init__(message)
