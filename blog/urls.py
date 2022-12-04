from django.urls import path
from rest_framework.routers import SimpleRouter

from blog.views import BlogView

router = SimpleRouter()
router.register(r'blogs', BlogView, basename='Blogs')

urlpatterns = [
]

urlpatterns += router.urls

