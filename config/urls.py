"""URL configuration for the Aaradhana Bachat backend."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from apps.content.views import (
    AdminEventViewSet,
    AdminLegalViewSet,
    PublicEventViewSet,
    PublicLegalViewSet,
    PublicNewsViewSet,
)
from apps.core.views import WebsiteSettingsView
from apps.enquiries.views import AdminEnquiryViewSet, EnquiryCreateView
from apps.media_library.views import (
    AdminGalleryCategoryViewSet,
    AdminGalleryImageViewSet,
    AdminVideoViewSet,
    PublicGalleryCategoryViewSet,
    PublicGalleryImageViewSet,
    PublicVideoViewSet,
)
from apps.members.views import AdminMemberViewSet, MemberProfileView
from apps.plans.views import (
    AdminPlanTableRowViewSet,
    AdminPlanViewSet,
    PublicPlanViewSet,
)

# --- Public API router ------------------------------------------------------
public_router = DefaultRouter()
public_router.register("plans", PublicPlanViewSet, basename="plans")
public_router.register("legal-documents", PublicLegalViewSet, basename="legal-documents")
public_router.register("gallery/categories", PublicGalleryCategoryViewSet, basename="gallery-categories")
public_router.register("gallery/images", PublicGalleryImageViewSet, basename="gallery-images")
public_router.register("videos", PublicVideoViewSet, basename="videos")
public_router.register("events", PublicEventViewSet, basename="events")
public_router.register("news", PublicNewsViewSet, basename="news")

# --- Admin API router -------------------------------------------------------
admin_router = DefaultRouter()
admin_router.register("plans", AdminPlanViewSet, basename="admin-plans")
admin_router.register("plan-table-rows", AdminPlanTableRowViewSet, basename="admin-plan-table-rows")
admin_router.register("legal-documents", AdminLegalViewSet, basename="admin-legal-documents")
admin_router.register("gallery/categories", AdminGalleryCategoryViewSet, basename="admin-gallery-categories")
admin_router.register("gallery/images", AdminGalleryImageViewSet, basename="admin-gallery-images")
admin_router.register("videos", AdminVideoViewSet, basename="admin-videos")
admin_router.register("events", AdminEventViewSet, basename="admin-events")
admin_router.register("enquiries", AdminEnquiryViewSet, basename="admin-enquiries")
admin_router.register("members", AdminMemberViewSet, basename="admin-members")

api_v1 = [
    path("auth/", include("apps.accounts.urls")),
    path("website-settings/", WebsiteSettingsView.as_view(), name="website-settings"),
    path("enquiries/", EnquiryCreateView.as_view(), name="enquiry-create"),
    path("member/profile/", MemberProfileView.as_view(), name="member-profile"),
    path("admin/website-settings/", WebsiteSettingsView.as_view(), name="admin-website-settings"),
    path("", include(public_router.urls)),
    path("admin/", include(admin_router.urls)),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include((api_v1, "api"))),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
