from errors.error_instance import error_instance
from email_validator import validate_email, EmailNotValidError
from password_validator import PasswordValidator

password_instance = PasswordValidator()
password_instance.min(8)
password_instance.max(100)
password_instance.has().uppercase()
password_instance.has().lowercase()


def office_validation(office: str):
    text_to_pattern = office.capitalize()
    possible_offices = ['Default', 'Admin']

    if text_to_pattern not in possible_offices:
        error_instance(510, "Office can be only Default or Admin")
    return


def email_validation(user):
    try:
        validate_email(user.email).email
    except EmailNotValidError as e:
        error_instance(510, "Email format is incorect.")


def password_validation(password: str):
    is_password_valid = password_instance.validate(password)
    if not is_password_valid:
        error_instance(401, "The password must contain uppercase, lowercase, numbers and more than eight characters.")