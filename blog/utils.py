from django.db.models import F
from django_filters.rest_framework import (
    BaseInFilter, CharFilter, FilterSet, RangeFilter
)

from blog.models import Posts


class CharFilterInFilter(BaseInFilter, CharFilter):
    ...


class PostFilter(FilterSet):
    tags = CharFilterInFilter(field_name='tags__title', lookup_expr='in')
    created_at = RangeFilter

    class Meta:
        model = Posts
        fields = ['tags', 'created_at']


def increase_views_of_post(post: Posts, user) -> None:
    if post.blog.owner != user:
        post.views = F('views') + 1
        post.save(update_fields=('views',))


def increase_likes_of_post(post: Posts) -> None:
    post.likes = F('likes') + 1
    post.save(update_fields=('likes',))
