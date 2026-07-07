from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from apps.accounts.permissions import IsAdminRole
from apps.content.views import AuditCreateMixin
from apps.media_library.filters import GalleryImageFilter
from apps.media_library.models import GalleryCategory, GalleryImage, Video
from apps.media_library.serializers import (
    GalleryCategorySerializer,
    GalleryImageSerializer,
    VideoSerializer,
)


# --- Gallery ----------------------------------------------------------------
class PublicGalleryCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = GalleryCategorySerializer
    queryset = GalleryCategory.objects.filter(is_active=True)


class PublicGalleryImageViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = GalleryImageSerializer
    queryset = GalleryImage.objects.filter(is_active=True).select_related("category")
    filter_backends = [DjangoFilterBackend]
    filterset_class = GalleryImageFilter


class AdminGalleryCategoryViewSet(AuditCreateMixin, viewsets.ModelViewSet):
    permission_classes = [IsAdminRole]
    serializer_class = GalleryCategorySerializer
    queryset = GalleryCategory.objects.all()


class AdminGalleryImageViewSet(AuditCreateMixin, viewsets.ModelViewSet):
    permission_classes = [IsAdminRole]
    serializer_class = GalleryImageSerializer
    queryset = GalleryImage.objects.select_related("category").all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category", "is_featured", "is_active"]


# --- Videos -----------------------------------------------------------------
class PublicVideoViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = VideoSerializer
    queryset = Video.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["video_type"]


class AdminVideoViewSet(AuditCreateMixin, viewsets.ModelViewSet):
    permission_classes = [IsAdminRole]
    serializer_class = VideoSerializer
    queryset = Video.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["video_type", "is_active"]
