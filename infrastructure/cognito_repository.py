import boto3
import uuid
from botocore.exceptions import ClientError
from domain.exceptions import CognitoError
from utils.logger import get_logger

logger = get_logger(__name__)

class CognitoRepository:

    def __init__(self, user_pool_id: str):
        self.client = boto3.client("cognito-idp")
        self.user_pool_id = user_pool_id

    def create_user(self, signup_request):

        try:
            # Generamos un Username válido que NO es email
            generated_username = str(uuid.uuid4())

            logger.info(f"Generated Username for Cognito: {generated_username}")

            response = self.client.admin_create_user(
                UserPoolId=self.user_pool_id,
                Username=generated_username,   # <<<<<< FIX
                TemporaryPassword=signup_request.password,
                MessageAction="SUPPRESS",
                UserAttributes=[
                    {"Name": "email", "Value": signup_request.email},
                    {"Name": "email_verified", "Value": "true"},

                    {"Name": "name", "Value": signup_request.name},
                    {"Name": "birthdate", "Value": signup_request.birthdate},
                    {"Name": "gender", "Value": signup_request.gender},
                    {"Name": "phone_number", "Value": signup_request.phone_number},
                ],
            )

            # Esto SIEMPRE existe ahora
            cognito_username = response["User"]["Username"]

            logger.info(f"Cognito returned Username: {cognito_username}")

            # Password permanente
            self.client.admin_set_user_password(
                UserPoolId=self.user_pool_id,
                Username=cognito_username,
                Password=signup_request.password,
                Permanent=True,
            )

            return {
                "email": signup_request.email,
                "username": cognito_username
            }

        except ClientError as e:
            logger.error(str(e))
            raise CognitoError(e.response["Error"]["Message"])
