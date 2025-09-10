import phonenumbers
from django.core.exceptions import ValidationError


def check_image_size(image):
    if image.size > 4 * 1024 * 1024:
        raise ValidationError("The image is too long")


def validate_phone_number(value):
    try:
        parsed_number = phonenumbers.parse(value)
        if not phonenumbers.is_valid_number(parsed_number) or not str(value[1:]).isdigit():
            raise ValidationError(message="Your phone number is in the wrong format")

        return True
    except phonenumbers.NumberParseException:
        raise ValidationError(message="Your phone number is in the wrong format. (+_)")

