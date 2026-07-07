from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from apps.accounts.permissions import IsAdminRole
from apps.enquiries.models import Enquiry
from apps.enquiries.serializers import EnquiryAdminSerializer, EnquiryCreateSerializer


class EnquiryCreateView(APIView):
    """Public enquiry submission (throttled to limit spam)."""

    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "enquiry"
    serializer_class = EnquiryCreateSerializer

    def post(self, request):
        serializer = EnquiryCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Your enquiry has been received."}, status=status.HTTP_201_CREATED
        )


class AdminEnquiryViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """Admin: list/retrieve enquiries and update status/notes."""

    permission_classes = [IsAdminRole]
    serializer_class = EnquiryAdminSerializer
    queryset = Enquiry.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status"]

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
