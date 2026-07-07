from django.conf import settings
from django.db import models


class TimeStampedModel(models.Model):
    """Abstract audit base model reused across apps."""

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class WebsiteSettings(TimeStampedModel):
    """Singleton-style site settings for header/footer/contact."""

    site_name = models.CharField(max_length=200, default="Aaradhana Bachat")
    logo = models.ImageField(upload_to="settings/", null=True, blank=True)
    primary_phone = models.CharField(max_length=30, blank=True)
    secondary_phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    google_map_embed_url = models.URLField(blank=True, max_length=500)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    whatsapp_number = models.CharField(max_length=30, blank=True)
    office_hours = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Website settings"
        verbose_name_plural = "Website settings"

    def __str__(self) -> str:
        return self.site_name

    @classmethod
    def load(cls) -> "WebsiteSettings":
        """Return the single active settings row, creating it if needed."""
        obj = cls.objects.filter(is_active=True).order_by("id").first()
        if obj is None:
            obj = cls.objects.create()
        return obj
