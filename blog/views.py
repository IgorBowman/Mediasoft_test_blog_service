from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, AllowAny

from blog.models import Blogs
from serializers import (
    UserSerializer, BlogSerializer, AddAuthorToBlogSerializer, \
    TagSerializer, PostSerializer, CommentsSerializer, CreateSubscriptionSerializer
)
from users.permissions import (
    IsAuthenticatedAndOwner,
    IsAuthenticatedAndAuthor,
    IsUserAdmin,
    IsUserAuthorOrBlogOwner,
    IsAdminOrReadOnly
)


class BlogView(ModelViewSet):
    queryset = Blogs
    serializer_class = BlogSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_fields = ['created_at']
    ordering_field = ['title', 'created_at']

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            permission_classes = [AllowAny]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticatedAndOwner | IsUserAdmin]
        return {permission() for permission in permission_classes}

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()
