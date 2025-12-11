from domain.models import SignUpRequest
from utils.validation import validate_signup_data
from infrastructure.cognito_repository import CognitoRepository
from domain.exceptions import DomainValidationError
from utils.logger import get_logger

logger = get_logger(__name__)

class SignUpService:

    def __init__(self, cognito_repo: CognitoRepository):
        self.cognito_repo = cognito_repo

    def signup(self, payload: dict):
        logger.info("Executing signup service...")

        # Validación a nivel de dominio
        validate_signup_data(payload)

        signup_request = SignUpRequest(
            email=payload["email"],
            password=payload["password"],
            name=payload["name"],
            birthdate=payload["birthdate"],
            gender=payload["gender"],
            phone_number=payload["phone_number"]
        )

        # Crear usuario en Cognito
        result = self.cognito_repo.create_user(signup_request)

        logger.info("User successfully created.")
        return {"message": "User created successfully", "user": signup_request.email}
