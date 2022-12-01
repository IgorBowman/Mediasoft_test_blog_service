from django.contrib import admin

from .models import Blogs, Tags, Posts, Comments

admin.site.register(Blogs)
admin.site.register(Tags)
admin.site.register(Posts)
admin.site.register(Comments)
