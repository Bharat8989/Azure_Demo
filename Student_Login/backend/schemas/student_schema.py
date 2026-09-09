import re


EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


def validate_register_payload(data):
    errors = {}

    if not isinstance(data, dict):
        return {
            "body": "Request body must be a JSON object."
        }

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not isinstance(name, str) or not name.strip():
        errors["name"] = "Name is required."

    elif len(name.strip()) < 2:
        errors["name"] = (
            "Name must contain at least 2 characters."
        )

    elif len(name.strip()) > 100:
        errors["name"] = (
            "Name cannot exceed 100 characters."
        )

    if not isinstance(email, str) or not email.strip():
        errors["email"] = "Email is required."

    elif not EMAIL_REGEX.match(email.strip()):
        errors["email"] = "Invalid email address."

    elif len(email.strip()) > 254:
        errors["email"] = "Email is too long."

    if not isinstance(password, str) or not password:
        errors["password"] = "Password is required."

    elif len(password) < 8:
        errors["password"] = (
            "Password must contain at least 8 characters."
        )

    elif len(password) > 128:
        errors["password"] = (
            "Password cannot exceed 128 characters."
        )

    return errors


def validate_login_payload(data):
    errors = {}

    if not isinstance(data, dict):
        return {
            "body": "Request body must be a JSON object."
        }

    email = data.get("email")
    password = data.get("password")

    if not isinstance(email, str) or not email.strip():
        errors["email"] = "Email is required."

    if not isinstance(password, str) or not password:
        errors["password"] = "Password is required."

    return errors


def validate_forget_password_payload(data):
    errors = {}

    if not isinstance(data, dict):
        return {
            "body": "Request body must be a JSON object."
        }

    email = data.get("email")

    if not isinstance(email, str) or not email.strip():
        errors["email"] = "Email is required."

    elif not EMAIL_REGEX.match(email.strip()):
        errors["email"] = "Invalid email address."

    return errors