import json
from application.signup_service import SignUpService
from infrastructure.cognito_repository import CognitoRepository
from utils.response import success, error
from domain.exceptions import DomainValidationError, CognitoError
from utils.logger import get_logger
import os

logger = get_logger(__name__)

USER_POOL_ID = os.environ["USER_POOL_ID"]

cognito_repo = CognitoRepository(USER_POOL_ID)
signup_service = SignUpService(cognito_repo)

def lambda_handler(event, context):
    logger.info("Signup Lambda invoked")

    try:
        body = json.loads(event.get("body", "{}"))
        result = signup_service.signup(body)
        return success(result, 201)

    except DomainValidationError as e:
        return error(str(e), 400)

    except CognitoError as e:
        return error(str(e), 500)

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return error("Internal server error", 500)
