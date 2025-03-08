class ResourceNotFoundError(Exception):
    """Exception raised when a resource is not found."""
    def __init__(self, message="Resource not found"):
        self.message = message
        super().__init__(self.message)

class ValidationError(Exception):
    """Exception raised for validation errors."""
    def __init__(self, message="Validation error", errors=None):
        self.message = message
        self.errors = errors or {}
        super().__init__(self.message)
