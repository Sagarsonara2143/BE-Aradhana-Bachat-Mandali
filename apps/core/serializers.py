from rest_framework import serializers

from apps.core.models import WebsiteSettings


class WebsiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebsiteSettings
        fields = [
            "site_name",
            "logo",
            "primary_phone",
            "secondary_phone",
            "email",
            "address",
            "google_map_embed_url",
            "facebook_url",
            "instagram_url",
            "youtube_url",
            "whatsapp_number",
            "office_hours",
        ]
