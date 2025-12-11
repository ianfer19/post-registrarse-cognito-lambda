import boto3
from botocore.exceptions import ClientError
from uuid import uuid4
from domain.exceptions import CognitoError
from utils.logger import get_logger

logger = get_logger(__name__)

class CognitoRepository:

    def __init__(self, user_pool_id, client_id):
        self.client = boto3.client("cognito-idp")
        self.user_pool_id = user_pool_id
        self.client_id = client_id

    def signup_user(self, signup_request):

        try:
            generated_username = str(uuid4())

            # 1️⃣ Crear usuario SIN confirmarlo
            response = self.client.admin_create_user(
                UserPoolId=self.user_pool_id,
                Username=generated_username,
                MessageAction="SUPPRESS",  # no envia email automático
                UserAttributes=[
                    {"Name": "email", "Value": signup_request.email},
                    {"Name": "email_verified", "Value": "false"},
                    {"Name": "name", "Value": signup_request.name},
                    {"Name": "birthdate", "Value": signup_request.birthdate},
                    {"Name": "gender", "Value": signup_request.gender},
                    {"Name": "phone_number", "Value": signup_request.phone_number},
                ],
            )

            logger.info(f"User created in Cognito: {generated_username}")

            # 2️⃣ Establecer contraseña temporal
            self.client.admin_set_user_password(
                UserPoolId=self.user_pool_id,
                Username=generated_username,
                Password=signup_request.password,
                Permanent=False  # ← muy importante, debe ser TEMPORAL
            )

            # 3️⃣ Mandar email de confirmación manualmente
            self.client.resend_confirmation_code(
                ClientId=self.client_id,
                Username=generated_username
            )

            return {
                "username": generated_username,
                "email": signup_request.email
            }

        except ClientError as e:
            logger.error(str(e))
            raise CognitoError(e.response["Error"]["Message"])
