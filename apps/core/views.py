from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsAdminRole
from apps.core.models import WebsiteSettings
from apps.core.serializers import WebsiteSettingsSerializer


class WebsiteSettingsView(APIView):
    """GET public website settings; PATCH (admin) to update the single record."""

    serializer_class = WebsiteSettingsSerializer

    def get_permissions(self):
        if self.request.method == "PATCH":
            return [IsAdminRole()]
        return [AllowAny()]

    def get(self, request):
        return Response(WebsiteSettingsSerializer(WebsiteSettings.load()).data)

    def patch(self, request):
        settings_obj = WebsiteSettings.load()
        serializer = WebsiteSettingsSerializer(settings_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
