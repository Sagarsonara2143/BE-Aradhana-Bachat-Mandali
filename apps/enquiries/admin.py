from django.contrib import admin

from apps.enquiries.models import Enquiry


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ("full_name", "subject", "mobile_number", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("full_name", "mobile_number", "email", "subject")
    readonly_fields = (
        "full_name",
        "mobile_number",
        "email",
        "subject",
        "message",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    )
