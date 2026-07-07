from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel


class MemberStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"
    BLOCKED = "BLOCKED", "Blocked"


class Member(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="member_profile",
    )
    member_code = models.CharField(max_length=40, unique=True)
    full_name = models.CharField(max_length=150)
    mobile_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    status = models.CharField(
        max_length=10, choices=MemberStatus.choices, default=MemberStatus.ACTIVE, db_index=True
    )
    joined_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.member_code} — {self.full_name}"
