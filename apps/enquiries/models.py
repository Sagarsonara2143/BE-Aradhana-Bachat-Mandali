from django.db import models

from apps.core.models import TimeStampedModel


class EnquiryStatus(models.TextChoices):
    NEW = "NEW", "New"
    IN_PROGRESS = "IN_PROGRESS", "In Progress"
    CLOSED = "CLOSED", "Closed"


class Enquiry(TimeStampedModel):
    full_name = models.CharField(max_length=150)
    mobile_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(
        max_length=15, choices=EnquiryStatus.choices, default=EnquiryStatus.NEW, db_index=True
    )
    admin_notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Enquiries"

    def __str__(self) -> str:
        return f"{self.full_name} — {self.subject}"
