import boto3
from botocore.exceptions import ClientError
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

            # 🚀 Registro normal que sí envía correo de confirmación
            response = self.client.sign_up(
                ClientId=self.client_id,
                Username=signup_request.email,
                Password=signup_request.password,
                UserAttributes=[
                    {"Name": "email", "Value": signup_request.email},
                    {"Name": "name", "Value": signup_request.name},
                    {"Name": "birthdate", "Value": signup_request.birthdate},
                    {"Name": "gender", "Value": signup_request.gender},
                    {"Name": "phone_number", "Value": signup_request.phone_number},
                ]
            )

            logger.info("User signed up. Confirmation code sent.")

            return {
                "username": signup_request.email,
                "email": signup_request.email,
                "message": "Confirmation code sent to email."
            }

        except ClientError as e:
            logger.error(str(e))
            raise CognitoError(e.response["Error"]["Message"])
