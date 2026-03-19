import re


def validate_email(email: str) -> str:
    email = email.strip().lower()
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(pattern, email):
        raise Exception("Invalid email address")
    return email


def validate_password(password: str) -> None:
    if len(password) < 8:
        raise Exception("Password must be at least 8 characters")
    if len(password) > 72:
        raise Exception("Password cannot exceed 72 characters")
    if not any(c.isupper() for c in password):
        raise Exception("Password must contain at least one uppercase letter")
    if not any(c.isdigit() for c in password):
        raise Exception("Password must contain at least one number")


def validate_name(name: str, field: str) -> str:
    name = name.strip()
    if not name:
        raise Exception(f"{field} cannot be empty")
    if len(name) < 2:
        raise Exception(f"{field} must be at least 2 characters")
    if len(name) > 50:
        raise Exception(f"{field} cannot exceed 50 characters")

    return name
