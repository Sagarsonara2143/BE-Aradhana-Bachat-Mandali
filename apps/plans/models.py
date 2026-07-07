from django.db import models

from apps.core.models import TimeStampedModel


class PlanType(models.TextChoices):
    RD = "RD", "RD Plan"
    TERM = "TERM", "Term Plan"
    DT = "DT", "DT Plan"
    SN = "SN", "SN Plan"


class Plan(TimeStampedModel):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True)
    plan_type = models.CharField(max_length=10, choices=PlanType.choices, db_index=True)
    short_description = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    benefits = models.JSONField(default=list, blank=True, help_text="List of benefit strings")
    terms_conditions = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    sort_order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self) -> str:
        return self.name


class PlanTableRow(TimeStampedModel):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="table_rows")
    label = models.CharField(max_length=120, blank=True)
    duration_years = models.PositiveIntegerField(null=True, blank=True)
    deposit_amount = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    premium_amount = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    maturity_amount = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    fund_value = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    surrender_value = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    family_protection = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    monthly_income = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self) -> str:
        return f"{self.plan.name} row {self.pk}"
