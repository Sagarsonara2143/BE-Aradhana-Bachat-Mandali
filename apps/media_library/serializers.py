from rest_framework import serializers

from apps.media_library.models import GalleryCategory, GalleryImage, Video, VideoType


class GalleryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryCategory
        fields = ["id", "name", "slug", "sort_order", "is_active"]
        read_only_fields = ["is_active"]


class GalleryImageSerializer(serializers.ModelSerializer):
    category_slug = serializers.SlugRelatedField(
        source="category", slug_field="slug", read_only=True
    )

    class Meta:
        model = GalleryImage
        fields = [
            "id",
            "title",
            "category",
            "category_slug",
            "image",
            "caption",
            "event_date",
            "sort_order",
            "is_featured",
            "is_active",
        ]
        read_only_fields = ["is_active"]


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = [
            "id",
            "title",
            "description",
            "video_type",
            "youtube_url",
            "video_file",
            "thumbnail",
            "published_date",
            "sort_order",
            "is_active",
        ]
        read_only_fields = ["is_active"]

    def validate(self, attrs):
        video_type = attrs.get("video_type", getattr(self.instance, "video_type", None))
        youtube_url = attrs.get("youtube_url", getattr(self.instance, "youtube_url", ""))
        video_file = attrs.get("video_file", getattr(self.instance, "video_file", None))
        if video_type == VideoType.YOUTUBE:
            url = youtube_url or ""
            if not url:
                raise serializers.ValidationError({"youtube_url": "Required for YouTube videos."})
            if "youtube.com" not in url and "youtu.be" not in url:
                raise serializers.ValidationError({"youtube_url": "Enter a valid YouTube URL."})
        elif video_type == VideoType.UPLOAD and not video_file:
            raise serializers.ValidationError({"video_file": "Required for uploaded videos."})
        return attrs
