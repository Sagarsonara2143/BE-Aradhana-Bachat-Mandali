from django.db import models

from apps.core.models import TimeStampedModel
from apps.core.validators import validate_image, validate_video


class GalleryCategory(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=110, unique=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name_plural = "Gallery categories"

    def __str__(self) -> str:
        return self.name


class GalleryImage(TimeStampedModel):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(
        GalleryCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="images",
    )
    image = models.ImageField(upload_to="gallery/", validators=[validate_image])
    caption = models.CharField(max_length=300, blank=True)
    event_date = models.DateField(null=True, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ["sort_order", "-event_date", "title"]

    def __str__(self) -> str:
        return self.title


class VideoType(models.TextChoices):
    YOUTUBE = "YOUTUBE", "YouTube"
    UPLOAD = "UPLOAD", "Upload"


class Video(TimeStampedModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_type = models.CharField(
        max_length=10, choices=VideoType.choices, default=VideoType.YOUTUBE, db_index=True
    )
    youtube_url = models.URLField(blank=True)
    video_file = models.FileField(
        upload_to="videos/", null=True, blank=True, validators=[validate_video]
    )
    thumbnail = models.ImageField(
        upload_to="videos/thumbnails/", null=True, blank=True, validators=[validate_image]
    )
    published_date = models.DateField(null=True, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "-published_date", "title"]

    def __str__(self) -> str:
        return self.title
