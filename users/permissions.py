from rest_framework import permissions

from blog.models import Posts


class IsAuthenticatedAndOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Posts):
            obj = obj.blog
            if request.user and request.user.is_authenticated \
                    and obj.ownerobj.owner == request.user:
                return True
            return False


class IsAuthenticatedAndAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated \
                and request.user in obj.authors.all():
            return True
        return False


class IsUserAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsUserAuthorOrBlogOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Posts):
            obj = obj.blog

            if request.user in obj.authors.all() \
                    or obj.owner == request.user:
                return True
            return False
