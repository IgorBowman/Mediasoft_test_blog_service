from django.urls import path
from rest_framework.routers import SimpleRouter

from blog.views import (
    BlogView, SubscribeToBlogView, FavoriteListBlogsView,
    AddAuthorsToBlogView, ListPostsOfBlogView, ListUserPostsView,
    PostsView, LikePostView, TagsView,
)

router = SimpleRouter()
router.register(r'blogs', BlogView, basename='Blogs')
router.register(r'posts', PostsView, basename='Posts')
router.register(r'tags', TagsView, basename='Tags')

urlpatterns = [
    path('blogs/<int:pk>/subscribe', SubscribeToBlogView.as_view(),
         name='subscribe-to-blog'),
    path('blogs/favorites', FavoriteListBlogsView.as_view(),
         name='my-favorite-blogs'),
    path('blogs/<int:pk>/add-authors', AddAuthorsToBlogView.as_view(),
         name='add-authors-to-blog'),
    path('blogs/<int:pk>/posts', ListPostsOfBlogView.as_view(),
         name='posts-of-blog'),
    path('posts/my', ListUserPostsView.as_view(), name='my-posts'),
    path('posts/<int:pk>/add-like', LikePostView.as_view(), name='like-post'),
]

urlpatterns += router.urls
