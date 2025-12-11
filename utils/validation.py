import re
from domain.exceptions import DomainValidationError

PASSWORD_REGEX = (
    r'^(?=.*[a-z])'       # 1 minúscula
    r'(?=.*[A-Z])'        # 1 mayúscula
    r'(?=.*\d)'           # 1 número
    r'(?=.*[\W_])'        # 1 caracter especial
    r'.{8,}$'             # mínimo 8 caracteres
)

def validate_signup_data(data):
    required = ["email", "password", "name", "birthdate", "gender", "phone_number"]

    missing = [field for field in required if field not in data or not data[field]]
    if missing:
        raise DomainValidationError(f"Missing required fields: {', '.join(missing)}")

    if not re.match(PASSWORD_REGEX, data["password"]):
        raise DomainValidationError(
            "Password does not meet complexity requirements: "
            "min 8 chars, 1 number, 1 special char, 1 uppercase, 1 lowercase."
        )
