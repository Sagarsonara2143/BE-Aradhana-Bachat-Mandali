from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsAdminRole, IsMember
from apps.members.models import Member
from apps.members.serializers import MemberProfileSerializer, MemberSerializer


class MemberProfileView(APIView):
    """Authenticated member's own profile."""

    permission_classes = [IsMember]
    serializer_class = MemberProfileSerializer

    def get(self, request):
        member = Member.objects.filter(user=request.user).first()
        if member is None:
            raise NotFound("No member profile linked to this account.")
        return Response(MemberProfileSerializer(member).data)


class AdminMemberViewSet(viewsets.ModelViewSet):
    """Admin CRUD for members."""

    permission_classes = [IsAdminRole]
    serializer_class = MemberSerializer
    queryset = Member.objects.select_related("user").all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
