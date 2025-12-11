import boto3
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
            logger.info("Creating user in Cognito...")

            response = self.client.admin_create_user(
                UserPoolId=self.user_pool_id,
                Username=signup_request.email,
                TemporaryPassword=signup_request.password,
                MessageAction="SUPPRESS",
                UserAttributes=[
                    {"Name": "email", "Value": signup_request.email},
                    {"Name": "name", "Value": signup_request.name},
                    {"Name": "birthdate", "Value": signup_request.birthdate},
                    {"Name": "gender", "Value": signup_request.gender},
                    {"Name": "phone_number", "Value": signup_request.phone_number},
                ]
            )

            # Forzar el password como definitivo (no temporal)
            self.client.admin_set_user_password(
                UserPoolId=self.user_pool_id,
                Username=response["User"]["Username"],
                Password=signup_request.password,
                Permanent=True
            )

            return response

        except ClientError as e:
            logger.error(f"Cognito error: {str(e)}")
            raise CognitoError(e.response["Error"]["Message"])
