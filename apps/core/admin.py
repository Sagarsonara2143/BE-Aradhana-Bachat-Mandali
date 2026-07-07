from django.contrib import admin

from apps.core.models import WebsiteSettings


@admin.register(WebsiteSettings)
class WebsiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_name", "primary_phone", "email", "is_active", "updated_at")
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")
