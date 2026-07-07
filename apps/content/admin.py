from django.contrib import admin

from apps.content.models import Event, LegalDocument


@admin.register(LegalDocument)
class LegalDocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "published_date", "sort_order", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("title", "category")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "event_date", "is_featured", "sort_order", "is_active")
    list_filter = ("type", "is_featured", "is_active")
    search_fields = ("title", "short_description")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")
