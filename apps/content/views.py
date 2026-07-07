from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import AllowAny

from apps.accounts.permissions import IsAdminRole
from apps.content.models import ContentType, Event, LegalDocument
from apps.content.serializers import (
    EventAdminSerializer,
    EventDetailSerializer,
    EventListSerializer,
    LegalDocumentAdminSerializer,
    LegalDocumentSerializer,
)


class AuditCreateMixin:
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


# --- Legal ------------------------------------------------------------------
class PublicLegalViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    lookup_field = "slug"
    serializer_class = LegalDocumentSerializer
    queryset = LegalDocument.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category"]


class AdminLegalViewSet(AuditCreateMixin, viewsets.ModelViewSet):
    permission_classes = [IsAdminRole]
    serializer_class = LegalDocumentAdminSerializer
    queryset = LegalDocument.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["category", "is_active"]
    search_fields = ["title", "category"]


# --- Events / News ----------------------------------------------------------
class PublicEventViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    lookup_field = "slug"
    queryset = Event.objects.filter(is_active=True, type=ContentType.EVENT)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["is_featured"]

    def get_serializer_class(self):
        return EventListSerializer if self.action == "list" else EventDetailSerializer


class PublicNewsViewSet(PublicEventViewSet):
    queryset = Event.objects.filter(is_active=True, type=ContentType.NEWS)


class AdminEventViewSet(AuditCreateMixin, viewsets.ModelViewSet):
    permission_classes = [IsAdminRole]
    serializer_class = EventAdminSerializer
    queryset = Event.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["type", "is_featured", "is_active"]
    search_fields = ["title", "short_description"]
