from django.db import models

from apps.core.models import TimeStampedModel
from apps.core.validators import validate_document, validate_image


class LegalDocument(TimeStampedModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=210, unique=True)
    category = models.CharField(max_length=100, db_index=True)
    document_file = models.FileField(upload_to="legal/", validators=[validate_document])
    description = models.TextField(blank=True)
    published_date = models.DateField(null=True, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "-published_date", "title"]

    def __str__(self) -> str:
        return self.title


class ContentType(models.TextChoices):
    EVENT = "EVENT", "Event"
    NEWS = "NEWS", "News"


class Event(TimeStampedModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=210, unique=True)
    type = models.CharField(
        max_length=10, choices=ContentType.choices, default=ContentType.EVENT, db_index=True
    )
    short_description = models.CharField(max_length=400, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to="events/", null=True, blank=True, validators=[validate_image])
    event_date = models.DateField(null=True, blank=True)
    published_date = models.DateField(null=True, blank=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-event_date", "-published_date", "sort_order"]

    def __str__(self) -> str:
        return self.title
