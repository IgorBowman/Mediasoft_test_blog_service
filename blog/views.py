from rest_framework.decorators import permission_classes
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import UpdateAPIView, ListAPIView, UpdateAPIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny

from blog.models import Blogs, Posts
from .serializers import (
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
from .utils import PostFilter


class BlogView(ModelViewSet):
    queryset = Blogs
    serializer_class = BlogSerializer
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
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


class SubscribeToBlogView(UpdateAPIView):
    queryset = Blogs.objects.prefetch_related('subscriptions').all()
    permission_classes = [IsAuthenticated]
    serializer_class = CreateSubscriptionSerializer
    http_method_names = ['patch']


class FavoriteListBlogsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BlogSerializer
    filter_backend = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filter_fields = ['created_at']
    ordering_fields = ['title', 'created_at']

    def get_queryset(self):
        return Blogs.objects.prefetch_related('subscriptions').filter(
            subscriptions__id=self.request.user.id
        )


class AddAuthorsToBlogView(UpdateAPIView):
    permission_classes = [IsAuthenticatedAndOwner | IsUserAdmin]
    serializer_class = AddAuthorToBlogSerializer
    http_method_names = ['patch']

    def get_queryset(self):
        return Blogs.objects.prefetch_related('authors').filter(
            owner=self.request.user.id
        )


class ListPostsOfBlogView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = PostSerializer
    filter_backend = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filterset_class = PostFilter
    ordering_fields = ['title', 'created_at', 'likes']

    def get_queryset(self):
        queryset = Posts.objects.none()
        if not getattr(self, 'swagger_fake_view', False):
            queryset = Posts.objects.filter(
                is_published=True,
                blog=self.kwargs['pk']
            )
        return queryset
