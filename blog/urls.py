from django.urls import path
from rest_framework.routers import SimpleRouter

from blog.views import BlogView, SubscribeToBlogView

router = SimpleRouter()
router.register(r'blogs', BlogView, basename='Blogs')

urlpatterns = [
    path('blogs/<int:pk>/subscribe', SubscribeToBlogView.as_view(),
         name='subscribe-to-blog'),

]

urlpatterns += router.urls

