from django.contrib import admin

from apps.members.models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("member_code", "full_name", "mobile_number", "status", "joined_date")
    list_filter = ("status",)
    search_fields = ("member_code", "full_name", "mobile_number", "email")
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")
