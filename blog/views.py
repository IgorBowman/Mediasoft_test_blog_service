from django.utils import timezone
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.viewsets import ModelViewSet
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
from .utils import PostFilter, increase_views_of_post, increase_likes_of_post
from .mixins import MixinFilterData


class BlogView(ModelViewSet, MixinFilterData):
    queryset = Blogs
    serializer_class = BlogSerializer
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


class FavoriteListBlogsView(ListAPIView, MixinFilterData):
    permission_classes = [IsAuthenticated]
    serializer_class = BlogSerializer
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


class ListPostsOfBlogView(ListAPIView, MixinFilterData):
    permission_classes = [AllowAny]
    serializer_class = PostSerializer
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


class ListUserPostsView(ListAPIView, MixinFilterData):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    filterset_class = PostFilter
    ordering_fields = ['title', 'created_at', 'likes']

    def get_queryset(self):
        return Posts.objects.filter(authors=self.request.user.id)


class PostsView(ModelViewSet, MixinFilterData):
    serializer_class = PostSerializer
    filterset_class = PostFilter
    ordering_fields = ['title', 'created_at', 'likes']

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            permission_classes = [AllowAny]
        elif self.action == 'create':
            permission_classes = [
                IsAuthenticated,
                IsUserAdmin | IsUserAuthorOrBlogOwner
            ]
        else:
            permission_classes = [IsAuthenticatedAndOwner | IsUserAdmin]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Posts.objects.all()
        if self.action == 'list':
            queryset = Posts.objects.filter(is_published=True)
        elif self.action == 'retrieve':
            queryset = Posts.objects.select_related('blog').all()

        return queryset

    def perform_create(self, serializer):
        self.check_obkect_permissions(
            self.request,
            serializer.validated_data['blog']
        )

        serializer.validate_data['author'] = self.request.user
        is_published = serializer.validate_data.get('is_published', False)

        if is_published:
            serializer.validate_data['created_at'] = timezone.now()

        serializer.save()


    def perform_update(self, serializer):
        post = self.get_object()
        is_published = serializer.validate_data.get('is_published', False)

        if is_published and not post.created_at:
            serializer.validate_data['created_at'] = timezone.now()
        serializer.save()

    def retrieve(self, request, *args, **kwargs):
        increase_views_of_post(post=self.get_object(),
                                        user=self.request.user)
        return super().retrieve(request, *args, **kwargs)
