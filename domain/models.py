from dataclasses import dataclass

@dataclass
class SignUpRequest:
    email: str
    password: str
    name: str
    birthdate: str
    gender: str
    phone_number: str
