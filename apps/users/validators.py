from django.core.validators import RegexValidator
from rest_framework.exceptions import ValidationError

phone_validator = RegexValidator(
    regex=r'^\d{9}$',
    message="Phone number must be exactly 9 digits long!",
)


def activation_code_validator(value):
    if not (isinstance(value, int) and 100000 <= value <= 999999):
        raise ValidationError('Code must be a 6-digit integer!')

