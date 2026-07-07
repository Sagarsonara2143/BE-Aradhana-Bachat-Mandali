from django.contrib import admin

from apps.media_library.models import GalleryCategory, GalleryImage, Video


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "sort_order", "is_active")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "event_date", "is_featured", "sort_order", "is_active")
    list_filter = ("category", "is_featured", "is_active")
    search_fields = ("title", "caption")
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "video_type", "published_date", "sort_order", "is_active")
    list_filter = ("video_type", "is_active")
    search_fields = ("title", "description")
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")
