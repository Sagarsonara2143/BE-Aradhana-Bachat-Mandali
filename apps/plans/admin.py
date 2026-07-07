from django.contrib import admin

from apps.plans.models import Plan, PlanTableRow


class PlanTableRowInline(admin.TabularInline):
    model = PlanTableRow
    extra = 1


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "plan_type", "is_featured", "sort_order", "is_active")
    list_filter = ("plan_type", "is_featured", "is_active")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("sort_order", "name")
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")
    inlines = [PlanTableRowInline]


@admin.register(PlanTableRow)
class PlanTableRowAdmin(admin.ModelAdmin):
    list_display = ("plan", "label", "duration_years", "maturity_amount", "sort_order", "is_active")
    list_filter = ("plan", "is_active")
    search_fields = ("plan__name", "label")
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")
