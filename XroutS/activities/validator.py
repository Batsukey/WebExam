from django.core.exceptions import ValidationError


def validate_activity_file_size(image_object):
    if image_object.size > 3242880:
        raise ValidationError("The maximum file size that can be uploaded is 3mb")