import pytest
from unittest.mock import MagicMock
from application.signup_service import SignUpService
from domain.exceptions import DomainValidationError, CognitoError

VALID_PAYLOAD = {
    "email": "test@example.com",
    "password": "Password1!",
    "name": "John Doe",
    "birthdate": "1990-01-01",
    "gender": "male",
    "phone_number": "+1234567890"
}

def test_signup_success():
    # Mock del repositorio
    mock_repo = MagicMock()
    mock_repo.create_user.return_value = {"User": "created"}

    service = SignUpService(mock_repo)

    result = service.signup(VALID_PAYLOAD)

    assert result["message"] == "User created successfully"
    assert result["user"] == VALID_PAYLOAD["email"]
    mock_repo.create_user.assert_called_once()


def test_signup_missing_fields():
    service = SignUpService(MagicMock())

    invalid_payload = VALID_PAYLOAD.copy()
    invalid_payload.pop("email")

    with pytest.raises(DomainValidationError):
        service.signup(invalid_payload)


def test_signup_invalid_password():
    service = SignUpService(MagicMock())

    invalid_payload = VALID_PAYLOAD.copy()
    invalid_payload["password"] = "abc"  # No cumple los requisitos

    with pytest.raises(DomainValidationError):
        service.signup(invalid_payload)


def test_signup_cognito_error():
    mock_repo = MagicMock()
    mock_repo.create_user.side_effect = CognitoError("Cognito failure")

    service = SignUpService(mock_repo)

    with pytest.raises(CognitoError):
        service.signup(VALID_PAYLOAD)
