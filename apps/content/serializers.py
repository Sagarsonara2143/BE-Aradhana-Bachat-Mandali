from rest_framework import serializers

from apps.content.models import Event, LegalDocument


class LegalDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalDocument
        fields = [
            "id",
            "title",
            "slug",
            "category",
            "document_file",
            "description",
            "published_date",
            "sort_order",
            "is_active",
        ]
        read_only_fields = ["is_active"]


class LegalDocumentAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalDocument
        fields = [
            "id",
            "title",
            "slug",
            "category",
            "document_file",
            "description",
            "published_date",
            "sort_order",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "slug",
            "type",
            "short_description",
            "image",
            "event_date",
            "published_date",
            "is_featured",
        ]


class EventDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "slug",
            "type",
            "short_description",
            "content",
            "image",
            "event_date",
            "published_date",
            "is_featured",
        ]


class EventAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "slug",
            "type",
            "short_description",
            "content",
            "image",
            "event_date",
            "published_date",
            "is_featured",
            "sort_order",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
