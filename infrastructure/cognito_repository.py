import boto3
from botocore.exceptions import ClientError
from uuid import uuid4
from domain.exceptions import CognitoError
from utils.logger import get_logger

logger = get_logger(__name__)

class CognitoRepository:

    def __init__(self, client_id):
        self.client = boto3.client("cognito-idp")
        self.client_id = client_id

    def signup_user(self, signup_request):
        try:
            logger.info("Signing up user in Cognito using sign_up API...")

            # 👈 Username NO PUEDE ser email porque tienes alias activado
            generated_username = str(uuid4())

            response = self.client.sign_up(
                ClientId=self.client_id,
                Username=generated_username,  # 👈 UUID como username
                Password=signup_request.password,
                UserAttributes=[
                    {"Name": "email", "Value": signup_request.email},
                    {"Name": "name", "Value": signup_request.name},
                    {"Name": "birthdate", "Value": signup_request.birthdate},
                    {"Name": "gender", "Value": signup_request.gender},
                    {"Name": "phone_number", "Value": signup_request.phone_number},
                ]
            )

            logger.info(f"Cognito sign_up success. Username: {generated_username}")

            return {
                "username": generated_username,  # 👈 este UUID es el que debes usar en confirm
                "email": signup_request.email,
                "message": "Confirmation code sent to email."
            }

        except ClientError as e:
            logger.error(str(e))
            raise CognitoError(e.response["Error"]["Message"])
