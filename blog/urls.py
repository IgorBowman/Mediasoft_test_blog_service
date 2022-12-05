from django.urls import path
from rest_framework.routers import SimpleRouter

from blog.views import (
    BlogView, SubscribeToBlogView, FavoriteListBlogsView,
    AddAuthorsToBlogView,
)

router = SimpleRouter()
router.register(r'blogs', BlogView, basename='Blogs')

urlpatterns = [
    path('blogs/<int:pk>/subscribe', SubscribeToBlogView.as_view(),
         name='subscribe-to-blog'),
    path('blogs/favorites', FavoriteListBlogsView.as_view(),
         name='my-favorite-blogs'),
    path('blogs/<int:pk>/add-authors', AddAuthorsToBlogView.as_view(),
         name='add-authors-to-blog'),
]

urlpatterns += router.urls
