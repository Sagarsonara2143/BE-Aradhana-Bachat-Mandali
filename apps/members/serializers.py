from rest_framework import serializers

from apps.members.models import Member


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = [
            "id",
            "user",
            "member_code",
            "full_name",
            "mobile_number",
            "email",
            "address",
            "status",
            "joined_date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class MemberProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = [
            "member_code",
            "full_name",
            "mobile_number",
            "email",
            "address",
            "status",
            "joined_date",
        ]
        read_only_fields = fields
