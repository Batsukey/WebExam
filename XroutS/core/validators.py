# custom validators
import re

from django.core.exceptions import ValidationError


def validate_only_characters(value):
    if not re.match(r'^[a-zA-Z]*$', value):
        raise ValidationError('Only characters are allowed.')

def validate_file_size(image_object):
    if image_object.size > 1242880:
        raise ValidationError("The maximum file size that can be uploaded is 1mb")
