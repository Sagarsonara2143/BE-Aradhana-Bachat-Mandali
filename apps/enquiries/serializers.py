from rest_framework import serializers

from apps.enquiries.models import Enquiry


class EnquiryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = ["full_name", "mobile_number", "email", "subject", "message"]

    def validate_mobile_number(self, value):
        cleaned = value.strip()
        if len(cleaned) < 7:
            raise serializers.ValidationError("Please enter a valid mobile number.")
        return cleaned


class EnquiryAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = [
            "id",
            "full_name",
            "mobile_number",
            "email",
            "subject",
            "message",
            "status",
            "admin_notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "full_name",
            "mobile_number",
            "email",
            "subject",
            "message",
            "created_at",
            "updated_at",
        ]
