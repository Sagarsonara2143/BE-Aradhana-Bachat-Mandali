import os

from django.conf import settings
from django.core.exceptions import ValidationError

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
DOCUMENT_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png"}
VIDEO_EXTENSIONS = {".mp4", ".webm", ".mov"}


def _ext(value) -> str:
    return os.path.splitext(value.name)[1].lower()


def _validate(value, allowed: set[str], max_size: int) -> None:
    ext = _ext(value)
    if ext not in allowed:
        raise ValidationError(
            f"Unsupported file type '{ext}'. Allowed: {', '.join(sorted(allowed))}."
        )
    size = getattr(value, "size", 0)
    if size and size > max_size:
        raise ValidationError(
            f"File too large ({size // 1024} KB). Maximum is {max_size // 1024} KB."
        )


def validate_image(value):
    _validate(value, IMAGE_EXTENSIONS, settings.MAX_UPLOAD_SIZE_IMAGE)


def validate_document(value):
    _validate(value, DOCUMENT_EXTENSIONS, settings.MAX_UPLOAD_SIZE_DOCUMENT)


def validate_video(value):
    _validate(value, VIDEO_EXTENSIONS, settings.MAX_UPLOAD_SIZE_VIDEO)
