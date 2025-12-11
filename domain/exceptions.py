class DomainValidationError(Exception):
    """Raised when business validation fails."""


class CognitoError(Exception):
    """Raised when Cognito returns an error."""
