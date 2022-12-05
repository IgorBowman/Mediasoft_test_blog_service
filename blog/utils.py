from django_filters.rest_framework import (
    BaseInFilter, CharFilter, FilterSet, RangeFilter)

from blog.models import Posts


class CharFilterInFilter(BaseInFilter, CharFilter):
    ...


class PostFilter(FilterSet):
    tags = CharFilterInFilter(field_name='tags__title', lookup_expr='in')
    created_at = RangeFilter

    class Meta:
        model = Posts
        fields = ['tags', 'created_at']
