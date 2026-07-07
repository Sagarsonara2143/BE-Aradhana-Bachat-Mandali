import django_filters

from apps.media_library.models import GalleryImage


class GalleryImageFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category__slug", lookup_expr="exact")
    is_featured = django_filters.BooleanFilter()

    class Meta:
        model = GalleryImage
        fields = ["category", "is_featured"]
