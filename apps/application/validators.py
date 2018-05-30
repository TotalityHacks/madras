from django.conf import settings
import os
from django.core.exceptions import ValidationError


def validate_resume(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf']
    if not ext.lower() in valid_extensions:
        raise ValidationError(
            'Unsupported file extension.',
            'Upload should be a pdf')
    limit = settings.MAX_RESUME_SIZE
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MiB.')
