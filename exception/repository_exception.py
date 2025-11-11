class RepositoryException(Exception):
    """Custom exception for repository errors with context."""

    def __init__(self, message: str, context: dict = None):
        """
        Args:
            message (str): The error message.
            context (dict, optional): Additional context info for debugging.
        """
        if not message:
            raise ValueError("RepositoryException requires a message parameter")
        super().__init__(message)
        self.context = context

    def __str__(self):
        base_msg = super().__str__()
        if self.context:
            base_msg += f" | Context: {self.context}"
        return base_msg